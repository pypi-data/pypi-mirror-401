r'''
# `aws_codebuild_project`

Refer to the Terraform Registry for docs: [`aws_codebuild_project`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project).
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


class CodebuildProject(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProject",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project aws_codebuild_project}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        artifacts: typing.Union["CodebuildProjectArtifacts", typing.Dict[builtins.str, typing.Any]],
        environment: typing.Union["CodebuildProjectEnvironment", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        service_role: builtins.str,
        source: typing.Union["CodebuildProjectSource", typing.Dict[builtins.str, typing.Any]],
        auto_retry_limit: typing.Optional[jsii.Number] = None,
        badge_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        build_batch_config: typing.Optional[typing.Union["CodebuildProjectBuildBatchConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        build_timeout: typing.Optional[jsii.Number] = None,
        cache: typing.Optional[typing.Union["CodebuildProjectCache", typing.Dict[builtins.str, typing.Any]]] = None,
        concurrent_build_limit: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        file_system_locations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodebuildProjectFileSystemLocations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        logs_config: typing.Optional[typing.Union["CodebuildProjectLogsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project_visibility: typing.Optional[builtins.str] = None,
        queued_timeout: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        resource_access_role: typing.Optional[builtins.str] = None,
        secondary_artifacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodebuildProjectSecondaryArtifacts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        secondary_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodebuildProjectSecondarySources", typing.Dict[builtins.str, typing.Any]]]]] = None,
        secondary_source_version: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodebuildProjectSecondarySourceVersion", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc_config: typing.Optional[typing.Union["CodebuildProjectVpcConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project aws_codebuild_project} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param artifacts: artifacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#artifacts CodebuildProject#artifacts}
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#environment CodebuildProject#environment}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#name CodebuildProject#name}.
        :param service_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#service_role CodebuildProject#service_role}.
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#source CodebuildProject#source}
        :param auto_retry_limit: Maximum number of additional automatic retries after a failed build. The default value is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#auto_retry_limit CodebuildProject#auto_retry_limit}
        :param badge_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#badge_enabled CodebuildProject#badge_enabled}.
        :param build_batch_config: build_batch_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#build_batch_config CodebuildProject#build_batch_config}
        :param build_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#build_timeout CodebuildProject#build_timeout}.
        :param cache: cache block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#cache CodebuildProject#cache}
        :param concurrent_build_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#concurrent_build_limit CodebuildProject#concurrent_build_limit}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#description CodebuildProject#description}.
        :param encryption_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#encryption_key CodebuildProject#encryption_key}.
        :param file_system_locations: file_system_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#file_system_locations CodebuildProject#file_system_locations}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#id CodebuildProject#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logs_config: logs_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#logs_config CodebuildProject#logs_config}
        :param project_visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#project_visibility CodebuildProject#project_visibility}.
        :param queued_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#queued_timeout CodebuildProject#queued_timeout}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#region CodebuildProject#region}
        :param resource_access_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#resource_access_role CodebuildProject#resource_access_role}.
        :param secondary_artifacts: secondary_artifacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#secondary_artifacts CodebuildProject#secondary_artifacts}
        :param secondary_sources: secondary_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#secondary_sources CodebuildProject#secondary_sources}
        :param secondary_source_version: secondary_source_version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#secondary_source_version CodebuildProject#secondary_source_version}
        :param source_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#source_version CodebuildProject#source_version}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#tags CodebuildProject#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#tags_all CodebuildProject#tags_all}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#vpc_config CodebuildProject#vpc_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e635c728797e9d93bc57ba8c75d88f714e52b834b14417ad24b50d08d732d6e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CodebuildProjectConfig(
            artifacts=artifacts,
            environment=environment,
            name=name,
            service_role=service_role,
            source=source,
            auto_retry_limit=auto_retry_limit,
            badge_enabled=badge_enabled,
            build_batch_config=build_batch_config,
            build_timeout=build_timeout,
            cache=cache,
            concurrent_build_limit=concurrent_build_limit,
            description=description,
            encryption_key=encryption_key,
            file_system_locations=file_system_locations,
            id=id,
            logs_config=logs_config,
            project_visibility=project_visibility,
            queued_timeout=queued_timeout,
            region=region,
            resource_access_role=resource_access_role,
            secondary_artifacts=secondary_artifacts,
            secondary_sources=secondary_sources,
            secondary_source_version=secondary_source_version,
            source_version=source_version,
            tags=tags,
            tags_all=tags_all,
            vpc_config=vpc_config,
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
        '''Generates CDKTF code for importing a CodebuildProject resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CodebuildProject to import.
        :param import_from_id: The id of the existing CodebuildProject that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CodebuildProject to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c2a79cf03f863fa328ebf13d0d166e00c554ae19c88c31d4577d7f9b86a4cd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putArtifacts")
    def put_artifacts(
        self,
        *,
        type: builtins.str,
        artifact_identifier: typing.Optional[builtins.str] = None,
        bucket_owner_access: typing.Optional[builtins.str] = None,
        encryption_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        namespace_type: typing.Optional[builtins.str] = None,
        override_artifact_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        packaging: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.
        :param artifact_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#artifact_identifier CodebuildProject#artifact_identifier}.
        :param bucket_owner_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#bucket_owner_access CodebuildProject#bucket_owner_access}.
        :param encryption_disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#encryption_disabled CodebuildProject#encryption_disabled}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#location CodebuildProject#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#name CodebuildProject#name}.
        :param namespace_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#namespace_type CodebuildProject#namespace_type}.
        :param override_artifact_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#override_artifact_name CodebuildProject#override_artifact_name}.
        :param packaging: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#packaging CodebuildProject#packaging}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#path CodebuildProject#path}.
        '''
        value = CodebuildProjectArtifacts(
            type=type,
            artifact_identifier=artifact_identifier,
            bucket_owner_access=bucket_owner_access,
            encryption_disabled=encryption_disabled,
            location=location,
            name=name,
            namespace_type=namespace_type,
            override_artifact_name=override_artifact_name,
            packaging=packaging,
            path=path,
        )

        return typing.cast(None, jsii.invoke(self, "putArtifacts", [value]))

    @jsii.member(jsii_name="putBuildBatchConfig")
    def put_build_batch_config(
        self,
        *,
        service_role: builtins.str,
        combine_artifacts: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restrictions: typing.Optional[typing.Union["CodebuildProjectBuildBatchConfigRestrictions", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_in_mins: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param service_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#service_role CodebuildProject#service_role}.
        :param combine_artifacts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#combine_artifacts CodebuildProject#combine_artifacts}.
        :param restrictions: restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#restrictions CodebuildProject#restrictions}
        :param timeout_in_mins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#timeout_in_mins CodebuildProject#timeout_in_mins}.
        '''
        value = CodebuildProjectBuildBatchConfig(
            service_role=service_role,
            combine_artifacts=combine_artifacts,
            restrictions=restrictions,
            timeout_in_mins=timeout_in_mins,
        )

        return typing.cast(None, jsii.invoke(self, "putBuildBatchConfig", [value]))

    @jsii.member(jsii_name="putCache")
    def put_cache(
        self,
        *,
        cache_namespace: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        modes: typing.Optional[typing.Sequence[builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cache_namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#cache_namespace CodebuildProject#cache_namespace}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#location CodebuildProject#location}.
        :param modes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#modes CodebuildProject#modes}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.
        '''
        value = CodebuildProjectCache(
            cache_namespace=cache_namespace, location=location, modes=modes, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putCache", [value]))

    @jsii.member(jsii_name="putEnvironment")
    def put_environment(
        self,
        *,
        compute_type: builtins.str,
        image: builtins.str,
        type: builtins.str,
        certificate: typing.Optional[builtins.str] = None,
        docker_server: typing.Optional[typing.Union["CodebuildProjectEnvironmentDockerServer", typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodebuildProjectEnvironmentEnvironmentVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        fleet: typing.Optional[typing.Union["CodebuildProjectEnvironmentFleet", typing.Dict[builtins.str, typing.Any]]] = None,
        image_pull_credentials_type: typing.Optional[builtins.str] = None,
        privileged_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        registry_credential: typing.Optional[typing.Union["CodebuildProjectEnvironmentRegistryCredential", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param compute_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#compute_type CodebuildProject#compute_type}.
        :param image: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#image CodebuildProject#image}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.
        :param certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#certificate CodebuildProject#certificate}.
        :param docker_server: docker_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#docker_server CodebuildProject#docker_server}
        :param environment_variable: environment_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#environment_variable CodebuildProject#environment_variable}
        :param fleet: fleet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#fleet CodebuildProject#fleet}
        :param image_pull_credentials_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#image_pull_credentials_type CodebuildProject#image_pull_credentials_type}.
        :param privileged_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#privileged_mode CodebuildProject#privileged_mode}.
        :param registry_credential: registry_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#registry_credential CodebuildProject#registry_credential}
        '''
        value = CodebuildProjectEnvironment(
            compute_type=compute_type,
            image=image,
            type=type,
            certificate=certificate,
            docker_server=docker_server,
            environment_variable=environment_variable,
            fleet=fleet,
            image_pull_credentials_type=image_pull_credentials_type,
            privileged_mode=privileged_mode,
            registry_credential=registry_credential,
        )

        return typing.cast(None, jsii.invoke(self, "putEnvironment", [value]))

    @jsii.member(jsii_name="putFileSystemLocations")
    def put_file_system_locations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodebuildProjectFileSystemLocations", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efea8faea33f7db5f59ffd4f7bb5370a4ad5ded6b99e0a2ffdd6ced06d4f3486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFileSystemLocations", [value]))

    @jsii.member(jsii_name="putLogsConfig")
    def put_logs_config(
        self,
        *,
        cloudwatch_logs: typing.Optional[typing.Union["CodebuildProjectLogsConfigCloudwatchLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_logs: typing.Optional[typing.Union["CodebuildProjectLogsConfigS3Logs", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_logs: cloudwatch_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#cloudwatch_logs CodebuildProject#cloudwatch_logs}
        :param s3_logs: s3_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#s3_logs CodebuildProject#s3_logs}
        '''
        value = CodebuildProjectLogsConfig(
            cloudwatch_logs=cloudwatch_logs, s3_logs=s3_logs
        )

        return typing.cast(None, jsii.invoke(self, "putLogsConfig", [value]))

    @jsii.member(jsii_name="putSecondaryArtifacts")
    def put_secondary_artifacts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodebuildProjectSecondaryArtifacts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9311bd2758106d5da7378bc8cf4e7fb6f67d3f2cc7b36dbfff2c2eb64044e760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecondaryArtifacts", [value]))

    @jsii.member(jsii_name="putSecondarySources")
    def put_secondary_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodebuildProjectSecondarySources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f4378878fc54ae99bef184f22186dab27c4b7a7efde78ccfc896228a2a0fac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecondarySources", [value]))

    @jsii.member(jsii_name="putSecondarySourceVersion")
    def put_secondary_source_version(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodebuildProjectSecondarySourceVersion", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5b454117aedb5b3bd73404d8f759a629c5a38b9c47f3b610591f975dfe02b13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecondarySourceVersion", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        type: builtins.str,
        auth: typing.Optional[typing.Union["CodebuildProjectSourceAuth", typing.Dict[builtins.str, typing.Any]]] = None,
        buildspec: typing.Optional[builtins.str] = None,
        build_status_config: typing.Optional[typing.Union["CodebuildProjectSourceBuildStatusConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        git_clone_depth: typing.Optional[jsii.Number] = None,
        git_submodules_config: typing.Optional[typing.Union["CodebuildProjectSourceGitSubmodulesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        insecure_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        location: typing.Optional[builtins.str] = None,
        report_build_status: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.
        :param auth: auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#auth CodebuildProject#auth}
        :param buildspec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#buildspec CodebuildProject#buildspec}.
        :param build_status_config: build_status_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#build_status_config CodebuildProject#build_status_config}
        :param git_clone_depth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#git_clone_depth CodebuildProject#git_clone_depth}.
        :param git_submodules_config: git_submodules_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#git_submodules_config CodebuildProject#git_submodules_config}
        :param insecure_ssl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#insecure_ssl CodebuildProject#insecure_ssl}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#location CodebuildProject#location}.
        :param report_build_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#report_build_status CodebuildProject#report_build_status}.
        '''
        value = CodebuildProjectSource(
            type=type,
            auth=auth,
            buildspec=buildspec,
            build_status_config=build_status_config,
            git_clone_depth=git_clone_depth,
            git_submodules_config=git_submodules_config,
            insecure_ssl=insecure_ssl,
            location=location,
            report_build_status=report_build_status,
        )

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="putVpcConfig")
    def put_vpc_config(
        self,
        *,
        security_group_ids: typing.Sequence[builtins.str],
        subnets: typing.Sequence[builtins.str],
        vpc_id: builtins.str,
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#security_group_ids CodebuildProject#security_group_ids}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#subnets CodebuildProject#subnets}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#vpc_id CodebuildProject#vpc_id}.
        '''
        value = CodebuildProjectVpcConfig(
            security_group_ids=security_group_ids, subnets=subnets, vpc_id=vpc_id
        )

        return typing.cast(None, jsii.invoke(self, "putVpcConfig", [value]))

    @jsii.member(jsii_name="resetAutoRetryLimit")
    def reset_auto_retry_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoRetryLimit", []))

    @jsii.member(jsii_name="resetBadgeEnabled")
    def reset_badge_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBadgeEnabled", []))

    @jsii.member(jsii_name="resetBuildBatchConfig")
    def reset_build_batch_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildBatchConfig", []))

    @jsii.member(jsii_name="resetBuildTimeout")
    def reset_build_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildTimeout", []))

    @jsii.member(jsii_name="resetCache")
    def reset_cache(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCache", []))

    @jsii.member(jsii_name="resetConcurrentBuildLimit")
    def reset_concurrent_build_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConcurrentBuildLimit", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEncryptionKey")
    def reset_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKey", []))

    @jsii.member(jsii_name="resetFileSystemLocations")
    def reset_file_system_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileSystemLocations", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogsConfig")
    def reset_logs_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogsConfig", []))

    @jsii.member(jsii_name="resetProjectVisibility")
    def reset_project_visibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectVisibility", []))

    @jsii.member(jsii_name="resetQueuedTimeout")
    def reset_queued_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueuedTimeout", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetResourceAccessRole")
    def reset_resource_access_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceAccessRole", []))

    @jsii.member(jsii_name="resetSecondaryArtifacts")
    def reset_secondary_artifacts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryArtifacts", []))

    @jsii.member(jsii_name="resetSecondarySources")
    def reset_secondary_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondarySources", []))

    @jsii.member(jsii_name="resetSecondarySourceVersion")
    def reset_secondary_source_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondarySourceVersion", []))

    @jsii.member(jsii_name="resetSourceVersion")
    def reset_source_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceVersion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetVpcConfig")
    def reset_vpc_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcConfig", []))

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
    @jsii.member(jsii_name="artifacts")
    def artifacts(self) -> "CodebuildProjectArtifactsOutputReference":
        return typing.cast("CodebuildProjectArtifactsOutputReference", jsii.get(self, "artifacts"))

    @builtins.property
    @jsii.member(jsii_name="badgeUrl")
    def badge_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "badgeUrl"))

    @builtins.property
    @jsii.member(jsii_name="buildBatchConfig")
    def build_batch_config(self) -> "CodebuildProjectBuildBatchConfigOutputReference":
        return typing.cast("CodebuildProjectBuildBatchConfigOutputReference", jsii.get(self, "buildBatchConfig"))

    @builtins.property
    @jsii.member(jsii_name="cache")
    def cache(self) -> "CodebuildProjectCacheOutputReference":
        return typing.cast("CodebuildProjectCacheOutputReference", jsii.get(self, "cache"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> "CodebuildProjectEnvironmentOutputReference":
        return typing.cast("CodebuildProjectEnvironmentOutputReference", jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="fileSystemLocations")
    def file_system_locations(self) -> "CodebuildProjectFileSystemLocationsList":
        return typing.cast("CodebuildProjectFileSystemLocationsList", jsii.get(self, "fileSystemLocations"))

    @builtins.property
    @jsii.member(jsii_name="logsConfig")
    def logs_config(self) -> "CodebuildProjectLogsConfigOutputReference":
        return typing.cast("CodebuildProjectLogsConfigOutputReference", jsii.get(self, "logsConfig"))

    @builtins.property
    @jsii.member(jsii_name="publicProjectAlias")
    def public_project_alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicProjectAlias"))

    @builtins.property
    @jsii.member(jsii_name="secondaryArtifacts")
    def secondary_artifacts(self) -> "CodebuildProjectSecondaryArtifactsList":
        return typing.cast("CodebuildProjectSecondaryArtifactsList", jsii.get(self, "secondaryArtifacts"))

    @builtins.property
    @jsii.member(jsii_name="secondarySources")
    def secondary_sources(self) -> "CodebuildProjectSecondarySourcesList":
        return typing.cast("CodebuildProjectSecondarySourcesList", jsii.get(self, "secondarySources"))

    @builtins.property
    @jsii.member(jsii_name="secondarySourceVersion")
    def secondary_source_version(self) -> "CodebuildProjectSecondarySourceVersionList":
        return typing.cast("CodebuildProjectSecondarySourceVersionList", jsii.get(self, "secondarySourceVersion"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "CodebuildProjectSourceOutputReference":
        return typing.cast("CodebuildProjectSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(self) -> "CodebuildProjectVpcConfigOutputReference":
        return typing.cast("CodebuildProjectVpcConfigOutputReference", jsii.get(self, "vpcConfig"))

    @builtins.property
    @jsii.member(jsii_name="artifactsInput")
    def artifacts_input(self) -> typing.Optional["CodebuildProjectArtifacts"]:
        return typing.cast(typing.Optional["CodebuildProjectArtifacts"], jsii.get(self, "artifactsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoRetryLimitInput")
    def auto_retry_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "autoRetryLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="badgeEnabledInput")
    def badge_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "badgeEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="buildBatchConfigInput")
    def build_batch_config_input(
        self,
    ) -> typing.Optional["CodebuildProjectBuildBatchConfig"]:
        return typing.cast(typing.Optional["CodebuildProjectBuildBatchConfig"], jsii.get(self, "buildBatchConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="buildTimeoutInput")
    def build_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "buildTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheInput")
    def cache_input(self) -> typing.Optional["CodebuildProjectCache"]:
        return typing.cast(typing.Optional["CodebuildProjectCache"], jsii.get(self, "cacheInput"))

    @builtins.property
    @jsii.member(jsii_name="concurrentBuildLimitInput")
    def concurrent_build_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "concurrentBuildLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyInput")
    def encryption_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(self) -> typing.Optional["CodebuildProjectEnvironment"]:
        return typing.cast(typing.Optional["CodebuildProjectEnvironment"], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="fileSystemLocationsInput")
    def file_system_locations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodebuildProjectFileSystemLocations"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodebuildProjectFileSystemLocations"]]], jsii.get(self, "fileSystemLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logsConfigInput")
    def logs_config_input(self) -> typing.Optional["CodebuildProjectLogsConfig"]:
        return typing.cast(typing.Optional["CodebuildProjectLogsConfig"], jsii.get(self, "logsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectVisibilityInput")
    def project_visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectVisibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="queuedTimeoutInput")
    def queued_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queuedTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceAccessRoleInput")
    def resource_access_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceAccessRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryArtifactsInput")
    def secondary_artifacts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodebuildProjectSecondaryArtifacts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodebuildProjectSecondaryArtifacts"]]], jsii.get(self, "secondaryArtifactsInput"))

    @builtins.property
    @jsii.member(jsii_name="secondarySourcesInput")
    def secondary_sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodebuildProjectSecondarySources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodebuildProjectSecondarySources"]]], jsii.get(self, "secondarySourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="secondarySourceVersionInput")
    def secondary_source_version_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodebuildProjectSecondarySourceVersion"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodebuildProjectSecondarySourceVersion"]]], jsii.get(self, "secondarySourceVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceRoleInput")
    def service_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional["CodebuildProjectSource"]:
        return typing.cast(typing.Optional["CodebuildProjectSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceVersionInput")
    def source_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceVersionInput"))

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
    @jsii.member(jsii_name="vpcConfigInput")
    def vpc_config_input(self) -> typing.Optional["CodebuildProjectVpcConfig"]:
        return typing.cast(typing.Optional["CodebuildProjectVpcConfig"], jsii.get(self, "vpcConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="autoRetryLimit")
    def auto_retry_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoRetryLimit"))

    @auto_retry_limit.setter
    def auto_retry_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b63dbea74c44b413d8b7a9486b6a7615a7c3f06f2d4ca87f5567e8deeaf231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoRetryLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="badgeEnabled")
    def badge_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "badgeEnabled"))

    @badge_enabled.setter
    def badge_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbd9f66ca0f09eda9758cf23e157c56ceef0499ae86b2b0e1e7eea4a062b6ff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "badgeEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="buildTimeout")
    def build_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "buildTimeout"))

    @build_timeout.setter
    def build_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__585aee88331322cd11b9a6e35bf3f6df7963f2ff679c9ac1084ad1312c3438d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="concurrentBuildLimit")
    def concurrent_build_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "concurrentBuildLimit"))

    @concurrent_build_limit.setter
    def concurrent_build_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7143b8f47ab5b76d468fa003920a85b68c8422818db506f07f5b244c35c85b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "concurrentBuildLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc378072c8f825cb20310465f6e860f3ef1de3b3a5dc20ea9d42b065300d82a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKey"))

    @encryption_key.setter
    def encryption_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc067b4383ae988440974a7254f86ed2c2fe1e1b0ab2ce9a92e373d76b6c8ea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aca9e625e2a19b50c2858daf982ecb67566808a1082984511e62d1e8e31d4cfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0744de8cb6fc0b0fc38070d5e21e681054f163202c033ad6c2af90b9cbf08e76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectVisibility")
    def project_visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectVisibility"))

    @project_visibility.setter
    def project_visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e941585937ba258d1dbff3d8827a5ea1558b9b920d0f8759874d9b3b4d2dd8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectVisibility", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queuedTimeout")
    def queued_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queuedTimeout"))

    @queued_timeout.setter
    def queued_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce2866ec4818709e5fcd3d6c1c896006cfb4f5a25e27a714fe18fea8f2724aed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queuedTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b7519e969b5e007f30572528c6e83359b93711b58a8ebf4e95bdd0761cbeba4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceAccessRole")
    def resource_access_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceAccessRole"))

    @resource_access_role.setter
    def resource_access_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e04e3e3f195b1148c33246b826643c387f10fa1307125383e61021c3bface7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceAccessRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceRole")
    def service_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceRole"))

    @service_role.setter
    def service_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de086bd003e44f3a73d6c76b0172aa06c9852f95be9a448c8a68fdc70952f73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceVersion")
    def source_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceVersion"))

    @source_version.setter
    def source_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda1ce33304aba369dba9ef92363a0ef7ac7d73dafe4df98f9e4a02bd68cc033)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa43788d8b1be61344948501cadf986eda1f94373e35b196256c68073077a06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ffee8f06d6d785208d9a463a9fbf05fdfffdbd1109d20d9a0195bba983f23c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectArtifacts",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "artifact_identifier": "artifactIdentifier",
        "bucket_owner_access": "bucketOwnerAccess",
        "encryption_disabled": "encryptionDisabled",
        "location": "location",
        "name": "name",
        "namespace_type": "namespaceType",
        "override_artifact_name": "overrideArtifactName",
        "packaging": "packaging",
        "path": "path",
    },
)
class CodebuildProjectArtifacts:
    def __init__(
        self,
        *,
        type: builtins.str,
        artifact_identifier: typing.Optional[builtins.str] = None,
        bucket_owner_access: typing.Optional[builtins.str] = None,
        encryption_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        namespace_type: typing.Optional[builtins.str] = None,
        override_artifact_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        packaging: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.
        :param artifact_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#artifact_identifier CodebuildProject#artifact_identifier}.
        :param bucket_owner_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#bucket_owner_access CodebuildProject#bucket_owner_access}.
        :param encryption_disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#encryption_disabled CodebuildProject#encryption_disabled}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#location CodebuildProject#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#name CodebuildProject#name}.
        :param namespace_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#namespace_type CodebuildProject#namespace_type}.
        :param override_artifact_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#override_artifact_name CodebuildProject#override_artifact_name}.
        :param packaging: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#packaging CodebuildProject#packaging}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#path CodebuildProject#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__367c68db7701463b58dbd741bf2047d160603865f81ed6437e94655a53b9ef0a)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument artifact_identifier", value=artifact_identifier, expected_type=type_hints["artifact_identifier"])
            check_type(argname="argument bucket_owner_access", value=bucket_owner_access, expected_type=type_hints["bucket_owner_access"])
            check_type(argname="argument encryption_disabled", value=encryption_disabled, expected_type=type_hints["encryption_disabled"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace_type", value=namespace_type, expected_type=type_hints["namespace_type"])
            check_type(argname="argument override_artifact_name", value=override_artifact_name, expected_type=type_hints["override_artifact_name"])
            check_type(argname="argument packaging", value=packaging, expected_type=type_hints["packaging"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if artifact_identifier is not None:
            self._values["artifact_identifier"] = artifact_identifier
        if bucket_owner_access is not None:
            self._values["bucket_owner_access"] = bucket_owner_access
        if encryption_disabled is not None:
            self._values["encryption_disabled"] = encryption_disabled
        if location is not None:
            self._values["location"] = location
        if name is not None:
            self._values["name"] = name
        if namespace_type is not None:
            self._values["namespace_type"] = namespace_type
        if override_artifact_name is not None:
            self._values["override_artifact_name"] = override_artifact_name
        if packaging is not None:
            self._values["packaging"] = packaging
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def artifact_identifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#artifact_identifier CodebuildProject#artifact_identifier}.'''
        result = self._values.get("artifact_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_owner_access(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#bucket_owner_access CodebuildProject#bucket_owner_access}.'''
        result = self._values.get("bucket_owner_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#encryption_disabled CodebuildProject#encryption_disabled}.'''
        result = self._values.get("encryption_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#location CodebuildProject#location}.'''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#name CodebuildProject#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#namespace_type CodebuildProject#namespace_type}.'''
        result = self._values.get("namespace_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def override_artifact_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#override_artifact_name CodebuildProject#override_artifact_name}.'''
        result = self._values.get("override_artifact_name")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def packaging(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#packaging CodebuildProject#packaging}.'''
        result = self._values.get("packaging")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#path CodebuildProject#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectArtifacts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectArtifactsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectArtifactsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e58ff103ac66e5d4e845cc4fbed4d7bc6da504f0bdd8672c1b3f4b98beffe60e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArtifactIdentifier")
    def reset_artifact_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArtifactIdentifier", []))

    @jsii.member(jsii_name="resetBucketOwnerAccess")
    def reset_bucket_owner_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketOwnerAccess", []))

    @jsii.member(jsii_name="resetEncryptionDisabled")
    def reset_encryption_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionDisabled", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamespaceType")
    def reset_namespace_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespaceType", []))

    @jsii.member(jsii_name="resetOverrideArtifactName")
    def reset_override_artifact_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrideArtifactName", []))

    @jsii.member(jsii_name="resetPackaging")
    def reset_packaging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPackaging", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="artifactIdentifierInput")
    def artifact_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketOwnerAccessInput")
    def bucket_owner_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketOwnerAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionDisabledInput")
    def encryption_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptionDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceTypeInput")
    def namespace_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideArtifactNameInput")
    def override_artifact_name_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overrideArtifactNameInput"))

    @builtins.property
    @jsii.member(jsii_name="packagingInput")
    def packaging_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "packagingInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactIdentifier")
    def artifact_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "artifactIdentifier"))

    @artifact_identifier.setter
    def artifact_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be5cd18789e47935551a874c9b64588007c27c6bbc55e46dc25a8c8398227648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketOwnerAccess")
    def bucket_owner_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketOwnerAccess"))

    @bucket_owner_access.setter
    def bucket_owner_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff539a2ea34398296fd6e5bec1354910a03b3395d5d2a5b8273dc692610feb94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketOwnerAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionDisabled")
    def encryption_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encryptionDisabled"))

    @encryption_disabled.setter
    def encryption_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29d8f1ac1b7f0a51a37d1c4f0bfcd5a916e0bfe954f52de67d83c82e968707f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adefcb518c22b6588473798d5e370fdaaf929c73661134bdf84a551c4447db1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d02240a1a15f6a87affdb351123db7de077ae058642dbb17cf89cd773a6baf80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespaceType")
    def namespace_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespaceType"))

    @namespace_type.setter
    def namespace_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f055a113a306a4c14ab31be8d16a596b10e9961f01b1721a6b1b204958ba8c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overrideArtifactName")
    def override_artifact_name(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "overrideArtifactName"))

    @override_artifact_name.setter
    def override_artifact_name(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__658d34651b65c75435178e3b24dbef8301f2d7a22ba24d2a5ffd305804b1247c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overrideArtifactName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="packaging")
    def packaging(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "packaging"))

    @packaging.setter
    def packaging(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a346d17abab5af2d3bb347d63f1b07057648639c310927d2502d0e92f4c300ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packaging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40287970ea6f38a2c1722f7d0962c3f7bd15345a8e7e5208f5e602e360083f6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e35dc077252154f384978e1fa79ffae5a4f2689df20e72dfa54ff1e26412032d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CodebuildProjectArtifacts]:
        return typing.cast(typing.Optional[CodebuildProjectArtifacts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CodebuildProjectArtifacts]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e8e548f6ee8ab577e0e5eb0a48b33ca7927c1a7c4ae526c49a50f22d5b473ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectBuildBatchConfig",
    jsii_struct_bases=[],
    name_mapping={
        "service_role": "serviceRole",
        "combine_artifacts": "combineArtifacts",
        "restrictions": "restrictions",
        "timeout_in_mins": "timeoutInMins",
    },
)
class CodebuildProjectBuildBatchConfig:
    def __init__(
        self,
        *,
        service_role: builtins.str,
        combine_artifacts: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restrictions: typing.Optional[typing.Union["CodebuildProjectBuildBatchConfigRestrictions", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_in_mins: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param service_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#service_role CodebuildProject#service_role}.
        :param combine_artifacts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#combine_artifacts CodebuildProject#combine_artifacts}.
        :param restrictions: restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#restrictions CodebuildProject#restrictions}
        :param timeout_in_mins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#timeout_in_mins CodebuildProject#timeout_in_mins}.
        '''
        if isinstance(restrictions, dict):
            restrictions = CodebuildProjectBuildBatchConfigRestrictions(**restrictions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c4cabd621704978ae24bba751edf0dbf039034619aa5f97fc6493625d806c9e)
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument combine_artifacts", value=combine_artifacts, expected_type=type_hints["combine_artifacts"])
            check_type(argname="argument restrictions", value=restrictions, expected_type=type_hints["restrictions"])
            check_type(argname="argument timeout_in_mins", value=timeout_in_mins, expected_type=type_hints["timeout_in_mins"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_role": service_role,
        }
        if combine_artifacts is not None:
            self._values["combine_artifacts"] = combine_artifacts
        if restrictions is not None:
            self._values["restrictions"] = restrictions
        if timeout_in_mins is not None:
            self._values["timeout_in_mins"] = timeout_in_mins

    @builtins.property
    def service_role(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#service_role CodebuildProject#service_role}.'''
        result = self._values.get("service_role")
        assert result is not None, "Required property 'service_role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def combine_artifacts(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#combine_artifacts CodebuildProject#combine_artifacts}.'''
        result = self._values.get("combine_artifacts")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def restrictions(
        self,
    ) -> typing.Optional["CodebuildProjectBuildBatchConfigRestrictions"]:
        '''restrictions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#restrictions CodebuildProject#restrictions}
        '''
        result = self._values.get("restrictions")
        return typing.cast(typing.Optional["CodebuildProjectBuildBatchConfigRestrictions"], result)

    @builtins.property
    def timeout_in_mins(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#timeout_in_mins CodebuildProject#timeout_in_mins}.'''
        result = self._values.get("timeout_in_mins")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectBuildBatchConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectBuildBatchConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectBuildBatchConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a73ac71b336da06fbbc87e683a43936cfc8aa206a2879af51a23f0de56cbfc28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRestrictions")
    def put_restrictions(
        self,
        *,
        compute_types_allowed: typing.Optional[typing.Sequence[builtins.str]] = None,
        maximum_builds_allowed: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param compute_types_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#compute_types_allowed CodebuildProject#compute_types_allowed}.
        :param maximum_builds_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#maximum_builds_allowed CodebuildProject#maximum_builds_allowed}.
        '''
        value = CodebuildProjectBuildBatchConfigRestrictions(
            compute_types_allowed=compute_types_allowed,
            maximum_builds_allowed=maximum_builds_allowed,
        )

        return typing.cast(None, jsii.invoke(self, "putRestrictions", [value]))

    @jsii.member(jsii_name="resetCombineArtifacts")
    def reset_combine_artifacts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCombineArtifacts", []))

    @jsii.member(jsii_name="resetRestrictions")
    def reset_restrictions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictions", []))

    @jsii.member(jsii_name="resetTimeoutInMins")
    def reset_timeout_in_mins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutInMins", []))

    @builtins.property
    @jsii.member(jsii_name="restrictions")
    def restrictions(
        self,
    ) -> "CodebuildProjectBuildBatchConfigRestrictionsOutputReference":
        return typing.cast("CodebuildProjectBuildBatchConfigRestrictionsOutputReference", jsii.get(self, "restrictions"))

    @builtins.property
    @jsii.member(jsii_name="combineArtifactsInput")
    def combine_artifacts_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "combineArtifactsInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictionsInput")
    def restrictions_input(
        self,
    ) -> typing.Optional["CodebuildProjectBuildBatchConfigRestrictions"]:
        return typing.cast(typing.Optional["CodebuildProjectBuildBatchConfigRestrictions"], jsii.get(self, "restrictionsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceRoleInput")
    def service_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInMinsInput")
    def timeout_in_mins_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInMinsInput"))

    @builtins.property
    @jsii.member(jsii_name="combineArtifacts")
    def combine_artifacts(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "combineArtifacts"))

    @combine_artifacts.setter
    def combine_artifacts(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bca3737457adb2221b1fb2767b0944ef94061ea8af27c4d5c8ebd976807a371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "combineArtifacts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceRole")
    def service_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceRole"))

    @service_role.setter
    def service_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1c2123bbe106808f790b5a9490256e5f3f1c843d26f3a061ddeab85698b803f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutInMins")
    def timeout_in_mins(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutInMins"))

    @timeout_in_mins.setter
    def timeout_in_mins(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a324c807f7fd5cc268cd74837042310e48e06b9fb604fb794525ad97aaf1735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutInMins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CodebuildProjectBuildBatchConfig]:
        return typing.cast(typing.Optional[CodebuildProjectBuildBatchConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodebuildProjectBuildBatchConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467288dc4e4f0bcac92c2b65d3d1ad921cbe331dbe7ff1e5dadacbb68ac5c2ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectBuildBatchConfigRestrictions",
    jsii_struct_bases=[],
    name_mapping={
        "compute_types_allowed": "computeTypesAllowed",
        "maximum_builds_allowed": "maximumBuildsAllowed",
    },
)
class CodebuildProjectBuildBatchConfigRestrictions:
    def __init__(
        self,
        *,
        compute_types_allowed: typing.Optional[typing.Sequence[builtins.str]] = None,
        maximum_builds_allowed: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param compute_types_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#compute_types_allowed CodebuildProject#compute_types_allowed}.
        :param maximum_builds_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#maximum_builds_allowed CodebuildProject#maximum_builds_allowed}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5803e660d212afaa9e9e7fe5ca1067bc9119b67c9779e25dfdb7404829da1b99)
            check_type(argname="argument compute_types_allowed", value=compute_types_allowed, expected_type=type_hints["compute_types_allowed"])
            check_type(argname="argument maximum_builds_allowed", value=maximum_builds_allowed, expected_type=type_hints["maximum_builds_allowed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_types_allowed is not None:
            self._values["compute_types_allowed"] = compute_types_allowed
        if maximum_builds_allowed is not None:
            self._values["maximum_builds_allowed"] = maximum_builds_allowed

    @builtins.property
    def compute_types_allowed(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#compute_types_allowed CodebuildProject#compute_types_allowed}.'''
        result = self._values.get("compute_types_allowed")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def maximum_builds_allowed(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#maximum_builds_allowed CodebuildProject#maximum_builds_allowed}.'''
        result = self._values.get("maximum_builds_allowed")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectBuildBatchConfigRestrictions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectBuildBatchConfigRestrictionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectBuildBatchConfigRestrictionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbdc7e4e3a4c2f2f60656800ee2520eeea2d4720991468f82695d3f7d1aa7096)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetComputeTypesAllowed")
    def reset_compute_types_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeTypesAllowed", []))

    @jsii.member(jsii_name="resetMaximumBuildsAllowed")
    def reset_maximum_builds_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBuildsAllowed", []))

    @builtins.property
    @jsii.member(jsii_name="computeTypesAllowedInput")
    def compute_types_allowed_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "computeTypesAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBuildsAllowedInput")
    def maximum_builds_allowed_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBuildsAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="computeTypesAllowed")
    def compute_types_allowed(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "computeTypesAllowed"))

    @compute_types_allowed.setter
    def compute_types_allowed(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca82e62f891da80e30f2bd094e77c5e34c82445b169f42dc5dd31011fc1c445b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeTypesAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBuildsAllowed")
    def maximum_builds_allowed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBuildsAllowed"))

    @maximum_builds_allowed.setter
    def maximum_builds_allowed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d2be1fcc13bfd79601b806ca6f5df703fcb4ee9ae960cc8fb972c09ee709de2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBuildsAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodebuildProjectBuildBatchConfigRestrictions]:
        return typing.cast(typing.Optional[CodebuildProjectBuildBatchConfigRestrictions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodebuildProjectBuildBatchConfigRestrictions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8c909e4b2a2bdc73f4ba3d48aa61b66e9112f56221903e677404074586e1141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectCache",
    jsii_struct_bases=[],
    name_mapping={
        "cache_namespace": "cacheNamespace",
        "location": "location",
        "modes": "modes",
        "type": "type",
    },
)
class CodebuildProjectCache:
    def __init__(
        self,
        *,
        cache_namespace: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        modes: typing.Optional[typing.Sequence[builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cache_namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#cache_namespace CodebuildProject#cache_namespace}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#location CodebuildProject#location}.
        :param modes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#modes CodebuildProject#modes}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2ed786da98726b28b45fd9644570ba5fbf776e60249d5518b4de8f3ff484710)
            check_type(argname="argument cache_namespace", value=cache_namespace, expected_type=type_hints["cache_namespace"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument modes", value=modes, expected_type=type_hints["modes"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cache_namespace is not None:
            self._values["cache_namespace"] = cache_namespace
        if location is not None:
            self._values["location"] = location
        if modes is not None:
            self._values["modes"] = modes
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def cache_namespace(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#cache_namespace CodebuildProject#cache_namespace}.'''
        result = self._values.get("cache_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#location CodebuildProject#location}.'''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def modes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#modes CodebuildProject#modes}.'''
        result = self._values.get("modes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectCache(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectCacheOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectCacheOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bcc2a24921ec4ac3d2e10c1024eb0a19cc05615eea2d9a615384f016ade05c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCacheNamespace")
    def reset_cache_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheNamespace", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetModes")
    def reset_modes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModes", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="cacheNamespaceInput")
    def cache_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="modesInput")
    def modes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "modesInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheNamespace")
    def cache_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheNamespace"))

    @cache_namespace.setter
    def cache_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44567c77923ac8311036b67f1f733e2522930908c86a1fcaa4b5a30758ccf4d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0947fb2d092f78c4ded9965a382295cb593ea2ccf1dc6c7a5e0c21e62d1e785)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modes")
    def modes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "modes"))

    @modes.setter
    def modes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24dd73c09a857f9dbe39b0aeb9bbf17e2f899cef2d5bf7026a9b73345332eba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca06f3fb9ab37a09ce3e3ec43e72f1f9be354af430778383e07872b62dac6553)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CodebuildProjectCache]:
        return typing.cast(typing.Optional[CodebuildProjectCache], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CodebuildProjectCache]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a12152939335ec46e3efbd783b8e015154f64f0617900cbcfdd364e9ac968464)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "artifacts": "artifacts",
        "environment": "environment",
        "name": "name",
        "service_role": "serviceRole",
        "source": "source",
        "auto_retry_limit": "autoRetryLimit",
        "badge_enabled": "badgeEnabled",
        "build_batch_config": "buildBatchConfig",
        "build_timeout": "buildTimeout",
        "cache": "cache",
        "concurrent_build_limit": "concurrentBuildLimit",
        "description": "description",
        "encryption_key": "encryptionKey",
        "file_system_locations": "fileSystemLocations",
        "id": "id",
        "logs_config": "logsConfig",
        "project_visibility": "projectVisibility",
        "queued_timeout": "queuedTimeout",
        "region": "region",
        "resource_access_role": "resourceAccessRole",
        "secondary_artifacts": "secondaryArtifacts",
        "secondary_sources": "secondarySources",
        "secondary_source_version": "secondarySourceVersion",
        "source_version": "sourceVersion",
        "tags": "tags",
        "tags_all": "tagsAll",
        "vpc_config": "vpcConfig",
    },
)
class CodebuildProjectConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        artifacts: typing.Union[CodebuildProjectArtifacts, typing.Dict[builtins.str, typing.Any]],
        environment: typing.Union["CodebuildProjectEnvironment", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        service_role: builtins.str,
        source: typing.Union["CodebuildProjectSource", typing.Dict[builtins.str, typing.Any]],
        auto_retry_limit: typing.Optional[jsii.Number] = None,
        badge_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        build_batch_config: typing.Optional[typing.Union[CodebuildProjectBuildBatchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        build_timeout: typing.Optional[jsii.Number] = None,
        cache: typing.Optional[typing.Union[CodebuildProjectCache, typing.Dict[builtins.str, typing.Any]]] = None,
        concurrent_build_limit: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        file_system_locations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodebuildProjectFileSystemLocations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        logs_config: typing.Optional[typing.Union["CodebuildProjectLogsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project_visibility: typing.Optional[builtins.str] = None,
        queued_timeout: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        resource_access_role: typing.Optional[builtins.str] = None,
        secondary_artifacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodebuildProjectSecondaryArtifacts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        secondary_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodebuildProjectSecondarySources", typing.Dict[builtins.str, typing.Any]]]]] = None,
        secondary_source_version: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodebuildProjectSecondarySourceVersion", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc_config: typing.Optional[typing.Union["CodebuildProjectVpcConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param artifacts: artifacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#artifacts CodebuildProject#artifacts}
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#environment CodebuildProject#environment}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#name CodebuildProject#name}.
        :param service_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#service_role CodebuildProject#service_role}.
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#source CodebuildProject#source}
        :param auto_retry_limit: Maximum number of additional automatic retries after a failed build. The default value is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#auto_retry_limit CodebuildProject#auto_retry_limit}
        :param badge_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#badge_enabled CodebuildProject#badge_enabled}.
        :param build_batch_config: build_batch_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#build_batch_config CodebuildProject#build_batch_config}
        :param build_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#build_timeout CodebuildProject#build_timeout}.
        :param cache: cache block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#cache CodebuildProject#cache}
        :param concurrent_build_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#concurrent_build_limit CodebuildProject#concurrent_build_limit}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#description CodebuildProject#description}.
        :param encryption_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#encryption_key CodebuildProject#encryption_key}.
        :param file_system_locations: file_system_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#file_system_locations CodebuildProject#file_system_locations}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#id CodebuildProject#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logs_config: logs_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#logs_config CodebuildProject#logs_config}
        :param project_visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#project_visibility CodebuildProject#project_visibility}.
        :param queued_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#queued_timeout CodebuildProject#queued_timeout}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#region CodebuildProject#region}
        :param resource_access_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#resource_access_role CodebuildProject#resource_access_role}.
        :param secondary_artifacts: secondary_artifacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#secondary_artifacts CodebuildProject#secondary_artifacts}
        :param secondary_sources: secondary_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#secondary_sources CodebuildProject#secondary_sources}
        :param secondary_source_version: secondary_source_version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#secondary_source_version CodebuildProject#secondary_source_version}
        :param source_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#source_version CodebuildProject#source_version}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#tags CodebuildProject#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#tags_all CodebuildProject#tags_all}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#vpc_config CodebuildProject#vpc_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(artifacts, dict):
            artifacts = CodebuildProjectArtifacts(**artifacts)
        if isinstance(environment, dict):
            environment = CodebuildProjectEnvironment(**environment)
        if isinstance(source, dict):
            source = CodebuildProjectSource(**source)
        if isinstance(build_batch_config, dict):
            build_batch_config = CodebuildProjectBuildBatchConfig(**build_batch_config)
        if isinstance(cache, dict):
            cache = CodebuildProjectCache(**cache)
        if isinstance(logs_config, dict):
            logs_config = CodebuildProjectLogsConfig(**logs_config)
        if isinstance(vpc_config, dict):
            vpc_config = CodebuildProjectVpcConfig(**vpc_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b7d66f42f49ba671e9db03c7f520fdd509c7ad961970b7f6d95ba05a09be328)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument auto_retry_limit", value=auto_retry_limit, expected_type=type_hints["auto_retry_limit"])
            check_type(argname="argument badge_enabled", value=badge_enabled, expected_type=type_hints["badge_enabled"])
            check_type(argname="argument build_batch_config", value=build_batch_config, expected_type=type_hints["build_batch_config"])
            check_type(argname="argument build_timeout", value=build_timeout, expected_type=type_hints["build_timeout"])
            check_type(argname="argument cache", value=cache, expected_type=type_hints["cache"])
            check_type(argname="argument concurrent_build_limit", value=concurrent_build_limit, expected_type=type_hints["concurrent_build_limit"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument file_system_locations", value=file_system_locations, expected_type=type_hints["file_system_locations"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logs_config", value=logs_config, expected_type=type_hints["logs_config"])
            check_type(argname="argument project_visibility", value=project_visibility, expected_type=type_hints["project_visibility"])
            check_type(argname="argument queued_timeout", value=queued_timeout, expected_type=type_hints["queued_timeout"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument resource_access_role", value=resource_access_role, expected_type=type_hints["resource_access_role"])
            check_type(argname="argument secondary_artifacts", value=secondary_artifacts, expected_type=type_hints["secondary_artifacts"])
            check_type(argname="argument secondary_sources", value=secondary_sources, expected_type=type_hints["secondary_sources"])
            check_type(argname="argument secondary_source_version", value=secondary_source_version, expected_type=type_hints["secondary_source_version"])
            check_type(argname="argument source_version", value=source_version, expected_type=type_hints["source_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifacts": artifacts,
            "environment": environment,
            "name": name,
            "service_role": service_role,
            "source": source,
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
        if auto_retry_limit is not None:
            self._values["auto_retry_limit"] = auto_retry_limit
        if badge_enabled is not None:
            self._values["badge_enabled"] = badge_enabled
        if build_batch_config is not None:
            self._values["build_batch_config"] = build_batch_config
        if build_timeout is not None:
            self._values["build_timeout"] = build_timeout
        if cache is not None:
            self._values["cache"] = cache
        if concurrent_build_limit is not None:
            self._values["concurrent_build_limit"] = concurrent_build_limit
        if description is not None:
            self._values["description"] = description
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if file_system_locations is not None:
            self._values["file_system_locations"] = file_system_locations
        if id is not None:
            self._values["id"] = id
        if logs_config is not None:
            self._values["logs_config"] = logs_config
        if project_visibility is not None:
            self._values["project_visibility"] = project_visibility
        if queued_timeout is not None:
            self._values["queued_timeout"] = queued_timeout
        if region is not None:
            self._values["region"] = region
        if resource_access_role is not None:
            self._values["resource_access_role"] = resource_access_role
        if secondary_artifacts is not None:
            self._values["secondary_artifacts"] = secondary_artifacts
        if secondary_sources is not None:
            self._values["secondary_sources"] = secondary_sources
        if secondary_source_version is not None:
            self._values["secondary_source_version"] = secondary_source_version
        if source_version is not None:
            self._values["source_version"] = source_version
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

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
    def artifacts(self) -> CodebuildProjectArtifacts:
        '''artifacts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#artifacts CodebuildProject#artifacts}
        '''
        result = self._values.get("artifacts")
        assert result is not None, "Required property 'artifacts' is missing"
        return typing.cast(CodebuildProjectArtifacts, result)

    @builtins.property
    def environment(self) -> "CodebuildProjectEnvironment":
        '''environment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#environment CodebuildProject#environment}
        '''
        result = self._values.get("environment")
        assert result is not None, "Required property 'environment' is missing"
        return typing.cast("CodebuildProjectEnvironment", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#name CodebuildProject#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_role(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#service_role CodebuildProject#service_role}.'''
        result = self._values.get("service_role")
        assert result is not None, "Required property 'service_role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> "CodebuildProjectSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#source CodebuildProject#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("CodebuildProjectSource", result)

    @builtins.property
    def auto_retry_limit(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of additional automatic retries after a failed build. The default value is 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#auto_retry_limit CodebuildProject#auto_retry_limit}
        '''
        result = self._values.get("auto_retry_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def badge_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#badge_enabled CodebuildProject#badge_enabled}.'''
        result = self._values.get("badge_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def build_batch_config(self) -> typing.Optional[CodebuildProjectBuildBatchConfig]:
        '''build_batch_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#build_batch_config CodebuildProject#build_batch_config}
        '''
        result = self._values.get("build_batch_config")
        return typing.cast(typing.Optional[CodebuildProjectBuildBatchConfig], result)

    @builtins.property
    def build_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#build_timeout CodebuildProject#build_timeout}.'''
        result = self._values.get("build_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cache(self) -> typing.Optional[CodebuildProjectCache]:
        '''cache block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#cache CodebuildProject#cache}
        '''
        result = self._values.get("cache")
        return typing.cast(typing.Optional[CodebuildProjectCache], result)

    @builtins.property
    def concurrent_build_limit(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#concurrent_build_limit CodebuildProject#concurrent_build_limit}.'''
        result = self._values.get("concurrent_build_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#description CodebuildProject#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#encryption_key CodebuildProject#encryption_key}.'''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_system_locations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodebuildProjectFileSystemLocations"]]]:
        '''file_system_locations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#file_system_locations CodebuildProject#file_system_locations}
        '''
        result = self._values.get("file_system_locations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodebuildProjectFileSystemLocations"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#id CodebuildProject#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logs_config(self) -> typing.Optional["CodebuildProjectLogsConfig"]:
        '''logs_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#logs_config CodebuildProject#logs_config}
        '''
        result = self._values.get("logs_config")
        return typing.cast(typing.Optional["CodebuildProjectLogsConfig"], result)

    @builtins.property
    def project_visibility(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#project_visibility CodebuildProject#project_visibility}.'''
        result = self._values.get("project_visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queued_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#queued_timeout CodebuildProject#queued_timeout}.'''
        result = self._values.get("queued_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#region CodebuildProject#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_access_role(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#resource_access_role CodebuildProject#resource_access_role}.'''
        result = self._values.get("resource_access_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_artifacts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodebuildProjectSecondaryArtifacts"]]]:
        '''secondary_artifacts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#secondary_artifacts CodebuildProject#secondary_artifacts}
        '''
        result = self._values.get("secondary_artifacts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodebuildProjectSecondaryArtifacts"]]], result)

    @builtins.property
    def secondary_sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodebuildProjectSecondarySources"]]]:
        '''secondary_sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#secondary_sources CodebuildProject#secondary_sources}
        '''
        result = self._values.get("secondary_sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodebuildProjectSecondarySources"]]], result)

    @builtins.property
    def secondary_source_version(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodebuildProjectSecondarySourceVersion"]]]:
        '''secondary_source_version block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#secondary_source_version CodebuildProject#secondary_source_version}
        '''
        result = self._values.get("secondary_source_version")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodebuildProjectSecondarySourceVersion"]]], result)

    @builtins.property
    def source_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#source_version CodebuildProject#source_version}.'''
        result = self._values.get("source_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#tags CodebuildProject#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#tags_all CodebuildProject#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vpc_config(self) -> typing.Optional["CodebuildProjectVpcConfig"]:
        '''vpc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#vpc_config CodebuildProject#vpc_config}
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional["CodebuildProjectVpcConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectEnvironment",
    jsii_struct_bases=[],
    name_mapping={
        "compute_type": "computeType",
        "image": "image",
        "type": "type",
        "certificate": "certificate",
        "docker_server": "dockerServer",
        "environment_variable": "environmentVariable",
        "fleet": "fleet",
        "image_pull_credentials_type": "imagePullCredentialsType",
        "privileged_mode": "privilegedMode",
        "registry_credential": "registryCredential",
    },
)
class CodebuildProjectEnvironment:
    def __init__(
        self,
        *,
        compute_type: builtins.str,
        image: builtins.str,
        type: builtins.str,
        certificate: typing.Optional[builtins.str] = None,
        docker_server: typing.Optional[typing.Union["CodebuildProjectEnvironmentDockerServer", typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodebuildProjectEnvironmentEnvironmentVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        fleet: typing.Optional[typing.Union["CodebuildProjectEnvironmentFleet", typing.Dict[builtins.str, typing.Any]]] = None,
        image_pull_credentials_type: typing.Optional[builtins.str] = None,
        privileged_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        registry_credential: typing.Optional[typing.Union["CodebuildProjectEnvironmentRegistryCredential", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param compute_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#compute_type CodebuildProject#compute_type}.
        :param image: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#image CodebuildProject#image}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.
        :param certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#certificate CodebuildProject#certificate}.
        :param docker_server: docker_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#docker_server CodebuildProject#docker_server}
        :param environment_variable: environment_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#environment_variable CodebuildProject#environment_variable}
        :param fleet: fleet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#fleet CodebuildProject#fleet}
        :param image_pull_credentials_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#image_pull_credentials_type CodebuildProject#image_pull_credentials_type}.
        :param privileged_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#privileged_mode CodebuildProject#privileged_mode}.
        :param registry_credential: registry_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#registry_credential CodebuildProject#registry_credential}
        '''
        if isinstance(docker_server, dict):
            docker_server = CodebuildProjectEnvironmentDockerServer(**docker_server)
        if isinstance(fleet, dict):
            fleet = CodebuildProjectEnvironmentFleet(**fleet)
        if isinstance(registry_credential, dict):
            registry_credential = CodebuildProjectEnvironmentRegistryCredential(**registry_credential)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c54475e4262ccd7c534e789e96384cc7c8204715e868718c53ed5be2139e9c4)
            check_type(argname="argument compute_type", value=compute_type, expected_type=type_hints["compute_type"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument docker_server", value=docker_server, expected_type=type_hints["docker_server"])
            check_type(argname="argument environment_variable", value=environment_variable, expected_type=type_hints["environment_variable"])
            check_type(argname="argument fleet", value=fleet, expected_type=type_hints["fleet"])
            check_type(argname="argument image_pull_credentials_type", value=image_pull_credentials_type, expected_type=type_hints["image_pull_credentials_type"])
            check_type(argname="argument privileged_mode", value=privileged_mode, expected_type=type_hints["privileged_mode"])
            check_type(argname="argument registry_credential", value=registry_credential, expected_type=type_hints["registry_credential"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compute_type": compute_type,
            "image": image,
            "type": type,
        }
        if certificate is not None:
            self._values["certificate"] = certificate
        if docker_server is not None:
            self._values["docker_server"] = docker_server
        if environment_variable is not None:
            self._values["environment_variable"] = environment_variable
        if fleet is not None:
            self._values["fleet"] = fleet
        if image_pull_credentials_type is not None:
            self._values["image_pull_credentials_type"] = image_pull_credentials_type
        if privileged_mode is not None:
            self._values["privileged_mode"] = privileged_mode
        if registry_credential is not None:
            self._values["registry_credential"] = registry_credential

    @builtins.property
    def compute_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#compute_type CodebuildProject#compute_type}.'''
        result = self._values.get("compute_type")
        assert result is not None, "Required property 'compute_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#image CodebuildProject#image}.'''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#certificate CodebuildProject#certificate}.'''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_server(
        self,
    ) -> typing.Optional["CodebuildProjectEnvironmentDockerServer"]:
        '''docker_server block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#docker_server CodebuildProject#docker_server}
        '''
        result = self._values.get("docker_server")
        return typing.cast(typing.Optional["CodebuildProjectEnvironmentDockerServer"], result)

    @builtins.property
    def environment_variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodebuildProjectEnvironmentEnvironmentVariable"]]]:
        '''environment_variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#environment_variable CodebuildProject#environment_variable}
        '''
        result = self._values.get("environment_variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodebuildProjectEnvironmentEnvironmentVariable"]]], result)

    @builtins.property
    def fleet(self) -> typing.Optional["CodebuildProjectEnvironmentFleet"]:
        '''fleet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#fleet CodebuildProject#fleet}
        '''
        result = self._values.get("fleet")
        return typing.cast(typing.Optional["CodebuildProjectEnvironmentFleet"], result)

    @builtins.property
    def image_pull_credentials_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#image_pull_credentials_type CodebuildProject#image_pull_credentials_type}.'''
        result = self._values.get("image_pull_credentials_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def privileged_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#privileged_mode CodebuildProject#privileged_mode}.'''
        result = self._values.get("privileged_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def registry_credential(
        self,
    ) -> typing.Optional["CodebuildProjectEnvironmentRegistryCredential"]:
        '''registry_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#registry_credential CodebuildProject#registry_credential}
        '''
        result = self._values.get("registry_credential")
        return typing.cast(typing.Optional["CodebuildProjectEnvironmentRegistryCredential"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectEnvironment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectEnvironmentDockerServer",
    jsii_struct_bases=[],
    name_mapping={
        "compute_type": "computeType",
        "security_group_ids": "securityGroupIds",
    },
)
class CodebuildProjectEnvironmentDockerServer:
    def __init__(
        self,
        *,
        compute_type: builtins.str,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param compute_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#compute_type CodebuildProject#compute_type}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#security_group_ids CodebuildProject#security_group_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1adee899118d3b1836a8dd3ed3577416bcbdbac4dc2bc058931a05b8df39655)
            check_type(argname="argument compute_type", value=compute_type, expected_type=type_hints["compute_type"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compute_type": compute_type,
        }
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids

    @builtins.property
    def compute_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#compute_type CodebuildProject#compute_type}.'''
        result = self._values.get("compute_type")
        assert result is not None, "Required property 'compute_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#security_group_ids CodebuildProject#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectEnvironmentDockerServer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectEnvironmentDockerServerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectEnvironmentDockerServerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69cad0aa1264e14ea522999c80fa71dc55702efdedef884cde88804ec177cc34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSecurityGroupIds")
    def reset_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupIds", []))

    @builtins.property
    @jsii.member(jsii_name="computeTypeInput")
    def compute_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="computeType")
    def compute_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computeType"))

    @compute_type.setter
    def compute_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__807b897a3daaf00ad948876f8eaa95c5b04e0954e68bb3b9763ac6a873083cd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__793464acf36973bddd00997bd4912443dd1a107ca77a3bdd787c228a8ad580eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodebuildProjectEnvironmentDockerServer]:
        return typing.cast(typing.Optional[CodebuildProjectEnvironmentDockerServer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodebuildProjectEnvironmentDockerServer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f837b374e4dbd5d62938f7d0cf3c799c67490d3cbe612432310dc2df8c76505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectEnvironmentEnvironmentVariable",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value", "type": "type"},
)
class CodebuildProjectEnvironmentEnvironmentVariable:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: builtins.str,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#name CodebuildProject#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#value CodebuildProject#value}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c43517826bd4a8e0305a9ddd654e8182c1da8079d67aa2408a3ff1783ccb39b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#name CodebuildProject#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#value CodebuildProject#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectEnvironmentEnvironmentVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectEnvironmentEnvironmentVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectEnvironmentEnvironmentVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__104223f325d364c3a9d17ab248a91027cee22624ccc009e1aa31f6fada641200)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodebuildProjectEnvironmentEnvironmentVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a40b143e842210110a27210605b429587d793805a7cc7fb10d93bb7f4c6e5b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodebuildProjectEnvironmentEnvironmentVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35392f577670fc87c8cd1634d4f5d9a754a77efcd54920a2606cd203f4cd05fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ad767b60c99263391bcc93e57e06c01f551d2ea8d6192276c87d033d766eea3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4120d6e1aff491698dc5d785fa3525a8064390aaf8fdd8484969dd9450a3f749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectEnvironmentEnvironmentVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectEnvironmentEnvironmentVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectEnvironmentEnvironmentVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83cb412a5edb3bf96def113692ec0e44e14de7b93bf21da125d6d49542b36d6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodebuildProjectEnvironmentEnvironmentVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectEnvironmentEnvironmentVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b96035234318835cf559f02ce8ef60039d78eec7fee7f83a72afd14c9f673c51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2ae37313c7c6c9321c23b5d1f0c02565f0c65ef877e90e46307dfa85325dd444)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dc68bd37dc173a95d160f5f9986e18d9693b1974ab3b32dc3b2188127bad120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__557077950d51482bfcdf48caf00eadf8bf7635710559e633dd44a593e5b48d3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectEnvironmentEnvironmentVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectEnvironmentEnvironmentVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectEnvironmentEnvironmentVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17e63ccde55938d3bffe3e327c623a662afb53ab073285c8e93fb1eae1f50796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectEnvironmentFleet",
    jsii_struct_bases=[],
    name_mapping={"fleet_arn": "fleetArn"},
)
class CodebuildProjectEnvironmentFleet:
    def __init__(self, *, fleet_arn: typing.Optional[builtins.str] = None) -> None:
        '''
        :param fleet_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#fleet_arn CodebuildProject#fleet_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c18bf4cc9cb059de67accb3f6c9f3ca411f90daf0cef2f9c75f9c22e56edc86b)
            check_type(argname="argument fleet_arn", value=fleet_arn, expected_type=type_hints["fleet_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fleet_arn is not None:
            self._values["fleet_arn"] = fleet_arn

    @builtins.property
    def fleet_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#fleet_arn CodebuildProject#fleet_arn}.'''
        result = self._values.get("fleet_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectEnvironmentFleet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectEnvironmentFleetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectEnvironmentFleetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8dfb21b5642e3888493b8eeed12861e0e05332d620333c252a22a75e80b4ff7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFleetArn")
    def reset_fleet_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFleetArn", []))

    @builtins.property
    @jsii.member(jsii_name="fleetArnInput")
    def fleet_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fleetArnInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetArn")
    def fleet_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fleetArn"))

    @fleet_arn.setter
    def fleet_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60812a27c6fa89b05fdc19cc2459aaabb4cafc01bd01457cf163477327e6c3d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fleetArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CodebuildProjectEnvironmentFleet]:
        return typing.cast(typing.Optional[CodebuildProjectEnvironmentFleet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodebuildProjectEnvironmentFleet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7378347325eef2cbfbf1547ee22a0884b4dbcfcbc76bd22ec255508205fc5d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodebuildProjectEnvironmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectEnvironmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73f896f3fa34a120886702f8328592ae24eed3c0544406dc9d32124f6ee7f9eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDockerServer")
    def put_docker_server(
        self,
        *,
        compute_type: builtins.str,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param compute_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#compute_type CodebuildProject#compute_type}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#security_group_ids CodebuildProject#security_group_ids}.
        '''
        value = CodebuildProjectEnvironmentDockerServer(
            compute_type=compute_type, security_group_ids=security_group_ids
        )

        return typing.cast(None, jsii.invoke(self, "putDockerServer", [value]))

    @jsii.member(jsii_name="putEnvironmentVariable")
    def put_environment_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodebuildProjectEnvironmentEnvironmentVariable, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81fe24e99ddf72ea5b13ab09e8fd2faef33d5aa9fcdef9c820cbbfc77b67278b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnvironmentVariable", [value]))

    @jsii.member(jsii_name="putFleet")
    def put_fleet(self, *, fleet_arn: typing.Optional[builtins.str] = None) -> None:
        '''
        :param fleet_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#fleet_arn CodebuildProject#fleet_arn}.
        '''
        value = CodebuildProjectEnvironmentFleet(fleet_arn=fleet_arn)

        return typing.cast(None, jsii.invoke(self, "putFleet", [value]))

    @jsii.member(jsii_name="putRegistryCredential")
    def put_registry_credential(
        self,
        *,
        credential: builtins.str,
        credential_provider: builtins.str,
    ) -> None:
        '''
        :param credential: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#credential CodebuildProject#credential}.
        :param credential_provider: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#credential_provider CodebuildProject#credential_provider}.
        '''
        value = CodebuildProjectEnvironmentRegistryCredential(
            credential=credential, credential_provider=credential_provider
        )

        return typing.cast(None, jsii.invoke(self, "putRegistryCredential", [value]))

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetDockerServer")
    def reset_docker_server(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerServer", []))

    @jsii.member(jsii_name="resetEnvironmentVariable")
    def reset_environment_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentVariable", []))

    @jsii.member(jsii_name="resetFleet")
    def reset_fleet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFleet", []))

    @jsii.member(jsii_name="resetImagePullCredentialsType")
    def reset_image_pull_credentials_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImagePullCredentialsType", []))

    @jsii.member(jsii_name="resetPrivilegedMode")
    def reset_privileged_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivilegedMode", []))

    @jsii.member(jsii_name="resetRegistryCredential")
    def reset_registry_credential(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistryCredential", []))

    @builtins.property
    @jsii.member(jsii_name="dockerServer")
    def docker_server(self) -> CodebuildProjectEnvironmentDockerServerOutputReference:
        return typing.cast(CodebuildProjectEnvironmentDockerServerOutputReference, jsii.get(self, "dockerServer"))

    @builtins.property
    @jsii.member(jsii_name="environmentVariable")
    def environment_variable(
        self,
    ) -> CodebuildProjectEnvironmentEnvironmentVariableList:
        return typing.cast(CodebuildProjectEnvironmentEnvironmentVariableList, jsii.get(self, "environmentVariable"))

    @builtins.property
    @jsii.member(jsii_name="fleet")
    def fleet(self) -> CodebuildProjectEnvironmentFleetOutputReference:
        return typing.cast(CodebuildProjectEnvironmentFleetOutputReference, jsii.get(self, "fleet"))

    @builtins.property
    @jsii.member(jsii_name="registryCredential")
    def registry_credential(
        self,
    ) -> "CodebuildProjectEnvironmentRegistryCredentialOutputReference":
        return typing.cast("CodebuildProjectEnvironmentRegistryCredentialOutputReference", jsii.get(self, "registryCredential"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="computeTypeInput")
    def compute_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerServerInput")
    def docker_server_input(
        self,
    ) -> typing.Optional[CodebuildProjectEnvironmentDockerServer]:
        return typing.cast(typing.Optional[CodebuildProjectEnvironmentDockerServer], jsii.get(self, "dockerServerInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentVariableInput")
    def environment_variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectEnvironmentEnvironmentVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectEnvironmentEnvironmentVariable]]], jsii.get(self, "environmentVariableInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetInput")
    def fleet_input(self) -> typing.Optional[CodebuildProjectEnvironmentFleet]:
        return typing.cast(typing.Optional[CodebuildProjectEnvironmentFleet], jsii.get(self, "fleetInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="imagePullCredentialsTypeInput")
    def image_pull_credentials_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imagePullCredentialsTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="privilegedModeInput")
    def privileged_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "privilegedModeInput"))

    @builtins.property
    @jsii.member(jsii_name="registryCredentialInput")
    def registry_credential_input(
        self,
    ) -> typing.Optional["CodebuildProjectEnvironmentRegistryCredential"]:
        return typing.cast(typing.Optional["CodebuildProjectEnvironmentRegistryCredential"], jsii.get(self, "registryCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15f8145222bed4871cf47477399120992171d3bfa7460db071f090c61b1f0d18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="computeType")
    def compute_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computeType"))

    @compute_type.setter
    def compute_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a5e083a7c2f3f7a1d5021434bdebba6777ad5b784ba2e3fdfb174886e235be5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf9b1f0a738dca4e2f8c92a32f3fd6537486480a2db36309af209fbfd21b1bb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imagePullCredentialsType")
    def image_pull_credentials_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imagePullCredentialsType"))

    @image_pull_credentials_type.setter
    def image_pull_credentials_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb91fdeb106e3b53a196e7b6bde43c8bf260ac2b4943f6310c565b525245dba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imagePullCredentialsType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privilegedMode")
    def privileged_mode(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "privilegedMode"))

    @privileged_mode.setter
    def privileged_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__620d1fa94b532acc85f40868bbefe16f48830e0fa306ea6042c91cbe9b126b1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privilegedMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4752dc13d217593e137c8264f968eff9d7f538ede46dc3647902ec943a801869)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CodebuildProjectEnvironment]:
        return typing.cast(typing.Optional[CodebuildProjectEnvironment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodebuildProjectEnvironment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d42622debae3b34179b9c0bae588fdfe000bdf75d6519a0d7d2a38a9312be77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectEnvironmentRegistryCredential",
    jsii_struct_bases=[],
    name_mapping={
        "credential": "credential",
        "credential_provider": "credentialProvider",
    },
)
class CodebuildProjectEnvironmentRegistryCredential:
    def __init__(
        self,
        *,
        credential: builtins.str,
        credential_provider: builtins.str,
    ) -> None:
        '''
        :param credential: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#credential CodebuildProject#credential}.
        :param credential_provider: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#credential_provider CodebuildProject#credential_provider}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6deec6f18e65734f0767d81dc837537ca6431a5adf20d53c19080089b33c7e2)
            check_type(argname="argument credential", value=credential, expected_type=type_hints["credential"])
            check_type(argname="argument credential_provider", value=credential_provider, expected_type=type_hints["credential_provider"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "credential": credential,
            "credential_provider": credential_provider,
        }

    @builtins.property
    def credential(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#credential CodebuildProject#credential}.'''
        result = self._values.get("credential")
        assert result is not None, "Required property 'credential' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def credential_provider(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#credential_provider CodebuildProject#credential_provider}.'''
        result = self._values.get("credential_provider")
        assert result is not None, "Required property 'credential_provider' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectEnvironmentRegistryCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectEnvironmentRegistryCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectEnvironmentRegistryCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77428e21e32ac09ae620c1f4126a427aa82184be5ce798b0288e830515c8166d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="credentialInput")
    def credential_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialProviderInput")
    def credential_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="credential")
    def credential(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credential"))

    @credential.setter
    def credential(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81896d43703251509e8cef556b7f4f75ceedfbd52156ef8f6087fb606ac0d4d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credential", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="credentialProvider")
    def credential_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialProvider"))

    @credential_provider.setter
    def credential_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__100939022f49a80259c4c9a76cd4faff412f7c7cdb09c1f1be98b5f89f6656c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialProvider", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodebuildProjectEnvironmentRegistryCredential]:
        return typing.cast(typing.Optional[CodebuildProjectEnvironmentRegistryCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodebuildProjectEnvironmentRegistryCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6e5a34101ec926319934c60e5a294478b5827d5609a2874c7d0f65d4d82cba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectFileSystemLocations",
    jsii_struct_bases=[],
    name_mapping={
        "identifier": "identifier",
        "location": "location",
        "mount_options": "mountOptions",
        "mount_point": "mountPoint",
        "type": "type",
    },
)
class CodebuildProjectFileSystemLocations:
    def __init__(
        self,
        *,
        identifier: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        mount_options: typing.Optional[builtins.str] = None,
        mount_point: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#identifier CodebuildProject#identifier}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#location CodebuildProject#location}.
        :param mount_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#mount_options CodebuildProject#mount_options}.
        :param mount_point: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#mount_point CodebuildProject#mount_point}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d445b44cf48bf0c774f8d26ca66eef0d5af059484995e733296c071e0f22eccd)
            check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
            check_type(argname="argument mount_point", value=mount_point, expected_type=type_hints["mount_point"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identifier is not None:
            self._values["identifier"] = identifier
        if location is not None:
            self._values["location"] = location
        if mount_options is not None:
            self._values["mount_options"] = mount_options
        if mount_point is not None:
            self._values["mount_point"] = mount_point
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def identifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#identifier CodebuildProject#identifier}.'''
        result = self._values.get("identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#location CodebuildProject#location}.'''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mount_options(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#mount_options CodebuildProject#mount_options}.'''
        result = self._values.get("mount_options")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mount_point(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#mount_point CodebuildProject#mount_point}.'''
        result = self._values.get("mount_point")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectFileSystemLocations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectFileSystemLocationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectFileSystemLocationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6897c3c0f278bcd7cc6f5bb6f293b6b2fd1f8e2e6d009f3cfd8b0c181e8d14c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodebuildProjectFileSystemLocationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba0f84a66f64713b220e07eb8fe1b704c1f8bd92bc733998d1de4bd691e83ac3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodebuildProjectFileSystemLocationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b49b5030ac131d2681e6856a96cc0800957fe2986d71e9b8aa244aed28e5c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1289d0c9fd60c75cb9447c967950b6e6a0833ecb61aa2061966f65beeb68871)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e085b49f91b93f6ef97667c0db12882d742a853ebe188145711921a46bc7e793)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectFileSystemLocations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectFileSystemLocations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectFileSystemLocations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c3f850fe869748bfd33a12e6b4c7cfb71ae3cf2893f4513d06fd02c7af69b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodebuildProjectFileSystemLocationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectFileSystemLocationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3f327ed1a951bb018e619fe899a3e27cc2bcc48f75240be6c62e8a890ae0166)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIdentifier")
    def reset_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentifier", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetMountOptions")
    def reset_mount_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMountOptions", []))

    @jsii.member(jsii_name="resetMountPoint")
    def reset_mount_point(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMountPoint", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="identifierInput")
    def identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identifierInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="mountOptionsInput")
    def mount_options_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="mountPointInput")
    def mount_point_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountPointInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identifier"))

    @identifier.setter
    def identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6979c7466b3e85470ff25e6d4633e37ef7c0a4740ac5f2d106350419cfb601e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97d5f31c62aa4d8208df351cf39ba68075047a418c9b0708b25e9c62cc7ed01d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mountOptions")
    def mount_options(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountOptions"))

    @mount_options.setter
    def mount_options(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7571cad55600038cafd9e0dc63529119707a8996f8902c4a110cb88636d6dfdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mountPoint")
    def mount_point(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountPoint"))

    @mount_point.setter
    def mount_point(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da696801b25aebafa575b7417510af9f383ab10a73ba4bbc543c374cf945b715)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountPoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e10df9d55316b4e62c5ba4e8f10862fced41b721d814a5c185e6d61f7099c75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectFileSystemLocations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectFileSystemLocations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectFileSystemLocations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df655a13a5401681ea3ed06da57e90298552b3281315860c43a13fa23dc75737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectLogsConfig",
    jsii_struct_bases=[],
    name_mapping={"cloudwatch_logs": "cloudwatchLogs", "s3_logs": "s3Logs"},
)
class CodebuildProjectLogsConfig:
    def __init__(
        self,
        *,
        cloudwatch_logs: typing.Optional[typing.Union["CodebuildProjectLogsConfigCloudwatchLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_logs: typing.Optional[typing.Union["CodebuildProjectLogsConfigS3Logs", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_logs: cloudwatch_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#cloudwatch_logs CodebuildProject#cloudwatch_logs}
        :param s3_logs: s3_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#s3_logs CodebuildProject#s3_logs}
        '''
        if isinstance(cloudwatch_logs, dict):
            cloudwatch_logs = CodebuildProjectLogsConfigCloudwatchLogs(**cloudwatch_logs)
        if isinstance(s3_logs, dict):
            s3_logs = CodebuildProjectLogsConfigS3Logs(**s3_logs)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a50a885337922104c9c2d41fea26b09b4bc188e3c3029046076aa83746483e16)
            check_type(argname="argument cloudwatch_logs", value=cloudwatch_logs, expected_type=type_hints["cloudwatch_logs"])
            check_type(argname="argument s3_logs", value=s3_logs, expected_type=type_hints["s3_logs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloudwatch_logs is not None:
            self._values["cloudwatch_logs"] = cloudwatch_logs
        if s3_logs is not None:
            self._values["s3_logs"] = s3_logs

    @builtins.property
    def cloudwatch_logs(
        self,
    ) -> typing.Optional["CodebuildProjectLogsConfigCloudwatchLogs"]:
        '''cloudwatch_logs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#cloudwatch_logs CodebuildProject#cloudwatch_logs}
        '''
        result = self._values.get("cloudwatch_logs")
        return typing.cast(typing.Optional["CodebuildProjectLogsConfigCloudwatchLogs"], result)

    @builtins.property
    def s3_logs(self) -> typing.Optional["CodebuildProjectLogsConfigS3Logs"]:
        '''s3_logs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#s3_logs CodebuildProject#s3_logs}
        '''
        result = self._values.get("s3_logs")
        return typing.cast(typing.Optional["CodebuildProjectLogsConfigS3Logs"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectLogsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectLogsConfigCloudwatchLogs",
    jsii_struct_bases=[],
    name_mapping={
        "group_name": "groupName",
        "status": "status",
        "stream_name": "streamName",
    },
)
class CodebuildProjectLogsConfigCloudwatchLogs:
    def __init__(
        self,
        *,
        group_name: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#group_name CodebuildProject#group_name}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#status CodebuildProject#status}.
        :param stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#stream_name CodebuildProject#stream_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ce9a8cacb5b15fc2921c1c6f38eabe183a4405c786b5b41a5cb7ac83013a87)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_name is not None:
            self._values["group_name"] = group_name
        if status is not None:
            self._values["status"] = status
        if stream_name is not None:
            self._values["stream_name"] = stream_name

    @builtins.property
    def group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#group_name CodebuildProject#group_name}.'''
        result = self._values.get("group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#status CodebuildProject#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stream_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#stream_name CodebuildProject#stream_name}.'''
        result = self._values.get("stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectLogsConfigCloudwatchLogs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectLogsConfigCloudwatchLogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectLogsConfigCloudwatchLogsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5328e281c32eb53221ce1dfca88037919aae3ca3fb959e901f82e7dcc5be425)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGroupName")
    def reset_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupName", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetStreamName")
    def reset_stream_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStreamName", []))

    @builtins.property
    @jsii.member(jsii_name="groupNameInput")
    def group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="streamNameInput")
    def stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupName"))

    @group_name.setter
    def group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a503f03b59dcb704621450163c252dd0bfe543f68283202e5e8feebb3d2d23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be999bb9b0a41efe96068e4ed81da9d10701ab706e7397f3f0556102b96dea3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamName"))

    @stream_name.setter
    def stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701f863321d47853026ecee6ccaa9dbcac4a72f765c0486806883a5f57511d4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodebuildProjectLogsConfigCloudwatchLogs]:
        return typing.cast(typing.Optional[CodebuildProjectLogsConfigCloudwatchLogs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodebuildProjectLogsConfigCloudwatchLogs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78eb559b6f34cb332acead3acdb393a3ca8bdfa73f06f881a6de21fa1289f259)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodebuildProjectLogsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectLogsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86dd660310c53cf510fe5824a265b0bde374d73c2fe1ca9926c0177ab1822443)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLogs")
    def put_cloudwatch_logs(
        self,
        *,
        group_name: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#group_name CodebuildProject#group_name}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#status CodebuildProject#status}.
        :param stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#stream_name CodebuildProject#stream_name}.
        '''
        value = CodebuildProjectLogsConfigCloudwatchLogs(
            group_name=group_name, status=status, stream_name=stream_name
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLogs", [value]))

    @jsii.member(jsii_name="putS3Logs")
    def put_s3_logs(
        self,
        *,
        bucket_owner_access: typing.Optional[builtins.str] = None,
        encryption_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        location: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_owner_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#bucket_owner_access CodebuildProject#bucket_owner_access}.
        :param encryption_disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#encryption_disabled CodebuildProject#encryption_disabled}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#location CodebuildProject#location}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#status CodebuildProject#status}.
        '''
        value = CodebuildProjectLogsConfigS3Logs(
            bucket_owner_access=bucket_owner_access,
            encryption_disabled=encryption_disabled,
            location=location,
            status=status,
        )

        return typing.cast(None, jsii.invoke(self, "putS3Logs", [value]))

    @jsii.member(jsii_name="resetCloudwatchLogs")
    def reset_cloudwatch_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogs", []))

    @jsii.member(jsii_name="resetS3Logs")
    def reset_s3_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Logs", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogs")
    def cloudwatch_logs(
        self,
    ) -> CodebuildProjectLogsConfigCloudwatchLogsOutputReference:
        return typing.cast(CodebuildProjectLogsConfigCloudwatchLogsOutputReference, jsii.get(self, "cloudwatchLogs"))

    @builtins.property
    @jsii.member(jsii_name="s3Logs")
    def s3_logs(self) -> "CodebuildProjectLogsConfigS3LogsOutputReference":
        return typing.cast("CodebuildProjectLogsConfigS3LogsOutputReference", jsii.get(self, "s3Logs"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsInput")
    def cloudwatch_logs_input(
        self,
    ) -> typing.Optional[CodebuildProjectLogsConfigCloudwatchLogs]:
        return typing.cast(typing.Optional[CodebuildProjectLogsConfigCloudwatchLogs], jsii.get(self, "cloudwatchLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="s3LogsInput")
    def s3_logs_input(self) -> typing.Optional["CodebuildProjectLogsConfigS3Logs"]:
        return typing.cast(typing.Optional["CodebuildProjectLogsConfigS3Logs"], jsii.get(self, "s3LogsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CodebuildProjectLogsConfig]:
        return typing.cast(typing.Optional[CodebuildProjectLogsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodebuildProjectLogsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e2c6ee8ea517c54042ec5bf236a7f9449cf305b8808025b094e45612cb76b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectLogsConfigS3Logs",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_owner_access": "bucketOwnerAccess",
        "encryption_disabled": "encryptionDisabled",
        "location": "location",
        "status": "status",
    },
)
class CodebuildProjectLogsConfigS3Logs:
    def __init__(
        self,
        *,
        bucket_owner_access: typing.Optional[builtins.str] = None,
        encryption_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        location: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_owner_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#bucket_owner_access CodebuildProject#bucket_owner_access}.
        :param encryption_disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#encryption_disabled CodebuildProject#encryption_disabled}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#location CodebuildProject#location}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#status CodebuildProject#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ecb150279926621f0a3c1cb804c98b559aaa735bd9d68a923a2925938c078f)
            check_type(argname="argument bucket_owner_access", value=bucket_owner_access, expected_type=type_hints["bucket_owner_access"])
            check_type(argname="argument encryption_disabled", value=encryption_disabled, expected_type=type_hints["encryption_disabled"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_owner_access is not None:
            self._values["bucket_owner_access"] = bucket_owner_access
        if encryption_disabled is not None:
            self._values["encryption_disabled"] = encryption_disabled
        if location is not None:
            self._values["location"] = location
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def bucket_owner_access(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#bucket_owner_access CodebuildProject#bucket_owner_access}.'''
        result = self._values.get("bucket_owner_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#encryption_disabled CodebuildProject#encryption_disabled}.'''
        result = self._values.get("encryption_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#location CodebuildProject#location}.'''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#status CodebuildProject#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectLogsConfigS3Logs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectLogsConfigS3LogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectLogsConfigS3LogsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b66f4a0fe7509d1d2d9f780cfebb790706f71b386826c68e0cbc49e3fd6bb6ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketOwnerAccess")
    def reset_bucket_owner_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketOwnerAccess", []))

    @jsii.member(jsii_name="resetEncryptionDisabled")
    def reset_encryption_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionDisabled", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="bucketOwnerAccessInput")
    def bucket_owner_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketOwnerAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionDisabledInput")
    def encryption_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptionDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketOwnerAccess")
    def bucket_owner_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketOwnerAccess"))

    @bucket_owner_access.setter
    def bucket_owner_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__091270440cc5d178757fd2443224daaa658b0315cadee77a0aba1e319052b68f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketOwnerAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionDisabled")
    def encryption_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encryptionDisabled"))

    @encryption_disabled.setter
    def encryption_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66b67225131d11ec66f9f6b143d8851fe234eea882b846dffed2b37e67ee0f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e6fc8264af4b6a6e77785f8ba54fc6c678410d35610b25cedbc54cab5bba7c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dc0aa56e36a81a0c65733441a8e62f980adf6b88c78a47d94f877d902bf503d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CodebuildProjectLogsConfigS3Logs]:
        return typing.cast(typing.Optional[CodebuildProjectLogsConfigS3Logs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodebuildProjectLogsConfigS3Logs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6ab1914a2de8e39d23275578c5d9245435b19cfa2052bf8245f86b65dddf84c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSecondaryArtifacts",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_identifier": "artifactIdentifier",
        "type": "type",
        "bucket_owner_access": "bucketOwnerAccess",
        "encryption_disabled": "encryptionDisabled",
        "location": "location",
        "name": "name",
        "namespace_type": "namespaceType",
        "override_artifact_name": "overrideArtifactName",
        "packaging": "packaging",
        "path": "path",
    },
)
class CodebuildProjectSecondaryArtifacts:
    def __init__(
        self,
        *,
        artifact_identifier: builtins.str,
        type: builtins.str,
        bucket_owner_access: typing.Optional[builtins.str] = None,
        encryption_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        namespace_type: typing.Optional[builtins.str] = None,
        override_artifact_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        packaging: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param artifact_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#artifact_identifier CodebuildProject#artifact_identifier}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.
        :param bucket_owner_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#bucket_owner_access CodebuildProject#bucket_owner_access}.
        :param encryption_disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#encryption_disabled CodebuildProject#encryption_disabled}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#location CodebuildProject#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#name CodebuildProject#name}.
        :param namespace_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#namespace_type CodebuildProject#namespace_type}.
        :param override_artifact_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#override_artifact_name CodebuildProject#override_artifact_name}.
        :param packaging: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#packaging CodebuildProject#packaging}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#path CodebuildProject#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e948569a1479a8aca3b95b2ddd1f42cf365db9a2aa82e7cba65715dc45a83af7)
            check_type(argname="argument artifact_identifier", value=artifact_identifier, expected_type=type_hints["artifact_identifier"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument bucket_owner_access", value=bucket_owner_access, expected_type=type_hints["bucket_owner_access"])
            check_type(argname="argument encryption_disabled", value=encryption_disabled, expected_type=type_hints["encryption_disabled"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace_type", value=namespace_type, expected_type=type_hints["namespace_type"])
            check_type(argname="argument override_artifact_name", value=override_artifact_name, expected_type=type_hints["override_artifact_name"])
            check_type(argname="argument packaging", value=packaging, expected_type=type_hints["packaging"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_identifier": artifact_identifier,
            "type": type,
        }
        if bucket_owner_access is not None:
            self._values["bucket_owner_access"] = bucket_owner_access
        if encryption_disabled is not None:
            self._values["encryption_disabled"] = encryption_disabled
        if location is not None:
            self._values["location"] = location
        if name is not None:
            self._values["name"] = name
        if namespace_type is not None:
            self._values["namespace_type"] = namespace_type
        if override_artifact_name is not None:
            self._values["override_artifact_name"] = override_artifact_name
        if packaging is not None:
            self._values["packaging"] = packaging
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def artifact_identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#artifact_identifier CodebuildProject#artifact_identifier}.'''
        result = self._values.get("artifact_identifier")
        assert result is not None, "Required property 'artifact_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_owner_access(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#bucket_owner_access CodebuildProject#bucket_owner_access}.'''
        result = self._values.get("bucket_owner_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#encryption_disabled CodebuildProject#encryption_disabled}.'''
        result = self._values.get("encryption_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#location CodebuildProject#location}.'''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#name CodebuildProject#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#namespace_type CodebuildProject#namespace_type}.'''
        result = self._values.get("namespace_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def override_artifact_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#override_artifact_name CodebuildProject#override_artifact_name}.'''
        result = self._values.get("override_artifact_name")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def packaging(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#packaging CodebuildProject#packaging}.'''
        result = self._values.get("packaging")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#path CodebuildProject#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectSecondaryArtifacts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectSecondaryArtifactsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSecondaryArtifactsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5c40d9175da38c9cd632945f967f5f5e87cd3ff21523292b8817296bbf7f537)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodebuildProjectSecondaryArtifactsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__109b02dc3e6b8c33bfcca9b5cbd9d9634f2a8046d576518b055a165ff8783418)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodebuildProjectSecondaryArtifactsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89cfc1221e7e7ae8ca178b274760f62479b05a696060ba20ee6c701bd324d19a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d11300da1ced62838a3b943894330e03a9d0d6ff41a377cccb084647c80d435)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61870e099675d36adf96edf2372dede4aaea06fe36c9f178f4fb2bff99a3adf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectSecondaryArtifacts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectSecondaryArtifacts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectSecondaryArtifacts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3453f3975dd2cb45545c97fcbf438e14c450f78a3605632cdd857016e4e5be7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodebuildProjectSecondaryArtifactsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSecondaryArtifactsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__671ef36202c69481d7c6cd2680ef83c0b6ebba6c2354b97eed4140820ef0e94c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBucketOwnerAccess")
    def reset_bucket_owner_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketOwnerAccess", []))

    @jsii.member(jsii_name="resetEncryptionDisabled")
    def reset_encryption_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionDisabled", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamespaceType")
    def reset_namespace_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespaceType", []))

    @jsii.member(jsii_name="resetOverrideArtifactName")
    def reset_override_artifact_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrideArtifactName", []))

    @jsii.member(jsii_name="resetPackaging")
    def reset_packaging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPackaging", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="artifactIdentifierInput")
    def artifact_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketOwnerAccessInput")
    def bucket_owner_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketOwnerAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionDisabledInput")
    def encryption_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptionDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceTypeInput")
    def namespace_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideArtifactNameInput")
    def override_artifact_name_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overrideArtifactNameInput"))

    @builtins.property
    @jsii.member(jsii_name="packagingInput")
    def packaging_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "packagingInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactIdentifier")
    def artifact_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "artifactIdentifier"))

    @artifact_identifier.setter
    def artifact_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c68595c9a17e1b42908b20a6726ee176c03a111e826f5f25da65dcccb6cc23a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketOwnerAccess")
    def bucket_owner_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketOwnerAccess"))

    @bucket_owner_access.setter
    def bucket_owner_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2e8f01c4f56eef00885737b632d3652a3e2189cb889e5cc4818b5f647bcda67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketOwnerAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionDisabled")
    def encryption_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encryptionDisabled"))

    @encryption_disabled.setter
    def encryption_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fa1cc66ed4b8d83a262e37ddfd3371241be83171da01106af2c3999fdbaf76f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf7b27e9e6896d752d9300741abb772e4b409eb5b993a741278a2280bab91801)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f69fc28bfbb4e8ebb5533a052cd8eca4b6ea07f4211112b93897fa0ee4a8c99d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespaceType")
    def namespace_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespaceType"))

    @namespace_type.setter
    def namespace_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c82484553d9c8f2c630b1ae69e17071609b8804f95b08644f4b21bd2caf7fd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overrideArtifactName")
    def override_artifact_name(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "overrideArtifactName"))

    @override_artifact_name.setter
    def override_artifact_name(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d4193a8f767105e182b2d306c6c71f1f1d99dd157756a86a458827170af6167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overrideArtifactName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="packaging")
    def packaging(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "packaging"))

    @packaging.setter
    def packaging(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__531f065410f50b70ea0b1898b23b972d6899c386d8f1aca53d9d686c559d9d79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packaging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__987374ca934de8b6af5cd8a2e3b4fde8e52fefa586220578fa5571980bdadf10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e13590f321762f8d39a14aac79cb571782d21190e286285e6268f37622a282)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectSecondaryArtifacts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectSecondaryArtifacts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectSecondaryArtifacts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95c4939d9d1c2e13fd2dff7355315caf203c5014619955cac40fd4961ae98c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSecondarySourceVersion",
    jsii_struct_bases=[],
    name_mapping={
        "source_identifier": "sourceIdentifier",
        "source_version": "sourceVersion",
    },
)
class CodebuildProjectSecondarySourceVersion:
    def __init__(
        self,
        *,
        source_identifier: builtins.str,
        source_version: builtins.str,
    ) -> None:
        '''
        :param source_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#source_identifier CodebuildProject#source_identifier}.
        :param source_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#source_version CodebuildProject#source_version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__414193f01d464365535e1fb562af95f517845115f22519c56efcffb81405da7e)
            check_type(argname="argument source_identifier", value=source_identifier, expected_type=type_hints["source_identifier"])
            check_type(argname="argument source_version", value=source_version, expected_type=type_hints["source_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_identifier": source_identifier,
            "source_version": source_version,
        }

    @builtins.property
    def source_identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#source_identifier CodebuildProject#source_identifier}.'''
        result = self._values.get("source_identifier")
        assert result is not None, "Required property 'source_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#source_version CodebuildProject#source_version}.'''
        result = self._values.get("source_version")
        assert result is not None, "Required property 'source_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectSecondarySourceVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectSecondarySourceVersionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSecondarySourceVersionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9eb156e2e59010e8bf5f1d00ad7f06c91defef179ea7516929c35cdd3c76766)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodebuildProjectSecondarySourceVersionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ea704b91248e4e15371ef0cd3741e57f22ef6ff10eb7b5abcf4846f03a04bc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodebuildProjectSecondarySourceVersionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e6de5532beaafc4c4e152a67703489089a03a91f725d24c74a2b3de19e51ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fc202a2a792c2cecb4210977606b7cb7dae7418d83d9e2975598ce6859ccbd5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dae486652a2452d84e4dd220acd8f5b8542e4e224fa51f5c623cdfd68a51fa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectSecondarySourceVersion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectSecondarySourceVersion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectSecondarySourceVersion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f9477c9d9050a98a55a49fd0fb03bb717da8b9c6ed4fa080b4f8b325b09e83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodebuildProjectSecondarySourceVersionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSecondarySourceVersionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8888ea638ed48518d2753b69c01caec2f251da212593c1ab3b929f51bf0724d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="sourceIdentifierInput")
    def source_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceVersionInput")
    def source_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceIdentifier")
    def source_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceIdentifier"))

    @source_identifier.setter
    def source_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5cd674d04c5f6eb7e78aaf94e100d190376e6e68183c0d54399e9cb94b40ab1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceVersion")
    def source_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceVersion"))

    @source_version.setter
    def source_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf62f2e05bf9f425a771ba00eb6fac602c81f3d78e66d7e9ac257df64c92e6e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectSecondarySourceVersion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectSecondarySourceVersion]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectSecondarySourceVersion]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2946f0c9a774b0ba11b5237a5f8db8a1def9d60ace972ec75f41a0524ccb3865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSecondarySources",
    jsii_struct_bases=[],
    name_mapping={
        "source_identifier": "sourceIdentifier",
        "type": "type",
        "auth": "auth",
        "buildspec": "buildspec",
        "build_status_config": "buildStatusConfig",
        "git_clone_depth": "gitCloneDepth",
        "git_submodules_config": "gitSubmodulesConfig",
        "insecure_ssl": "insecureSsl",
        "location": "location",
        "report_build_status": "reportBuildStatus",
    },
)
class CodebuildProjectSecondarySources:
    def __init__(
        self,
        *,
        source_identifier: builtins.str,
        type: builtins.str,
        auth: typing.Optional[typing.Union["CodebuildProjectSecondarySourcesAuth", typing.Dict[builtins.str, typing.Any]]] = None,
        buildspec: typing.Optional[builtins.str] = None,
        build_status_config: typing.Optional[typing.Union["CodebuildProjectSecondarySourcesBuildStatusConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        git_clone_depth: typing.Optional[jsii.Number] = None,
        git_submodules_config: typing.Optional[typing.Union["CodebuildProjectSecondarySourcesGitSubmodulesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        insecure_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        location: typing.Optional[builtins.str] = None,
        report_build_status: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#source_identifier CodebuildProject#source_identifier}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.
        :param auth: auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#auth CodebuildProject#auth}
        :param buildspec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#buildspec CodebuildProject#buildspec}.
        :param build_status_config: build_status_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#build_status_config CodebuildProject#build_status_config}
        :param git_clone_depth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#git_clone_depth CodebuildProject#git_clone_depth}.
        :param git_submodules_config: git_submodules_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#git_submodules_config CodebuildProject#git_submodules_config}
        :param insecure_ssl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#insecure_ssl CodebuildProject#insecure_ssl}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#location CodebuildProject#location}.
        :param report_build_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#report_build_status CodebuildProject#report_build_status}.
        '''
        if isinstance(auth, dict):
            auth = CodebuildProjectSecondarySourcesAuth(**auth)
        if isinstance(build_status_config, dict):
            build_status_config = CodebuildProjectSecondarySourcesBuildStatusConfig(**build_status_config)
        if isinstance(git_submodules_config, dict):
            git_submodules_config = CodebuildProjectSecondarySourcesGitSubmodulesConfig(**git_submodules_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b7ff432626ebb901a6c5ac2e06bff4d0ced4af02f40f58b37341eb082e2b74)
            check_type(argname="argument source_identifier", value=source_identifier, expected_type=type_hints["source_identifier"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
            check_type(argname="argument buildspec", value=buildspec, expected_type=type_hints["buildspec"])
            check_type(argname="argument build_status_config", value=build_status_config, expected_type=type_hints["build_status_config"])
            check_type(argname="argument git_clone_depth", value=git_clone_depth, expected_type=type_hints["git_clone_depth"])
            check_type(argname="argument git_submodules_config", value=git_submodules_config, expected_type=type_hints["git_submodules_config"])
            check_type(argname="argument insecure_ssl", value=insecure_ssl, expected_type=type_hints["insecure_ssl"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument report_build_status", value=report_build_status, expected_type=type_hints["report_build_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_identifier": source_identifier,
            "type": type,
        }
        if auth is not None:
            self._values["auth"] = auth
        if buildspec is not None:
            self._values["buildspec"] = buildspec
        if build_status_config is not None:
            self._values["build_status_config"] = build_status_config
        if git_clone_depth is not None:
            self._values["git_clone_depth"] = git_clone_depth
        if git_submodules_config is not None:
            self._values["git_submodules_config"] = git_submodules_config
        if insecure_ssl is not None:
            self._values["insecure_ssl"] = insecure_ssl
        if location is not None:
            self._values["location"] = location
        if report_build_status is not None:
            self._values["report_build_status"] = report_build_status

    @builtins.property
    def source_identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#source_identifier CodebuildProject#source_identifier}.'''
        result = self._values.get("source_identifier")
        assert result is not None, "Required property 'source_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth(self) -> typing.Optional["CodebuildProjectSecondarySourcesAuth"]:
        '''auth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#auth CodebuildProject#auth}
        '''
        result = self._values.get("auth")
        return typing.cast(typing.Optional["CodebuildProjectSecondarySourcesAuth"], result)

    @builtins.property
    def buildspec(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#buildspec CodebuildProject#buildspec}.'''
        result = self._values.get("buildspec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_status_config(
        self,
    ) -> typing.Optional["CodebuildProjectSecondarySourcesBuildStatusConfig"]:
        '''build_status_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#build_status_config CodebuildProject#build_status_config}
        '''
        result = self._values.get("build_status_config")
        return typing.cast(typing.Optional["CodebuildProjectSecondarySourcesBuildStatusConfig"], result)

    @builtins.property
    def git_clone_depth(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#git_clone_depth CodebuildProject#git_clone_depth}.'''
        result = self._values.get("git_clone_depth")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def git_submodules_config(
        self,
    ) -> typing.Optional["CodebuildProjectSecondarySourcesGitSubmodulesConfig"]:
        '''git_submodules_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#git_submodules_config CodebuildProject#git_submodules_config}
        '''
        result = self._values.get("git_submodules_config")
        return typing.cast(typing.Optional["CodebuildProjectSecondarySourcesGitSubmodulesConfig"], result)

    @builtins.property
    def insecure_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#insecure_ssl CodebuildProject#insecure_ssl}.'''
        result = self._values.get("insecure_ssl")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#location CodebuildProject#location}.'''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def report_build_status(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#report_build_status CodebuildProject#report_build_status}.'''
        result = self._values.get("report_build_status")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectSecondarySources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSecondarySourcesAuth",
    jsii_struct_bases=[],
    name_mapping={"resource": "resource", "type": "type"},
)
class CodebuildProjectSecondarySourcesAuth:
    def __init__(self, *, resource: builtins.str, type: builtins.str) -> None:
        '''
        :param resource: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#resource CodebuildProject#resource}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0446230067839efc8c9d36fb7ba2f149c4c5d9801ee024bc6ace3660ef685f03)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource": resource,
            "type": type,
        }

    @builtins.property
    def resource(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#resource CodebuildProject#resource}.'''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectSecondarySourcesAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectSecondarySourcesAuthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSecondarySourcesAuthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__800170204b762563a971f6c953d46e1eb8bd1c3214e3d2697524488049b68dea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3369a24ebf3f79b8000388703c9b3e2ac313f0ad69fccb4a64ddfa5bbb0747f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f2ac8fb2dd505ca826407b5abbe1700ff4b356b2212cfe266320af4a3aa437f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CodebuildProjectSecondarySourcesAuth]:
        return typing.cast(typing.Optional[CodebuildProjectSecondarySourcesAuth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodebuildProjectSecondarySourcesAuth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f5d90a4ced4212e7b29f70be1dc17dca94177e0e0de4198e81676d18686d7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSecondarySourcesBuildStatusConfig",
    jsii_struct_bases=[],
    name_mapping={"context": "context", "target_url": "targetUrl"},
)
class CodebuildProjectSecondarySourcesBuildStatusConfig:
    def __init__(
        self,
        *,
        context: typing.Optional[builtins.str] = None,
        target_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param context: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#context CodebuildProject#context}.
        :param target_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#target_url CodebuildProject#target_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a48b394b69179de3d7f5510175f12b3e76bf944db640af8a4549fceb06a65d7)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument target_url", value=target_url, expected_type=type_hints["target_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if context is not None:
            self._values["context"] = context
        if target_url is not None:
            self._values["target_url"] = target_url

    @builtins.property
    def context(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#context CodebuildProject#context}.'''
        result = self._values.get("context")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#target_url CodebuildProject#target_url}.'''
        result = self._values.get("target_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectSecondarySourcesBuildStatusConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectSecondarySourcesBuildStatusConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSecondarySourcesBuildStatusConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c686f390d536847e200e850676a7b9e78e309026f23407c852dca8390734993d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContext")
    def reset_context(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContext", []))

    @jsii.member(jsii_name="resetTargetUrl")
    def reset_target_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="contextInput")
    def context_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextInput"))

    @builtins.property
    @jsii.member(jsii_name="targetUrlInput")
    def target_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "context"))

    @context.setter
    def context(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c22fa002302ddb997c0163ec182ba3cc42be3c1f792cfdbf8453d9b4762b5d80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetUrl")
    def target_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetUrl"))

    @target_url.setter
    def target_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b37e0b440a77b45483d877c858ce030ff4e5ade1d4802916b5b4668668c5f0f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodebuildProjectSecondarySourcesBuildStatusConfig]:
        return typing.cast(typing.Optional[CodebuildProjectSecondarySourcesBuildStatusConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodebuildProjectSecondarySourcesBuildStatusConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60cd5d41d32de5878216619a461a4b495bad3a1f90f3791bf682f379a0693c60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSecondarySourcesGitSubmodulesConfig",
    jsii_struct_bases=[],
    name_mapping={"fetch_submodules": "fetchSubmodules"},
)
class CodebuildProjectSecondarySourcesGitSubmodulesConfig:
    def __init__(
        self,
        *,
        fetch_submodules: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param fetch_submodules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#fetch_submodules CodebuildProject#fetch_submodules}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3832849a463c1cedc830a0047a47c5835ea368bf7bb308d544fc9c4844f6f31)
            check_type(argname="argument fetch_submodules", value=fetch_submodules, expected_type=type_hints["fetch_submodules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fetch_submodules": fetch_submodules,
        }

    @builtins.property
    def fetch_submodules(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#fetch_submodules CodebuildProject#fetch_submodules}.'''
        result = self._values.get("fetch_submodules")
        assert result is not None, "Required property 'fetch_submodules' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectSecondarySourcesGitSubmodulesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectSecondarySourcesGitSubmodulesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSecondarySourcesGitSubmodulesConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65af3654ef5e7fbaf06fb174625316f42373e72eb2e5b6d4927e33922a6736a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="fetchSubmodulesInput")
    def fetch_submodules_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchSubmodulesInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchSubmodules")
    def fetch_submodules(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchSubmodules"))

    @fetch_submodules.setter
    def fetch_submodules(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b79fb6ffb5be8974010bd7d7c467e099f5f78ffa1443a44e7b50168c9825d449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchSubmodules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodebuildProjectSecondarySourcesGitSubmodulesConfig]:
        return typing.cast(typing.Optional[CodebuildProjectSecondarySourcesGitSubmodulesConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodebuildProjectSecondarySourcesGitSubmodulesConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c6fca07118de6c8e5c323655b10584132ceb54787e13221fc3f54145e064a01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodebuildProjectSecondarySourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSecondarySourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b1f28badc89ea32d13011c50a0ad266df1452e7b5b6625f96f3f15fd43bbe16)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodebuildProjectSecondarySourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f90a8824ae53597d802c7ab0519048639243db55f9f3c729ad5705d2d48e50dc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodebuildProjectSecondarySourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6d800bd2496c5797e2e4104045544399a69d7003f286842bc7e0dd936c1b65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62c07f64899b6b4dc50c17929768fa6b7ca67a6e3c497450bb1d5ead0ba75a0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14a1e9b4d099d1d4a9d922312fbfb9c2d5ec35a5d0fa4291aeaa8de63141a06f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectSecondarySources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectSecondarySources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectSecondarySources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79092f990c12292a301dafc70a7fca013bb14a5b737c7ec248f2f7fb6ed92bd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodebuildProjectSecondarySourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSecondarySourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3fca9d04a04f8fac26ebf16af649e7b20befd19d7c6118b06295fe5b97fe7c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAuth")
    def put_auth(self, *, resource: builtins.str, type: builtins.str) -> None:
        '''
        :param resource: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#resource CodebuildProject#resource}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.
        '''
        value = CodebuildProjectSecondarySourcesAuth(resource=resource, type=type)

        return typing.cast(None, jsii.invoke(self, "putAuth", [value]))

    @jsii.member(jsii_name="putBuildStatusConfig")
    def put_build_status_config(
        self,
        *,
        context: typing.Optional[builtins.str] = None,
        target_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param context: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#context CodebuildProject#context}.
        :param target_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#target_url CodebuildProject#target_url}.
        '''
        value = CodebuildProjectSecondarySourcesBuildStatusConfig(
            context=context, target_url=target_url
        )

        return typing.cast(None, jsii.invoke(self, "putBuildStatusConfig", [value]))

    @jsii.member(jsii_name="putGitSubmodulesConfig")
    def put_git_submodules_config(
        self,
        *,
        fetch_submodules: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param fetch_submodules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#fetch_submodules CodebuildProject#fetch_submodules}.
        '''
        value = CodebuildProjectSecondarySourcesGitSubmodulesConfig(
            fetch_submodules=fetch_submodules
        )

        return typing.cast(None, jsii.invoke(self, "putGitSubmodulesConfig", [value]))

    @jsii.member(jsii_name="resetAuth")
    def reset_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuth", []))

    @jsii.member(jsii_name="resetBuildspec")
    def reset_buildspec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildspec", []))

    @jsii.member(jsii_name="resetBuildStatusConfig")
    def reset_build_status_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildStatusConfig", []))

    @jsii.member(jsii_name="resetGitCloneDepth")
    def reset_git_clone_depth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitCloneDepth", []))

    @jsii.member(jsii_name="resetGitSubmodulesConfig")
    def reset_git_submodules_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitSubmodulesConfig", []))

    @jsii.member(jsii_name="resetInsecureSsl")
    def reset_insecure_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecureSsl", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetReportBuildStatus")
    def reset_report_build_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReportBuildStatus", []))

    @builtins.property
    @jsii.member(jsii_name="auth")
    def auth(self) -> CodebuildProjectSecondarySourcesAuthOutputReference:
        return typing.cast(CodebuildProjectSecondarySourcesAuthOutputReference, jsii.get(self, "auth"))

    @builtins.property
    @jsii.member(jsii_name="buildStatusConfig")
    def build_status_config(
        self,
    ) -> CodebuildProjectSecondarySourcesBuildStatusConfigOutputReference:
        return typing.cast(CodebuildProjectSecondarySourcesBuildStatusConfigOutputReference, jsii.get(self, "buildStatusConfig"))

    @builtins.property
    @jsii.member(jsii_name="gitSubmodulesConfig")
    def git_submodules_config(
        self,
    ) -> CodebuildProjectSecondarySourcesGitSubmodulesConfigOutputReference:
        return typing.cast(CodebuildProjectSecondarySourcesGitSubmodulesConfigOutputReference, jsii.get(self, "gitSubmodulesConfig"))

    @builtins.property
    @jsii.member(jsii_name="authInput")
    def auth_input(self) -> typing.Optional[CodebuildProjectSecondarySourcesAuth]:
        return typing.cast(typing.Optional[CodebuildProjectSecondarySourcesAuth], jsii.get(self, "authInput"))

    @builtins.property
    @jsii.member(jsii_name="buildspecInput")
    def buildspec_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildspecInput"))

    @builtins.property
    @jsii.member(jsii_name="buildStatusConfigInput")
    def build_status_config_input(
        self,
    ) -> typing.Optional[CodebuildProjectSecondarySourcesBuildStatusConfig]:
        return typing.cast(typing.Optional[CodebuildProjectSecondarySourcesBuildStatusConfig], jsii.get(self, "buildStatusConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="gitCloneDepthInput")
    def git_clone_depth_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gitCloneDepthInput"))

    @builtins.property
    @jsii.member(jsii_name="gitSubmodulesConfigInput")
    def git_submodules_config_input(
        self,
    ) -> typing.Optional[CodebuildProjectSecondarySourcesGitSubmodulesConfig]:
        return typing.cast(typing.Optional[CodebuildProjectSecondarySourcesGitSubmodulesConfig], jsii.get(self, "gitSubmodulesConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureSslInput")
    def insecure_ssl_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureSslInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="reportBuildStatusInput")
    def report_build_status_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "reportBuildStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceIdentifierInput")
    def source_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="buildspec")
    def buildspec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildspec"))

    @buildspec.setter
    def buildspec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f5ca0197087711911e84822eb7757e7e5d0324f7a13f32aa0a4f3bdff27a67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildspec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gitCloneDepth")
    def git_clone_depth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gitCloneDepth"))

    @git_clone_depth.setter
    def git_clone_depth(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d2e3bbb8fcab12a78a1b898c6b17532759e9eb84a2b91a8f354c699adcc654c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitCloneDepth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insecureSsl")
    def insecure_ssl(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "insecureSsl"))

    @insecure_ssl.setter
    def insecure_ssl(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b6be904b60538607280b517312fa7f498e50ff3a6f94e54fd12eb65075d7722)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecureSsl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6633f23c28b9cfe38cf2f0febfd94d99cc25c0728cb76c34871e04b2d2b8c065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reportBuildStatus")
    def report_build_status(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "reportBuildStatus"))

    @report_build_status.setter
    def report_build_status(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc882301ec89f2dbb3ed02b8faab74778b4d42eb0a0107614598714288cdf09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reportBuildStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceIdentifier")
    def source_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceIdentifier"))

    @source_identifier.setter
    def source_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fadec5a0812345d034fced01b888f36a6fbeedc838e3d9f5f306f170e7d46a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f4a262a32b7c06b4e7cb1c8ac1e4c52cccd4e4538651bf3d949c984e792a403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectSecondarySources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectSecondarySources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectSecondarySources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e5b6099d40a021997a086e394e6317ca38db3612aeafc7bfca856668b08c292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSource",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "auth": "auth",
        "buildspec": "buildspec",
        "build_status_config": "buildStatusConfig",
        "git_clone_depth": "gitCloneDepth",
        "git_submodules_config": "gitSubmodulesConfig",
        "insecure_ssl": "insecureSsl",
        "location": "location",
        "report_build_status": "reportBuildStatus",
    },
)
class CodebuildProjectSource:
    def __init__(
        self,
        *,
        type: builtins.str,
        auth: typing.Optional[typing.Union["CodebuildProjectSourceAuth", typing.Dict[builtins.str, typing.Any]]] = None,
        buildspec: typing.Optional[builtins.str] = None,
        build_status_config: typing.Optional[typing.Union["CodebuildProjectSourceBuildStatusConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        git_clone_depth: typing.Optional[jsii.Number] = None,
        git_submodules_config: typing.Optional[typing.Union["CodebuildProjectSourceGitSubmodulesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        insecure_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        location: typing.Optional[builtins.str] = None,
        report_build_status: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.
        :param auth: auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#auth CodebuildProject#auth}
        :param buildspec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#buildspec CodebuildProject#buildspec}.
        :param build_status_config: build_status_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#build_status_config CodebuildProject#build_status_config}
        :param git_clone_depth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#git_clone_depth CodebuildProject#git_clone_depth}.
        :param git_submodules_config: git_submodules_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#git_submodules_config CodebuildProject#git_submodules_config}
        :param insecure_ssl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#insecure_ssl CodebuildProject#insecure_ssl}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#location CodebuildProject#location}.
        :param report_build_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#report_build_status CodebuildProject#report_build_status}.
        '''
        if isinstance(auth, dict):
            auth = CodebuildProjectSourceAuth(**auth)
        if isinstance(build_status_config, dict):
            build_status_config = CodebuildProjectSourceBuildStatusConfig(**build_status_config)
        if isinstance(git_submodules_config, dict):
            git_submodules_config = CodebuildProjectSourceGitSubmodulesConfig(**git_submodules_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60dea0af75f9450cba4e281f943ac4e69ba356f4d832c280d491fdc616612337)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
            check_type(argname="argument buildspec", value=buildspec, expected_type=type_hints["buildspec"])
            check_type(argname="argument build_status_config", value=build_status_config, expected_type=type_hints["build_status_config"])
            check_type(argname="argument git_clone_depth", value=git_clone_depth, expected_type=type_hints["git_clone_depth"])
            check_type(argname="argument git_submodules_config", value=git_submodules_config, expected_type=type_hints["git_submodules_config"])
            check_type(argname="argument insecure_ssl", value=insecure_ssl, expected_type=type_hints["insecure_ssl"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument report_build_status", value=report_build_status, expected_type=type_hints["report_build_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if auth is not None:
            self._values["auth"] = auth
        if buildspec is not None:
            self._values["buildspec"] = buildspec
        if build_status_config is not None:
            self._values["build_status_config"] = build_status_config
        if git_clone_depth is not None:
            self._values["git_clone_depth"] = git_clone_depth
        if git_submodules_config is not None:
            self._values["git_submodules_config"] = git_submodules_config
        if insecure_ssl is not None:
            self._values["insecure_ssl"] = insecure_ssl
        if location is not None:
            self._values["location"] = location
        if report_build_status is not None:
            self._values["report_build_status"] = report_build_status

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth(self) -> typing.Optional["CodebuildProjectSourceAuth"]:
        '''auth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#auth CodebuildProject#auth}
        '''
        result = self._values.get("auth")
        return typing.cast(typing.Optional["CodebuildProjectSourceAuth"], result)

    @builtins.property
    def buildspec(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#buildspec CodebuildProject#buildspec}.'''
        result = self._values.get("buildspec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_status_config(
        self,
    ) -> typing.Optional["CodebuildProjectSourceBuildStatusConfig"]:
        '''build_status_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#build_status_config CodebuildProject#build_status_config}
        '''
        result = self._values.get("build_status_config")
        return typing.cast(typing.Optional["CodebuildProjectSourceBuildStatusConfig"], result)

    @builtins.property
    def git_clone_depth(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#git_clone_depth CodebuildProject#git_clone_depth}.'''
        result = self._values.get("git_clone_depth")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def git_submodules_config(
        self,
    ) -> typing.Optional["CodebuildProjectSourceGitSubmodulesConfig"]:
        '''git_submodules_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#git_submodules_config CodebuildProject#git_submodules_config}
        '''
        result = self._values.get("git_submodules_config")
        return typing.cast(typing.Optional["CodebuildProjectSourceGitSubmodulesConfig"], result)

    @builtins.property
    def insecure_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#insecure_ssl CodebuildProject#insecure_ssl}.'''
        result = self._values.get("insecure_ssl")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#location CodebuildProject#location}.'''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def report_build_status(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#report_build_status CodebuildProject#report_build_status}.'''
        result = self._values.get("report_build_status")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSourceAuth",
    jsii_struct_bases=[],
    name_mapping={"resource": "resource", "type": "type"},
)
class CodebuildProjectSourceAuth:
    def __init__(self, *, resource: builtins.str, type: builtins.str) -> None:
        '''
        :param resource: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#resource CodebuildProject#resource}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1441f442f65aaa20cfe939b709958255762f051c5e5f49b8d12cdfb3b4c38b49)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource": resource,
            "type": type,
        }

    @builtins.property
    def resource(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#resource CodebuildProject#resource}.'''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectSourceAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectSourceAuthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSourceAuthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c585257d34ba0eab608085a44f2378db0a824ae8af4c7a87c52a63e8ad12402b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__529a6a170e59a09c3996b63bb5ad6bac4faf2eea75f3ab0d2dabbf194d8ce9d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2617c5e1c3d182531b2f7ec772f8f61352d28a31643ddc25a177bc7f5bab20a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CodebuildProjectSourceAuth]:
        return typing.cast(typing.Optional[CodebuildProjectSourceAuth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodebuildProjectSourceAuth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e785cbfff2a30d01c46a3f40a170a37917d41d6c87a9dcb4bb2682d25442b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSourceBuildStatusConfig",
    jsii_struct_bases=[],
    name_mapping={"context": "context", "target_url": "targetUrl"},
)
class CodebuildProjectSourceBuildStatusConfig:
    def __init__(
        self,
        *,
        context: typing.Optional[builtins.str] = None,
        target_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param context: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#context CodebuildProject#context}.
        :param target_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#target_url CodebuildProject#target_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59dc0128327ba9c292ca3a3b04d325b852d6f715dd77c8fdf7ea75edbbad327f)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument target_url", value=target_url, expected_type=type_hints["target_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if context is not None:
            self._values["context"] = context
        if target_url is not None:
            self._values["target_url"] = target_url

    @builtins.property
    def context(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#context CodebuildProject#context}.'''
        result = self._values.get("context")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#target_url CodebuildProject#target_url}.'''
        result = self._values.get("target_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectSourceBuildStatusConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectSourceBuildStatusConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSourceBuildStatusConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1db9b5809a72663c84139219e7c4c717262beb8d55aa74fa131f9c3c15020e13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContext")
    def reset_context(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContext", []))

    @jsii.member(jsii_name="resetTargetUrl")
    def reset_target_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="contextInput")
    def context_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextInput"))

    @builtins.property
    @jsii.member(jsii_name="targetUrlInput")
    def target_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "context"))

    @context.setter
    def context(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2bb9534ae82141e24f775b67a4d0fd1bbfe23dc72aa18c5291008302e0bc80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetUrl")
    def target_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetUrl"))

    @target_url.setter
    def target_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77a5c184073a18a90ab4f02aff10e861728a37fbc5577f9fb5115f210216c24e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodebuildProjectSourceBuildStatusConfig]:
        return typing.cast(typing.Optional[CodebuildProjectSourceBuildStatusConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodebuildProjectSourceBuildStatusConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9772cef88580791da98b981e80f5f813a1f80c0df3f5221192aa30e07e8068a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSourceGitSubmodulesConfig",
    jsii_struct_bases=[],
    name_mapping={"fetch_submodules": "fetchSubmodules"},
)
class CodebuildProjectSourceGitSubmodulesConfig:
    def __init__(
        self,
        *,
        fetch_submodules: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param fetch_submodules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#fetch_submodules CodebuildProject#fetch_submodules}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__656f95a20c176def450d1ca184469d3a9a16836593bf42e5641b8c22428d2677)
            check_type(argname="argument fetch_submodules", value=fetch_submodules, expected_type=type_hints["fetch_submodules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fetch_submodules": fetch_submodules,
        }

    @builtins.property
    def fetch_submodules(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#fetch_submodules CodebuildProject#fetch_submodules}.'''
        result = self._values.get("fetch_submodules")
        assert result is not None, "Required property 'fetch_submodules' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectSourceGitSubmodulesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectSourceGitSubmodulesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSourceGitSubmodulesConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b42d6cba84ae19b497051c11a3250c557ee7754eae4fddd9b542f358211e3502)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="fetchSubmodulesInput")
    def fetch_submodules_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchSubmodulesInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchSubmodules")
    def fetch_submodules(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchSubmodules"))

    @fetch_submodules.setter
    def fetch_submodules(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ce1cce101158cc6a97ca6f319fe42e86871a095f543790e43a19dd447cc96d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchSubmodules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodebuildProjectSourceGitSubmodulesConfig]:
        return typing.cast(typing.Optional[CodebuildProjectSourceGitSubmodulesConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodebuildProjectSourceGitSubmodulesConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adbe52de10c58a39f77e48435bba8eb69a03dd73d178db18814fdd16a037a4b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodebuildProjectSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cbc01a0dd105e1400d1e0c949fb58e4d008bdc90cf3ae842e64aa5dbd00e294)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuth")
    def put_auth(self, *, resource: builtins.str, type: builtins.str) -> None:
        '''
        :param resource: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#resource CodebuildProject#resource}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#type CodebuildProject#type}.
        '''
        value = CodebuildProjectSourceAuth(resource=resource, type=type)

        return typing.cast(None, jsii.invoke(self, "putAuth", [value]))

    @jsii.member(jsii_name="putBuildStatusConfig")
    def put_build_status_config(
        self,
        *,
        context: typing.Optional[builtins.str] = None,
        target_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param context: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#context CodebuildProject#context}.
        :param target_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#target_url CodebuildProject#target_url}.
        '''
        value = CodebuildProjectSourceBuildStatusConfig(
            context=context, target_url=target_url
        )

        return typing.cast(None, jsii.invoke(self, "putBuildStatusConfig", [value]))

    @jsii.member(jsii_name="putGitSubmodulesConfig")
    def put_git_submodules_config(
        self,
        *,
        fetch_submodules: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param fetch_submodules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#fetch_submodules CodebuildProject#fetch_submodules}.
        '''
        value = CodebuildProjectSourceGitSubmodulesConfig(
            fetch_submodules=fetch_submodules
        )

        return typing.cast(None, jsii.invoke(self, "putGitSubmodulesConfig", [value]))

    @jsii.member(jsii_name="resetAuth")
    def reset_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuth", []))

    @jsii.member(jsii_name="resetBuildspec")
    def reset_buildspec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildspec", []))

    @jsii.member(jsii_name="resetBuildStatusConfig")
    def reset_build_status_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildStatusConfig", []))

    @jsii.member(jsii_name="resetGitCloneDepth")
    def reset_git_clone_depth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitCloneDepth", []))

    @jsii.member(jsii_name="resetGitSubmodulesConfig")
    def reset_git_submodules_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitSubmodulesConfig", []))

    @jsii.member(jsii_name="resetInsecureSsl")
    def reset_insecure_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecureSsl", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetReportBuildStatus")
    def reset_report_build_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReportBuildStatus", []))

    @builtins.property
    @jsii.member(jsii_name="auth")
    def auth(self) -> CodebuildProjectSourceAuthOutputReference:
        return typing.cast(CodebuildProjectSourceAuthOutputReference, jsii.get(self, "auth"))

    @builtins.property
    @jsii.member(jsii_name="buildStatusConfig")
    def build_status_config(
        self,
    ) -> CodebuildProjectSourceBuildStatusConfigOutputReference:
        return typing.cast(CodebuildProjectSourceBuildStatusConfigOutputReference, jsii.get(self, "buildStatusConfig"))

    @builtins.property
    @jsii.member(jsii_name="gitSubmodulesConfig")
    def git_submodules_config(
        self,
    ) -> CodebuildProjectSourceGitSubmodulesConfigOutputReference:
        return typing.cast(CodebuildProjectSourceGitSubmodulesConfigOutputReference, jsii.get(self, "gitSubmodulesConfig"))

    @builtins.property
    @jsii.member(jsii_name="authInput")
    def auth_input(self) -> typing.Optional[CodebuildProjectSourceAuth]:
        return typing.cast(typing.Optional[CodebuildProjectSourceAuth], jsii.get(self, "authInput"))

    @builtins.property
    @jsii.member(jsii_name="buildspecInput")
    def buildspec_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildspecInput"))

    @builtins.property
    @jsii.member(jsii_name="buildStatusConfigInput")
    def build_status_config_input(
        self,
    ) -> typing.Optional[CodebuildProjectSourceBuildStatusConfig]:
        return typing.cast(typing.Optional[CodebuildProjectSourceBuildStatusConfig], jsii.get(self, "buildStatusConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="gitCloneDepthInput")
    def git_clone_depth_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gitCloneDepthInput"))

    @builtins.property
    @jsii.member(jsii_name="gitSubmodulesConfigInput")
    def git_submodules_config_input(
        self,
    ) -> typing.Optional[CodebuildProjectSourceGitSubmodulesConfig]:
        return typing.cast(typing.Optional[CodebuildProjectSourceGitSubmodulesConfig], jsii.get(self, "gitSubmodulesConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureSslInput")
    def insecure_ssl_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureSslInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="reportBuildStatusInput")
    def report_build_status_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "reportBuildStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="buildspec")
    def buildspec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildspec"))

    @buildspec.setter
    def buildspec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b2920a7c121da67d7011bbfff770e8104c528b251c04ba40c337bd550bbe4c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildspec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gitCloneDepth")
    def git_clone_depth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gitCloneDepth"))

    @git_clone_depth.setter
    def git_clone_depth(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dce497e52fbaa6f73f0c8533963d7254931590b08304794661dfdc6b39e07d7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitCloneDepth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insecureSsl")
    def insecure_ssl(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "insecureSsl"))

    @insecure_ssl.setter
    def insecure_ssl(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb61f931a8017431a0f10f25a83782aa2d98c7daf4fc07b80b61db765603d9bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecureSsl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__045dff1b15447a0fc43e35bda8bce371082770e61b4209b91aeab8ffc19ad952)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reportBuildStatus")
    def report_build_status(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "reportBuildStatus"))

    @report_build_status.setter
    def report_build_status(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3a80050c0907aca67a4442b01646e7373e363b4fd7209add0809801df1fcc54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reportBuildStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__834e77653a66a396c1378ef61583620682df3fd6e36b1b43ac1ef26b896dfc18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CodebuildProjectSource]:
        return typing.cast(typing.Optional[CodebuildProjectSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CodebuildProjectSource]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe72e77a30a763e84e8e818d09b51a97301f3b7de03186c3c5af3d30da6e0ffd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectVpcConfig",
    jsii_struct_bases=[],
    name_mapping={
        "security_group_ids": "securityGroupIds",
        "subnets": "subnets",
        "vpc_id": "vpcId",
    },
)
class CodebuildProjectVpcConfig:
    def __init__(
        self,
        *,
        security_group_ids: typing.Sequence[builtins.str],
        subnets: typing.Sequence[builtins.str],
        vpc_id: builtins.str,
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#security_group_ids CodebuildProject#security_group_ids}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#subnets CodebuildProject#subnets}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#vpc_id CodebuildProject#vpc_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caefb8b2a10a2e75f077907f23034e1510e157f33f156cb61cf93b2ae51bb5ca)
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "security_group_ids": security_group_ids,
            "subnets": subnets,
            "vpc_id": vpc_id,
        }

    @builtins.property
    def security_group_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#security_group_ids CodebuildProject#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        assert result is not None, "Required property 'security_group_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subnets(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#subnets CodebuildProject#subnets}.'''
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/codebuild_project#vpc_id CodebuildProject#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodebuildProjectVpcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodebuildProjectVpcConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.codebuildProject.CodebuildProjectVpcConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e1be631a1d2c8cf4e8a028bb3289dcc681538cf385eb61f4e90de4a7403f20c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetsInput")
    def subnets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__471c12b5375fc6c7cfbfcd705b0900a22d9bf1af8f91d402504b9561d1466630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnets"))

    @subnets.setter
    def subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e6037e9545733fcbbfc636edd57b00a4d5bd03c168ee4eaf8bcfc23ad848af5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6df28c1898d16f55bdde5e384b798dccdd68fb8ec0f9035dd38ae4644dd0f3c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CodebuildProjectVpcConfig]:
        return typing.cast(typing.Optional[CodebuildProjectVpcConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CodebuildProjectVpcConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ee3abc6bcd1acf62cd0d7b3bad15d8ed6d7bbb56ac7c019fe3f6ca42edfeda2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CodebuildProject",
    "CodebuildProjectArtifacts",
    "CodebuildProjectArtifactsOutputReference",
    "CodebuildProjectBuildBatchConfig",
    "CodebuildProjectBuildBatchConfigOutputReference",
    "CodebuildProjectBuildBatchConfigRestrictions",
    "CodebuildProjectBuildBatchConfigRestrictionsOutputReference",
    "CodebuildProjectCache",
    "CodebuildProjectCacheOutputReference",
    "CodebuildProjectConfig",
    "CodebuildProjectEnvironment",
    "CodebuildProjectEnvironmentDockerServer",
    "CodebuildProjectEnvironmentDockerServerOutputReference",
    "CodebuildProjectEnvironmentEnvironmentVariable",
    "CodebuildProjectEnvironmentEnvironmentVariableList",
    "CodebuildProjectEnvironmentEnvironmentVariableOutputReference",
    "CodebuildProjectEnvironmentFleet",
    "CodebuildProjectEnvironmentFleetOutputReference",
    "CodebuildProjectEnvironmentOutputReference",
    "CodebuildProjectEnvironmentRegistryCredential",
    "CodebuildProjectEnvironmentRegistryCredentialOutputReference",
    "CodebuildProjectFileSystemLocations",
    "CodebuildProjectFileSystemLocationsList",
    "CodebuildProjectFileSystemLocationsOutputReference",
    "CodebuildProjectLogsConfig",
    "CodebuildProjectLogsConfigCloudwatchLogs",
    "CodebuildProjectLogsConfigCloudwatchLogsOutputReference",
    "CodebuildProjectLogsConfigOutputReference",
    "CodebuildProjectLogsConfigS3Logs",
    "CodebuildProjectLogsConfigS3LogsOutputReference",
    "CodebuildProjectSecondaryArtifacts",
    "CodebuildProjectSecondaryArtifactsList",
    "CodebuildProjectSecondaryArtifactsOutputReference",
    "CodebuildProjectSecondarySourceVersion",
    "CodebuildProjectSecondarySourceVersionList",
    "CodebuildProjectSecondarySourceVersionOutputReference",
    "CodebuildProjectSecondarySources",
    "CodebuildProjectSecondarySourcesAuth",
    "CodebuildProjectSecondarySourcesAuthOutputReference",
    "CodebuildProjectSecondarySourcesBuildStatusConfig",
    "CodebuildProjectSecondarySourcesBuildStatusConfigOutputReference",
    "CodebuildProjectSecondarySourcesGitSubmodulesConfig",
    "CodebuildProjectSecondarySourcesGitSubmodulesConfigOutputReference",
    "CodebuildProjectSecondarySourcesList",
    "CodebuildProjectSecondarySourcesOutputReference",
    "CodebuildProjectSource",
    "CodebuildProjectSourceAuth",
    "CodebuildProjectSourceAuthOutputReference",
    "CodebuildProjectSourceBuildStatusConfig",
    "CodebuildProjectSourceBuildStatusConfigOutputReference",
    "CodebuildProjectSourceGitSubmodulesConfig",
    "CodebuildProjectSourceGitSubmodulesConfigOutputReference",
    "CodebuildProjectSourceOutputReference",
    "CodebuildProjectVpcConfig",
    "CodebuildProjectVpcConfigOutputReference",
]

publication.publish()

def _typecheckingstub__1e635c728797e9d93bc57ba8c75d88f714e52b834b14417ad24b50d08d732d6e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    artifacts: typing.Union[CodebuildProjectArtifacts, typing.Dict[builtins.str, typing.Any]],
    environment: typing.Union[CodebuildProjectEnvironment, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    service_role: builtins.str,
    source: typing.Union[CodebuildProjectSource, typing.Dict[builtins.str, typing.Any]],
    auto_retry_limit: typing.Optional[jsii.Number] = None,
    badge_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    build_batch_config: typing.Optional[typing.Union[CodebuildProjectBuildBatchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    build_timeout: typing.Optional[jsii.Number] = None,
    cache: typing.Optional[typing.Union[CodebuildProjectCache, typing.Dict[builtins.str, typing.Any]]] = None,
    concurrent_build_limit: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    file_system_locations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodebuildProjectFileSystemLocations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    logs_config: typing.Optional[typing.Union[CodebuildProjectLogsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project_visibility: typing.Optional[builtins.str] = None,
    queued_timeout: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    resource_access_role: typing.Optional[builtins.str] = None,
    secondary_artifacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodebuildProjectSecondaryArtifacts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    secondary_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodebuildProjectSecondarySources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    secondary_source_version: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodebuildProjectSecondarySourceVersion, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc_config: typing.Optional[typing.Union[CodebuildProjectVpcConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__80c2a79cf03f863fa328ebf13d0d166e00c554ae19c88c31d4577d7f9b86a4cd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efea8faea33f7db5f59ffd4f7bb5370a4ad5ded6b99e0a2ffdd6ced06d4f3486(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodebuildProjectFileSystemLocations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9311bd2758106d5da7378bc8cf4e7fb6f67d3f2cc7b36dbfff2c2eb64044e760(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodebuildProjectSecondaryArtifacts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4378878fc54ae99bef184f22186dab27c4b7a7efde78ccfc896228a2a0fac7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodebuildProjectSecondarySources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b454117aedb5b3bd73404d8f759a629c5a38b9c47f3b610591f975dfe02b13(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodebuildProjectSecondarySourceVersion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b63dbea74c44b413d8b7a9486b6a7615a7c3f06f2d4ca87f5567e8deeaf231(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd9f66ca0f09eda9758cf23e157c56ceef0499ae86b2b0e1e7eea4a062b6ff5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585aee88331322cd11b9a6e35bf3f6df7963f2ff679c9ac1084ad1312c3438d4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7143b8f47ab5b76d468fa003920a85b68c8422818db506f07f5b244c35c85b8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc378072c8f825cb20310465f6e860f3ef1de3b3a5dc20ea9d42b065300d82a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc067b4383ae988440974a7254f86ed2c2fe1e1b0ab2ce9a92e373d76b6c8ea9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca9e625e2a19b50c2858daf982ecb67566808a1082984511e62d1e8e31d4cfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0744de8cb6fc0b0fc38070d5e21e681054f163202c033ad6c2af90b9cbf08e76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e941585937ba258d1dbff3d8827a5ea1558b9b920d0f8759874d9b3b4d2dd8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce2866ec4818709e5fcd3d6c1c896006cfb4f5a25e27a714fe18fea8f2724aed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7519e969b5e007f30572528c6e83359b93711b58a8ebf4e95bdd0761cbeba4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e04e3e3f195b1148c33246b826643c387f10fa1307125383e61021c3bface7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de086bd003e44f3a73d6c76b0172aa06c9852f95be9a448c8a68fdc70952f73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda1ce33304aba369dba9ef92363a0ef7ac7d73dafe4df98f9e4a02bd68cc033(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa43788d8b1be61344948501cadf986eda1f94373e35b196256c68073077a06(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ffee8f06d6d785208d9a463a9fbf05fdfffdbd1109d20d9a0195bba983f23c7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367c68db7701463b58dbd741bf2047d160603865f81ed6437e94655a53b9ef0a(
    *,
    type: builtins.str,
    artifact_identifier: typing.Optional[builtins.str] = None,
    bucket_owner_access: typing.Optional[builtins.str] = None,
    encryption_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    namespace_type: typing.Optional[builtins.str] = None,
    override_artifact_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    packaging: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58ff103ac66e5d4e845cc4fbed4d7bc6da504f0bdd8672c1b3f4b98beffe60e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be5cd18789e47935551a874c9b64588007c27c6bbc55e46dc25a8c8398227648(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff539a2ea34398296fd6e5bec1354910a03b3395d5d2a5b8273dc692610feb94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29d8f1ac1b7f0a51a37d1c4f0bfcd5a916e0bfe954f52de67d83c82e968707f1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adefcb518c22b6588473798d5e370fdaaf929c73661134bdf84a551c4447db1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d02240a1a15f6a87affdb351123db7de077ae058642dbb17cf89cd773a6baf80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f055a113a306a4c14ab31be8d16a596b10e9961f01b1721a6b1b204958ba8c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__658d34651b65c75435178e3b24dbef8301f2d7a22ba24d2a5ffd305804b1247c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a346d17abab5af2d3bb347d63f1b07057648639c310927d2502d0e92f4c300ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40287970ea6f38a2c1722f7d0962c3f7bd15345a8e7e5208f5e602e360083f6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35dc077252154f384978e1fa79ffae5a4f2689df20e72dfa54ff1e26412032d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8e548f6ee8ab577e0e5eb0a48b33ca7927c1a7c4ae526c49a50f22d5b473ce(
    value: typing.Optional[CodebuildProjectArtifacts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c4cabd621704978ae24bba751edf0dbf039034619aa5f97fc6493625d806c9e(
    *,
    service_role: builtins.str,
    combine_artifacts: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restrictions: typing.Optional[typing.Union[CodebuildProjectBuildBatchConfigRestrictions, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_in_mins: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73ac71b336da06fbbc87e683a43936cfc8aa206a2879af51a23f0de56cbfc28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bca3737457adb2221b1fb2767b0944ef94061ea8af27c4d5c8ebd976807a371(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1c2123bbe106808f790b5a9490256e5f3f1c843d26f3a061ddeab85698b803f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a324c807f7fd5cc268cd74837042310e48e06b9fb604fb794525ad97aaf1735(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467288dc4e4f0bcac92c2b65d3d1ad921cbe331dbe7ff1e5dadacbb68ac5c2ab(
    value: typing.Optional[CodebuildProjectBuildBatchConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5803e660d212afaa9e9e7fe5ca1067bc9119b67c9779e25dfdb7404829da1b99(
    *,
    compute_types_allowed: typing.Optional[typing.Sequence[builtins.str]] = None,
    maximum_builds_allowed: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbdc7e4e3a4c2f2f60656800ee2520eeea2d4720991468f82695d3f7d1aa7096(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca82e62f891da80e30f2bd094e77c5e34c82445b169f42dc5dd31011fc1c445b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d2be1fcc13bfd79601b806ca6f5df703fcb4ee9ae960cc8fb972c09ee709de2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c909e4b2a2bdc73f4ba3d48aa61b66e9112f56221903e677404074586e1141(
    value: typing.Optional[CodebuildProjectBuildBatchConfigRestrictions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2ed786da98726b28b45fd9644570ba5fbf776e60249d5518b4de8f3ff484710(
    *,
    cache_namespace: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    modes: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bcc2a24921ec4ac3d2e10c1024eb0a19cc05615eea2d9a615384f016ade05c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44567c77923ac8311036b67f1f733e2522930908c86a1fcaa4b5a30758ccf4d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0947fb2d092f78c4ded9965a382295cb593ea2ccf1dc6c7a5e0c21e62d1e785(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24dd73c09a857f9dbe39b0aeb9bbf17e2f899cef2d5bf7026a9b73345332eba5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca06f3fb9ab37a09ce3e3ec43e72f1f9be354af430778383e07872b62dac6553(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a12152939335ec46e3efbd783b8e015154f64f0617900cbcfdd364e9ac968464(
    value: typing.Optional[CodebuildProjectCache],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7d66f42f49ba671e9db03c7f520fdd509c7ad961970b7f6d95ba05a09be328(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    artifacts: typing.Union[CodebuildProjectArtifacts, typing.Dict[builtins.str, typing.Any]],
    environment: typing.Union[CodebuildProjectEnvironment, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    service_role: builtins.str,
    source: typing.Union[CodebuildProjectSource, typing.Dict[builtins.str, typing.Any]],
    auto_retry_limit: typing.Optional[jsii.Number] = None,
    badge_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    build_batch_config: typing.Optional[typing.Union[CodebuildProjectBuildBatchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    build_timeout: typing.Optional[jsii.Number] = None,
    cache: typing.Optional[typing.Union[CodebuildProjectCache, typing.Dict[builtins.str, typing.Any]]] = None,
    concurrent_build_limit: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    file_system_locations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodebuildProjectFileSystemLocations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    logs_config: typing.Optional[typing.Union[CodebuildProjectLogsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project_visibility: typing.Optional[builtins.str] = None,
    queued_timeout: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    resource_access_role: typing.Optional[builtins.str] = None,
    secondary_artifacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodebuildProjectSecondaryArtifacts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    secondary_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodebuildProjectSecondarySources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    secondary_source_version: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodebuildProjectSecondarySourceVersion, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc_config: typing.Optional[typing.Union[CodebuildProjectVpcConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c54475e4262ccd7c534e789e96384cc7c8204715e868718c53ed5be2139e9c4(
    *,
    compute_type: builtins.str,
    image: builtins.str,
    type: builtins.str,
    certificate: typing.Optional[builtins.str] = None,
    docker_server: typing.Optional[typing.Union[CodebuildProjectEnvironmentDockerServer, typing.Dict[builtins.str, typing.Any]]] = None,
    environment_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodebuildProjectEnvironmentEnvironmentVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    fleet: typing.Optional[typing.Union[CodebuildProjectEnvironmentFleet, typing.Dict[builtins.str, typing.Any]]] = None,
    image_pull_credentials_type: typing.Optional[builtins.str] = None,
    privileged_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    registry_credential: typing.Optional[typing.Union[CodebuildProjectEnvironmentRegistryCredential, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1adee899118d3b1836a8dd3ed3577416bcbdbac4dc2bc058931a05b8df39655(
    *,
    compute_type: builtins.str,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69cad0aa1264e14ea522999c80fa71dc55702efdedef884cde88804ec177cc34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807b897a3daaf00ad948876f8eaa95c5b04e0954e68bb3b9763ac6a873083cd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793464acf36973bddd00997bd4912443dd1a107ca77a3bdd787c228a8ad580eb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f837b374e4dbd5d62938f7d0cf3c799c67490d3cbe612432310dc2df8c76505(
    value: typing.Optional[CodebuildProjectEnvironmentDockerServer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c43517826bd4a8e0305a9ddd654e8182c1da8079d67aa2408a3ff1783ccb39b(
    *,
    name: builtins.str,
    value: builtins.str,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__104223f325d364c3a9d17ab248a91027cee22624ccc009e1aa31f6fada641200(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a40b143e842210110a27210605b429587d793805a7cc7fb10d93bb7f4c6e5b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35392f577670fc87c8cd1634d4f5d9a754a77efcd54920a2606cd203f4cd05fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad767b60c99263391bcc93e57e06c01f551d2ea8d6192276c87d033d766eea3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4120d6e1aff491698dc5d785fa3525a8064390aaf8fdd8484969dd9450a3f749(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83cb412a5edb3bf96def113692ec0e44e14de7b93bf21da125d6d49542b36d6b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectEnvironmentEnvironmentVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b96035234318835cf559f02ce8ef60039d78eec7fee7f83a72afd14c9f673c51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae37313c7c6c9321c23b5d1f0c02565f0c65ef877e90e46307dfa85325dd444(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc68bd37dc173a95d160f5f9986e18d9693b1974ab3b32dc3b2188127bad120(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557077950d51482bfcdf48caf00eadf8bf7635710559e633dd44a593e5b48d3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e63ccde55938d3bffe3e327c623a662afb53ab073285c8e93fb1eae1f50796(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectEnvironmentEnvironmentVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c18bf4cc9cb059de67accb3f6c9f3ca411f90daf0cef2f9c75f9c22e56edc86b(
    *,
    fleet_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8dfb21b5642e3888493b8eeed12861e0e05332d620333c252a22a75e80b4ff7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60812a27c6fa89b05fdc19cc2459aaabb4cafc01bd01457cf163477327e6c3d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7378347325eef2cbfbf1547ee22a0884b4dbcfcbc76bd22ec255508205fc5d6(
    value: typing.Optional[CodebuildProjectEnvironmentFleet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f896f3fa34a120886702f8328592ae24eed3c0544406dc9d32124f6ee7f9eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81fe24e99ddf72ea5b13ab09e8fd2faef33d5aa9fcdef9c820cbbfc77b67278b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodebuildProjectEnvironmentEnvironmentVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f8145222bed4871cf47477399120992171d3bfa7460db071f090c61b1f0d18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a5e083a7c2f3f7a1d5021434bdebba6777ad5b784ba2e3fdfb174886e235be5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9b1f0a738dca4e2f8c92a32f3fd6537486480a2db36309af209fbfd21b1bb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb91fdeb106e3b53a196e7b6bde43c8bf260ac2b4943f6310c565b525245dba7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__620d1fa94b532acc85f40868bbefe16f48830e0fa306ea6042c91cbe9b126b1f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4752dc13d217593e137c8264f968eff9d7f538ede46dc3647902ec943a801869(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d42622debae3b34179b9c0bae588fdfe000bdf75d6519a0d7d2a38a9312be77(
    value: typing.Optional[CodebuildProjectEnvironment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6deec6f18e65734f0767d81dc837537ca6431a5adf20d53c19080089b33c7e2(
    *,
    credential: builtins.str,
    credential_provider: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77428e21e32ac09ae620c1f4126a427aa82184be5ce798b0288e830515c8166d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81896d43703251509e8cef556b7f4f75ceedfbd52156ef8f6087fb606ac0d4d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__100939022f49a80259c4c9a76cd4faff412f7c7cdb09c1f1be98b5f89f6656c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e5a34101ec926319934c60e5a294478b5827d5609a2874c7d0f65d4d82cba1(
    value: typing.Optional[CodebuildProjectEnvironmentRegistryCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d445b44cf48bf0c774f8d26ca66eef0d5af059484995e733296c071e0f22eccd(
    *,
    identifier: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    mount_options: typing.Optional[builtins.str] = None,
    mount_point: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6897c3c0f278bcd7cc6f5bb6f293b6b2fd1f8e2e6d009f3cfd8b0c181e8d14c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba0f84a66f64713b220e07eb8fe1b704c1f8bd92bc733998d1de4bd691e83ac3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b49b5030ac131d2681e6856a96cc0800957fe2986d71e9b8aa244aed28e5c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1289d0c9fd60c75cb9447c967950b6e6a0833ecb61aa2061966f65beeb68871(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e085b49f91b93f6ef97667c0db12882d742a853ebe188145711921a46bc7e793(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c3f850fe869748bfd33a12e6b4c7cfb71ae3cf2893f4513d06fd02c7af69b5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectFileSystemLocations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f327ed1a951bb018e619fe899a3e27cc2bcc48f75240be6c62e8a890ae0166(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6979c7466b3e85470ff25e6d4633e37ef7c0a4740ac5f2d106350419cfb601e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97d5f31c62aa4d8208df351cf39ba68075047a418c9b0708b25e9c62cc7ed01d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7571cad55600038cafd9e0dc63529119707a8996f8902c4a110cb88636d6dfdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da696801b25aebafa575b7417510af9f383ab10a73ba4bbc543c374cf945b715(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e10df9d55316b4e62c5ba4e8f10862fced41b721d814a5c185e6d61f7099c75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df655a13a5401681ea3ed06da57e90298552b3281315860c43a13fa23dc75737(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectFileSystemLocations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a50a885337922104c9c2d41fea26b09b4bc188e3c3029046076aa83746483e16(
    *,
    cloudwatch_logs: typing.Optional[typing.Union[CodebuildProjectLogsConfigCloudwatchLogs, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_logs: typing.Optional[typing.Union[CodebuildProjectLogsConfigS3Logs, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ce9a8cacb5b15fc2921c1c6f38eabe183a4405c786b5b41a5cb7ac83013a87(
    *,
    group_name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5328e281c32eb53221ce1dfca88037919aae3ca3fb959e901f82e7dcc5be425(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a503f03b59dcb704621450163c252dd0bfe543f68283202e5e8feebb3d2d23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be999bb9b0a41efe96068e4ed81da9d10701ab706e7397f3f0556102b96dea3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701f863321d47853026ecee6ccaa9dbcac4a72f765c0486806883a5f57511d4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78eb559b6f34cb332acead3acdb393a3ca8bdfa73f06f881a6de21fa1289f259(
    value: typing.Optional[CodebuildProjectLogsConfigCloudwatchLogs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86dd660310c53cf510fe5824a265b0bde374d73c2fe1ca9926c0177ab1822443(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e2c6ee8ea517c54042ec5bf236a7f9449cf305b8808025b094e45612cb76b2(
    value: typing.Optional[CodebuildProjectLogsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ecb150279926621f0a3c1cb804c98b559aaa735bd9d68a923a2925938c078f(
    *,
    bucket_owner_access: typing.Optional[builtins.str] = None,
    encryption_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    location: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66f4a0fe7509d1d2d9f780cfebb790706f71b386826c68e0cbc49e3fd6bb6ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091270440cc5d178757fd2443224daaa658b0315cadee77a0aba1e319052b68f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66b67225131d11ec66f9f6b143d8851fe234eea882b846dffed2b37e67ee0f1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e6fc8264af4b6a6e77785f8ba54fc6c678410d35610b25cedbc54cab5bba7c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc0aa56e36a81a0c65733441a8e62f980adf6b88c78a47d94f877d902bf503d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ab1914a2de8e39d23275578c5d9245435b19cfa2052bf8245f86b65dddf84c(
    value: typing.Optional[CodebuildProjectLogsConfigS3Logs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e948569a1479a8aca3b95b2ddd1f42cf365db9a2aa82e7cba65715dc45a83af7(
    *,
    artifact_identifier: builtins.str,
    type: builtins.str,
    bucket_owner_access: typing.Optional[builtins.str] = None,
    encryption_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    namespace_type: typing.Optional[builtins.str] = None,
    override_artifact_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    packaging: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c40d9175da38c9cd632945f967f5f5e87cd3ff21523292b8817296bbf7f537(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109b02dc3e6b8c33bfcca9b5cbd9d9634f2a8046d576518b055a165ff8783418(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89cfc1221e7e7ae8ca178b274760f62479b05a696060ba20ee6c701bd324d19a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d11300da1ced62838a3b943894330e03a9d0d6ff41a377cccb084647c80d435(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61870e099675d36adf96edf2372dede4aaea06fe36c9f178f4fb2bff99a3adf5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3453f3975dd2cb45545c97fcbf438e14c450f78a3605632cdd857016e4e5be7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectSecondaryArtifacts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__671ef36202c69481d7c6cd2680ef83c0b6ebba6c2354b97eed4140820ef0e94c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c68595c9a17e1b42908b20a6726ee176c03a111e826f5f25da65dcccb6cc23a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e8f01c4f56eef00885737b632d3652a3e2189cb889e5cc4818b5f647bcda67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa1cc66ed4b8d83a262e37ddfd3371241be83171da01106af2c3999fdbaf76f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7b27e9e6896d752d9300741abb772e4b409eb5b993a741278a2280bab91801(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69fc28bfbb4e8ebb5533a052cd8eca4b6ea07f4211112b93897fa0ee4a8c99d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c82484553d9c8f2c630b1ae69e17071609b8804f95b08644f4b21bd2caf7fd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d4193a8f767105e182b2d306c6c71f1f1d99dd157756a86a458827170af6167(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__531f065410f50b70ea0b1898b23b972d6899c386d8f1aca53d9d686c559d9d79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__987374ca934de8b6af5cd8a2e3b4fde8e52fefa586220578fa5571980bdadf10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e13590f321762f8d39a14aac79cb571782d21190e286285e6268f37622a282(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c4939d9d1c2e13fd2dff7355315caf203c5014619955cac40fd4961ae98c50(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectSecondaryArtifacts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__414193f01d464365535e1fb562af95f517845115f22519c56efcffb81405da7e(
    *,
    source_identifier: builtins.str,
    source_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9eb156e2e59010e8bf5f1d00ad7f06c91defef179ea7516929c35cdd3c76766(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ea704b91248e4e15371ef0cd3741e57f22ef6ff10eb7b5abcf4846f03a04bc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e6de5532beaafc4c4e152a67703489089a03a91f725d24c74a2b3de19e51ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc202a2a792c2cecb4210977606b7cb7dae7418d83d9e2975598ce6859ccbd5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dae486652a2452d84e4dd220acd8f5b8542e4e224fa51f5c623cdfd68a51fa0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f9477c9d9050a98a55a49fd0fb03bb717da8b9c6ed4fa080b4f8b325b09e83(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectSecondarySourceVersion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8888ea638ed48518d2753b69c01caec2f251da212593c1ab3b929f51bf0724d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5cd674d04c5f6eb7e78aaf94e100d190376e6e68183c0d54399e9cb94b40ab1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf62f2e05bf9f425a771ba00eb6fac602c81f3d78e66d7e9ac257df64c92e6e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2946f0c9a774b0ba11b5237a5f8db8a1def9d60ace972ec75f41a0524ccb3865(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectSecondarySourceVersion]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b7ff432626ebb901a6c5ac2e06bff4d0ced4af02f40f58b37341eb082e2b74(
    *,
    source_identifier: builtins.str,
    type: builtins.str,
    auth: typing.Optional[typing.Union[CodebuildProjectSecondarySourcesAuth, typing.Dict[builtins.str, typing.Any]]] = None,
    buildspec: typing.Optional[builtins.str] = None,
    build_status_config: typing.Optional[typing.Union[CodebuildProjectSecondarySourcesBuildStatusConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    git_clone_depth: typing.Optional[jsii.Number] = None,
    git_submodules_config: typing.Optional[typing.Union[CodebuildProjectSecondarySourcesGitSubmodulesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    insecure_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    location: typing.Optional[builtins.str] = None,
    report_build_status: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0446230067839efc8c9d36fb7ba2f149c4c5d9801ee024bc6ace3660ef685f03(
    *,
    resource: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__800170204b762563a971f6c953d46e1eb8bd1c3214e3d2697524488049b68dea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3369a24ebf3f79b8000388703c9b3e2ac313f0ad69fccb4a64ddfa5bbb0747f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2ac8fb2dd505ca826407b5abbe1700ff4b356b2212cfe266320af4a3aa437f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f5d90a4ced4212e7b29f70be1dc17dca94177e0e0de4198e81676d18686d7e(
    value: typing.Optional[CodebuildProjectSecondarySourcesAuth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a48b394b69179de3d7f5510175f12b3e76bf944db640af8a4549fceb06a65d7(
    *,
    context: typing.Optional[builtins.str] = None,
    target_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c686f390d536847e200e850676a7b9e78e309026f23407c852dca8390734993d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c22fa002302ddb997c0163ec182ba3cc42be3c1f792cfdbf8453d9b4762b5d80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37e0b440a77b45483d877c858ce030ff4e5ade1d4802916b5b4668668c5f0f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60cd5d41d32de5878216619a461a4b495bad3a1f90f3791bf682f379a0693c60(
    value: typing.Optional[CodebuildProjectSecondarySourcesBuildStatusConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3832849a463c1cedc830a0047a47c5835ea368bf7bb308d544fc9c4844f6f31(
    *,
    fetch_submodules: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65af3654ef5e7fbaf06fb174625316f42373e72eb2e5b6d4927e33922a6736a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b79fb6ffb5be8974010bd7d7c467e099f5f78ffa1443a44e7b50168c9825d449(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c6fca07118de6c8e5c323655b10584132ceb54787e13221fc3f54145e064a01(
    value: typing.Optional[CodebuildProjectSecondarySourcesGitSubmodulesConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b1f28badc89ea32d13011c50a0ad266df1452e7b5b6625f96f3f15fd43bbe16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90a8824ae53597d802c7ab0519048639243db55f9f3c729ad5705d2d48e50dc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6d800bd2496c5797e2e4104045544399a69d7003f286842bc7e0dd936c1b65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c07f64899b6b4dc50c17929768fa6b7ca67a6e3c497450bb1d5ead0ba75a0a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a1e9b4d099d1d4a9d922312fbfb9c2d5ec35a5d0fa4291aeaa8de63141a06f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79092f990c12292a301dafc70a7fca013bb14a5b737c7ec248f2f7fb6ed92bd0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodebuildProjectSecondarySources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3fca9d04a04f8fac26ebf16af649e7b20befd19d7c6118b06295fe5b97fe7c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f5ca0197087711911e84822eb7757e7e5d0324f7a13f32aa0a4f3bdff27a67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d2e3bbb8fcab12a78a1b898c6b17532759e9eb84a2b91a8f354c699adcc654c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6be904b60538607280b517312fa7f498e50ff3a6f94e54fd12eb65075d7722(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6633f23c28b9cfe38cf2f0febfd94d99cc25c0728cb76c34871e04b2d2b8c065(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc882301ec89f2dbb3ed02b8faab74778b4d42eb0a0107614598714288cdf09(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fadec5a0812345d034fced01b888f36a6fbeedc838e3d9f5f306f170e7d46a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4a262a32b7c06b4e7cb1c8ac1e4c52cccd4e4538651bf3d949c984e792a403(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e5b6099d40a021997a086e394e6317ca38db3612aeafc7bfca856668b08c292(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodebuildProjectSecondarySources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60dea0af75f9450cba4e281f943ac4e69ba356f4d832c280d491fdc616612337(
    *,
    type: builtins.str,
    auth: typing.Optional[typing.Union[CodebuildProjectSourceAuth, typing.Dict[builtins.str, typing.Any]]] = None,
    buildspec: typing.Optional[builtins.str] = None,
    build_status_config: typing.Optional[typing.Union[CodebuildProjectSourceBuildStatusConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    git_clone_depth: typing.Optional[jsii.Number] = None,
    git_submodules_config: typing.Optional[typing.Union[CodebuildProjectSourceGitSubmodulesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    insecure_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    location: typing.Optional[builtins.str] = None,
    report_build_status: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1441f442f65aaa20cfe939b709958255762f051c5e5f49b8d12cdfb3b4c38b49(
    *,
    resource: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c585257d34ba0eab608085a44f2378db0a824ae8af4c7a87c52a63e8ad12402b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__529a6a170e59a09c3996b63bb5ad6bac4faf2eea75f3ab0d2dabbf194d8ce9d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2617c5e1c3d182531b2f7ec772f8f61352d28a31643ddc25a177bc7f5bab20a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e785cbfff2a30d01c46a3f40a170a37917d41d6c87a9dcb4bb2682d25442b9(
    value: typing.Optional[CodebuildProjectSourceAuth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59dc0128327ba9c292ca3a3b04d325b852d6f715dd77c8fdf7ea75edbbad327f(
    *,
    context: typing.Optional[builtins.str] = None,
    target_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db9b5809a72663c84139219e7c4c717262beb8d55aa74fa131f9c3c15020e13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2bb9534ae82141e24f775b67a4d0fd1bbfe23dc72aa18c5291008302e0bc80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a5c184073a18a90ab4f02aff10e861728a37fbc5577f9fb5115f210216c24e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9772cef88580791da98b981e80f5f813a1f80c0df3f5221192aa30e07e8068a7(
    value: typing.Optional[CodebuildProjectSourceBuildStatusConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__656f95a20c176def450d1ca184469d3a9a16836593bf42e5641b8c22428d2677(
    *,
    fetch_submodules: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42d6cba84ae19b497051c11a3250c557ee7754eae4fddd9b542f358211e3502(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce1cce101158cc6a97ca6f319fe42e86871a095f543790e43a19dd447cc96d6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adbe52de10c58a39f77e48435bba8eb69a03dd73d178db18814fdd16a037a4b2(
    value: typing.Optional[CodebuildProjectSourceGitSubmodulesConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbc01a0dd105e1400d1e0c949fb58e4d008bdc90cf3ae842e64aa5dbd00e294(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2920a7c121da67d7011bbfff770e8104c528b251c04ba40c337bd550bbe4c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce497e52fbaa6f73f0c8533963d7254931590b08304794661dfdc6b39e07d7d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb61f931a8017431a0f10f25a83782aa2d98c7daf4fc07b80b61db765603d9bc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045dff1b15447a0fc43e35bda8bce371082770e61b4209b91aeab8ffc19ad952(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a80050c0907aca67a4442b01646e7373e363b4fd7209add0809801df1fcc54(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834e77653a66a396c1378ef61583620682df3fd6e36b1b43ac1ef26b896dfc18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe72e77a30a763e84e8e818d09b51a97301f3b7de03186c3c5af3d30da6e0ffd(
    value: typing.Optional[CodebuildProjectSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caefb8b2a10a2e75f077907f23034e1510e157f33f156cb61cf93b2ae51bb5ca(
    *,
    security_group_ids: typing.Sequence[builtins.str],
    subnets: typing.Sequence[builtins.str],
    vpc_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1be631a1d2c8cf4e8a028bb3289dcc681538cf385eb61f4e90de4a7403f20c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471c12b5375fc6c7cfbfcd705b0900a22d9bf1af8f91d402504b9561d1466630(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e6037e9545733fcbbfc636edd57b00a4d5bd03c168ee4eaf8bcfc23ad848af5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df28c1898d16f55bdde5e384b798dccdd68fb8ec0f9035dd38ae4644dd0f3c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee3abc6bcd1acf62cd0d7b3bad15d8ed6d7bbb56ac7c019fe3f6ca42edfeda2(
    value: typing.Optional[CodebuildProjectVpcConfig],
) -> None:
    """Type checking stubs"""
    pass
