r'''
# `aws_lambda_function`

Refer to the Terraform Registry for docs: [`aws_lambda_function`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function).
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


class LambdaFunction(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunction",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function aws_lambda_function}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        function_name: builtins.str,
        role: builtins.str,
        architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
        capacity_provider_config: typing.Optional[typing.Union["LambdaFunctionCapacityProviderConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        code_sha256: typing.Optional[builtins.str] = None,
        code_signing_config_arn: typing.Optional[builtins.str] = None,
        dead_letter_config: typing.Optional[typing.Union["LambdaFunctionDeadLetterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        durable_config: typing.Optional[typing.Union["LambdaFunctionDurableConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        environment: typing.Optional[typing.Union["LambdaFunctionEnvironment", typing.Dict[builtins.str, typing.Any]]] = None,
        ephemeral_storage: typing.Optional[typing.Union["LambdaFunctionEphemeralStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        filename: typing.Optional[builtins.str] = None,
        file_system_config: typing.Optional[typing.Union["LambdaFunctionFileSystemConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        handler: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_config: typing.Optional[typing.Union["LambdaFunctionImageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        image_uri: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        layers: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["LambdaFunctionLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        package_type: typing.Optional[builtins.str] = None,
        publish: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        publish_to: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        replacement_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        replace_security_groups_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        runtime: typing.Optional[builtins.str] = None,
        s3_bucket: typing.Optional[builtins.str] = None,
        s3_key: typing.Optional[builtins.str] = None,
        s3_object_version: typing.Optional[builtins.str] = None,
        skip_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        snap_start: typing.Optional[typing.Union["LambdaFunctionSnapStart", typing.Dict[builtins.str, typing.Any]]] = None,
        source_code_hash: typing.Optional[builtins.str] = None,
        source_kms_key_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tenancy_config: typing.Optional[typing.Union["LambdaFunctionTenancyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["LambdaFunctionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tracing_config: typing.Optional[typing.Union["LambdaFunctionTracingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_config: typing.Optional[typing.Union["LambdaFunctionVpcConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function aws_lambda_function} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param function_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#function_name LambdaFunction#function_name}.
        :param role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#role LambdaFunction#role}.
        :param architectures: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#architectures LambdaFunction#architectures}.
        :param capacity_provider_config: capacity_provider_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#capacity_provider_config LambdaFunction#capacity_provider_config}
        :param code_sha256: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#code_sha256 LambdaFunction#code_sha256}.
        :param code_signing_config_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#code_signing_config_arn LambdaFunction#code_signing_config_arn}.
        :param dead_letter_config: dead_letter_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#dead_letter_config LambdaFunction#dead_letter_config}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#description LambdaFunction#description}.
        :param durable_config: durable_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#durable_config LambdaFunction#durable_config}
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#environment LambdaFunction#environment}
        :param ephemeral_storage: ephemeral_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#ephemeral_storage LambdaFunction#ephemeral_storage}
        :param filename: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#filename LambdaFunction#filename}.
        :param file_system_config: file_system_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#file_system_config LambdaFunction#file_system_config}
        :param handler: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#handler LambdaFunction#handler}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#id LambdaFunction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_config: image_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#image_config LambdaFunction#image_config}
        :param image_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#image_uri LambdaFunction#image_uri}.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#kms_key_arn LambdaFunction#kms_key_arn}.
        :param layers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#layers LambdaFunction#layers}.
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#logging_config LambdaFunction#logging_config}
        :param memory_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#memory_size LambdaFunction#memory_size}.
        :param package_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#package_type LambdaFunction#package_type}.
        :param publish: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#publish LambdaFunction#publish}.
        :param publish_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#publish_to LambdaFunction#publish_to}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#region LambdaFunction#region}
        :param replacement_security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#replacement_security_group_ids LambdaFunction#replacement_security_group_ids}.
        :param replace_security_groups_on_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#replace_security_groups_on_destroy LambdaFunction#replace_security_groups_on_destroy}.
        :param reserved_concurrent_executions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#reserved_concurrent_executions LambdaFunction#reserved_concurrent_executions}.
        :param runtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#runtime LambdaFunction#runtime}.
        :param s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#s3_bucket LambdaFunction#s3_bucket}.
        :param s3_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#s3_key LambdaFunction#s3_key}.
        :param s3_object_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#s3_object_version LambdaFunction#s3_object_version}.
        :param skip_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#skip_destroy LambdaFunction#skip_destroy}.
        :param snap_start: snap_start block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#snap_start LambdaFunction#snap_start}
        :param source_code_hash: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#source_code_hash LambdaFunction#source_code_hash}.
        :param source_kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#source_kms_key_arn LambdaFunction#source_kms_key_arn}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#tags LambdaFunction#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#tags_all LambdaFunction#tags_all}.
        :param tenancy_config: tenancy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#tenancy_config LambdaFunction#tenancy_config}
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#timeout LambdaFunction#timeout}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#timeouts LambdaFunction#timeouts}
        :param tracing_config: tracing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#tracing_config LambdaFunction#tracing_config}
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#vpc_config LambdaFunction#vpc_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9f9bcc20c47302251ac3342669dea0f494d535b5ac68a155e82e28d3c2ea17)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LambdaFunctionConfig(
            function_name=function_name,
            role=role,
            architectures=architectures,
            capacity_provider_config=capacity_provider_config,
            code_sha256=code_sha256,
            code_signing_config_arn=code_signing_config_arn,
            dead_letter_config=dead_letter_config,
            description=description,
            durable_config=durable_config,
            environment=environment,
            ephemeral_storage=ephemeral_storage,
            filename=filename,
            file_system_config=file_system_config,
            handler=handler,
            id=id,
            image_config=image_config,
            image_uri=image_uri,
            kms_key_arn=kms_key_arn,
            layers=layers,
            logging_config=logging_config,
            memory_size=memory_size,
            package_type=package_type,
            publish=publish,
            publish_to=publish_to,
            region=region,
            replacement_security_group_ids=replacement_security_group_ids,
            replace_security_groups_on_destroy=replace_security_groups_on_destroy,
            reserved_concurrent_executions=reserved_concurrent_executions,
            runtime=runtime,
            s3_bucket=s3_bucket,
            s3_key=s3_key,
            s3_object_version=s3_object_version,
            skip_destroy=skip_destroy,
            snap_start=snap_start,
            source_code_hash=source_code_hash,
            source_kms_key_arn=source_kms_key_arn,
            tags=tags,
            tags_all=tags_all,
            tenancy_config=tenancy_config,
            timeout=timeout,
            timeouts=timeouts,
            tracing_config=tracing_config,
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
        '''Generates CDKTF code for importing a LambdaFunction resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LambdaFunction to import.
        :param import_from_id: The id of the existing LambdaFunction that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LambdaFunction to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d28da6e72ad207e96695858d0ca907a9068ff320f420e8e9e79a677f3bd14c7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCapacityProviderConfig")
    def put_capacity_provider_config(
        self,
        *,
        lambda_managed_instances_capacity_provider_config: typing.Union["LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param lambda_managed_instances_capacity_provider_config: lambda_managed_instances_capacity_provider_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#lambda_managed_instances_capacity_provider_config LambdaFunction#lambda_managed_instances_capacity_provider_config}
        '''
        value = LambdaFunctionCapacityProviderConfig(
            lambda_managed_instances_capacity_provider_config=lambda_managed_instances_capacity_provider_config,
        )

        return typing.cast(None, jsii.invoke(self, "putCapacityProviderConfig", [value]))

    @jsii.member(jsii_name="putDeadLetterConfig")
    def put_dead_letter_config(self, *, target_arn: builtins.str) -> None:
        '''
        :param target_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#target_arn LambdaFunction#target_arn}.
        '''
        value = LambdaFunctionDeadLetterConfig(target_arn=target_arn)

        return typing.cast(None, jsii.invoke(self, "putDeadLetterConfig", [value]))

    @jsii.member(jsii_name="putDurableConfig")
    def put_durable_config(
        self,
        *,
        execution_timeout: jsii.Number,
        retention_period: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param execution_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#execution_timeout LambdaFunction#execution_timeout}.
        :param retention_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#retention_period LambdaFunction#retention_period}.
        '''
        value = LambdaFunctionDurableConfig(
            execution_timeout=execution_timeout, retention_period=retention_period
        )

        return typing.cast(None, jsii.invoke(self, "putDurableConfig", [value]))

    @jsii.member(jsii_name="putEnvironment")
    def put_environment(
        self,
        *,
        variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param variables: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#variables LambdaFunction#variables}.
        '''
        value = LambdaFunctionEnvironment(variables=variables)

        return typing.cast(None, jsii.invoke(self, "putEnvironment", [value]))

    @jsii.member(jsii_name="putEphemeralStorage")
    def put_ephemeral_storage(
        self,
        *,
        size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#size LambdaFunction#size}.
        '''
        value = LambdaFunctionEphemeralStorage(size=size)

        return typing.cast(None, jsii.invoke(self, "putEphemeralStorage", [value]))

    @jsii.member(jsii_name="putFileSystemConfig")
    def put_file_system_config(
        self,
        *,
        arn: builtins.str,
        local_mount_path: builtins.str,
    ) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#arn LambdaFunction#arn}.
        :param local_mount_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#local_mount_path LambdaFunction#local_mount_path}.
        '''
        value = LambdaFunctionFileSystemConfig(
            arn=arn, local_mount_path=local_mount_path
        )

        return typing.cast(None, jsii.invoke(self, "putFileSystemConfig", [value]))

    @jsii.member(jsii_name="putImageConfig")
    def put_image_config(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        entry_point: typing.Optional[typing.Sequence[builtins.str]] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#command LambdaFunction#command}.
        :param entry_point: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#entry_point LambdaFunction#entry_point}.
        :param working_directory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#working_directory LambdaFunction#working_directory}.
        '''
        value = LambdaFunctionImageConfig(
            command=command,
            entry_point=entry_point,
            working_directory=working_directory,
        )

        return typing.cast(None, jsii.invoke(self, "putImageConfig", [value]))

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        log_format: builtins.str,
        application_log_level: typing.Optional[builtins.str] = None,
        log_group: typing.Optional[builtins.str] = None,
        system_log_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#log_format LambdaFunction#log_format}.
        :param application_log_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#application_log_level LambdaFunction#application_log_level}.
        :param log_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#log_group LambdaFunction#log_group}.
        :param system_log_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#system_log_level LambdaFunction#system_log_level}.
        '''
        value = LambdaFunctionLoggingConfig(
            log_format=log_format,
            application_log_level=application_log_level,
            log_group=log_group,
            system_log_level=system_log_level,
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="putSnapStart")
    def put_snap_start(self, *, apply_on: builtins.str) -> None:
        '''
        :param apply_on: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#apply_on LambdaFunction#apply_on}.
        '''
        value = LambdaFunctionSnapStart(apply_on=apply_on)

        return typing.cast(None, jsii.invoke(self, "putSnapStart", [value]))

    @jsii.member(jsii_name="putTenancyConfig")
    def put_tenancy_config(self, *, tenant_isolation_mode: builtins.str) -> None:
        '''
        :param tenant_isolation_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#tenant_isolation_mode LambdaFunction#tenant_isolation_mode}.
        '''
        value = LambdaFunctionTenancyConfig(
            tenant_isolation_mode=tenant_isolation_mode
        )

        return typing.cast(None, jsii.invoke(self, "putTenancyConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#create LambdaFunction#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#delete LambdaFunction#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#update LambdaFunction#update}.
        '''
        value = LambdaFunctionTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTracingConfig")
    def put_tracing_config(self, *, mode: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#mode LambdaFunction#mode}.
        '''
        value = LambdaFunctionTracingConfig(mode=mode)

        return typing.cast(None, jsii.invoke(self, "putTracingConfig", [value]))

    @jsii.member(jsii_name="putVpcConfig")
    def put_vpc_config(
        self,
        *,
        security_group_ids: typing.Sequence[builtins.str],
        subnet_ids: typing.Sequence[builtins.str],
        ipv6_allowed_for_dual_stack: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#security_group_ids LambdaFunction#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#subnet_ids LambdaFunction#subnet_ids}.
        :param ipv6_allowed_for_dual_stack: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#ipv6_allowed_for_dual_stack LambdaFunction#ipv6_allowed_for_dual_stack}.
        '''
        value = LambdaFunctionVpcConfig(
            security_group_ids=security_group_ids,
            subnet_ids=subnet_ids,
            ipv6_allowed_for_dual_stack=ipv6_allowed_for_dual_stack,
        )

        return typing.cast(None, jsii.invoke(self, "putVpcConfig", [value]))

    @jsii.member(jsii_name="resetArchitectures")
    def reset_architectures(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchitectures", []))

    @jsii.member(jsii_name="resetCapacityProviderConfig")
    def reset_capacity_provider_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacityProviderConfig", []))

    @jsii.member(jsii_name="resetCodeSha256")
    def reset_code_sha256(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeSha256", []))

    @jsii.member(jsii_name="resetCodeSigningConfigArn")
    def reset_code_signing_config_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeSigningConfigArn", []))

    @jsii.member(jsii_name="resetDeadLetterConfig")
    def reset_dead_letter_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeadLetterConfig", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDurableConfig")
    def reset_durable_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDurableConfig", []))

    @jsii.member(jsii_name="resetEnvironment")
    def reset_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironment", []))

    @jsii.member(jsii_name="resetEphemeralStorage")
    def reset_ephemeral_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEphemeralStorage", []))

    @jsii.member(jsii_name="resetFilename")
    def reset_filename(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilename", []))

    @jsii.member(jsii_name="resetFileSystemConfig")
    def reset_file_system_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileSystemConfig", []))

    @jsii.member(jsii_name="resetHandler")
    def reset_handler(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHandler", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImageConfig")
    def reset_image_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageConfig", []))

    @jsii.member(jsii_name="resetImageUri")
    def reset_image_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageUri", []))

    @jsii.member(jsii_name="resetKmsKeyArn")
    def reset_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyArn", []))

    @jsii.member(jsii_name="resetLayers")
    def reset_layers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLayers", []))

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetMemorySize")
    def reset_memory_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemorySize", []))

    @jsii.member(jsii_name="resetPackageType")
    def reset_package_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPackageType", []))

    @jsii.member(jsii_name="resetPublish")
    def reset_publish(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublish", []))

    @jsii.member(jsii_name="resetPublishTo")
    def reset_publish_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublishTo", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetReplacementSecurityGroupIds")
    def reset_replacement_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplacementSecurityGroupIds", []))

    @jsii.member(jsii_name="resetReplaceSecurityGroupsOnDestroy")
    def reset_replace_security_groups_on_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplaceSecurityGroupsOnDestroy", []))

    @jsii.member(jsii_name="resetReservedConcurrentExecutions")
    def reset_reserved_concurrent_executions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservedConcurrentExecutions", []))

    @jsii.member(jsii_name="resetRuntime")
    def reset_runtime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntime", []))

    @jsii.member(jsii_name="resetS3Bucket")
    def reset_s3_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Bucket", []))

    @jsii.member(jsii_name="resetS3Key")
    def reset_s3_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Key", []))

    @jsii.member(jsii_name="resetS3ObjectVersion")
    def reset_s3_object_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3ObjectVersion", []))

    @jsii.member(jsii_name="resetSkipDestroy")
    def reset_skip_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipDestroy", []))

    @jsii.member(jsii_name="resetSnapStart")
    def reset_snap_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapStart", []))

    @jsii.member(jsii_name="resetSourceCodeHash")
    def reset_source_code_hash(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceCodeHash", []))

    @jsii.member(jsii_name="resetSourceKmsKeyArn")
    def reset_source_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceKmsKeyArn", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTenancyConfig")
    def reset_tenancy_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenancyConfig", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTracingConfig")
    def reset_tracing_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTracingConfig", []))

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
    @jsii.member(jsii_name="capacityProviderConfig")
    def capacity_provider_config(
        self,
    ) -> "LambdaFunctionCapacityProviderConfigOutputReference":
        return typing.cast("LambdaFunctionCapacityProviderConfigOutputReference", jsii.get(self, "capacityProviderConfig"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterConfig")
    def dead_letter_config(self) -> "LambdaFunctionDeadLetterConfigOutputReference":
        return typing.cast("LambdaFunctionDeadLetterConfigOutputReference", jsii.get(self, "deadLetterConfig"))

    @builtins.property
    @jsii.member(jsii_name="durableConfig")
    def durable_config(self) -> "LambdaFunctionDurableConfigOutputReference":
        return typing.cast("LambdaFunctionDurableConfigOutputReference", jsii.get(self, "durableConfig"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> "LambdaFunctionEnvironmentOutputReference":
        return typing.cast("LambdaFunctionEnvironmentOutputReference", jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorage")
    def ephemeral_storage(self) -> "LambdaFunctionEphemeralStorageOutputReference":
        return typing.cast("LambdaFunctionEphemeralStorageOutputReference", jsii.get(self, "ephemeralStorage"))

    @builtins.property
    @jsii.member(jsii_name="fileSystemConfig")
    def file_system_config(self) -> "LambdaFunctionFileSystemConfigOutputReference":
        return typing.cast("LambdaFunctionFileSystemConfigOutputReference", jsii.get(self, "fileSystemConfig"))

    @builtins.property
    @jsii.member(jsii_name="imageConfig")
    def image_config(self) -> "LambdaFunctionImageConfigOutputReference":
        return typing.cast("LambdaFunctionImageConfigOutputReference", jsii.get(self, "imageConfig"))

    @builtins.property
    @jsii.member(jsii_name="invokeArn")
    def invoke_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "invokeArn"))

    @builtins.property
    @jsii.member(jsii_name="lastModified")
    def last_modified(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModified"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(self) -> "LambdaFunctionLoggingConfigOutputReference":
        return typing.cast("LambdaFunctionLoggingConfigOutputReference", jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="qualifiedArn")
    def qualified_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "qualifiedArn"))

    @builtins.property
    @jsii.member(jsii_name="qualifiedInvokeArn")
    def qualified_invoke_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "qualifiedInvokeArn"))

    @builtins.property
    @jsii.member(jsii_name="responseStreamingInvokeArn")
    def response_streaming_invoke_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseStreamingInvokeArn"))

    @builtins.property
    @jsii.member(jsii_name="signingJobArn")
    def signing_job_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signingJobArn"))

    @builtins.property
    @jsii.member(jsii_name="signingProfileVersionArn")
    def signing_profile_version_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signingProfileVersionArn"))

    @builtins.property
    @jsii.member(jsii_name="snapStart")
    def snap_start(self) -> "LambdaFunctionSnapStartOutputReference":
        return typing.cast("LambdaFunctionSnapStartOutputReference", jsii.get(self, "snapStart"))

    @builtins.property
    @jsii.member(jsii_name="sourceCodeSize")
    def source_code_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sourceCodeSize"))

    @builtins.property
    @jsii.member(jsii_name="tenancyConfig")
    def tenancy_config(self) -> "LambdaFunctionTenancyConfigOutputReference":
        return typing.cast("LambdaFunctionTenancyConfigOutputReference", jsii.get(self, "tenancyConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "LambdaFunctionTimeoutsOutputReference":
        return typing.cast("LambdaFunctionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="tracingConfig")
    def tracing_config(self) -> "LambdaFunctionTracingConfigOutputReference":
        return typing.cast("LambdaFunctionTracingConfigOutputReference", jsii.get(self, "tracingConfig"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(self) -> "LambdaFunctionVpcConfigOutputReference":
        return typing.cast("LambdaFunctionVpcConfigOutputReference", jsii.get(self, "vpcConfig"))

    @builtins.property
    @jsii.member(jsii_name="architecturesInput")
    def architectures_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "architecturesInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityProviderConfigInput")
    def capacity_provider_config_input(
        self,
    ) -> typing.Optional["LambdaFunctionCapacityProviderConfig"]:
        return typing.cast(typing.Optional["LambdaFunctionCapacityProviderConfig"], jsii.get(self, "capacityProviderConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="codeSha256Input")
    def code_sha256_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codeSha256Input"))

    @builtins.property
    @jsii.member(jsii_name="codeSigningConfigArnInput")
    def code_signing_config_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codeSigningConfigArnInput"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterConfigInput")
    def dead_letter_config_input(
        self,
    ) -> typing.Optional["LambdaFunctionDeadLetterConfig"]:
        return typing.cast(typing.Optional["LambdaFunctionDeadLetterConfig"], jsii.get(self, "deadLetterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="durableConfigInput")
    def durable_config_input(self) -> typing.Optional["LambdaFunctionDurableConfig"]:
        return typing.cast(typing.Optional["LambdaFunctionDurableConfig"], jsii.get(self, "durableConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(self) -> typing.Optional["LambdaFunctionEnvironment"]:
        return typing.cast(typing.Optional["LambdaFunctionEnvironment"], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorageInput")
    def ephemeral_storage_input(
        self,
    ) -> typing.Optional["LambdaFunctionEphemeralStorage"]:
        return typing.cast(typing.Optional["LambdaFunctionEphemeralStorage"], jsii.get(self, "ephemeralStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="filenameInput")
    def filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameInput"))

    @builtins.property
    @jsii.member(jsii_name="fileSystemConfigInput")
    def file_system_config_input(
        self,
    ) -> typing.Optional["LambdaFunctionFileSystemConfig"]:
        return typing.cast(typing.Optional["LambdaFunctionFileSystemConfig"], jsii.get(self, "fileSystemConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="functionNameInput")
    def function_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="handlerInput")
    def handler_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "handlerInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageConfigInput")
    def image_config_input(self) -> typing.Optional["LambdaFunctionImageConfig"]:
        return typing.cast(typing.Optional["LambdaFunctionImageConfig"], jsii.get(self, "imageConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="imageUriInput")
    def image_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageUriInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="layersInput")
    def layers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "layersInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(self) -> typing.Optional["LambdaFunctionLoggingConfig"]:
        return typing.cast(typing.Optional["LambdaFunctionLoggingConfig"], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="memorySizeInput")
    def memory_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySizeInput"))

    @builtins.property
    @jsii.member(jsii_name="packageTypeInput")
    def package_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "packageTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="publishInput")
    def publish_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publishInput"))

    @builtins.property
    @jsii.member(jsii_name="publishToInput")
    def publish_to_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publishToInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="replacementSecurityGroupIdsInput")
    def replacement_security_group_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "replacementSecurityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="replaceSecurityGroupsOnDestroyInput")
    def replace_security_groups_on_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "replaceSecurityGroupsOnDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="reservedConcurrentExecutionsInput")
    def reserved_concurrent_executions_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "reservedConcurrentExecutionsInput"))

    @builtins.property
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeInput")
    def runtime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketInput")
    def s3_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BucketInput"))

    @builtins.property
    @jsii.member(jsii_name="s3KeyInput")
    def s3_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3KeyInput"))

    @builtins.property
    @jsii.member(jsii_name="s3ObjectVersionInput")
    def s3_object_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3ObjectVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="skipDestroyInput")
    def skip_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="snapStartInput")
    def snap_start_input(self) -> typing.Optional["LambdaFunctionSnapStart"]:
        return typing.cast(typing.Optional["LambdaFunctionSnapStart"], jsii.get(self, "snapStartInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceCodeHashInput")
    def source_code_hash_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceCodeHashInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceKmsKeyArnInput")
    def source_kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceKmsKeyArnInput"))

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
    @jsii.member(jsii_name="tenancyConfigInput")
    def tenancy_config_input(self) -> typing.Optional["LambdaFunctionTenancyConfig"]:
        return typing.cast(typing.Optional["LambdaFunctionTenancyConfig"], jsii.get(self, "tenancyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LambdaFunctionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LambdaFunctionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="tracingConfigInput")
    def tracing_config_input(self) -> typing.Optional["LambdaFunctionTracingConfig"]:
        return typing.cast(typing.Optional["LambdaFunctionTracingConfig"], jsii.get(self, "tracingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfigInput")
    def vpc_config_input(self) -> typing.Optional["LambdaFunctionVpcConfig"]:
        return typing.cast(typing.Optional["LambdaFunctionVpcConfig"], jsii.get(self, "vpcConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="architectures")
    def architectures(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "architectures"))

    @architectures.setter
    def architectures(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0081b8d150f56d0e6e196e56f61a81a2a08ea1461e3b5bdaa987a584896ccbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "architectures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="codeSha256")
    def code_sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "codeSha256"))

    @code_sha256.setter
    def code_sha256(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56eb329d4b0e107459619e8a8ec4b1c3280281b58df979365a837fbeddc7192f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codeSha256", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="codeSigningConfigArn")
    def code_signing_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "codeSigningConfigArn"))

    @code_signing_config_arn.setter
    def code_signing_config_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__255423580eb4164e4067be8426d32cb890fd4006ca1937128af94f2b3b9c3aab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codeSigningConfigArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3efa727e0be1fa73870655f616a931a8cbe655c0826d04e576fb804be5584d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59562d31349ea4751740db083dc2137a727adb076b1e153a791c04a88a0133e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filename", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionName"))

    @function_name.setter
    def function_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e08a264e672efd6f49b16083341d0be13e145696cbebd089bf8d028374928ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "handler"))

    @handler.setter
    def handler(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a13ac45377f4e06db0fea0f9600c018fae32bd093f6334f642a811fe7f3f9b3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "handler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ced7a49bfb5335d9b92d76c2ad497d1ebbbb33a06e57547c1029dbf94c3f9fbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8d3ea7ad035e957376518b62e2e6cdbee03e89929144ea5efed760f31098da1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__245280a466adb36f3dfc51a7dd1b2204b82db8f1a57e4f7d435e1b37e38d2649)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="layers")
    def layers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "layers"))

    @layers.setter
    def layers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42e6105b91df61cbfac1623c615903e5fbb456b0d2a842cd077d030f3509453a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "layers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memorySize")
    def memory_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySize"))

    @memory_size.setter
    def memory_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2431e04a597c3c59b9398fda096bb6107e8e6fd71e6f799988d27322096073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorySize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="packageType")
    def package_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "packageType"))

    @package_type.setter
    def package_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a27d57941d5e8f5af6ff066e9280a8b28ceeb1d4361c77139af0535a7dc9f2a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publish")
    def publish(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publish"))

    @publish.setter
    def publish(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca00244dac88e84b521b417cd9901b5b0a78979df4902f07b10b1e52d7bfa8e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publish", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publishTo")
    def publish_to(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publishTo"))

    @publish_to.setter
    def publish_to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0593ce93cea0791919a9e64dbd23fd7c402fa02567305eeb7544841b14268c14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishTo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaa43a95b0488ad520b21c56f6ef54127b8a4029e8d10900f737426224511c64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replacementSecurityGroupIds")
    def replacement_security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "replacementSecurityGroupIds"))

    @replacement_security_group_ids.setter
    def replacement_security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ecf9039032d6de31da9ede5891d177341dcd3f4b4719338a3946556d2582b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replacementSecurityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replaceSecurityGroupsOnDestroy")
    def replace_security_groups_on_destroy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "replaceSecurityGroupsOnDestroy"))

    @replace_security_groups_on_destroy.setter
    def replace_security_groups_on_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08a552ee9ca2f9a5a0b68bc82049c7f2ab70650da88f3cd32576d50d8782f65d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replaceSecurityGroupsOnDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservedConcurrentExecutions")
    def reserved_concurrent_executions(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "reservedConcurrentExecutions"))

    @reserved_concurrent_executions.setter
    def reserved_concurrent_executions(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c8b567f3d538aedea3645f623e4c9b1723db8ce227ad1ac093ec85541756226)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedConcurrentExecutions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a5e59942de33b413b2e04205e025ec2432f7b9b889d0443f41f205a85872f6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e718c2909dff752640be4ee82851fdf016c591db09b03ef736d95769a8ad3f22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Bucket"))

    @s3_bucket.setter
    def s3_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac5829134c55180c4e28fcf5013c28a8e13b697cfc231fcddbc90ce204dd5495)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Key")
    def s3_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Key"))

    @s3_key.setter
    def s3_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a257ef37137b57c9e9b0f5317ab2a0cfbe9f1dd904740522fa3bac9fefd8c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3ObjectVersion")
    def s3_object_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3ObjectVersion"))

    @s3_object_version.setter
    def s3_object_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb3d8614e1fe9d724fb23f6da9e35775e07bb80b16eaa916f1303bfb1329081b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3ObjectVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipDestroy")
    def skip_destroy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipDestroy"))

    @skip_destroy.setter
    def skip_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e13d3f8110dd4fcd8a9382dbda5555dc1deac95baba0c4d5c69a1f27195ead40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceCodeHash")
    def source_code_hash(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceCodeHash"))

    @source_code_hash.setter
    def source_code_hash(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5fc937621a98551aba9673abaaebe7638018b79ba627faebde58cf5eb7db42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceCodeHash", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceKmsKeyArn")
    def source_kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceKmsKeyArn"))

    @source_kms_key_arn.setter
    def source_kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee87c9fd6d4dde163d87dda42c4960c029adc1af1ab84a3770b2874542b740f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceKmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d28e9873b46954b35d8794e436608ce9203d80b66e84ade4c5f2c90d07ef4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__978d880d95909bd18b3cc9f596b744b8de46d5cc7d0b8c8934c6e4a16e5efceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c11951df6d6331d97b98333de696a5449fe295b83d1e167f19920548f35243e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionCapacityProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "lambda_managed_instances_capacity_provider_config": "lambdaManagedInstancesCapacityProviderConfig",
    },
)
class LambdaFunctionCapacityProviderConfig:
    def __init__(
        self,
        *,
        lambda_managed_instances_capacity_provider_config: typing.Union["LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param lambda_managed_instances_capacity_provider_config: lambda_managed_instances_capacity_provider_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#lambda_managed_instances_capacity_provider_config LambdaFunction#lambda_managed_instances_capacity_provider_config}
        '''
        if isinstance(lambda_managed_instances_capacity_provider_config, dict):
            lambda_managed_instances_capacity_provider_config = LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfig(**lambda_managed_instances_capacity_provider_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05b1e1e5f5a3d3670ec304766b092fd7504e0a5f021179b4335e6921fa5610be)
            check_type(argname="argument lambda_managed_instances_capacity_provider_config", value=lambda_managed_instances_capacity_provider_config, expected_type=type_hints["lambda_managed_instances_capacity_provider_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lambda_managed_instances_capacity_provider_config": lambda_managed_instances_capacity_provider_config,
        }

    @builtins.property
    def lambda_managed_instances_capacity_provider_config(
        self,
    ) -> "LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfig":
        '''lambda_managed_instances_capacity_provider_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#lambda_managed_instances_capacity_provider_config LambdaFunction#lambda_managed_instances_capacity_provider_config}
        '''
        result = self._values.get("lambda_managed_instances_capacity_provider_config")
        assert result is not None, "Required property 'lambda_managed_instances_capacity_provider_config' is missing"
        return typing.cast("LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionCapacityProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "capacity_provider_arn": "capacityProviderArn",
        "execution_environment_memory_gib_per_vcpu": "executionEnvironmentMemoryGibPerVcpu",
        "per_execution_environment_max_concurrency": "perExecutionEnvironmentMaxConcurrency",
    },
)
class LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfig:
    def __init__(
        self,
        *,
        capacity_provider_arn: builtins.str,
        execution_environment_memory_gib_per_vcpu: typing.Optional[jsii.Number] = None,
        per_execution_environment_max_concurrency: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param capacity_provider_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#capacity_provider_arn LambdaFunction#capacity_provider_arn}.
        :param execution_environment_memory_gib_per_vcpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#execution_environment_memory_gib_per_vcpu LambdaFunction#execution_environment_memory_gib_per_vcpu}.
        :param per_execution_environment_max_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#per_execution_environment_max_concurrency LambdaFunction#per_execution_environment_max_concurrency}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d52ce5e6eb13449bc274f433e23b84abc8537404418e85d78a9cb0d3842e29)
            check_type(argname="argument capacity_provider_arn", value=capacity_provider_arn, expected_type=type_hints["capacity_provider_arn"])
            check_type(argname="argument execution_environment_memory_gib_per_vcpu", value=execution_environment_memory_gib_per_vcpu, expected_type=type_hints["execution_environment_memory_gib_per_vcpu"])
            check_type(argname="argument per_execution_environment_max_concurrency", value=per_execution_environment_max_concurrency, expected_type=type_hints["per_execution_environment_max_concurrency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capacity_provider_arn": capacity_provider_arn,
        }
        if execution_environment_memory_gib_per_vcpu is not None:
            self._values["execution_environment_memory_gib_per_vcpu"] = execution_environment_memory_gib_per_vcpu
        if per_execution_environment_max_concurrency is not None:
            self._values["per_execution_environment_max_concurrency"] = per_execution_environment_max_concurrency

    @builtins.property
    def capacity_provider_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#capacity_provider_arn LambdaFunction#capacity_provider_arn}.'''
        result = self._values.get("capacity_provider_arn")
        assert result is not None, "Required property 'capacity_provider_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def execution_environment_memory_gib_per_vcpu(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#execution_environment_memory_gib_per_vcpu LambdaFunction#execution_environment_memory_gib_per_vcpu}.'''
        result = self._values.get("execution_environment_memory_gib_per_vcpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def per_execution_environment_max_concurrency(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#per_execution_environment_max_concurrency LambdaFunction#per_execution_environment_max_concurrency}.'''
        result = self._values.get("per_execution_environment_max_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f8e34d406fda01b6602e9355d3287cb7d0ae9a0245b5cce518d68c07f1f5961)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExecutionEnvironmentMemoryGibPerVcpu")
    def reset_execution_environment_memory_gib_per_vcpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionEnvironmentMemoryGibPerVcpu", []))

    @jsii.member(jsii_name="resetPerExecutionEnvironmentMaxConcurrency")
    def reset_per_execution_environment_max_concurrency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerExecutionEnvironmentMaxConcurrency", []))

    @builtins.property
    @jsii.member(jsii_name="capacityProviderArnInput")
    def capacity_provider_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "capacityProviderArnInput"))

    @builtins.property
    @jsii.member(jsii_name="executionEnvironmentMemoryGibPerVcpuInput")
    def execution_environment_memory_gib_per_vcpu_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "executionEnvironmentMemoryGibPerVcpuInput"))

    @builtins.property
    @jsii.member(jsii_name="perExecutionEnvironmentMaxConcurrencyInput")
    def per_execution_environment_max_concurrency_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "perExecutionEnvironmentMaxConcurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityProviderArn")
    def capacity_provider_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "capacityProviderArn"))

    @capacity_provider_arn.setter
    def capacity_provider_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ee838436c1827309bb2223d38f269cc86f99cf6bdb4446efb67d2bcc87752a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityProviderArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionEnvironmentMemoryGibPerVcpu")
    def execution_environment_memory_gib_per_vcpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "executionEnvironmentMemoryGibPerVcpu"))

    @execution_environment_memory_gib_per_vcpu.setter
    def execution_environment_memory_gib_per_vcpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9652d173eba79a23a5e77fe9a7e4760c73d2a63a16aabe74434eb8c5156db192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionEnvironmentMemoryGibPerVcpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="perExecutionEnvironmentMaxConcurrency")
    def per_execution_environment_max_concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "perExecutionEnvironmentMaxConcurrency"))

    @per_execution_environment_max_concurrency.setter
    def per_execution_environment_max_concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c635b0766fa6629bb60462073e6e7572ad738f4f904f38dabcb30b809cfdcd8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "perExecutionEnvironmentMaxConcurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfig]:
        return typing.cast(typing.Optional[LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43259731ec17b4e4569a569da7844b0bbc5912eb18f877159e48eb3e7529b923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaFunctionCapacityProviderConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionCapacityProviderConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8fcb4628e407ff2f3ef91eb9475787cea025c5591cb11aed3b8ea27b1348c2c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLambdaManagedInstancesCapacityProviderConfig")
    def put_lambda_managed_instances_capacity_provider_config(
        self,
        *,
        capacity_provider_arn: builtins.str,
        execution_environment_memory_gib_per_vcpu: typing.Optional[jsii.Number] = None,
        per_execution_environment_max_concurrency: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param capacity_provider_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#capacity_provider_arn LambdaFunction#capacity_provider_arn}.
        :param execution_environment_memory_gib_per_vcpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#execution_environment_memory_gib_per_vcpu LambdaFunction#execution_environment_memory_gib_per_vcpu}.
        :param per_execution_environment_max_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#per_execution_environment_max_concurrency LambdaFunction#per_execution_environment_max_concurrency}.
        '''
        value = LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfig(
            capacity_provider_arn=capacity_provider_arn,
            execution_environment_memory_gib_per_vcpu=execution_environment_memory_gib_per_vcpu,
            per_execution_environment_max_concurrency=per_execution_environment_max_concurrency,
        )

        return typing.cast(None, jsii.invoke(self, "putLambdaManagedInstancesCapacityProviderConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="lambdaManagedInstancesCapacityProviderConfig")
    def lambda_managed_instances_capacity_provider_config(
        self,
    ) -> LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfigOutputReference:
        return typing.cast(LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfigOutputReference, jsii.get(self, "lambdaManagedInstancesCapacityProviderConfig"))

    @builtins.property
    @jsii.member(jsii_name="lambdaManagedInstancesCapacityProviderConfigInput")
    def lambda_managed_instances_capacity_provider_config_input(
        self,
    ) -> typing.Optional[LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfig]:
        return typing.cast(typing.Optional[LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfig], jsii.get(self, "lambdaManagedInstancesCapacityProviderConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaFunctionCapacityProviderConfig]:
        return typing.cast(typing.Optional[LambdaFunctionCapacityProviderConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaFunctionCapacityProviderConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b5c26644702b4b7203cc303a1914df18fb3393a0b8b700779388d84086e87f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "function_name": "functionName",
        "role": "role",
        "architectures": "architectures",
        "capacity_provider_config": "capacityProviderConfig",
        "code_sha256": "codeSha256",
        "code_signing_config_arn": "codeSigningConfigArn",
        "dead_letter_config": "deadLetterConfig",
        "description": "description",
        "durable_config": "durableConfig",
        "environment": "environment",
        "ephemeral_storage": "ephemeralStorage",
        "filename": "filename",
        "file_system_config": "fileSystemConfig",
        "handler": "handler",
        "id": "id",
        "image_config": "imageConfig",
        "image_uri": "imageUri",
        "kms_key_arn": "kmsKeyArn",
        "layers": "layers",
        "logging_config": "loggingConfig",
        "memory_size": "memorySize",
        "package_type": "packageType",
        "publish": "publish",
        "publish_to": "publishTo",
        "region": "region",
        "replacement_security_group_ids": "replacementSecurityGroupIds",
        "replace_security_groups_on_destroy": "replaceSecurityGroupsOnDestroy",
        "reserved_concurrent_executions": "reservedConcurrentExecutions",
        "runtime": "runtime",
        "s3_bucket": "s3Bucket",
        "s3_key": "s3Key",
        "s3_object_version": "s3ObjectVersion",
        "skip_destroy": "skipDestroy",
        "snap_start": "snapStart",
        "source_code_hash": "sourceCodeHash",
        "source_kms_key_arn": "sourceKmsKeyArn",
        "tags": "tags",
        "tags_all": "tagsAll",
        "tenancy_config": "tenancyConfig",
        "timeout": "timeout",
        "timeouts": "timeouts",
        "tracing_config": "tracingConfig",
        "vpc_config": "vpcConfig",
    },
)
class LambdaFunctionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        function_name: builtins.str,
        role: builtins.str,
        architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
        capacity_provider_config: typing.Optional[typing.Union[LambdaFunctionCapacityProviderConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        code_sha256: typing.Optional[builtins.str] = None,
        code_signing_config_arn: typing.Optional[builtins.str] = None,
        dead_letter_config: typing.Optional[typing.Union["LambdaFunctionDeadLetterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        durable_config: typing.Optional[typing.Union["LambdaFunctionDurableConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        environment: typing.Optional[typing.Union["LambdaFunctionEnvironment", typing.Dict[builtins.str, typing.Any]]] = None,
        ephemeral_storage: typing.Optional[typing.Union["LambdaFunctionEphemeralStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        filename: typing.Optional[builtins.str] = None,
        file_system_config: typing.Optional[typing.Union["LambdaFunctionFileSystemConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        handler: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_config: typing.Optional[typing.Union["LambdaFunctionImageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        image_uri: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        layers: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["LambdaFunctionLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        package_type: typing.Optional[builtins.str] = None,
        publish: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        publish_to: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        replacement_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        replace_security_groups_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        runtime: typing.Optional[builtins.str] = None,
        s3_bucket: typing.Optional[builtins.str] = None,
        s3_key: typing.Optional[builtins.str] = None,
        s3_object_version: typing.Optional[builtins.str] = None,
        skip_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        snap_start: typing.Optional[typing.Union["LambdaFunctionSnapStart", typing.Dict[builtins.str, typing.Any]]] = None,
        source_code_hash: typing.Optional[builtins.str] = None,
        source_kms_key_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tenancy_config: typing.Optional[typing.Union["LambdaFunctionTenancyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["LambdaFunctionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tracing_config: typing.Optional[typing.Union["LambdaFunctionTracingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_config: typing.Optional[typing.Union["LambdaFunctionVpcConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param function_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#function_name LambdaFunction#function_name}.
        :param role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#role LambdaFunction#role}.
        :param architectures: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#architectures LambdaFunction#architectures}.
        :param capacity_provider_config: capacity_provider_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#capacity_provider_config LambdaFunction#capacity_provider_config}
        :param code_sha256: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#code_sha256 LambdaFunction#code_sha256}.
        :param code_signing_config_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#code_signing_config_arn LambdaFunction#code_signing_config_arn}.
        :param dead_letter_config: dead_letter_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#dead_letter_config LambdaFunction#dead_letter_config}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#description LambdaFunction#description}.
        :param durable_config: durable_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#durable_config LambdaFunction#durable_config}
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#environment LambdaFunction#environment}
        :param ephemeral_storage: ephemeral_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#ephemeral_storage LambdaFunction#ephemeral_storage}
        :param filename: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#filename LambdaFunction#filename}.
        :param file_system_config: file_system_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#file_system_config LambdaFunction#file_system_config}
        :param handler: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#handler LambdaFunction#handler}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#id LambdaFunction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_config: image_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#image_config LambdaFunction#image_config}
        :param image_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#image_uri LambdaFunction#image_uri}.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#kms_key_arn LambdaFunction#kms_key_arn}.
        :param layers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#layers LambdaFunction#layers}.
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#logging_config LambdaFunction#logging_config}
        :param memory_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#memory_size LambdaFunction#memory_size}.
        :param package_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#package_type LambdaFunction#package_type}.
        :param publish: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#publish LambdaFunction#publish}.
        :param publish_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#publish_to LambdaFunction#publish_to}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#region LambdaFunction#region}
        :param replacement_security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#replacement_security_group_ids LambdaFunction#replacement_security_group_ids}.
        :param replace_security_groups_on_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#replace_security_groups_on_destroy LambdaFunction#replace_security_groups_on_destroy}.
        :param reserved_concurrent_executions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#reserved_concurrent_executions LambdaFunction#reserved_concurrent_executions}.
        :param runtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#runtime LambdaFunction#runtime}.
        :param s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#s3_bucket LambdaFunction#s3_bucket}.
        :param s3_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#s3_key LambdaFunction#s3_key}.
        :param s3_object_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#s3_object_version LambdaFunction#s3_object_version}.
        :param skip_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#skip_destroy LambdaFunction#skip_destroy}.
        :param snap_start: snap_start block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#snap_start LambdaFunction#snap_start}
        :param source_code_hash: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#source_code_hash LambdaFunction#source_code_hash}.
        :param source_kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#source_kms_key_arn LambdaFunction#source_kms_key_arn}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#tags LambdaFunction#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#tags_all LambdaFunction#tags_all}.
        :param tenancy_config: tenancy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#tenancy_config LambdaFunction#tenancy_config}
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#timeout LambdaFunction#timeout}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#timeouts LambdaFunction#timeouts}
        :param tracing_config: tracing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#tracing_config LambdaFunction#tracing_config}
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#vpc_config LambdaFunction#vpc_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(capacity_provider_config, dict):
            capacity_provider_config = LambdaFunctionCapacityProviderConfig(**capacity_provider_config)
        if isinstance(dead_letter_config, dict):
            dead_letter_config = LambdaFunctionDeadLetterConfig(**dead_letter_config)
        if isinstance(durable_config, dict):
            durable_config = LambdaFunctionDurableConfig(**durable_config)
        if isinstance(environment, dict):
            environment = LambdaFunctionEnvironment(**environment)
        if isinstance(ephemeral_storage, dict):
            ephemeral_storage = LambdaFunctionEphemeralStorage(**ephemeral_storage)
        if isinstance(file_system_config, dict):
            file_system_config = LambdaFunctionFileSystemConfig(**file_system_config)
        if isinstance(image_config, dict):
            image_config = LambdaFunctionImageConfig(**image_config)
        if isinstance(logging_config, dict):
            logging_config = LambdaFunctionLoggingConfig(**logging_config)
        if isinstance(snap_start, dict):
            snap_start = LambdaFunctionSnapStart(**snap_start)
        if isinstance(tenancy_config, dict):
            tenancy_config = LambdaFunctionTenancyConfig(**tenancy_config)
        if isinstance(timeouts, dict):
            timeouts = LambdaFunctionTimeouts(**timeouts)
        if isinstance(tracing_config, dict):
            tracing_config = LambdaFunctionTracingConfig(**tracing_config)
        if isinstance(vpc_config, dict):
            vpc_config = LambdaFunctionVpcConfig(**vpc_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d146b73e2024d599b61cb4863166738c3f18d097865dd8af3728961976b17466)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument architectures", value=architectures, expected_type=type_hints["architectures"])
            check_type(argname="argument capacity_provider_config", value=capacity_provider_config, expected_type=type_hints["capacity_provider_config"])
            check_type(argname="argument code_sha256", value=code_sha256, expected_type=type_hints["code_sha256"])
            check_type(argname="argument code_signing_config_arn", value=code_signing_config_arn, expected_type=type_hints["code_signing_config_arn"])
            check_type(argname="argument dead_letter_config", value=dead_letter_config, expected_type=type_hints["dead_letter_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument durable_config", value=durable_config, expected_type=type_hints["durable_config"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument ephemeral_storage", value=ephemeral_storage, expected_type=type_hints["ephemeral_storage"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
            check_type(argname="argument file_system_config", value=file_system_config, expected_type=type_hints["file_system_config"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_config", value=image_config, expected_type=type_hints["image_config"])
            check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument layers", value=layers, expected_type=type_hints["layers"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
            check_type(argname="argument package_type", value=package_type, expected_type=type_hints["package_type"])
            check_type(argname="argument publish", value=publish, expected_type=type_hints["publish"])
            check_type(argname="argument publish_to", value=publish_to, expected_type=type_hints["publish_to"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument replacement_security_group_ids", value=replacement_security_group_ids, expected_type=type_hints["replacement_security_group_ids"])
            check_type(argname="argument replace_security_groups_on_destroy", value=replace_security_groups_on_destroy, expected_type=type_hints["replace_security_groups_on_destroy"])
            check_type(argname="argument reserved_concurrent_executions", value=reserved_concurrent_executions, expected_type=type_hints["reserved_concurrent_executions"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
            check_type(argname="argument s3_object_version", value=s3_object_version, expected_type=type_hints["s3_object_version"])
            check_type(argname="argument skip_destroy", value=skip_destroy, expected_type=type_hints["skip_destroy"])
            check_type(argname="argument snap_start", value=snap_start, expected_type=type_hints["snap_start"])
            check_type(argname="argument source_code_hash", value=source_code_hash, expected_type=type_hints["source_code_hash"])
            check_type(argname="argument source_kms_key_arn", value=source_kms_key_arn, expected_type=type_hints["source_kms_key_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument tenancy_config", value=tenancy_config, expected_type=type_hints["tenancy_config"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument tracing_config", value=tracing_config, expected_type=type_hints["tracing_config"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_name": function_name,
            "role": role,
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
        if architectures is not None:
            self._values["architectures"] = architectures
        if capacity_provider_config is not None:
            self._values["capacity_provider_config"] = capacity_provider_config
        if code_sha256 is not None:
            self._values["code_sha256"] = code_sha256
        if code_signing_config_arn is not None:
            self._values["code_signing_config_arn"] = code_signing_config_arn
        if dead_letter_config is not None:
            self._values["dead_letter_config"] = dead_letter_config
        if description is not None:
            self._values["description"] = description
        if durable_config is not None:
            self._values["durable_config"] = durable_config
        if environment is not None:
            self._values["environment"] = environment
        if ephemeral_storage is not None:
            self._values["ephemeral_storage"] = ephemeral_storage
        if filename is not None:
            self._values["filename"] = filename
        if file_system_config is not None:
            self._values["file_system_config"] = file_system_config
        if handler is not None:
            self._values["handler"] = handler
        if id is not None:
            self._values["id"] = id
        if image_config is not None:
            self._values["image_config"] = image_config
        if image_uri is not None:
            self._values["image_uri"] = image_uri
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if layers is not None:
            self._values["layers"] = layers
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if package_type is not None:
            self._values["package_type"] = package_type
        if publish is not None:
            self._values["publish"] = publish
        if publish_to is not None:
            self._values["publish_to"] = publish_to
        if region is not None:
            self._values["region"] = region
        if replacement_security_group_ids is not None:
            self._values["replacement_security_group_ids"] = replacement_security_group_ids
        if replace_security_groups_on_destroy is not None:
            self._values["replace_security_groups_on_destroy"] = replace_security_groups_on_destroy
        if reserved_concurrent_executions is not None:
            self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if runtime is not None:
            self._values["runtime"] = runtime
        if s3_bucket is not None:
            self._values["s3_bucket"] = s3_bucket
        if s3_key is not None:
            self._values["s3_key"] = s3_key
        if s3_object_version is not None:
            self._values["s3_object_version"] = s3_object_version
        if skip_destroy is not None:
            self._values["skip_destroy"] = skip_destroy
        if snap_start is not None:
            self._values["snap_start"] = snap_start
        if source_code_hash is not None:
            self._values["source_code_hash"] = source_code_hash
        if source_kms_key_arn is not None:
            self._values["source_kms_key_arn"] = source_kms_key_arn
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if tenancy_config is not None:
            self._values["tenancy_config"] = tenancy_config
        if timeout is not None:
            self._values["timeout"] = timeout
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if tracing_config is not None:
            self._values["tracing_config"] = tracing_config
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
    def function_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#function_name LambdaFunction#function_name}.'''
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#role LambdaFunction#role}.'''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def architectures(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#architectures LambdaFunction#architectures}.'''
        result = self._values.get("architectures")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def capacity_provider_config(
        self,
    ) -> typing.Optional[LambdaFunctionCapacityProviderConfig]:
        '''capacity_provider_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#capacity_provider_config LambdaFunction#capacity_provider_config}
        '''
        result = self._values.get("capacity_provider_config")
        return typing.cast(typing.Optional[LambdaFunctionCapacityProviderConfig], result)

    @builtins.property
    def code_sha256(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#code_sha256 LambdaFunction#code_sha256}.'''
        result = self._values.get("code_sha256")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_signing_config_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#code_signing_config_arn LambdaFunction#code_signing_config_arn}.'''
        result = self._values.get("code_signing_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dead_letter_config(self) -> typing.Optional["LambdaFunctionDeadLetterConfig"]:
        '''dead_letter_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#dead_letter_config LambdaFunction#dead_letter_config}
        '''
        result = self._values.get("dead_letter_config")
        return typing.cast(typing.Optional["LambdaFunctionDeadLetterConfig"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#description LambdaFunction#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def durable_config(self) -> typing.Optional["LambdaFunctionDurableConfig"]:
        '''durable_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#durable_config LambdaFunction#durable_config}
        '''
        result = self._values.get("durable_config")
        return typing.cast(typing.Optional["LambdaFunctionDurableConfig"], result)

    @builtins.property
    def environment(self) -> typing.Optional["LambdaFunctionEnvironment"]:
        '''environment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#environment LambdaFunction#environment}
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional["LambdaFunctionEnvironment"], result)

    @builtins.property
    def ephemeral_storage(self) -> typing.Optional["LambdaFunctionEphemeralStorage"]:
        '''ephemeral_storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#ephemeral_storage LambdaFunction#ephemeral_storage}
        '''
        result = self._values.get("ephemeral_storage")
        return typing.cast(typing.Optional["LambdaFunctionEphemeralStorage"], result)

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#filename LambdaFunction#filename}.'''
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_system_config(self) -> typing.Optional["LambdaFunctionFileSystemConfig"]:
        '''file_system_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#file_system_config LambdaFunction#file_system_config}
        '''
        result = self._values.get("file_system_config")
        return typing.cast(typing.Optional["LambdaFunctionFileSystemConfig"], result)

    @builtins.property
    def handler(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#handler LambdaFunction#handler}.'''
        result = self._values.get("handler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#id LambdaFunction#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_config(self) -> typing.Optional["LambdaFunctionImageConfig"]:
        '''image_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#image_config LambdaFunction#image_config}
        '''
        result = self._values.get("image_config")
        return typing.cast(typing.Optional["LambdaFunctionImageConfig"], result)

    @builtins.property
    def image_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#image_uri LambdaFunction#image_uri}.'''
        result = self._values.get("image_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#kms_key_arn LambdaFunction#kms_key_arn}.'''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def layers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#layers LambdaFunction#layers}.'''
        result = self._values.get("layers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logging_config(self) -> typing.Optional["LambdaFunctionLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#logging_config LambdaFunction#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["LambdaFunctionLoggingConfig"], result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#memory_size LambdaFunction#memory_size}.'''
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def package_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#package_type LambdaFunction#package_type}.'''
        result = self._values.get("package_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#publish LambdaFunction#publish}.'''
        result = self._values.get("publish")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def publish_to(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#publish_to LambdaFunction#publish_to}.'''
        result = self._values.get("publish_to")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#region LambdaFunction#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replacement_security_group_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#replacement_security_group_ids LambdaFunction#replacement_security_group_ids}.'''
        result = self._values.get("replacement_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def replace_security_groups_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#replace_security_groups_on_destroy LambdaFunction#replace_security_groups_on_destroy}.'''
        result = self._values.get("replace_security_groups_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#reserved_concurrent_executions LambdaFunction#reserved_concurrent_executions}.'''
        result = self._values.get("reserved_concurrent_executions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def runtime(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#runtime LambdaFunction#runtime}.'''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_bucket(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#s3_bucket LambdaFunction#s3_bucket}.'''
        result = self._values.get("s3_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#s3_key LambdaFunction#s3_key}.'''
        result = self._values.get("s3_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_object_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#s3_object_version LambdaFunction#s3_object_version}.'''
        result = self._values.get("s3_object_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#skip_destroy LambdaFunction#skip_destroy}.'''
        result = self._values.get("skip_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def snap_start(self) -> typing.Optional["LambdaFunctionSnapStart"]:
        '''snap_start block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#snap_start LambdaFunction#snap_start}
        '''
        result = self._values.get("snap_start")
        return typing.cast(typing.Optional["LambdaFunctionSnapStart"], result)

    @builtins.property
    def source_code_hash(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#source_code_hash LambdaFunction#source_code_hash}.'''
        result = self._values.get("source_code_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#source_kms_key_arn LambdaFunction#source_kms_key_arn}.'''
        result = self._values.get("source_kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#tags LambdaFunction#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#tags_all LambdaFunction#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tenancy_config(self) -> typing.Optional["LambdaFunctionTenancyConfig"]:
        '''tenancy_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#tenancy_config LambdaFunction#tenancy_config}
        '''
        result = self._values.get("tenancy_config")
        return typing.cast(typing.Optional["LambdaFunctionTenancyConfig"], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#timeout LambdaFunction#timeout}.'''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["LambdaFunctionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#timeouts LambdaFunction#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["LambdaFunctionTimeouts"], result)

    @builtins.property
    def tracing_config(self) -> typing.Optional["LambdaFunctionTracingConfig"]:
        '''tracing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#tracing_config LambdaFunction#tracing_config}
        '''
        result = self._values.get("tracing_config")
        return typing.cast(typing.Optional["LambdaFunctionTracingConfig"], result)

    @builtins.property
    def vpc_config(self) -> typing.Optional["LambdaFunctionVpcConfig"]:
        '''vpc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#vpc_config LambdaFunction#vpc_config}
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional["LambdaFunctionVpcConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionDeadLetterConfig",
    jsii_struct_bases=[],
    name_mapping={"target_arn": "targetArn"},
)
class LambdaFunctionDeadLetterConfig:
    def __init__(self, *, target_arn: builtins.str) -> None:
        '''
        :param target_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#target_arn LambdaFunction#target_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c466c792358aca96c9cc91ce5c999c2e731d572dfc31e48c649b9f2d324ada1)
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_arn": target_arn,
        }

    @builtins.property
    def target_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#target_arn LambdaFunction#target_arn}.'''
        result = self._values.get("target_arn")
        assert result is not None, "Required property 'target_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionDeadLetterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaFunctionDeadLetterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionDeadLetterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09650ae1babdb4834a24980cea78c6c1a52a6ade03fbb9d558e76495f6832add)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="targetArnInput")
    def target_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetArnInput"))

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))

    @target_arn.setter
    def target_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__385ce2d2be1aa12027f157064a094760d14ca79a4d1f8173a2051f22bd637c48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaFunctionDeadLetterConfig]:
        return typing.cast(typing.Optional[LambdaFunctionDeadLetterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaFunctionDeadLetterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f75e2e67b1fdfbeda81aad496b2a2f371aff6d59583f19d724832e4095361e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionDurableConfig",
    jsii_struct_bases=[],
    name_mapping={
        "execution_timeout": "executionTimeout",
        "retention_period": "retentionPeriod",
    },
)
class LambdaFunctionDurableConfig:
    def __init__(
        self,
        *,
        execution_timeout: jsii.Number,
        retention_period: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param execution_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#execution_timeout LambdaFunction#execution_timeout}.
        :param retention_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#retention_period LambdaFunction#retention_period}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef48f93a105558faf3f07bb46bc878758e16082046ae9aadaf263b96e849eab6)
            check_type(argname="argument execution_timeout", value=execution_timeout, expected_type=type_hints["execution_timeout"])
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execution_timeout": execution_timeout,
        }
        if retention_period is not None:
            self._values["retention_period"] = retention_period

    @builtins.property
    def execution_timeout(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#execution_timeout LambdaFunction#execution_timeout}.'''
        result = self._values.get("execution_timeout")
        assert result is not None, "Required property 'execution_timeout' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def retention_period(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#retention_period LambdaFunction#retention_period}.'''
        result = self._values.get("retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionDurableConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaFunctionDurableConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionDurableConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e07a28024d99be1918074d7241bb936505c0b0b4a4d49fba325e3b7b87b6ca77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRetentionPeriod")
    def reset_retention_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPeriod", []))

    @builtins.property
    @jsii.member(jsii_name="executionTimeoutInput")
    def execution_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "executionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodInput")
    def retention_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="executionTimeout")
    def execution_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "executionTimeout"))

    @execution_timeout.setter
    def execution_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe4e48dc561b387669aa956388d43bb3897cbe29f46c79e530dee8d7ac4e7a1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPeriod")
    def retention_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPeriod"))

    @retention_period.setter
    def retention_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d4a519a49b9b1f4a87020305e230b8fe636b3b187073d061569598cad9e6343)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaFunctionDurableConfig]:
        return typing.cast(typing.Optional[LambdaFunctionDurableConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaFunctionDurableConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef747f257f73587c7050aec3dad8b522fd1a0d0b653f11b59be53009d469bf28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionEnvironment",
    jsii_struct_bases=[],
    name_mapping={"variables": "variables"},
)
class LambdaFunctionEnvironment:
    def __init__(
        self,
        *,
        variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param variables: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#variables LambdaFunction#variables}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bd1e983cb8c70e81aa40991dfb620d6e296b20c2d87e47d24156bcc82337422)
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def variables(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#variables LambdaFunction#variables}.'''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionEnvironment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaFunctionEnvironmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionEnvironmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__460cc8140d99aaee7173ec987a6bf291cb5aefa2785d39138dc2bf00930afd3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetVariables")
    def reset_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariables", []))

    @builtins.property
    @jsii.member(jsii_name="variablesInput")
    def variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "variablesInput"))

    @builtins.property
    @jsii.member(jsii_name="variables")
    def variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "variables"))

    @variables.setter
    def variables(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cf6a97776e44ef8e3adcbe2c2c6deae0ee8f9e2283a54175b5c0bae0a31f86d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaFunctionEnvironment]:
        return typing.cast(typing.Optional[LambdaFunctionEnvironment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LambdaFunctionEnvironment]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3959d5d80d4c91ca6b2bd8c4a562e41618424ea81bfef07109732689467f9941)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionEphemeralStorage",
    jsii_struct_bases=[],
    name_mapping={"size": "size"},
)
class LambdaFunctionEphemeralStorage:
    def __init__(self, *, size: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#size LambdaFunction#size}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb78d596d06c4c6aeb48daabc6b769ea0d0f4f785fc70230300169b3d50107c)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if size is not None:
            self._values["size"] = size

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#size LambdaFunction#size}.'''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionEphemeralStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaFunctionEphemeralStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionEphemeralStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc04af79e9a5d7b13afc47d6b884a5310c20c25b66928cab5ab66cde9f514b13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f32da1e1ebdd103ad9f082918a0756338a9e18fa110606d0a3cc60f1228ecc87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaFunctionEphemeralStorage]:
        return typing.cast(typing.Optional[LambdaFunctionEphemeralStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaFunctionEphemeralStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c351b1d3a44e1087b48b67ac7e0c897c6133e42e2c18880f9023162a1531d37e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionFileSystemConfig",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn", "local_mount_path": "localMountPath"},
)
class LambdaFunctionFileSystemConfig:
    def __init__(self, *, arn: builtins.str, local_mount_path: builtins.str) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#arn LambdaFunction#arn}.
        :param local_mount_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#local_mount_path LambdaFunction#local_mount_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3fe280845a4e91dbe107a69c71271d93cf88948ad093cb0c5f60153592b5689)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument local_mount_path", value=local_mount_path, expected_type=type_hints["local_mount_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
            "local_mount_path": local_mount_path,
        }

    @builtins.property
    def arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#arn LambdaFunction#arn}.'''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_mount_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#local_mount_path LambdaFunction#local_mount_path}.'''
        result = self._values.get("local_mount_path")
        assert result is not None, "Required property 'local_mount_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionFileSystemConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaFunctionFileSystemConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionFileSystemConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d827df1514fb4236292cab719b5dabf61162ed86e9c74f5ec83d69ac4de1b7c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="arnInput")
    def arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arnInput"))

    @builtins.property
    @jsii.member(jsii_name="localMountPathInput")
    def local_mount_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localMountPathInput"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21557c512468baa81a3c5722d909da9bc411c91048866cd8468a6ea7199aeecb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localMountPath")
    def local_mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localMountPath"))

    @local_mount_path.setter
    def local_mount_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a8a16576edd76a6e2b8b5502ee5884398e7a014222d86be9281b9250f6d4446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localMountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaFunctionFileSystemConfig]:
        return typing.cast(typing.Optional[LambdaFunctionFileSystemConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaFunctionFileSystemConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb4a1169027a29bf9e9ea53683c21d3db526d9e53c2d3f8bf80ab9b1c8d5b5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionImageConfig",
    jsii_struct_bases=[],
    name_mapping={
        "command": "command",
        "entry_point": "entryPoint",
        "working_directory": "workingDirectory",
    },
)
class LambdaFunctionImageConfig:
    def __init__(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        entry_point: typing.Optional[typing.Sequence[builtins.str]] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#command LambdaFunction#command}.
        :param entry_point: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#entry_point LambdaFunction#entry_point}.
        :param working_directory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#working_directory LambdaFunction#working_directory}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58dae2761b0d26d0998f42fc034db7c245d862fd82cf05f52397b176b9c2a936)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument entry_point", value=entry_point, expected_type=type_hints["entry_point"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if command is not None:
            self._values["command"] = command
        if entry_point is not None:
            self._values["entry_point"] = entry_point
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#command LambdaFunction#command}.'''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def entry_point(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#entry_point LambdaFunction#entry_point}.'''
        result = self._values.get("entry_point")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#working_directory LambdaFunction#working_directory}.'''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionImageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaFunctionImageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionImageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df80d2924b0f05f75fca721afc944182a86fe634007a18cd48b383f3ac52d292)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetEntryPoint")
    def reset_entry_point(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntryPoint", []))

    @jsii.member(jsii_name="resetWorkingDirectory")
    def reset_working_directory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkingDirectory", []))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="entryPointInput")
    def entry_point_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "entryPointInput"))

    @builtins.property
    @jsii.member(jsii_name="workingDirectoryInput")
    def working_directory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workingDirectoryInput"))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a9b929d1d6f9b6ebce3f372a87b101b7da36a92913892d8a8947e2eb618b000)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entryPoint")
    def entry_point(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "entryPoint"))

    @entry_point.setter
    def entry_point(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1633b7bf84e1fea975cd9024fbf68d0b416b773315639dc9aac64eca23e5fa3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entryPoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workingDirectory")
    def working_directory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workingDirectory"))

    @working_directory.setter
    def working_directory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fe2d4f5543722a821bd70f3ea39ff4a271bfd3791d837ea458c3bb113febdaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workingDirectory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaFunctionImageConfig]:
        return typing.cast(typing.Optional[LambdaFunctionImageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LambdaFunctionImageConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d3fb60a81c9b8d9b009665e4d39889ebd548b7d135b2fc0b48f6ba7e00639f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "log_format": "logFormat",
        "application_log_level": "applicationLogLevel",
        "log_group": "logGroup",
        "system_log_level": "systemLogLevel",
    },
)
class LambdaFunctionLoggingConfig:
    def __init__(
        self,
        *,
        log_format: builtins.str,
        application_log_level: typing.Optional[builtins.str] = None,
        log_group: typing.Optional[builtins.str] = None,
        system_log_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#log_format LambdaFunction#log_format}.
        :param application_log_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#application_log_level LambdaFunction#application_log_level}.
        :param log_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#log_group LambdaFunction#log_group}.
        :param system_log_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#system_log_level LambdaFunction#system_log_level}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eef8f622da6a4ab047cdd4030a9b4d2f9d3962837837d8a86b40acf18e7f591a)
            check_type(argname="argument log_format", value=log_format, expected_type=type_hints["log_format"])
            check_type(argname="argument application_log_level", value=application_log_level, expected_type=type_hints["application_log_level"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument system_log_level", value=system_log_level, expected_type=type_hints["system_log_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_format": log_format,
        }
        if application_log_level is not None:
            self._values["application_log_level"] = application_log_level
        if log_group is not None:
            self._values["log_group"] = log_group
        if system_log_level is not None:
            self._values["system_log_level"] = system_log_level

    @builtins.property
    def log_format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#log_format LambdaFunction#log_format}.'''
        result = self._values.get("log_format")
        assert result is not None, "Required property 'log_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_log_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#application_log_level LambdaFunction#application_log_level}.'''
        result = self._values.get("application_log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#log_group LambdaFunction#log_group}.'''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def system_log_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#system_log_level LambdaFunction#system_log_level}.'''
        result = self._values.get("system_log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaFunctionLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abc378ac5cffc16f6751adcfd79958bf7ebee01e33d8f9502c455932e6249a25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetApplicationLogLevel")
    def reset_application_log_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationLogLevel", []))

    @jsii.member(jsii_name="resetLogGroup")
    def reset_log_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroup", []))

    @jsii.member(jsii_name="resetSystemLogLevel")
    def reset_system_log_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemLogLevel", []))

    @builtins.property
    @jsii.member(jsii_name="applicationLogLevelInput")
    def application_log_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationLogLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="logFormatInput")
    def log_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupInput")
    def log_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="systemLogLevelInput")
    def system_log_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "systemLogLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationLogLevel")
    def application_log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationLogLevel"))

    @application_log_level.setter
    def application_log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e9ba1854db252386d1b67d3f770f479945f79e01a10971f4db37cc036d76a62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationLogLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logFormat")
    def log_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logFormat"))

    @log_format.setter
    def log_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e952c377f0213113594a924f5ddf651ee862b460686889f72e54bdad22e3764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroup"))

    @log_group.setter
    def log_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ea6afd45666d1c77ee87be53459c24cbb1fdbadea6f6500e7424bf85708c983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemLogLevel")
    def system_log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemLogLevel"))

    @system_log_level.setter
    def system_log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__246a6ffe7ed551fca7f4946e67ac87bd4fb2caf64e166b97d6e95000c83d8732)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemLogLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaFunctionLoggingConfig]:
        return typing.cast(typing.Optional[LambdaFunctionLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaFunctionLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f71133246a049b74112d34391ff3cf69e8a81b9176c783e8a0810c77ea81a7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionSnapStart",
    jsii_struct_bases=[],
    name_mapping={"apply_on": "applyOn"},
)
class LambdaFunctionSnapStart:
    def __init__(self, *, apply_on: builtins.str) -> None:
        '''
        :param apply_on: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#apply_on LambdaFunction#apply_on}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a20d4394cf72a007046e0bbcc6638544b3c88eacf5868a4410ea7843284c60ae)
            check_type(argname="argument apply_on", value=apply_on, expected_type=type_hints["apply_on"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "apply_on": apply_on,
        }

    @builtins.property
    def apply_on(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#apply_on LambdaFunction#apply_on}.'''
        result = self._values.get("apply_on")
        assert result is not None, "Required property 'apply_on' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionSnapStart(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaFunctionSnapStartOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionSnapStartOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8947fe303ca6b4703bfaa059c68943a7f27feaeb65f436c8b965b874177a279f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="optimizationStatus")
    def optimization_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "optimizationStatus"))

    @builtins.property
    @jsii.member(jsii_name="applyOnInput")
    def apply_on_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applyOnInput"))

    @builtins.property
    @jsii.member(jsii_name="applyOn")
    def apply_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applyOn"))

    @apply_on.setter
    def apply_on(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a04ba411dab3a3919cc6b193c240b41b2c7679548cd82e62e3d576e88fedb0ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applyOn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaFunctionSnapStart]:
        return typing.cast(typing.Optional[LambdaFunctionSnapStart], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LambdaFunctionSnapStart]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b30262192d87175a40bd1f4069c13670e212d11833f5a4f2f9e800a11a7711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionTenancyConfig",
    jsii_struct_bases=[],
    name_mapping={"tenant_isolation_mode": "tenantIsolationMode"},
)
class LambdaFunctionTenancyConfig:
    def __init__(self, *, tenant_isolation_mode: builtins.str) -> None:
        '''
        :param tenant_isolation_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#tenant_isolation_mode LambdaFunction#tenant_isolation_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75af30ed60411b8d320d6264456f14fa761fa0c61fb1251331bd9f4d341ef30b)
            check_type(argname="argument tenant_isolation_mode", value=tenant_isolation_mode, expected_type=type_hints["tenant_isolation_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tenant_isolation_mode": tenant_isolation_mode,
        }

    @builtins.property
    def tenant_isolation_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#tenant_isolation_mode LambdaFunction#tenant_isolation_mode}.'''
        result = self._values.get("tenant_isolation_mode")
        assert result is not None, "Required property 'tenant_isolation_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionTenancyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaFunctionTenancyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionTenancyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31e360e4165acea82d85a317c98765491dac6f44b7f149c70525ac062b67b526)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="tenantIsolationModeInput")
    def tenant_isolation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIsolationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIsolationMode")
    def tenant_isolation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantIsolationMode"))

    @tenant_isolation_mode.setter
    def tenant_isolation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0319dad7ce9c6f4fb788dbdd611ffbd27b93462055d9ebffce2d842427ed85a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantIsolationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaFunctionTenancyConfig]:
        return typing.cast(typing.Optional[LambdaFunctionTenancyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaFunctionTenancyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ac357f195c6e0c82476d6b75a03bc3299a80e74bdaef77b61b503bc072adf9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class LambdaFunctionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#create LambdaFunction#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#delete LambdaFunction#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#update LambdaFunction#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fdffd628c4bca95ae48e0fa256fb2478b9e0407f8f12939f5a37868181c3edf)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#create LambdaFunction#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#delete LambdaFunction#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#update LambdaFunction#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaFunctionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94cb53f14a1774dee189082bb15fe72a78b79e8b15f824b6ea5e734b87a47ded)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a54271d74bbd2f401fdd6cbbd8d94130cb12331a08f3256b6a0937ac9b202799)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c340807d6ed834272400457d35751bec2da5e60898257a1381a75d0c9c6a639)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e142eadfc3dba3d449b95be1432155fa7e8eebd80e03132eb31d38318f75ce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaFunctionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaFunctionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaFunctionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fff9ec1d237aa92ba239af9e37d52a16b0feacb21809f655668591fdbe25ed9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionTracingConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode"},
)
class LambdaFunctionTracingConfig:
    def __init__(self, *, mode: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#mode LambdaFunction#mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d574178eaf19ad657a9a4653cb4b69943ae04edeb337e00fcd965a0bad94730)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#mode LambdaFunction#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionTracingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaFunctionTracingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionTracingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__533a78480848545b41c5b48653ab50705df4ceaef1623eec5cdbaf48e9a1e161)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a5caa02fedf7d00a4da87f01d1b7e11195109abb65530f4e0fdc82b6fba4597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaFunctionTracingConfig]:
        return typing.cast(typing.Optional[LambdaFunctionTracingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaFunctionTracingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e350f4a3b4fd4616755da924ecfc49d7d1b54873853527caeca5aa0fa8df26bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionVpcConfig",
    jsii_struct_bases=[],
    name_mapping={
        "security_group_ids": "securityGroupIds",
        "subnet_ids": "subnetIds",
        "ipv6_allowed_for_dual_stack": "ipv6AllowedForDualStack",
    },
)
class LambdaFunctionVpcConfig:
    def __init__(
        self,
        *,
        security_group_ids: typing.Sequence[builtins.str],
        subnet_ids: typing.Sequence[builtins.str],
        ipv6_allowed_for_dual_stack: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#security_group_ids LambdaFunction#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#subnet_ids LambdaFunction#subnet_ids}.
        :param ipv6_allowed_for_dual_stack: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#ipv6_allowed_for_dual_stack LambdaFunction#ipv6_allowed_for_dual_stack}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58093b50dc57561eed10cc00d3e046dcacc93568e31200abb6545702e6ba675)
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument ipv6_allowed_for_dual_stack", value=ipv6_allowed_for_dual_stack, expected_type=type_hints["ipv6_allowed_for_dual_stack"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "security_group_ids": security_group_ids,
            "subnet_ids": subnet_ids,
        }
        if ipv6_allowed_for_dual_stack is not None:
            self._values["ipv6_allowed_for_dual_stack"] = ipv6_allowed_for_dual_stack

    @builtins.property
    def security_group_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#security_group_ids LambdaFunction#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        assert result is not None, "Required property 'security_group_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#subnet_ids LambdaFunction#subnet_ids}.'''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def ipv6_allowed_for_dual_stack(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_function#ipv6_allowed_for_dual_stack LambdaFunction#ipv6_allowed_for_dual_stack}.'''
        result = self._values.get("ipv6_allowed_for_dual_stack")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionVpcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaFunctionVpcConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaFunction.LambdaFunctionVpcConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fbc88acecf3f48659349e6aab7ec7cd47194758e433a263ccfee3bf6988e42b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIpv6AllowedForDualStack")
    def reset_ipv6_allowed_for_dual_stack(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6AllowedForDualStack", []))

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @builtins.property
    @jsii.member(jsii_name="ipv6AllowedForDualStackInput")
    def ipv6_allowed_for_dual_stack_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ipv6AllowedForDualStackInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdsInput")
    def subnet_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6AllowedForDualStack")
    def ipv6_allowed_for_dual_stack(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ipv6AllowedForDualStack"))

    @ipv6_allowed_for_dual_stack.setter
    def ipv6_allowed_for_dual_stack(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa2f455a1de84fe4425233d0d339d0f2657b9c149142ca9911dda21533a1709)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6AllowedForDualStack", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c45fca8650bf01605061516426bf9383e85fb738f6df033fad7bad30b545b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c0a6b2786233a3ff7b4dfc6937617fff5a9e699300676d857b71d6a4d9ee45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaFunctionVpcConfig]:
        return typing.cast(typing.Optional[LambdaFunctionVpcConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LambdaFunctionVpcConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aff521f964770fd120bae72bdd179b1cb32e807930ebbad541de397edefa40c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LambdaFunction",
    "LambdaFunctionCapacityProviderConfig",
    "LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfig",
    "LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfigOutputReference",
    "LambdaFunctionCapacityProviderConfigOutputReference",
    "LambdaFunctionConfig",
    "LambdaFunctionDeadLetterConfig",
    "LambdaFunctionDeadLetterConfigOutputReference",
    "LambdaFunctionDurableConfig",
    "LambdaFunctionDurableConfigOutputReference",
    "LambdaFunctionEnvironment",
    "LambdaFunctionEnvironmentOutputReference",
    "LambdaFunctionEphemeralStorage",
    "LambdaFunctionEphemeralStorageOutputReference",
    "LambdaFunctionFileSystemConfig",
    "LambdaFunctionFileSystemConfigOutputReference",
    "LambdaFunctionImageConfig",
    "LambdaFunctionImageConfigOutputReference",
    "LambdaFunctionLoggingConfig",
    "LambdaFunctionLoggingConfigOutputReference",
    "LambdaFunctionSnapStart",
    "LambdaFunctionSnapStartOutputReference",
    "LambdaFunctionTenancyConfig",
    "LambdaFunctionTenancyConfigOutputReference",
    "LambdaFunctionTimeouts",
    "LambdaFunctionTimeoutsOutputReference",
    "LambdaFunctionTracingConfig",
    "LambdaFunctionTracingConfigOutputReference",
    "LambdaFunctionVpcConfig",
    "LambdaFunctionVpcConfigOutputReference",
]

publication.publish()

def _typecheckingstub__2f9f9bcc20c47302251ac3342669dea0f494d535b5ac68a155e82e28d3c2ea17(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    function_name: builtins.str,
    role: builtins.str,
    architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
    capacity_provider_config: typing.Optional[typing.Union[LambdaFunctionCapacityProviderConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    code_sha256: typing.Optional[builtins.str] = None,
    code_signing_config_arn: typing.Optional[builtins.str] = None,
    dead_letter_config: typing.Optional[typing.Union[LambdaFunctionDeadLetterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    durable_config: typing.Optional[typing.Union[LambdaFunctionDurableConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    environment: typing.Optional[typing.Union[LambdaFunctionEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
    ephemeral_storage: typing.Optional[typing.Union[LambdaFunctionEphemeralStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    filename: typing.Optional[builtins.str] = None,
    file_system_config: typing.Optional[typing.Union[LambdaFunctionFileSystemConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    handler: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_config: typing.Optional[typing.Union[LambdaFunctionImageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    image_uri: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    layers: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_config: typing.Optional[typing.Union[LambdaFunctionLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    package_type: typing.Optional[builtins.str] = None,
    publish: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    publish_to: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    replacement_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    replace_security_groups_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    runtime: typing.Optional[builtins.str] = None,
    s3_bucket: typing.Optional[builtins.str] = None,
    s3_key: typing.Optional[builtins.str] = None,
    s3_object_version: typing.Optional[builtins.str] = None,
    skip_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    snap_start: typing.Optional[typing.Union[LambdaFunctionSnapStart, typing.Dict[builtins.str, typing.Any]]] = None,
    source_code_hash: typing.Optional[builtins.str] = None,
    source_kms_key_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tenancy_config: typing.Optional[typing.Union[LambdaFunctionTenancyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[LambdaFunctionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tracing_config: typing.Optional[typing.Union[LambdaFunctionTracingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_config: typing.Optional[typing.Union[LambdaFunctionVpcConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2d28da6e72ad207e96695858d0ca907a9068ff320f420e8e9e79a677f3bd14c7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0081b8d150f56d0e6e196e56f61a81a2a08ea1461e3b5bdaa987a584896ccbd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56eb329d4b0e107459619e8a8ec4b1c3280281b58df979365a837fbeddc7192f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__255423580eb4164e4067be8426d32cb890fd4006ca1937128af94f2b3b9c3aab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3efa727e0be1fa73870655f616a931a8cbe655c0826d04e576fb804be5584d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59562d31349ea4751740db083dc2137a727adb076b1e153a791c04a88a0133e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e08a264e672efd6f49b16083341d0be13e145696cbebd089bf8d028374928ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a13ac45377f4e06db0fea0f9600c018fae32bd093f6334f642a811fe7f3f9b3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced7a49bfb5335d9b92d76c2ad497d1ebbbb33a06e57547c1029dbf94c3f9fbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d3ea7ad035e957376518b62e2e6cdbee03e89929144ea5efed760f31098da1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__245280a466adb36f3dfc51a7dd1b2204b82db8f1a57e4f7d435e1b37e38d2649(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e6105b91df61cbfac1623c615903e5fbb456b0d2a842cd077d030f3509453a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2431e04a597c3c59b9398fda096bb6107e8e6fd71e6f799988d27322096073(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a27d57941d5e8f5af6ff066e9280a8b28ceeb1d4361c77139af0535a7dc9f2a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca00244dac88e84b521b417cd9901b5b0a78979df4902f07b10b1e52d7bfa8e6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0593ce93cea0791919a9e64dbd23fd7c402fa02567305eeb7544841b14268c14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa43a95b0488ad520b21c56f6ef54127b8a4029e8d10900f737426224511c64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ecf9039032d6de31da9ede5891d177341dcd3f4b4719338a3946556d2582b3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08a552ee9ca2f9a5a0b68bc82049c7f2ab70650da88f3cd32576d50d8782f65d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8b567f3d538aedea3645f623e4c9b1723db8ce227ad1ac093ec85541756226(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5e59942de33b413b2e04205e025ec2432f7b9b889d0443f41f205a85872f6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e718c2909dff752640be4ee82851fdf016c591db09b03ef736d95769a8ad3f22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5829134c55180c4e28fcf5013c28a8e13b697cfc231fcddbc90ce204dd5495(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a257ef37137b57c9e9b0f5317ab2a0cfbe9f1dd904740522fa3bac9fefd8c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb3d8614e1fe9d724fb23f6da9e35775e07bb80b16eaa916f1303bfb1329081b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e13d3f8110dd4fcd8a9382dbda5555dc1deac95baba0c4d5c69a1f27195ead40(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5fc937621a98551aba9673abaaebe7638018b79ba627faebde58cf5eb7db42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee87c9fd6d4dde163d87dda42c4960c029adc1af1ab84a3770b2874542b740f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d28e9873b46954b35d8794e436608ce9203d80b66e84ade4c5f2c90d07ef4b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978d880d95909bd18b3cc9f596b744b8de46d5cc7d0b8c8934c6e4a16e5efceb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c11951df6d6331d97b98333de696a5449fe295b83d1e167f19920548f35243e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05b1e1e5f5a3d3670ec304766b092fd7504e0a5f021179b4335e6921fa5610be(
    *,
    lambda_managed_instances_capacity_provider_config: typing.Union[LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d52ce5e6eb13449bc274f433e23b84abc8537404418e85d78a9cb0d3842e29(
    *,
    capacity_provider_arn: builtins.str,
    execution_environment_memory_gib_per_vcpu: typing.Optional[jsii.Number] = None,
    per_execution_environment_max_concurrency: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f8e34d406fda01b6602e9355d3287cb7d0ae9a0245b5cce518d68c07f1f5961(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee838436c1827309bb2223d38f269cc86f99cf6bdb4446efb67d2bcc87752a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9652d173eba79a23a5e77fe9a7e4760c73d2a63a16aabe74434eb8c5156db192(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c635b0766fa6629bb60462073e6e7572ad738f4f904f38dabcb30b809cfdcd8e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43259731ec17b4e4569a569da7844b0bbc5912eb18f877159e48eb3e7529b923(
    value: typing.Optional[LambdaFunctionCapacityProviderConfigLambdaManagedInstancesCapacityProviderConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8fcb4628e407ff2f3ef91eb9475787cea025c5591cb11aed3b8ea27b1348c2c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b5c26644702b4b7203cc303a1914df18fb3393a0b8b700779388d84086e87f8(
    value: typing.Optional[LambdaFunctionCapacityProviderConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d146b73e2024d599b61cb4863166738c3f18d097865dd8af3728961976b17466(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    function_name: builtins.str,
    role: builtins.str,
    architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
    capacity_provider_config: typing.Optional[typing.Union[LambdaFunctionCapacityProviderConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    code_sha256: typing.Optional[builtins.str] = None,
    code_signing_config_arn: typing.Optional[builtins.str] = None,
    dead_letter_config: typing.Optional[typing.Union[LambdaFunctionDeadLetterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    durable_config: typing.Optional[typing.Union[LambdaFunctionDurableConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    environment: typing.Optional[typing.Union[LambdaFunctionEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
    ephemeral_storage: typing.Optional[typing.Union[LambdaFunctionEphemeralStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    filename: typing.Optional[builtins.str] = None,
    file_system_config: typing.Optional[typing.Union[LambdaFunctionFileSystemConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    handler: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_config: typing.Optional[typing.Union[LambdaFunctionImageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    image_uri: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    layers: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_config: typing.Optional[typing.Union[LambdaFunctionLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    package_type: typing.Optional[builtins.str] = None,
    publish: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    publish_to: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    replacement_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    replace_security_groups_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    runtime: typing.Optional[builtins.str] = None,
    s3_bucket: typing.Optional[builtins.str] = None,
    s3_key: typing.Optional[builtins.str] = None,
    s3_object_version: typing.Optional[builtins.str] = None,
    skip_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    snap_start: typing.Optional[typing.Union[LambdaFunctionSnapStart, typing.Dict[builtins.str, typing.Any]]] = None,
    source_code_hash: typing.Optional[builtins.str] = None,
    source_kms_key_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tenancy_config: typing.Optional[typing.Union[LambdaFunctionTenancyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[LambdaFunctionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tracing_config: typing.Optional[typing.Union[LambdaFunctionTracingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_config: typing.Optional[typing.Union[LambdaFunctionVpcConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c466c792358aca96c9cc91ce5c999c2e731d572dfc31e48c649b9f2d324ada1(
    *,
    target_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09650ae1babdb4834a24980cea78c6c1a52a6ade03fbb9d558e76495f6832add(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__385ce2d2be1aa12027f157064a094760d14ca79a4d1f8173a2051f22bd637c48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f75e2e67b1fdfbeda81aad496b2a2f371aff6d59583f19d724832e4095361e(
    value: typing.Optional[LambdaFunctionDeadLetterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef48f93a105558faf3f07bb46bc878758e16082046ae9aadaf263b96e849eab6(
    *,
    execution_timeout: jsii.Number,
    retention_period: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07a28024d99be1918074d7241bb936505c0b0b4a4d49fba325e3b7b87b6ca77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4e48dc561b387669aa956388d43bb3897cbe29f46c79e530dee8d7ac4e7a1d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d4a519a49b9b1f4a87020305e230b8fe636b3b187073d061569598cad9e6343(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef747f257f73587c7050aec3dad8b522fd1a0d0b653f11b59be53009d469bf28(
    value: typing.Optional[LambdaFunctionDurableConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bd1e983cb8c70e81aa40991dfb620d6e296b20c2d87e47d24156bcc82337422(
    *,
    variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460cc8140d99aaee7173ec987a6bf291cb5aefa2785d39138dc2bf00930afd3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf6a97776e44ef8e3adcbe2c2c6deae0ee8f9e2283a54175b5c0bae0a31f86d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3959d5d80d4c91ca6b2bd8c4a562e41618424ea81bfef07109732689467f9941(
    value: typing.Optional[LambdaFunctionEnvironment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb78d596d06c4c6aeb48daabc6b769ea0d0f4f785fc70230300169b3d50107c(
    *,
    size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc04af79e9a5d7b13afc47d6b884a5310c20c25b66928cab5ab66cde9f514b13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32da1e1ebdd103ad9f082918a0756338a9e18fa110606d0a3cc60f1228ecc87(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c351b1d3a44e1087b48b67ac7e0c897c6133e42e2c18880f9023162a1531d37e(
    value: typing.Optional[LambdaFunctionEphemeralStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3fe280845a4e91dbe107a69c71271d93cf88948ad093cb0c5f60153592b5689(
    *,
    arn: builtins.str,
    local_mount_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d827df1514fb4236292cab719b5dabf61162ed86e9c74f5ec83d69ac4de1b7c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21557c512468baa81a3c5722d909da9bc411c91048866cd8468a6ea7199aeecb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a8a16576edd76a6e2b8b5502ee5884398e7a014222d86be9281b9250f6d4446(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb4a1169027a29bf9e9ea53683c21d3db526d9e53c2d3f8bf80ab9b1c8d5b5b(
    value: typing.Optional[LambdaFunctionFileSystemConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58dae2761b0d26d0998f42fc034db7c245d862fd82cf05f52397b176b9c2a936(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    entry_point: typing.Optional[typing.Sequence[builtins.str]] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df80d2924b0f05f75fca721afc944182a86fe634007a18cd48b383f3ac52d292(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9b929d1d6f9b6ebce3f372a87b101b7da36a92913892d8a8947e2eb618b000(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1633b7bf84e1fea975cd9024fbf68d0b416b773315639dc9aac64eca23e5fa3b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe2d4f5543722a821bd70f3ea39ff4a271bfd3791d837ea458c3bb113febdaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d3fb60a81c9b8d9b009665e4d39889ebd548b7d135b2fc0b48f6ba7e00639f(
    value: typing.Optional[LambdaFunctionImageConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef8f622da6a4ab047cdd4030a9b4d2f9d3962837837d8a86b40acf18e7f591a(
    *,
    log_format: builtins.str,
    application_log_level: typing.Optional[builtins.str] = None,
    log_group: typing.Optional[builtins.str] = None,
    system_log_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc378ac5cffc16f6751adcfd79958bf7ebee01e33d8f9502c455932e6249a25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e9ba1854db252386d1b67d3f770f479945f79e01a10971f4db37cc036d76a62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e952c377f0213113594a924f5ddf651ee862b460686889f72e54bdad22e3764(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea6afd45666d1c77ee87be53459c24cbb1fdbadea6f6500e7424bf85708c983(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__246a6ffe7ed551fca7f4946e67ac87bd4fb2caf64e166b97d6e95000c83d8732(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f71133246a049b74112d34391ff3cf69e8a81b9176c783e8a0810c77ea81a7e(
    value: typing.Optional[LambdaFunctionLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a20d4394cf72a007046e0bbcc6638544b3c88eacf5868a4410ea7843284c60ae(
    *,
    apply_on: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8947fe303ca6b4703bfaa059c68943a7f27feaeb65f436c8b965b874177a279f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04ba411dab3a3919cc6b193c240b41b2c7679548cd82e62e3d576e88fedb0ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b30262192d87175a40bd1f4069c13670e212d11833f5a4f2f9e800a11a7711(
    value: typing.Optional[LambdaFunctionSnapStart],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75af30ed60411b8d320d6264456f14fa761fa0c61fb1251331bd9f4d341ef30b(
    *,
    tenant_isolation_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e360e4165acea82d85a317c98765491dac6f44b7f149c70525ac062b67b526(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0319dad7ce9c6f4fb788dbdd611ffbd27b93462055d9ebffce2d842427ed85a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac357f195c6e0c82476d6b75a03bc3299a80e74bdaef77b61b503bc072adf9c(
    value: typing.Optional[LambdaFunctionTenancyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fdffd628c4bca95ae48e0fa256fb2478b9e0407f8f12939f5a37868181c3edf(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94cb53f14a1774dee189082bb15fe72a78b79e8b15f824b6ea5e734b87a47ded(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54271d74bbd2f401fdd6cbbd8d94130cb12331a08f3256b6a0937ac9b202799(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c340807d6ed834272400457d35751bec2da5e60898257a1381a75d0c9c6a639(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e142eadfc3dba3d449b95be1432155fa7e8eebd80e03132eb31d38318f75ce3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fff9ec1d237aa92ba239af9e37d52a16b0feacb21809f655668591fdbe25ed9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaFunctionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d574178eaf19ad657a9a4653cb4b69943ae04edeb337e00fcd965a0bad94730(
    *,
    mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__533a78480848545b41c5b48653ab50705df4ceaef1623eec5cdbaf48e9a1e161(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5caa02fedf7d00a4da87f01d1b7e11195109abb65530f4e0fdc82b6fba4597(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e350f4a3b4fd4616755da924ecfc49d7d1b54873853527caeca5aa0fa8df26bc(
    value: typing.Optional[LambdaFunctionTracingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58093b50dc57561eed10cc00d3e046dcacc93568e31200abb6545702e6ba675(
    *,
    security_group_ids: typing.Sequence[builtins.str],
    subnet_ids: typing.Sequence[builtins.str],
    ipv6_allowed_for_dual_stack: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fbc88acecf3f48659349e6aab7ec7cd47194758e433a263ccfee3bf6988e42b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa2f455a1de84fe4425233d0d339d0f2657b9c149142ca9911dda21533a1709(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c45fca8650bf01605061516426bf9383e85fb738f6df033fad7bad30b545b39(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c0a6b2786233a3ff7b4dfc6937617fff5a9e699300676d857b71d6a4d9ee45(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff521f964770fd120bae72bdd179b1cb32e807930ebbad541de397edefa40c6(
    value: typing.Optional[LambdaFunctionVpcConfig],
) -> None:
    """Type checking stubs"""
    pass
