r'''
# `aws_workspaces_directory`

Refer to the Terraform Registry for docs: [`aws_workspaces_directory`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory).
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


class WorkspacesDirectory(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.workspacesDirectory.WorkspacesDirectory",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory aws_workspaces_directory}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        active_directory_config: typing.Optional[typing.Union["WorkspacesDirectoryActiveDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        certificate_based_auth_properties: typing.Optional[typing.Union["WorkspacesDirectoryCertificateBasedAuthProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        directory_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        saml_properties: typing.Optional[typing.Union["WorkspacesDirectorySamlProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        self_service_permissions: typing.Optional[typing.Union["WorkspacesDirectorySelfServicePermissions", typing.Dict[builtins.str, typing.Any]]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tenancy: typing.Optional[builtins.str] = None,
        user_identity_type: typing.Optional[builtins.str] = None,
        workspace_access_properties: typing.Optional[typing.Union["WorkspacesDirectoryWorkspaceAccessProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        workspace_creation_properties: typing.Optional[typing.Union["WorkspacesDirectoryWorkspaceCreationProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        workspace_directory_description: typing.Optional[builtins.str] = None,
        workspace_directory_name: typing.Optional[builtins.str] = None,
        workspace_type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory aws_workspaces_directory} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param active_directory_config: active_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#active_directory_config WorkspacesDirectory#active_directory_config}
        :param certificate_based_auth_properties: certificate_based_auth_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#certificate_based_auth_properties WorkspacesDirectory#certificate_based_auth_properties}
        :param directory_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#directory_id WorkspacesDirectory#directory_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#id WorkspacesDirectory#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#ip_group_ids WorkspacesDirectory#ip_group_ids}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#region WorkspacesDirectory#region}
        :param saml_properties: saml_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#saml_properties WorkspacesDirectory#saml_properties}
        :param self_service_permissions: self_service_permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#self_service_permissions WorkspacesDirectory#self_service_permissions}
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#subnet_ids WorkspacesDirectory#subnet_ids}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#tags WorkspacesDirectory#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#tags_all WorkspacesDirectory#tags_all}.
        :param tenancy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#tenancy WorkspacesDirectory#tenancy}.
        :param user_identity_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#user_identity_type WorkspacesDirectory#user_identity_type}.
        :param workspace_access_properties: workspace_access_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#workspace_access_properties WorkspacesDirectory#workspace_access_properties}
        :param workspace_creation_properties: workspace_creation_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#workspace_creation_properties WorkspacesDirectory#workspace_creation_properties}
        :param workspace_directory_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#workspace_directory_description WorkspacesDirectory#workspace_directory_description}.
        :param workspace_directory_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#workspace_directory_name WorkspacesDirectory#workspace_directory_name}.
        :param workspace_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#workspace_type WorkspacesDirectory#workspace_type}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5507e0f583d973a9163ed42587b6dcfdf1beb99d9e7e174e38e5dadc4f90e865)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WorkspacesDirectoryConfig(
            active_directory_config=active_directory_config,
            certificate_based_auth_properties=certificate_based_auth_properties,
            directory_id=directory_id,
            id=id,
            ip_group_ids=ip_group_ids,
            region=region,
            saml_properties=saml_properties,
            self_service_permissions=self_service_permissions,
            subnet_ids=subnet_ids,
            tags=tags,
            tags_all=tags_all,
            tenancy=tenancy,
            user_identity_type=user_identity_type,
            workspace_access_properties=workspace_access_properties,
            workspace_creation_properties=workspace_creation_properties,
            workspace_directory_description=workspace_directory_description,
            workspace_directory_name=workspace_directory_name,
            workspace_type=workspace_type,
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
        '''Generates CDKTF code for importing a WorkspacesDirectory resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WorkspacesDirectory to import.
        :param import_from_id: The id of the existing WorkspacesDirectory that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WorkspacesDirectory to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4180668777c24cd1221854a99c4911a2809d247c05feb899e45d3328958fcb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActiveDirectoryConfig")
    def put_active_directory_config(
        self,
        *,
        domain_name: builtins.str,
        service_account_secret_arn: builtins.str,
    ) -> None:
        '''
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#domain_name WorkspacesDirectory#domain_name}.
        :param service_account_secret_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#service_account_secret_arn WorkspacesDirectory#service_account_secret_arn}.
        '''
        value = WorkspacesDirectoryActiveDirectoryConfig(
            domain_name=domain_name,
            service_account_secret_arn=service_account_secret_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putActiveDirectoryConfig", [value]))

    @jsii.member(jsii_name="putCertificateBasedAuthProperties")
    def put_certificate_based_auth_properties(
        self,
        *,
        certificate_authority_arn: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param certificate_authority_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#certificate_authority_arn WorkspacesDirectory#certificate_authority_arn}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#status WorkspacesDirectory#status}.
        '''
        value = WorkspacesDirectoryCertificateBasedAuthProperties(
            certificate_authority_arn=certificate_authority_arn, status=status
        )

        return typing.cast(None, jsii.invoke(self, "putCertificateBasedAuthProperties", [value]))

    @jsii.member(jsii_name="putSamlProperties")
    def put_saml_properties(
        self,
        *,
        relay_state_parameter_name: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        user_access_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param relay_state_parameter_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#relay_state_parameter_name WorkspacesDirectory#relay_state_parameter_name}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#status WorkspacesDirectory#status}.
        :param user_access_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#user_access_url WorkspacesDirectory#user_access_url}.
        '''
        value = WorkspacesDirectorySamlProperties(
            relay_state_parameter_name=relay_state_parameter_name,
            status=status,
            user_access_url=user_access_url,
        )

        return typing.cast(None, jsii.invoke(self, "putSamlProperties", [value]))

    @jsii.member(jsii_name="putSelfServicePermissions")
    def put_self_service_permissions(
        self,
        *,
        change_compute_type: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        increase_volume_size: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rebuild_workspace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restart_workspace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        switch_running_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param change_compute_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#change_compute_type WorkspacesDirectory#change_compute_type}.
        :param increase_volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#increase_volume_size WorkspacesDirectory#increase_volume_size}.
        :param rebuild_workspace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#rebuild_workspace WorkspacesDirectory#rebuild_workspace}.
        :param restart_workspace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#restart_workspace WorkspacesDirectory#restart_workspace}.
        :param switch_running_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#switch_running_mode WorkspacesDirectory#switch_running_mode}.
        '''
        value = WorkspacesDirectorySelfServicePermissions(
            change_compute_type=change_compute_type,
            increase_volume_size=increase_volume_size,
            rebuild_workspace=rebuild_workspace,
            restart_workspace=restart_workspace,
            switch_running_mode=switch_running_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putSelfServicePermissions", [value]))

    @jsii.member(jsii_name="putWorkspaceAccessProperties")
    def put_workspace_access_properties(
        self,
        *,
        device_type_android: typing.Optional[builtins.str] = None,
        device_type_chromeos: typing.Optional[builtins.str] = None,
        device_type_ios: typing.Optional[builtins.str] = None,
        device_type_linux: typing.Optional[builtins.str] = None,
        device_type_osx: typing.Optional[builtins.str] = None,
        device_type_web: typing.Optional[builtins.str] = None,
        device_type_windows: typing.Optional[builtins.str] = None,
        device_type_zeroclient: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param device_type_android: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_android WorkspacesDirectory#device_type_android}.
        :param device_type_chromeos: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_chromeos WorkspacesDirectory#device_type_chromeos}.
        :param device_type_ios: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_ios WorkspacesDirectory#device_type_ios}.
        :param device_type_linux: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_linux WorkspacesDirectory#device_type_linux}.
        :param device_type_osx: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_osx WorkspacesDirectory#device_type_osx}.
        :param device_type_web: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_web WorkspacesDirectory#device_type_web}.
        :param device_type_windows: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_windows WorkspacesDirectory#device_type_windows}.
        :param device_type_zeroclient: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_zeroclient WorkspacesDirectory#device_type_zeroclient}.
        '''
        value = WorkspacesDirectoryWorkspaceAccessProperties(
            device_type_android=device_type_android,
            device_type_chromeos=device_type_chromeos,
            device_type_ios=device_type_ios,
            device_type_linux=device_type_linux,
            device_type_osx=device_type_osx,
            device_type_web=device_type_web,
            device_type_windows=device_type_windows,
            device_type_zeroclient=device_type_zeroclient,
        )

        return typing.cast(None, jsii.invoke(self, "putWorkspaceAccessProperties", [value]))

    @jsii.member(jsii_name="putWorkspaceCreationProperties")
    def put_workspace_creation_properties(
        self,
        *,
        custom_security_group_id: typing.Optional[builtins.str] = None,
        default_ou: typing.Optional[builtins.str] = None,
        enable_internet_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_maintenance_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_enabled_as_local_administrator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param custom_security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#custom_security_group_id WorkspacesDirectory#custom_security_group_id}.
        :param default_ou: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#default_ou WorkspacesDirectory#default_ou}.
        :param enable_internet_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#enable_internet_access WorkspacesDirectory#enable_internet_access}.
        :param enable_maintenance_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#enable_maintenance_mode WorkspacesDirectory#enable_maintenance_mode}.
        :param user_enabled_as_local_administrator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#user_enabled_as_local_administrator WorkspacesDirectory#user_enabled_as_local_administrator}.
        '''
        value = WorkspacesDirectoryWorkspaceCreationProperties(
            custom_security_group_id=custom_security_group_id,
            default_ou=default_ou,
            enable_internet_access=enable_internet_access,
            enable_maintenance_mode=enable_maintenance_mode,
            user_enabled_as_local_administrator=user_enabled_as_local_administrator,
        )

        return typing.cast(None, jsii.invoke(self, "putWorkspaceCreationProperties", [value]))

    @jsii.member(jsii_name="resetActiveDirectoryConfig")
    def reset_active_directory_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveDirectoryConfig", []))

    @jsii.member(jsii_name="resetCertificateBasedAuthProperties")
    def reset_certificate_based_auth_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateBasedAuthProperties", []))

    @jsii.member(jsii_name="resetDirectoryId")
    def reset_directory_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirectoryId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpGroupIds")
    def reset_ip_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpGroupIds", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSamlProperties")
    def reset_saml_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSamlProperties", []))

    @jsii.member(jsii_name="resetSelfServicePermissions")
    def reset_self_service_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelfServicePermissions", []))

    @jsii.member(jsii_name="resetSubnetIds")
    def reset_subnet_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetIds", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTenancy")
    def reset_tenancy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenancy", []))

    @jsii.member(jsii_name="resetUserIdentityType")
    def reset_user_identity_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserIdentityType", []))

    @jsii.member(jsii_name="resetWorkspaceAccessProperties")
    def reset_workspace_access_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkspaceAccessProperties", []))

    @jsii.member(jsii_name="resetWorkspaceCreationProperties")
    def reset_workspace_creation_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkspaceCreationProperties", []))

    @jsii.member(jsii_name="resetWorkspaceDirectoryDescription")
    def reset_workspace_directory_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkspaceDirectoryDescription", []))

    @jsii.member(jsii_name="resetWorkspaceDirectoryName")
    def reset_workspace_directory_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkspaceDirectoryName", []))

    @jsii.member(jsii_name="resetWorkspaceType")
    def reset_workspace_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkspaceType", []))

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
    @jsii.member(jsii_name="activeDirectoryConfig")
    def active_directory_config(
        self,
    ) -> "WorkspacesDirectoryActiveDirectoryConfigOutputReference":
        return typing.cast("WorkspacesDirectoryActiveDirectoryConfigOutputReference", jsii.get(self, "activeDirectoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alias"))

    @builtins.property
    @jsii.member(jsii_name="certificateBasedAuthProperties")
    def certificate_based_auth_properties(
        self,
    ) -> "WorkspacesDirectoryCertificateBasedAuthPropertiesOutputReference":
        return typing.cast("WorkspacesDirectoryCertificateBasedAuthPropertiesOutputReference", jsii.get(self, "certificateBasedAuthProperties"))

    @builtins.property
    @jsii.member(jsii_name="customerUserName")
    def customer_user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerUserName"))

    @builtins.property
    @jsii.member(jsii_name="directoryName")
    def directory_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "directoryName"))

    @builtins.property
    @jsii.member(jsii_name="directoryType")
    def directory_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "directoryType"))

    @builtins.property
    @jsii.member(jsii_name="dnsIpAddresses")
    def dns_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="iamRoleId")
    def iam_role_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iamRoleId"))

    @builtins.property
    @jsii.member(jsii_name="registrationCode")
    def registration_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registrationCode"))

    @builtins.property
    @jsii.member(jsii_name="samlProperties")
    def saml_properties(self) -> "WorkspacesDirectorySamlPropertiesOutputReference":
        return typing.cast("WorkspacesDirectorySamlPropertiesOutputReference", jsii.get(self, "samlProperties"))

    @builtins.property
    @jsii.member(jsii_name="selfServicePermissions")
    def self_service_permissions(
        self,
    ) -> "WorkspacesDirectorySelfServicePermissionsOutputReference":
        return typing.cast("WorkspacesDirectorySelfServicePermissionsOutputReference", jsii.get(self, "selfServicePermissions"))

    @builtins.property
    @jsii.member(jsii_name="workspaceAccessProperties")
    def workspace_access_properties(
        self,
    ) -> "WorkspacesDirectoryWorkspaceAccessPropertiesOutputReference":
        return typing.cast("WorkspacesDirectoryWorkspaceAccessPropertiesOutputReference", jsii.get(self, "workspaceAccessProperties"))

    @builtins.property
    @jsii.member(jsii_name="workspaceCreationProperties")
    def workspace_creation_properties(
        self,
    ) -> "WorkspacesDirectoryWorkspaceCreationPropertiesOutputReference":
        return typing.cast("WorkspacesDirectoryWorkspaceCreationPropertiesOutputReference", jsii.get(self, "workspaceCreationProperties"))

    @builtins.property
    @jsii.member(jsii_name="workspaceSecurityGroupId")
    def workspace_security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceSecurityGroupId"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryConfigInput")
    def active_directory_config_input(
        self,
    ) -> typing.Optional["WorkspacesDirectoryActiveDirectoryConfig"]:
        return typing.cast(typing.Optional["WorkspacesDirectoryActiveDirectoryConfig"], jsii.get(self, "activeDirectoryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateBasedAuthPropertiesInput")
    def certificate_based_auth_properties_input(
        self,
    ) -> typing.Optional["WorkspacesDirectoryCertificateBasedAuthProperties"]:
        return typing.cast(typing.Optional["WorkspacesDirectoryCertificateBasedAuthProperties"], jsii.get(self, "certificateBasedAuthPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="directoryIdInput")
    def directory_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directoryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipGroupIdsInput")
    def ip_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="samlPropertiesInput")
    def saml_properties_input(
        self,
    ) -> typing.Optional["WorkspacesDirectorySamlProperties"]:
        return typing.cast(typing.Optional["WorkspacesDirectorySamlProperties"], jsii.get(self, "samlPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="selfServicePermissionsInput")
    def self_service_permissions_input(
        self,
    ) -> typing.Optional["WorkspacesDirectorySelfServicePermissions"]:
        return typing.cast(typing.Optional["WorkspacesDirectorySelfServicePermissions"], jsii.get(self, "selfServicePermissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdsInput")
    def subnet_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIdsInput"))

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
    @jsii.member(jsii_name="tenancyInput")
    def tenancy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenancyInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdentityTypeInput")
    def user_identity_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userIdentityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceAccessPropertiesInput")
    def workspace_access_properties_input(
        self,
    ) -> typing.Optional["WorkspacesDirectoryWorkspaceAccessProperties"]:
        return typing.cast(typing.Optional["WorkspacesDirectoryWorkspaceAccessProperties"], jsii.get(self, "workspaceAccessPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceCreationPropertiesInput")
    def workspace_creation_properties_input(
        self,
    ) -> typing.Optional["WorkspacesDirectoryWorkspaceCreationProperties"]:
        return typing.cast(typing.Optional["WorkspacesDirectoryWorkspaceCreationProperties"], jsii.get(self, "workspaceCreationPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceDirectoryDescriptionInput")
    def workspace_directory_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceDirectoryDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceDirectoryNameInput")
    def workspace_directory_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceDirectoryNameInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceTypeInput")
    def workspace_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="directoryId")
    def directory_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "directoryId"))

    @directory_id.setter
    def directory_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb15ec31c43cd2d7014385f140b592d1bb42deb051d3063e83a5998db8ddcbba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directoryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f27e4c8f412daffa2c4efc8df9dea6974b517ade6acf14791a551411e6e4e10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipGroupIds")
    def ip_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipGroupIds"))

    @ip_group_ids.setter
    def ip_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1ac6e9dd1ef54e97c156292ddccdd103135ac48b172fa701d77378a6aec073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd886010213bf70c63427c8e7bf5d6a3a21d5aad716a2fe6f6f2e38a45c5839c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be37a78518ed1ab0e81fa15241d0f8ec557fdf14d250d6eebc573abe3bc21ff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701a96b57da218491536aab5add5c8ff0ccaf8268b5ecf1c7d191ea138bb9081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ce1985c562045fef951c0816c4d1b9c7d65dbdbb381339bb885a1da5bbeda50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenancy")
    def tenancy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenancy"))

    @tenancy.setter
    def tenancy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41e370f8b545fc7f01f015f99b657ae144ba7df1ef94ec73582be4e8b81b4245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenancy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userIdentityType")
    def user_identity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userIdentityType"))

    @user_identity_type.setter
    def user_identity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__679ec0cdfaefa1133bcd709373d48d7fe62b4d50c7209fa94849a5820e589311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userIdentityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspaceDirectoryDescription")
    def workspace_directory_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceDirectoryDescription"))

    @workspace_directory_description.setter
    def workspace_directory_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__309a81becb7965fca6d63093548c7bd3c60a5e531f9adc257ebeec707c2d68ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceDirectoryDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspaceDirectoryName")
    def workspace_directory_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceDirectoryName"))

    @workspace_directory_name.setter
    def workspace_directory_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015134dfdb00f7b458389036eb530115c2cea7032a23968fba8e4273fe290a51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceDirectoryName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspaceType")
    def workspace_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceType"))

    @workspace_type.setter
    def workspace_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd5ba46b759539d463bb247acf58dbd7a71c25368983babe4f3882094d0cd61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.workspacesDirectory.WorkspacesDirectoryActiveDirectoryConfig",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "service_account_secret_arn": "serviceAccountSecretArn",
    },
)
class WorkspacesDirectoryActiveDirectoryConfig:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        service_account_secret_arn: builtins.str,
    ) -> None:
        '''
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#domain_name WorkspacesDirectory#domain_name}.
        :param service_account_secret_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#service_account_secret_arn WorkspacesDirectory#service_account_secret_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b943d248b6838e52a06d6ac7fca464cf8def8e3a529dfc27c1e634fd9f4810e)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument service_account_secret_arn", value=service_account_secret_arn, expected_type=type_hints["service_account_secret_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
            "service_account_secret_arn": service_account_secret_arn,
        }

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#domain_name WorkspacesDirectory#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_account_secret_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#service_account_secret_arn WorkspacesDirectory#service_account_secret_arn}.'''
        result = self._values.get("service_account_secret_arn")
        assert result is not None, "Required property 'service_account_secret_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspacesDirectoryActiveDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkspacesDirectoryActiveDirectoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.workspacesDirectory.WorkspacesDirectoryActiveDirectoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b138f0d0bfdef6070fad665702bb3e5a8eae5fd3b3a7c6fce1b8123207e35f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountSecretArnInput")
    def service_account_secret_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountSecretArnInput"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76618b22e03c334f5587eaf9f6455afbff72248e3370f2456e599bd1843d78f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountSecretArn")
    def service_account_secret_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountSecretArn"))

    @service_account_secret_arn.setter
    def service_account_secret_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f7fc1d93623d085e224e3ad2cc0a8f9a31534d3a003f172cc286bec3be5308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountSecretArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkspacesDirectoryActiveDirectoryConfig]:
        return typing.cast(typing.Optional[WorkspacesDirectoryActiveDirectoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkspacesDirectoryActiveDirectoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac1cf7c636a2ea3cae78e1bb4d9a9903511c9cb580b6170d172ff1d8dadf5e3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.workspacesDirectory.WorkspacesDirectoryCertificateBasedAuthProperties",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_authority_arn": "certificateAuthorityArn",
        "status": "status",
    },
)
class WorkspacesDirectoryCertificateBasedAuthProperties:
    def __init__(
        self,
        *,
        certificate_authority_arn: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param certificate_authority_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#certificate_authority_arn WorkspacesDirectory#certificate_authority_arn}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#status WorkspacesDirectory#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a3eda9cb8d656525b4ed0a9b65cacbe291a3857efbb5bcf8efc976cb271add)
            check_type(argname="argument certificate_authority_arn", value=certificate_authority_arn, expected_type=type_hints["certificate_authority_arn"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_authority_arn is not None:
            self._values["certificate_authority_arn"] = certificate_authority_arn
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def certificate_authority_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#certificate_authority_arn WorkspacesDirectory#certificate_authority_arn}.'''
        result = self._values.get("certificate_authority_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#status WorkspacesDirectory#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspacesDirectoryCertificateBasedAuthProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkspacesDirectoryCertificateBasedAuthPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.workspacesDirectory.WorkspacesDirectoryCertificateBasedAuthPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48cb378b98a8246982b2eb4b5774a62b330579f3bd1dbe514bf26308c54690db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCertificateAuthorityArn")
    def reset_certificate_authority_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateAuthorityArn", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityArnInput")
    def certificate_authority_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateAuthorityArnInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateAuthorityArn"))

    @certificate_authority_arn.setter
    def certificate_authority_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e768abfef43544b467122922869c6a38687cd0b7faf0677c143f41602a8613f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateAuthorityArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2c885f82081b87a3813495e1143007f9dc0702f2d2bc557c270c1f07368b937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkspacesDirectoryCertificateBasedAuthProperties]:
        return typing.cast(typing.Optional[WorkspacesDirectoryCertificateBasedAuthProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkspacesDirectoryCertificateBasedAuthProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6f9557c8451832de5388894d8777b3ca449aa8c22c740b323a239957c35591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.workspacesDirectory.WorkspacesDirectoryConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "active_directory_config": "activeDirectoryConfig",
        "certificate_based_auth_properties": "certificateBasedAuthProperties",
        "directory_id": "directoryId",
        "id": "id",
        "ip_group_ids": "ipGroupIds",
        "region": "region",
        "saml_properties": "samlProperties",
        "self_service_permissions": "selfServicePermissions",
        "subnet_ids": "subnetIds",
        "tags": "tags",
        "tags_all": "tagsAll",
        "tenancy": "tenancy",
        "user_identity_type": "userIdentityType",
        "workspace_access_properties": "workspaceAccessProperties",
        "workspace_creation_properties": "workspaceCreationProperties",
        "workspace_directory_description": "workspaceDirectoryDescription",
        "workspace_directory_name": "workspaceDirectoryName",
        "workspace_type": "workspaceType",
    },
)
class WorkspacesDirectoryConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        active_directory_config: typing.Optional[typing.Union[WorkspacesDirectoryActiveDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        certificate_based_auth_properties: typing.Optional[typing.Union[WorkspacesDirectoryCertificateBasedAuthProperties, typing.Dict[builtins.str, typing.Any]]] = None,
        directory_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        saml_properties: typing.Optional[typing.Union["WorkspacesDirectorySamlProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        self_service_permissions: typing.Optional[typing.Union["WorkspacesDirectorySelfServicePermissions", typing.Dict[builtins.str, typing.Any]]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tenancy: typing.Optional[builtins.str] = None,
        user_identity_type: typing.Optional[builtins.str] = None,
        workspace_access_properties: typing.Optional[typing.Union["WorkspacesDirectoryWorkspaceAccessProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        workspace_creation_properties: typing.Optional[typing.Union["WorkspacesDirectoryWorkspaceCreationProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        workspace_directory_description: typing.Optional[builtins.str] = None,
        workspace_directory_name: typing.Optional[builtins.str] = None,
        workspace_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param active_directory_config: active_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#active_directory_config WorkspacesDirectory#active_directory_config}
        :param certificate_based_auth_properties: certificate_based_auth_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#certificate_based_auth_properties WorkspacesDirectory#certificate_based_auth_properties}
        :param directory_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#directory_id WorkspacesDirectory#directory_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#id WorkspacesDirectory#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#ip_group_ids WorkspacesDirectory#ip_group_ids}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#region WorkspacesDirectory#region}
        :param saml_properties: saml_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#saml_properties WorkspacesDirectory#saml_properties}
        :param self_service_permissions: self_service_permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#self_service_permissions WorkspacesDirectory#self_service_permissions}
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#subnet_ids WorkspacesDirectory#subnet_ids}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#tags WorkspacesDirectory#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#tags_all WorkspacesDirectory#tags_all}.
        :param tenancy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#tenancy WorkspacesDirectory#tenancy}.
        :param user_identity_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#user_identity_type WorkspacesDirectory#user_identity_type}.
        :param workspace_access_properties: workspace_access_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#workspace_access_properties WorkspacesDirectory#workspace_access_properties}
        :param workspace_creation_properties: workspace_creation_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#workspace_creation_properties WorkspacesDirectory#workspace_creation_properties}
        :param workspace_directory_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#workspace_directory_description WorkspacesDirectory#workspace_directory_description}.
        :param workspace_directory_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#workspace_directory_name WorkspacesDirectory#workspace_directory_name}.
        :param workspace_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#workspace_type WorkspacesDirectory#workspace_type}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(active_directory_config, dict):
            active_directory_config = WorkspacesDirectoryActiveDirectoryConfig(**active_directory_config)
        if isinstance(certificate_based_auth_properties, dict):
            certificate_based_auth_properties = WorkspacesDirectoryCertificateBasedAuthProperties(**certificate_based_auth_properties)
        if isinstance(saml_properties, dict):
            saml_properties = WorkspacesDirectorySamlProperties(**saml_properties)
        if isinstance(self_service_permissions, dict):
            self_service_permissions = WorkspacesDirectorySelfServicePermissions(**self_service_permissions)
        if isinstance(workspace_access_properties, dict):
            workspace_access_properties = WorkspacesDirectoryWorkspaceAccessProperties(**workspace_access_properties)
        if isinstance(workspace_creation_properties, dict):
            workspace_creation_properties = WorkspacesDirectoryWorkspaceCreationProperties(**workspace_creation_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f32ea060c923d45dd03bf9fb04e34f34eabc4160c71cbb8d0f409e8b93e03012)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument active_directory_config", value=active_directory_config, expected_type=type_hints["active_directory_config"])
            check_type(argname="argument certificate_based_auth_properties", value=certificate_based_auth_properties, expected_type=type_hints["certificate_based_auth_properties"])
            check_type(argname="argument directory_id", value=directory_id, expected_type=type_hints["directory_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_group_ids", value=ip_group_ids, expected_type=type_hints["ip_group_ids"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument saml_properties", value=saml_properties, expected_type=type_hints["saml_properties"])
            check_type(argname="argument self_service_permissions", value=self_service_permissions, expected_type=type_hints["self_service_permissions"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument tenancy", value=tenancy, expected_type=type_hints["tenancy"])
            check_type(argname="argument user_identity_type", value=user_identity_type, expected_type=type_hints["user_identity_type"])
            check_type(argname="argument workspace_access_properties", value=workspace_access_properties, expected_type=type_hints["workspace_access_properties"])
            check_type(argname="argument workspace_creation_properties", value=workspace_creation_properties, expected_type=type_hints["workspace_creation_properties"])
            check_type(argname="argument workspace_directory_description", value=workspace_directory_description, expected_type=type_hints["workspace_directory_description"])
            check_type(argname="argument workspace_directory_name", value=workspace_directory_name, expected_type=type_hints["workspace_directory_name"])
            check_type(argname="argument workspace_type", value=workspace_type, expected_type=type_hints["workspace_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if active_directory_config is not None:
            self._values["active_directory_config"] = active_directory_config
        if certificate_based_auth_properties is not None:
            self._values["certificate_based_auth_properties"] = certificate_based_auth_properties
        if directory_id is not None:
            self._values["directory_id"] = directory_id
        if id is not None:
            self._values["id"] = id
        if ip_group_ids is not None:
            self._values["ip_group_ids"] = ip_group_ids
        if region is not None:
            self._values["region"] = region
        if saml_properties is not None:
            self._values["saml_properties"] = saml_properties
        if self_service_permissions is not None:
            self._values["self_service_permissions"] = self_service_permissions
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if tenancy is not None:
            self._values["tenancy"] = tenancy
        if user_identity_type is not None:
            self._values["user_identity_type"] = user_identity_type
        if workspace_access_properties is not None:
            self._values["workspace_access_properties"] = workspace_access_properties
        if workspace_creation_properties is not None:
            self._values["workspace_creation_properties"] = workspace_creation_properties
        if workspace_directory_description is not None:
            self._values["workspace_directory_description"] = workspace_directory_description
        if workspace_directory_name is not None:
            self._values["workspace_directory_name"] = workspace_directory_name
        if workspace_type is not None:
            self._values["workspace_type"] = workspace_type

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
    def active_directory_config(
        self,
    ) -> typing.Optional[WorkspacesDirectoryActiveDirectoryConfig]:
        '''active_directory_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#active_directory_config WorkspacesDirectory#active_directory_config}
        '''
        result = self._values.get("active_directory_config")
        return typing.cast(typing.Optional[WorkspacesDirectoryActiveDirectoryConfig], result)

    @builtins.property
    def certificate_based_auth_properties(
        self,
    ) -> typing.Optional[WorkspacesDirectoryCertificateBasedAuthProperties]:
        '''certificate_based_auth_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#certificate_based_auth_properties WorkspacesDirectory#certificate_based_auth_properties}
        '''
        result = self._values.get("certificate_based_auth_properties")
        return typing.cast(typing.Optional[WorkspacesDirectoryCertificateBasedAuthProperties], result)

    @builtins.property
    def directory_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#directory_id WorkspacesDirectory#directory_id}.'''
        result = self._values.get("directory_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#id WorkspacesDirectory#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#ip_group_ids WorkspacesDirectory#ip_group_ids}.'''
        result = self._values.get("ip_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#region WorkspacesDirectory#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml_properties(self) -> typing.Optional["WorkspacesDirectorySamlProperties"]:
        '''saml_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#saml_properties WorkspacesDirectory#saml_properties}
        '''
        result = self._values.get("saml_properties")
        return typing.cast(typing.Optional["WorkspacesDirectorySamlProperties"], result)

    @builtins.property
    def self_service_permissions(
        self,
    ) -> typing.Optional["WorkspacesDirectorySelfServicePermissions"]:
        '''self_service_permissions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#self_service_permissions WorkspacesDirectory#self_service_permissions}
        '''
        result = self._values.get("self_service_permissions")
        return typing.cast(typing.Optional["WorkspacesDirectorySelfServicePermissions"], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#subnet_ids WorkspacesDirectory#subnet_ids}.'''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#tags WorkspacesDirectory#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#tags_all WorkspacesDirectory#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tenancy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#tenancy WorkspacesDirectory#tenancy}.'''
        result = self._values.get("tenancy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_identity_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#user_identity_type WorkspacesDirectory#user_identity_type}.'''
        result = self._values.get("user_identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_access_properties(
        self,
    ) -> typing.Optional["WorkspacesDirectoryWorkspaceAccessProperties"]:
        '''workspace_access_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#workspace_access_properties WorkspacesDirectory#workspace_access_properties}
        '''
        result = self._values.get("workspace_access_properties")
        return typing.cast(typing.Optional["WorkspacesDirectoryWorkspaceAccessProperties"], result)

    @builtins.property
    def workspace_creation_properties(
        self,
    ) -> typing.Optional["WorkspacesDirectoryWorkspaceCreationProperties"]:
        '''workspace_creation_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#workspace_creation_properties WorkspacesDirectory#workspace_creation_properties}
        '''
        result = self._values.get("workspace_creation_properties")
        return typing.cast(typing.Optional["WorkspacesDirectoryWorkspaceCreationProperties"], result)

    @builtins.property
    def workspace_directory_description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#workspace_directory_description WorkspacesDirectory#workspace_directory_description}.'''
        result = self._values.get("workspace_directory_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_directory_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#workspace_directory_name WorkspacesDirectory#workspace_directory_name}.'''
        result = self._values.get("workspace_directory_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#workspace_type WorkspacesDirectory#workspace_type}.'''
        result = self._values.get("workspace_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspacesDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.workspacesDirectory.WorkspacesDirectorySamlProperties",
    jsii_struct_bases=[],
    name_mapping={
        "relay_state_parameter_name": "relayStateParameterName",
        "status": "status",
        "user_access_url": "userAccessUrl",
    },
)
class WorkspacesDirectorySamlProperties:
    def __init__(
        self,
        *,
        relay_state_parameter_name: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        user_access_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param relay_state_parameter_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#relay_state_parameter_name WorkspacesDirectory#relay_state_parameter_name}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#status WorkspacesDirectory#status}.
        :param user_access_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#user_access_url WorkspacesDirectory#user_access_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf3c069f6cfd981ad2d429b511ad2a029d6723806a3fd9d7f7a7afb648524d9f)
            check_type(argname="argument relay_state_parameter_name", value=relay_state_parameter_name, expected_type=type_hints["relay_state_parameter_name"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument user_access_url", value=user_access_url, expected_type=type_hints["user_access_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if relay_state_parameter_name is not None:
            self._values["relay_state_parameter_name"] = relay_state_parameter_name
        if status is not None:
            self._values["status"] = status
        if user_access_url is not None:
            self._values["user_access_url"] = user_access_url

    @builtins.property
    def relay_state_parameter_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#relay_state_parameter_name WorkspacesDirectory#relay_state_parameter_name}.'''
        result = self._values.get("relay_state_parameter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#status WorkspacesDirectory#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_access_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#user_access_url WorkspacesDirectory#user_access_url}.'''
        result = self._values.get("user_access_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspacesDirectorySamlProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkspacesDirectorySamlPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.workspacesDirectory.WorkspacesDirectorySamlPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd010e0d4d9572d572adf4875f8324a744502cca2652b7f2c0c348f2c6179f84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRelayStateParameterName")
    def reset_relay_state_parameter_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelayStateParameterName", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetUserAccessUrl")
    def reset_user_access_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAccessUrl", []))

    @builtins.property
    @jsii.member(jsii_name="relayStateParameterNameInput")
    def relay_state_parameter_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "relayStateParameterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="userAccessUrlInput")
    def user_access_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userAccessUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="relayStateParameterName")
    def relay_state_parameter_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "relayStateParameterName"))

    @relay_state_parameter_name.setter
    def relay_state_parameter_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__303bacc15aaf60da40dff35ce857495c95b817259ce26c74600cd85fe049b985)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relayStateParameterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa656667669ceb61e9c39efd20b0a25cd570bba9ca7e36f0ec298159840c1087)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userAccessUrl")
    def user_access_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAccessUrl"))

    @user_access_url.setter
    def user_access_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26e0fef0be4d644fbb71d6954214a1c3c97cd8d9fe660d8c6f847b2c5999572a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAccessUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WorkspacesDirectorySamlProperties]:
        return typing.cast(typing.Optional[WorkspacesDirectorySamlProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkspacesDirectorySamlProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__073fe0978fe826ac6add6c1609de5dc9accadfcc1d9b0d766fcb3cb3b613723c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.workspacesDirectory.WorkspacesDirectorySelfServicePermissions",
    jsii_struct_bases=[],
    name_mapping={
        "change_compute_type": "changeComputeType",
        "increase_volume_size": "increaseVolumeSize",
        "rebuild_workspace": "rebuildWorkspace",
        "restart_workspace": "restartWorkspace",
        "switch_running_mode": "switchRunningMode",
    },
)
class WorkspacesDirectorySelfServicePermissions:
    def __init__(
        self,
        *,
        change_compute_type: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        increase_volume_size: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rebuild_workspace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restart_workspace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        switch_running_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param change_compute_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#change_compute_type WorkspacesDirectory#change_compute_type}.
        :param increase_volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#increase_volume_size WorkspacesDirectory#increase_volume_size}.
        :param rebuild_workspace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#rebuild_workspace WorkspacesDirectory#rebuild_workspace}.
        :param restart_workspace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#restart_workspace WorkspacesDirectory#restart_workspace}.
        :param switch_running_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#switch_running_mode WorkspacesDirectory#switch_running_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e4305e5557d83b3319e88333388ef209f8a1894df54cb46874e1d92deb26acd)
            check_type(argname="argument change_compute_type", value=change_compute_type, expected_type=type_hints["change_compute_type"])
            check_type(argname="argument increase_volume_size", value=increase_volume_size, expected_type=type_hints["increase_volume_size"])
            check_type(argname="argument rebuild_workspace", value=rebuild_workspace, expected_type=type_hints["rebuild_workspace"])
            check_type(argname="argument restart_workspace", value=restart_workspace, expected_type=type_hints["restart_workspace"])
            check_type(argname="argument switch_running_mode", value=switch_running_mode, expected_type=type_hints["switch_running_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if change_compute_type is not None:
            self._values["change_compute_type"] = change_compute_type
        if increase_volume_size is not None:
            self._values["increase_volume_size"] = increase_volume_size
        if rebuild_workspace is not None:
            self._values["rebuild_workspace"] = rebuild_workspace
        if restart_workspace is not None:
            self._values["restart_workspace"] = restart_workspace
        if switch_running_mode is not None:
            self._values["switch_running_mode"] = switch_running_mode

    @builtins.property
    def change_compute_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#change_compute_type WorkspacesDirectory#change_compute_type}.'''
        result = self._values.get("change_compute_type")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def increase_volume_size(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#increase_volume_size WorkspacesDirectory#increase_volume_size}.'''
        result = self._values.get("increase_volume_size")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rebuild_workspace(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#rebuild_workspace WorkspacesDirectory#rebuild_workspace}.'''
        result = self._values.get("rebuild_workspace")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def restart_workspace(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#restart_workspace WorkspacesDirectory#restart_workspace}.'''
        result = self._values.get("restart_workspace")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def switch_running_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#switch_running_mode WorkspacesDirectory#switch_running_mode}.'''
        result = self._values.get("switch_running_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspacesDirectorySelfServicePermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkspacesDirectorySelfServicePermissionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.workspacesDirectory.WorkspacesDirectorySelfServicePermissionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f2750f8c67fc48bc7226f1a60b9440221c65af13c74f6fcd1caa60a2a27b956)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetChangeComputeType")
    def reset_change_compute_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChangeComputeType", []))

    @jsii.member(jsii_name="resetIncreaseVolumeSize")
    def reset_increase_volume_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncreaseVolumeSize", []))

    @jsii.member(jsii_name="resetRebuildWorkspace")
    def reset_rebuild_workspace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRebuildWorkspace", []))

    @jsii.member(jsii_name="resetRestartWorkspace")
    def reset_restart_workspace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestartWorkspace", []))

    @jsii.member(jsii_name="resetSwitchRunningMode")
    def reset_switch_running_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSwitchRunningMode", []))

    @builtins.property
    @jsii.member(jsii_name="changeComputeTypeInput")
    def change_compute_type_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "changeComputeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="increaseVolumeSizeInput")
    def increase_volume_size_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "increaseVolumeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="rebuildWorkspaceInput")
    def rebuild_workspace_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rebuildWorkspaceInput"))

    @builtins.property
    @jsii.member(jsii_name="restartWorkspaceInput")
    def restart_workspace_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "restartWorkspaceInput"))

    @builtins.property
    @jsii.member(jsii_name="switchRunningModeInput")
    def switch_running_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "switchRunningModeInput"))

    @builtins.property
    @jsii.member(jsii_name="changeComputeType")
    def change_compute_type(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "changeComputeType"))

    @change_compute_type.setter
    def change_compute_type(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7fa051afd161dad3fed45ee1a52fcfedd9d7937574645d5ae61cf039bbe9609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "changeComputeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="increaseVolumeSize")
    def increase_volume_size(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "increaseVolumeSize"))

    @increase_volume_size.setter
    def increase_volume_size(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eb700e89f9c04222660eb417ebc20b0868929580d618134ed9687ac09d33d48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "increaseVolumeSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rebuildWorkspace")
    def rebuild_workspace(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rebuildWorkspace"))

    @rebuild_workspace.setter
    def rebuild_workspace(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5516f2e46edae4a101bb6d41275db092f50a998231a53452fd7858207c43d866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rebuildWorkspace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restartWorkspace")
    def restart_workspace(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "restartWorkspace"))

    @restart_workspace.setter
    def restart_workspace(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1006cf4e438f0c1c0c5cb3d5210f161c40a02279a1cecd93cefc131671bedd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restartWorkspace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="switchRunningMode")
    def switch_running_mode(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "switchRunningMode"))

    @switch_running_mode.setter
    def switch_running_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e4b3698cfdfcb8b8fce44f6715d36dc6fce1553e6a9e9f4fc54c650069f0975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "switchRunningMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkspacesDirectorySelfServicePermissions]:
        return typing.cast(typing.Optional[WorkspacesDirectorySelfServicePermissions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkspacesDirectorySelfServicePermissions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__881967ff04faaf639f38f97c1bf83802d405d0347cd1c1ab0408a4d98a468bc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.workspacesDirectory.WorkspacesDirectoryWorkspaceAccessProperties",
    jsii_struct_bases=[],
    name_mapping={
        "device_type_android": "deviceTypeAndroid",
        "device_type_chromeos": "deviceTypeChromeos",
        "device_type_ios": "deviceTypeIos",
        "device_type_linux": "deviceTypeLinux",
        "device_type_osx": "deviceTypeOsx",
        "device_type_web": "deviceTypeWeb",
        "device_type_windows": "deviceTypeWindows",
        "device_type_zeroclient": "deviceTypeZeroclient",
    },
)
class WorkspacesDirectoryWorkspaceAccessProperties:
    def __init__(
        self,
        *,
        device_type_android: typing.Optional[builtins.str] = None,
        device_type_chromeos: typing.Optional[builtins.str] = None,
        device_type_ios: typing.Optional[builtins.str] = None,
        device_type_linux: typing.Optional[builtins.str] = None,
        device_type_osx: typing.Optional[builtins.str] = None,
        device_type_web: typing.Optional[builtins.str] = None,
        device_type_windows: typing.Optional[builtins.str] = None,
        device_type_zeroclient: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param device_type_android: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_android WorkspacesDirectory#device_type_android}.
        :param device_type_chromeos: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_chromeos WorkspacesDirectory#device_type_chromeos}.
        :param device_type_ios: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_ios WorkspacesDirectory#device_type_ios}.
        :param device_type_linux: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_linux WorkspacesDirectory#device_type_linux}.
        :param device_type_osx: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_osx WorkspacesDirectory#device_type_osx}.
        :param device_type_web: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_web WorkspacesDirectory#device_type_web}.
        :param device_type_windows: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_windows WorkspacesDirectory#device_type_windows}.
        :param device_type_zeroclient: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_zeroclient WorkspacesDirectory#device_type_zeroclient}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b29e2eb91bedf3812c61235b8af9ebddc48f347268b042c1320cac04f8301c9a)
            check_type(argname="argument device_type_android", value=device_type_android, expected_type=type_hints["device_type_android"])
            check_type(argname="argument device_type_chromeos", value=device_type_chromeos, expected_type=type_hints["device_type_chromeos"])
            check_type(argname="argument device_type_ios", value=device_type_ios, expected_type=type_hints["device_type_ios"])
            check_type(argname="argument device_type_linux", value=device_type_linux, expected_type=type_hints["device_type_linux"])
            check_type(argname="argument device_type_osx", value=device_type_osx, expected_type=type_hints["device_type_osx"])
            check_type(argname="argument device_type_web", value=device_type_web, expected_type=type_hints["device_type_web"])
            check_type(argname="argument device_type_windows", value=device_type_windows, expected_type=type_hints["device_type_windows"])
            check_type(argname="argument device_type_zeroclient", value=device_type_zeroclient, expected_type=type_hints["device_type_zeroclient"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if device_type_android is not None:
            self._values["device_type_android"] = device_type_android
        if device_type_chromeos is not None:
            self._values["device_type_chromeos"] = device_type_chromeos
        if device_type_ios is not None:
            self._values["device_type_ios"] = device_type_ios
        if device_type_linux is not None:
            self._values["device_type_linux"] = device_type_linux
        if device_type_osx is not None:
            self._values["device_type_osx"] = device_type_osx
        if device_type_web is not None:
            self._values["device_type_web"] = device_type_web
        if device_type_windows is not None:
            self._values["device_type_windows"] = device_type_windows
        if device_type_zeroclient is not None:
            self._values["device_type_zeroclient"] = device_type_zeroclient

    @builtins.property
    def device_type_android(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_android WorkspacesDirectory#device_type_android}.'''
        result = self._values.get("device_type_android")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_type_chromeos(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_chromeos WorkspacesDirectory#device_type_chromeos}.'''
        result = self._values.get("device_type_chromeos")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_type_ios(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_ios WorkspacesDirectory#device_type_ios}.'''
        result = self._values.get("device_type_ios")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_type_linux(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_linux WorkspacesDirectory#device_type_linux}.'''
        result = self._values.get("device_type_linux")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_type_osx(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_osx WorkspacesDirectory#device_type_osx}.'''
        result = self._values.get("device_type_osx")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_type_web(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_web WorkspacesDirectory#device_type_web}.'''
        result = self._values.get("device_type_web")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_type_windows(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_windows WorkspacesDirectory#device_type_windows}.'''
        result = self._values.get("device_type_windows")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_type_zeroclient(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#device_type_zeroclient WorkspacesDirectory#device_type_zeroclient}.'''
        result = self._values.get("device_type_zeroclient")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspacesDirectoryWorkspaceAccessProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkspacesDirectoryWorkspaceAccessPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.workspacesDirectory.WorkspacesDirectoryWorkspaceAccessPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db5aa1b442be1d150924659608547f6fbbb6bfad5e9d33232043616a36cf89a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDeviceTypeAndroid")
    def reset_device_type_android(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceTypeAndroid", []))

    @jsii.member(jsii_name="resetDeviceTypeChromeos")
    def reset_device_type_chromeos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceTypeChromeos", []))

    @jsii.member(jsii_name="resetDeviceTypeIos")
    def reset_device_type_ios(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceTypeIos", []))

    @jsii.member(jsii_name="resetDeviceTypeLinux")
    def reset_device_type_linux(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceTypeLinux", []))

    @jsii.member(jsii_name="resetDeviceTypeOsx")
    def reset_device_type_osx(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceTypeOsx", []))

    @jsii.member(jsii_name="resetDeviceTypeWeb")
    def reset_device_type_web(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceTypeWeb", []))

    @jsii.member(jsii_name="resetDeviceTypeWindows")
    def reset_device_type_windows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceTypeWindows", []))

    @jsii.member(jsii_name="resetDeviceTypeZeroclient")
    def reset_device_type_zeroclient(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceTypeZeroclient", []))

    @builtins.property
    @jsii.member(jsii_name="deviceTypeAndroidInput")
    def device_type_android_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceTypeAndroidInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceTypeChromeosInput")
    def device_type_chromeos_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceTypeChromeosInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceTypeIosInput")
    def device_type_ios_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceTypeIosInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceTypeLinuxInput")
    def device_type_linux_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceTypeLinuxInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceTypeOsxInput")
    def device_type_osx_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceTypeOsxInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceTypeWebInput")
    def device_type_web_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceTypeWebInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceTypeWindowsInput")
    def device_type_windows_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceTypeWindowsInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceTypeZeroclientInput")
    def device_type_zeroclient_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceTypeZeroclientInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceTypeAndroid")
    def device_type_android(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceTypeAndroid"))

    @device_type_android.setter
    def device_type_android(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a005131979cd4cdbeb209344eecbef64223a6eb6d75726df38054426afe356a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceTypeAndroid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceTypeChromeos")
    def device_type_chromeos(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceTypeChromeos"))

    @device_type_chromeos.setter
    def device_type_chromeos(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45986b5ad6b18e66a2a69f6415501789ef40e6f5df7c32b96d3c1807d28dcde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceTypeChromeos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceTypeIos")
    def device_type_ios(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceTypeIos"))

    @device_type_ios.setter
    def device_type_ios(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d83e40f60c8c437f0d0dd6662a8a8f4bc347fb35bd2beeb838b8e49064ebf736)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceTypeIos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceTypeLinux")
    def device_type_linux(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceTypeLinux"))

    @device_type_linux.setter
    def device_type_linux(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d2c2dcc37420af45df46a9b6239ccc9573e8fdab6bb12757bddde1dca4fc890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceTypeLinux", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceTypeOsx")
    def device_type_osx(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceTypeOsx"))

    @device_type_osx.setter
    def device_type_osx(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab9ba0397511a4e190f9a70895cdb5fbdd204e23c358aeda02c43f9e24a8bc24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceTypeOsx", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceTypeWeb")
    def device_type_web(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceTypeWeb"))

    @device_type_web.setter
    def device_type_web(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a491ebb5f93187fbb8afb65c461083263a5210702fdb7c38b8f6ed276f1dd642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceTypeWeb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceTypeWindows")
    def device_type_windows(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceTypeWindows"))

    @device_type_windows.setter
    def device_type_windows(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dae86940a3a83012fe1ac7afcda423aa3fbaf310c438c1cbb6700976c8cca01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceTypeWindows", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceTypeZeroclient")
    def device_type_zeroclient(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceTypeZeroclient"))

    @device_type_zeroclient.setter
    def device_type_zeroclient(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__098a85d70d785af72522d94ce64961cf1da9c47e5c9aea4dd5aafecb43ab3827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceTypeZeroclient", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkspacesDirectoryWorkspaceAccessProperties]:
        return typing.cast(typing.Optional[WorkspacesDirectoryWorkspaceAccessProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkspacesDirectoryWorkspaceAccessProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e477943e9e314790fa841ebc3da770695dd86701ef1af07ff0ce6594ad046ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.workspacesDirectory.WorkspacesDirectoryWorkspaceCreationProperties",
    jsii_struct_bases=[],
    name_mapping={
        "custom_security_group_id": "customSecurityGroupId",
        "default_ou": "defaultOu",
        "enable_internet_access": "enableInternetAccess",
        "enable_maintenance_mode": "enableMaintenanceMode",
        "user_enabled_as_local_administrator": "userEnabledAsLocalAdministrator",
    },
)
class WorkspacesDirectoryWorkspaceCreationProperties:
    def __init__(
        self,
        *,
        custom_security_group_id: typing.Optional[builtins.str] = None,
        default_ou: typing.Optional[builtins.str] = None,
        enable_internet_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_maintenance_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_enabled_as_local_administrator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param custom_security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#custom_security_group_id WorkspacesDirectory#custom_security_group_id}.
        :param default_ou: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#default_ou WorkspacesDirectory#default_ou}.
        :param enable_internet_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#enable_internet_access WorkspacesDirectory#enable_internet_access}.
        :param enable_maintenance_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#enable_maintenance_mode WorkspacesDirectory#enable_maintenance_mode}.
        :param user_enabled_as_local_administrator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#user_enabled_as_local_administrator WorkspacesDirectory#user_enabled_as_local_administrator}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5bbcb01c66b17901813c3f741153d7b9d8905022fac0ef53fe1e3a31928268f)
            check_type(argname="argument custom_security_group_id", value=custom_security_group_id, expected_type=type_hints["custom_security_group_id"])
            check_type(argname="argument default_ou", value=default_ou, expected_type=type_hints["default_ou"])
            check_type(argname="argument enable_internet_access", value=enable_internet_access, expected_type=type_hints["enable_internet_access"])
            check_type(argname="argument enable_maintenance_mode", value=enable_maintenance_mode, expected_type=type_hints["enable_maintenance_mode"])
            check_type(argname="argument user_enabled_as_local_administrator", value=user_enabled_as_local_administrator, expected_type=type_hints["user_enabled_as_local_administrator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_security_group_id is not None:
            self._values["custom_security_group_id"] = custom_security_group_id
        if default_ou is not None:
            self._values["default_ou"] = default_ou
        if enable_internet_access is not None:
            self._values["enable_internet_access"] = enable_internet_access
        if enable_maintenance_mode is not None:
            self._values["enable_maintenance_mode"] = enable_maintenance_mode
        if user_enabled_as_local_administrator is not None:
            self._values["user_enabled_as_local_administrator"] = user_enabled_as_local_administrator

    @builtins.property
    def custom_security_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#custom_security_group_id WorkspacesDirectory#custom_security_group_id}.'''
        result = self._values.get("custom_security_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_ou(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#default_ou WorkspacesDirectory#default_ou}.'''
        result = self._values.get("default_ou")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#enable_internet_access WorkspacesDirectory#enable_internet_access}.'''
        result = self._values.get("enable_internet_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_maintenance_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#enable_maintenance_mode WorkspacesDirectory#enable_maintenance_mode}.'''
        result = self._values.get("enable_maintenance_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def user_enabled_as_local_administrator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/workspaces_directory#user_enabled_as_local_administrator WorkspacesDirectory#user_enabled_as_local_administrator}.'''
        result = self._values.get("user_enabled_as_local_administrator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspacesDirectoryWorkspaceCreationProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkspacesDirectoryWorkspaceCreationPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.workspacesDirectory.WorkspacesDirectoryWorkspaceCreationPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3eab1dd9c75e4bd2f51b34401cba3bcc30492a56848de14676c9255bee1cf1f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCustomSecurityGroupId")
    def reset_custom_security_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomSecurityGroupId", []))

    @jsii.member(jsii_name="resetDefaultOu")
    def reset_default_ou(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultOu", []))

    @jsii.member(jsii_name="resetEnableInternetAccess")
    def reset_enable_internet_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableInternetAccess", []))

    @jsii.member(jsii_name="resetEnableMaintenanceMode")
    def reset_enable_maintenance_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableMaintenanceMode", []))

    @jsii.member(jsii_name="resetUserEnabledAsLocalAdministrator")
    def reset_user_enabled_as_local_administrator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserEnabledAsLocalAdministrator", []))

    @builtins.property
    @jsii.member(jsii_name="customSecurityGroupIdInput")
    def custom_security_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customSecurityGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultOuInput")
    def default_ou_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultOuInput"))

    @builtins.property
    @jsii.member(jsii_name="enableInternetAccessInput")
    def enable_internet_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInternetAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="enableMaintenanceModeInput")
    def enable_maintenance_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableMaintenanceModeInput"))

    @builtins.property
    @jsii.member(jsii_name="userEnabledAsLocalAdministratorInput")
    def user_enabled_as_local_administrator_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "userEnabledAsLocalAdministratorInput"))

    @builtins.property
    @jsii.member(jsii_name="customSecurityGroupId")
    def custom_security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customSecurityGroupId"))

    @custom_security_group_id.setter
    def custom_security_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2512bf1c04b8c27606f1125c9387bb3150d2bb8569ee586ffe54d54cf1334dbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customSecurityGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultOu")
    def default_ou(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultOu"))

    @default_ou.setter
    def default_ou(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c155046ecc0e75a43cec257f3b1afbe4e226e097c04ee41c88b2ba8758204c57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultOu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableInternetAccess")
    def enable_internet_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableInternetAccess"))

    @enable_internet_access.setter
    def enable_internet_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3393d7f1b52919e4c5706d0bf465fc099998202673e57cd4b5371d7492141f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableInternetAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableMaintenanceMode")
    def enable_maintenance_mode(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableMaintenanceMode"))

    @enable_maintenance_mode.setter
    def enable_maintenance_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1877131438810a9bc401b2c3a6d216708f392716153ab0f2523c627d1b18a63a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableMaintenanceMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userEnabledAsLocalAdministrator")
    def user_enabled_as_local_administrator(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "userEnabledAsLocalAdministrator"))

    @user_enabled_as_local_administrator.setter
    def user_enabled_as_local_administrator(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f0d01e4222f300482f169a2c439d095a28ae09538021094486333c09fa3ed48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userEnabledAsLocalAdministrator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkspacesDirectoryWorkspaceCreationProperties]:
        return typing.cast(typing.Optional[WorkspacesDirectoryWorkspaceCreationProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkspacesDirectoryWorkspaceCreationProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffc6a9aff5cf54711d32c0c11f9e7dd529699bd6bac9da58c8187407807dcd53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WorkspacesDirectory",
    "WorkspacesDirectoryActiveDirectoryConfig",
    "WorkspacesDirectoryActiveDirectoryConfigOutputReference",
    "WorkspacesDirectoryCertificateBasedAuthProperties",
    "WorkspacesDirectoryCertificateBasedAuthPropertiesOutputReference",
    "WorkspacesDirectoryConfig",
    "WorkspacesDirectorySamlProperties",
    "WorkspacesDirectorySamlPropertiesOutputReference",
    "WorkspacesDirectorySelfServicePermissions",
    "WorkspacesDirectorySelfServicePermissionsOutputReference",
    "WorkspacesDirectoryWorkspaceAccessProperties",
    "WorkspacesDirectoryWorkspaceAccessPropertiesOutputReference",
    "WorkspacesDirectoryWorkspaceCreationProperties",
    "WorkspacesDirectoryWorkspaceCreationPropertiesOutputReference",
]

publication.publish()

def _typecheckingstub__5507e0f583d973a9163ed42587b6dcfdf1beb99d9e7e174e38e5dadc4f90e865(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    active_directory_config: typing.Optional[typing.Union[WorkspacesDirectoryActiveDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate_based_auth_properties: typing.Optional[typing.Union[WorkspacesDirectoryCertificateBasedAuthProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    directory_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    saml_properties: typing.Optional[typing.Union[WorkspacesDirectorySamlProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    self_service_permissions: typing.Optional[typing.Union[WorkspacesDirectorySelfServicePermissions, typing.Dict[builtins.str, typing.Any]]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tenancy: typing.Optional[builtins.str] = None,
    user_identity_type: typing.Optional[builtins.str] = None,
    workspace_access_properties: typing.Optional[typing.Union[WorkspacesDirectoryWorkspaceAccessProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    workspace_creation_properties: typing.Optional[typing.Union[WorkspacesDirectoryWorkspaceCreationProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    workspace_directory_description: typing.Optional[builtins.str] = None,
    workspace_directory_name: typing.Optional[builtins.str] = None,
    workspace_type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__2d4180668777c24cd1221854a99c4911a2809d247c05feb899e45d3328958fcb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb15ec31c43cd2d7014385f140b592d1bb42deb051d3063e83a5998db8ddcbba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f27e4c8f412daffa2c4efc8df9dea6974b517ade6acf14791a551411e6e4e10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1ac6e9dd1ef54e97c156292ddccdd103135ac48b172fa701d77378a6aec073(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd886010213bf70c63427c8e7bf5d6a3a21d5aad716a2fe6f6f2e38a45c5839c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be37a78518ed1ab0e81fa15241d0f8ec557fdf14d250d6eebc573abe3bc21ff2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701a96b57da218491536aab5add5c8ff0ccaf8268b5ecf1c7d191ea138bb9081(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce1985c562045fef951c0816c4d1b9c7d65dbdbb381339bb885a1da5bbeda50(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e370f8b545fc7f01f015f99b657ae144ba7df1ef94ec73582be4e8b81b4245(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679ec0cdfaefa1133bcd709373d48d7fe62b4d50c7209fa94849a5820e589311(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__309a81becb7965fca6d63093548c7bd3c60a5e531f9adc257ebeec707c2d68ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015134dfdb00f7b458389036eb530115c2cea7032a23968fba8e4273fe290a51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd5ba46b759539d463bb247acf58dbd7a71c25368983babe4f3882094d0cd61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b943d248b6838e52a06d6ac7fca464cf8def8e3a529dfc27c1e634fd9f4810e(
    *,
    domain_name: builtins.str,
    service_account_secret_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b138f0d0bfdef6070fad665702bb3e5a8eae5fd3b3a7c6fce1b8123207e35f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76618b22e03c334f5587eaf9f6455afbff72248e3370f2456e599bd1843d78f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f7fc1d93623d085e224e3ad2cc0a8f9a31534d3a003f172cc286bec3be5308(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac1cf7c636a2ea3cae78e1bb4d9a9903511c9cb580b6170d172ff1d8dadf5e3f(
    value: typing.Optional[WorkspacesDirectoryActiveDirectoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a3eda9cb8d656525b4ed0a9b65cacbe291a3857efbb5bcf8efc976cb271add(
    *,
    certificate_authority_arn: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48cb378b98a8246982b2eb4b5774a62b330579f3bd1dbe514bf26308c54690db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e768abfef43544b467122922869c6a38687cd0b7faf0677c143f41602a8613f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c885f82081b87a3813495e1143007f9dc0702f2d2bc557c270c1f07368b937(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6f9557c8451832de5388894d8777b3ca449aa8c22c740b323a239957c35591(
    value: typing.Optional[WorkspacesDirectoryCertificateBasedAuthProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32ea060c923d45dd03bf9fb04e34f34eabc4160c71cbb8d0f409e8b93e03012(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    active_directory_config: typing.Optional[typing.Union[WorkspacesDirectoryActiveDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate_based_auth_properties: typing.Optional[typing.Union[WorkspacesDirectoryCertificateBasedAuthProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    directory_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    saml_properties: typing.Optional[typing.Union[WorkspacesDirectorySamlProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    self_service_permissions: typing.Optional[typing.Union[WorkspacesDirectorySelfServicePermissions, typing.Dict[builtins.str, typing.Any]]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tenancy: typing.Optional[builtins.str] = None,
    user_identity_type: typing.Optional[builtins.str] = None,
    workspace_access_properties: typing.Optional[typing.Union[WorkspacesDirectoryWorkspaceAccessProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    workspace_creation_properties: typing.Optional[typing.Union[WorkspacesDirectoryWorkspaceCreationProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    workspace_directory_description: typing.Optional[builtins.str] = None,
    workspace_directory_name: typing.Optional[builtins.str] = None,
    workspace_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3c069f6cfd981ad2d429b511ad2a029d6723806a3fd9d7f7a7afb648524d9f(
    *,
    relay_state_parameter_name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    user_access_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd010e0d4d9572d572adf4875f8324a744502cca2652b7f2c0c348f2c6179f84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303bacc15aaf60da40dff35ce857495c95b817259ce26c74600cd85fe049b985(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa656667669ceb61e9c39efd20b0a25cd570bba9ca7e36f0ec298159840c1087(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e0fef0be4d644fbb71d6954214a1c3c97cd8d9fe660d8c6f847b2c5999572a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073fe0978fe826ac6add6c1609de5dc9accadfcc1d9b0d766fcb3cb3b613723c(
    value: typing.Optional[WorkspacesDirectorySamlProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e4305e5557d83b3319e88333388ef209f8a1894df54cb46874e1d92deb26acd(
    *,
    change_compute_type: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    increase_volume_size: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rebuild_workspace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restart_workspace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    switch_running_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2750f8c67fc48bc7226f1a60b9440221c65af13c74f6fcd1caa60a2a27b956(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fa051afd161dad3fed45ee1a52fcfedd9d7937574645d5ae61cf039bbe9609(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb700e89f9c04222660eb417ebc20b0868929580d618134ed9687ac09d33d48(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5516f2e46edae4a101bb6d41275db092f50a998231a53452fd7858207c43d866(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1006cf4e438f0c1c0c5cb3d5210f161c40a02279a1cecd93cefc131671bedd4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e4b3698cfdfcb8b8fce44f6715d36dc6fce1553e6a9e9f4fc54c650069f0975(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881967ff04faaf639f38f97c1bf83802d405d0347cd1c1ab0408a4d98a468bc3(
    value: typing.Optional[WorkspacesDirectorySelfServicePermissions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b29e2eb91bedf3812c61235b8af9ebddc48f347268b042c1320cac04f8301c9a(
    *,
    device_type_android: typing.Optional[builtins.str] = None,
    device_type_chromeos: typing.Optional[builtins.str] = None,
    device_type_ios: typing.Optional[builtins.str] = None,
    device_type_linux: typing.Optional[builtins.str] = None,
    device_type_osx: typing.Optional[builtins.str] = None,
    device_type_web: typing.Optional[builtins.str] = None,
    device_type_windows: typing.Optional[builtins.str] = None,
    device_type_zeroclient: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db5aa1b442be1d150924659608547f6fbbb6bfad5e9d33232043616a36cf89a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a005131979cd4cdbeb209344eecbef64223a6eb6d75726df38054426afe356a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45986b5ad6b18e66a2a69f6415501789ef40e6f5df7c32b96d3c1807d28dcde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83e40f60c8c437f0d0dd6662a8a8f4bc347fb35bd2beeb838b8e49064ebf736(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2c2dcc37420af45df46a9b6239ccc9573e8fdab6bb12757bddde1dca4fc890(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab9ba0397511a4e190f9a70895cdb5fbdd204e23c358aeda02c43f9e24a8bc24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a491ebb5f93187fbb8afb65c461083263a5210702fdb7c38b8f6ed276f1dd642(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dae86940a3a83012fe1ac7afcda423aa3fbaf310c438c1cbb6700976c8cca01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098a85d70d785af72522d94ce64961cf1da9c47e5c9aea4dd5aafecb43ab3827(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e477943e9e314790fa841ebc3da770695dd86701ef1af07ff0ce6594ad046ed(
    value: typing.Optional[WorkspacesDirectoryWorkspaceAccessProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bbcb01c66b17901813c3f741153d7b9d8905022fac0ef53fe1e3a31928268f(
    *,
    custom_security_group_id: typing.Optional[builtins.str] = None,
    default_ou: typing.Optional[builtins.str] = None,
    enable_internet_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_maintenance_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user_enabled_as_local_administrator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eab1dd9c75e4bd2f51b34401cba3bcc30492a56848de14676c9255bee1cf1f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2512bf1c04b8c27606f1125c9387bb3150d2bb8569ee586ffe54d54cf1334dbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c155046ecc0e75a43cec257f3b1afbe4e226e097c04ee41c88b2ba8758204c57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3393d7f1b52919e4c5706d0bf465fc099998202673e57cd4b5371d7492141f7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1877131438810a9bc401b2c3a6d216708f392716153ab0f2523c627d1b18a63a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f0d01e4222f300482f169a2c439d095a28ae09538021094486333c09fa3ed48(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc6a9aff5cf54711d32c0c11f9e7dd529699bd6bac9da58c8187407807dcd53(
    value: typing.Optional[WorkspacesDirectoryWorkspaceCreationProperties],
) -> None:
    """Type checking stubs"""
    pass
