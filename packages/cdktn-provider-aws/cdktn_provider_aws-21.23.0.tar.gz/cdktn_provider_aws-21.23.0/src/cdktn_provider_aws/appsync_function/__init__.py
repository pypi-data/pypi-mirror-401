r'''
# `aws_appsync_function`

Refer to the Terraform Registry for docs: [`aws_appsync_function`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function).
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


class AppsyncFunction(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appsyncFunction.AppsyncFunction",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function aws_appsync_function}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        api_id: builtins.str,
        data_source: builtins.str,
        name: builtins.str,
        code: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        function_version: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_batch_size: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        request_mapping_template: typing.Optional[builtins.str] = None,
        response_mapping_template: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[typing.Union["AppsyncFunctionRuntime", typing.Dict[builtins.str, typing.Any]]] = None,
        sync_config: typing.Optional[typing.Union["AppsyncFunctionSyncConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function aws_appsync_function} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#api_id AppsyncFunction#api_id}.
        :param data_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#data_source AppsyncFunction#data_source}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#name AppsyncFunction#name}.
        :param code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#code AppsyncFunction#code}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#description AppsyncFunction#description}.
        :param function_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#function_version AppsyncFunction#function_version}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#id AppsyncFunction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#max_batch_size AppsyncFunction#max_batch_size}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#region AppsyncFunction#region}
        :param request_mapping_template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#request_mapping_template AppsyncFunction#request_mapping_template}.
        :param response_mapping_template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#response_mapping_template AppsyncFunction#response_mapping_template}.
        :param runtime: runtime block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#runtime AppsyncFunction#runtime}
        :param sync_config: sync_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#sync_config AppsyncFunction#sync_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d73923a51e9f964e2f07064bda096e8e71808c1eef0fcd8c35fded8c002328)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppsyncFunctionConfig(
            api_id=api_id,
            data_source=data_source,
            name=name,
            code=code,
            description=description,
            function_version=function_version,
            id=id,
            max_batch_size=max_batch_size,
            region=region,
            request_mapping_template=request_mapping_template,
            response_mapping_template=response_mapping_template,
            runtime=runtime,
            sync_config=sync_config,
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
        '''Generates CDKTF code for importing a AppsyncFunction resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppsyncFunction to import.
        :param import_from_id: The id of the existing AppsyncFunction that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppsyncFunction to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8903f2ab2778c2e67731eba214f2cbb3903c656bcb05f3989ae79340789ba656)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRuntime")
    def put_runtime(self, *, name: builtins.str, runtime_version: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#name AppsyncFunction#name}.
        :param runtime_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#runtime_version AppsyncFunction#runtime_version}.
        '''
        value = AppsyncFunctionRuntime(name=name, runtime_version=runtime_version)

        return typing.cast(None, jsii.invoke(self, "putRuntime", [value]))

    @jsii.member(jsii_name="putSyncConfig")
    def put_sync_config(
        self,
        *,
        conflict_detection: typing.Optional[builtins.str] = None,
        conflict_handler: typing.Optional[builtins.str] = None,
        lambda_conflict_handler_config: typing.Optional[typing.Union["AppsyncFunctionSyncConfigLambdaConflictHandlerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param conflict_detection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#conflict_detection AppsyncFunction#conflict_detection}.
        :param conflict_handler: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#conflict_handler AppsyncFunction#conflict_handler}.
        :param lambda_conflict_handler_config: lambda_conflict_handler_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#lambda_conflict_handler_config AppsyncFunction#lambda_conflict_handler_config}
        '''
        value = AppsyncFunctionSyncConfig(
            conflict_detection=conflict_detection,
            conflict_handler=conflict_handler,
            lambda_conflict_handler_config=lambda_conflict_handler_config,
        )

        return typing.cast(None, jsii.invoke(self, "putSyncConfig", [value]))

    @jsii.member(jsii_name="resetCode")
    def reset_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCode", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFunctionVersion")
    def reset_function_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunctionVersion", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaxBatchSize")
    def reset_max_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxBatchSize", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRequestMappingTemplate")
    def reset_request_mapping_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestMappingTemplate", []))

    @jsii.member(jsii_name="resetResponseMappingTemplate")
    def reset_response_mapping_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseMappingTemplate", []))

    @jsii.member(jsii_name="resetRuntime")
    def reset_runtime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntime", []))

    @jsii.member(jsii_name="resetSyncConfig")
    def reset_sync_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncConfig", []))

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
    @jsii.member(jsii_name="functionId")
    def function_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionId"))

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> "AppsyncFunctionRuntimeOutputReference":
        return typing.cast("AppsyncFunctionRuntimeOutputReference", jsii.get(self, "runtime"))

    @builtins.property
    @jsii.member(jsii_name="syncConfig")
    def sync_config(self) -> "AppsyncFunctionSyncConfigOutputReference":
        return typing.cast("AppsyncFunctionSyncConfigOutputReference", jsii.get(self, "syncConfig"))

    @builtins.property
    @jsii.member(jsii_name="apiIdInput")
    def api_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiIdInput"))

    @builtins.property
    @jsii.member(jsii_name="codeInput")
    def code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codeInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceInput")
    def data_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="functionVersionInput")
    def function_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maxBatchSizeInput")
    def max_batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxBatchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="requestMappingTemplateInput")
    def request_mapping_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestMappingTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="responseMappingTemplateInput")
    def response_mapping_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseMappingTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeInput")
    def runtime_input(self) -> typing.Optional["AppsyncFunctionRuntime"]:
        return typing.cast(typing.Optional["AppsyncFunctionRuntime"], jsii.get(self, "runtimeInput"))

    @builtins.property
    @jsii.member(jsii_name="syncConfigInput")
    def sync_config_input(self) -> typing.Optional["AppsyncFunctionSyncConfig"]:
        return typing.cast(typing.Optional["AppsyncFunctionSyncConfig"], jsii.get(self, "syncConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae59e3d0356ec7514c5a177413048ce0fefd111b41b640f53e34d111dfc57b79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "code"))

    @code.setter
    def code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a0c703519f7c694662e7ca5d93e3492867560e6e030dd43bbebfe56f08d98c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataSource")
    def data_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSource"))

    @data_source.setter
    def data_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23400292df0377f3708b59c30c2b1919d629291cc5c77e2af0b8f860a838607d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ee8bb39f2b55c0ba2c7659c26fa84fb10d37f91938f718fb31a360ecb21f158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionVersion")
    def function_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionVersion"))

    @function_version.setter
    def function_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b8777baea348f046332661ee1c39d5e627399d489d23146718ae49a16c088e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2a006fb115616df0fc1c76fc1f83fecfcf40f34084a8883ebccda1f922dba70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxBatchSize")
    def max_batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxBatchSize"))

    @max_batch_size.setter
    def max_batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__511e03051facbd46d3a64275b164991b6fd316758362930aff150c7e73f6b5d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBatchSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0714bcec271a76dda8780d19a184cc6ea7a3aa4c5e08f6ea103a456d0a472e94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5017b2c6c5f935394de70950b91b1ad61b5cc1ab46713fc6a6e3cad4087e61c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestMappingTemplate")
    def request_mapping_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestMappingTemplate"))

    @request_mapping_template.setter
    def request_mapping_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5953d237a177620d96f18ec20b12d343c7708c9dc8fa08ac6b3c3569e472936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestMappingTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseMappingTemplate")
    def response_mapping_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseMappingTemplate"))

    @response_mapping_template.setter
    def response_mapping_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ca810a3fc9ec915a0a7f5d19c6b4e235badfc7e80854d44771dc92633006dea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseMappingTemplate", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appsyncFunction.AppsyncFunctionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "api_id": "apiId",
        "data_source": "dataSource",
        "name": "name",
        "code": "code",
        "description": "description",
        "function_version": "functionVersion",
        "id": "id",
        "max_batch_size": "maxBatchSize",
        "region": "region",
        "request_mapping_template": "requestMappingTemplate",
        "response_mapping_template": "responseMappingTemplate",
        "runtime": "runtime",
        "sync_config": "syncConfig",
    },
)
class AppsyncFunctionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        api_id: builtins.str,
        data_source: builtins.str,
        name: builtins.str,
        code: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        function_version: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_batch_size: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        request_mapping_template: typing.Optional[builtins.str] = None,
        response_mapping_template: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[typing.Union["AppsyncFunctionRuntime", typing.Dict[builtins.str, typing.Any]]] = None,
        sync_config: typing.Optional[typing.Union["AppsyncFunctionSyncConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param api_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#api_id AppsyncFunction#api_id}.
        :param data_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#data_source AppsyncFunction#data_source}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#name AppsyncFunction#name}.
        :param code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#code AppsyncFunction#code}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#description AppsyncFunction#description}.
        :param function_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#function_version AppsyncFunction#function_version}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#id AppsyncFunction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#max_batch_size AppsyncFunction#max_batch_size}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#region AppsyncFunction#region}
        :param request_mapping_template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#request_mapping_template AppsyncFunction#request_mapping_template}.
        :param response_mapping_template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#response_mapping_template AppsyncFunction#response_mapping_template}.
        :param runtime: runtime block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#runtime AppsyncFunction#runtime}
        :param sync_config: sync_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#sync_config AppsyncFunction#sync_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(runtime, dict):
            runtime = AppsyncFunctionRuntime(**runtime)
        if isinstance(sync_config, dict):
            sync_config = AppsyncFunctionSyncConfig(**sync_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7288b6a21947f30aa07e4bf991fedada205ecfa0a691a036b0d969b40aa72ae8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument function_version", value=function_version, expected_type=type_hints["function_version"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument max_batch_size", value=max_batch_size, expected_type=type_hints["max_batch_size"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument request_mapping_template", value=request_mapping_template, expected_type=type_hints["request_mapping_template"])
            check_type(argname="argument response_mapping_template", value=response_mapping_template, expected_type=type_hints["response_mapping_template"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument sync_config", value=sync_config, expected_type=type_hints["sync_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_id": api_id,
            "data_source": data_source,
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
        if code is not None:
            self._values["code"] = code
        if description is not None:
            self._values["description"] = description
        if function_version is not None:
            self._values["function_version"] = function_version
        if id is not None:
            self._values["id"] = id
        if max_batch_size is not None:
            self._values["max_batch_size"] = max_batch_size
        if region is not None:
            self._values["region"] = region
        if request_mapping_template is not None:
            self._values["request_mapping_template"] = request_mapping_template
        if response_mapping_template is not None:
            self._values["response_mapping_template"] = response_mapping_template
        if runtime is not None:
            self._values["runtime"] = runtime
        if sync_config is not None:
            self._values["sync_config"] = sync_config

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
    def api_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#api_id AppsyncFunction#api_id}.'''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#data_source AppsyncFunction#data_source}.'''
        result = self._values.get("data_source")
        assert result is not None, "Required property 'data_source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#name AppsyncFunction#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#code AppsyncFunction#code}.'''
        result = self._values.get("code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#description AppsyncFunction#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#function_version AppsyncFunction#function_version}.'''
        result = self._values.get("function_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#id AppsyncFunction#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#max_batch_size AppsyncFunction#max_batch_size}.'''
        result = self._values.get("max_batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#region AppsyncFunction#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_mapping_template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#request_mapping_template AppsyncFunction#request_mapping_template}.'''
        result = self._values.get("request_mapping_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_mapping_template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#response_mapping_template AppsyncFunction#response_mapping_template}.'''
        result = self._values.get("response_mapping_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime(self) -> typing.Optional["AppsyncFunctionRuntime"]:
        '''runtime block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#runtime AppsyncFunction#runtime}
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional["AppsyncFunctionRuntime"], result)

    @builtins.property
    def sync_config(self) -> typing.Optional["AppsyncFunctionSyncConfig"]:
        '''sync_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#sync_config AppsyncFunction#sync_config}
        '''
        result = self._values.get("sync_config")
        return typing.cast(typing.Optional["AppsyncFunctionSyncConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncFunctionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appsyncFunction.AppsyncFunctionRuntime",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "runtime_version": "runtimeVersion"},
)
class AppsyncFunctionRuntime:
    def __init__(self, *, name: builtins.str, runtime_version: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#name AppsyncFunction#name}.
        :param runtime_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#runtime_version AppsyncFunction#runtime_version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d9cc96115f8cca6fb687a881260a630762800cd92de97f0a35c51349ccff57d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "runtime_version": runtime_version,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#name AppsyncFunction#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#runtime_version AppsyncFunction#runtime_version}.'''
        result = self._values.get("runtime_version")
        assert result is not None, "Required property 'runtime_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncFunctionRuntime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncFunctionRuntimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appsyncFunction.AppsyncFunctionRuntimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73343d71c3bd24df0c62f5dabc59c343dfac93facf173eacbf800a962adfd743)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeVersionInput")
    def runtime_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3040aeaa442b8c64958bae42bc010f263e979f65660d63b91b9999f7bfd1d120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ca43cf5abdf5b8b464294c7cd9c71c363d16c7b28ab386fa506e8e1e11dc255)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppsyncFunctionRuntime]:
        return typing.cast(typing.Optional[AppsyncFunctionRuntime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AppsyncFunctionRuntime]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__834a686118a09a18eddc2d4f4bd39e2d898a44b58e82f75251ea4ed861a24896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appsyncFunction.AppsyncFunctionSyncConfig",
    jsii_struct_bases=[],
    name_mapping={
        "conflict_detection": "conflictDetection",
        "conflict_handler": "conflictHandler",
        "lambda_conflict_handler_config": "lambdaConflictHandlerConfig",
    },
)
class AppsyncFunctionSyncConfig:
    def __init__(
        self,
        *,
        conflict_detection: typing.Optional[builtins.str] = None,
        conflict_handler: typing.Optional[builtins.str] = None,
        lambda_conflict_handler_config: typing.Optional[typing.Union["AppsyncFunctionSyncConfigLambdaConflictHandlerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param conflict_detection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#conflict_detection AppsyncFunction#conflict_detection}.
        :param conflict_handler: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#conflict_handler AppsyncFunction#conflict_handler}.
        :param lambda_conflict_handler_config: lambda_conflict_handler_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#lambda_conflict_handler_config AppsyncFunction#lambda_conflict_handler_config}
        '''
        if isinstance(lambda_conflict_handler_config, dict):
            lambda_conflict_handler_config = AppsyncFunctionSyncConfigLambdaConflictHandlerConfig(**lambda_conflict_handler_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bd56ba9d1b6f0db6c14f3990814f73bfa63b4878c326b042f5fe50a1cff89eb)
            check_type(argname="argument conflict_detection", value=conflict_detection, expected_type=type_hints["conflict_detection"])
            check_type(argname="argument conflict_handler", value=conflict_handler, expected_type=type_hints["conflict_handler"])
            check_type(argname="argument lambda_conflict_handler_config", value=lambda_conflict_handler_config, expected_type=type_hints["lambda_conflict_handler_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if conflict_detection is not None:
            self._values["conflict_detection"] = conflict_detection
        if conflict_handler is not None:
            self._values["conflict_handler"] = conflict_handler
        if lambda_conflict_handler_config is not None:
            self._values["lambda_conflict_handler_config"] = lambda_conflict_handler_config

    @builtins.property
    def conflict_detection(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#conflict_detection AppsyncFunction#conflict_detection}.'''
        result = self._values.get("conflict_detection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def conflict_handler(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#conflict_handler AppsyncFunction#conflict_handler}.'''
        result = self._values.get("conflict_handler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_conflict_handler_config(
        self,
    ) -> typing.Optional["AppsyncFunctionSyncConfigLambdaConflictHandlerConfig"]:
        '''lambda_conflict_handler_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#lambda_conflict_handler_config AppsyncFunction#lambda_conflict_handler_config}
        '''
        result = self._values.get("lambda_conflict_handler_config")
        return typing.cast(typing.Optional["AppsyncFunctionSyncConfigLambdaConflictHandlerConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncFunctionSyncConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appsyncFunction.AppsyncFunctionSyncConfigLambdaConflictHandlerConfig",
    jsii_struct_bases=[],
    name_mapping={"lambda_conflict_handler_arn": "lambdaConflictHandlerArn"},
)
class AppsyncFunctionSyncConfigLambdaConflictHandlerConfig:
    def __init__(
        self,
        *,
        lambda_conflict_handler_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param lambda_conflict_handler_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#lambda_conflict_handler_arn AppsyncFunction#lambda_conflict_handler_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc0b47feca44288070c36aa8e624e3fe4068456ddec9374cfa83a9deb4bfbc6f)
            check_type(argname="argument lambda_conflict_handler_arn", value=lambda_conflict_handler_arn, expected_type=type_hints["lambda_conflict_handler_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if lambda_conflict_handler_arn is not None:
            self._values["lambda_conflict_handler_arn"] = lambda_conflict_handler_arn

    @builtins.property
    def lambda_conflict_handler_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#lambda_conflict_handler_arn AppsyncFunction#lambda_conflict_handler_arn}.'''
        result = self._values.get("lambda_conflict_handler_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncFunctionSyncConfigLambdaConflictHandlerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncFunctionSyncConfigLambdaConflictHandlerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appsyncFunction.AppsyncFunctionSyncConfigLambdaConflictHandlerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__576672d2a4d9db786f578dbe97fa009873f0a495386f88c7c86004f2902c40c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLambdaConflictHandlerArn")
    def reset_lambda_conflict_handler_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaConflictHandlerArn", []))

    @builtins.property
    @jsii.member(jsii_name="lambdaConflictHandlerArnInput")
    def lambda_conflict_handler_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaConflictHandlerArnInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaConflictHandlerArn")
    def lambda_conflict_handler_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaConflictHandlerArn"))

    @lambda_conflict_handler_arn.setter
    def lambda_conflict_handler_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d530118651c24d0b1ea3cb3c3222416336cd85cf48661337a4f282f7bb6ecad7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaConflictHandlerArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppsyncFunctionSyncConfigLambdaConflictHandlerConfig]:
        return typing.cast(typing.Optional[AppsyncFunctionSyncConfigLambdaConflictHandlerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncFunctionSyncConfigLambdaConflictHandlerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a588ba3266a36a7038172195692523a714a2c2c939cc336b4e28749cd9d97e41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncFunctionSyncConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appsyncFunction.AppsyncFunctionSyncConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c433ca4357b3d1550667da308c0f0ed6dbfad19e262e574fa984ed3c1168934)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLambdaConflictHandlerConfig")
    def put_lambda_conflict_handler_config(
        self,
        *,
        lambda_conflict_handler_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param lambda_conflict_handler_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_function#lambda_conflict_handler_arn AppsyncFunction#lambda_conflict_handler_arn}.
        '''
        value = AppsyncFunctionSyncConfigLambdaConflictHandlerConfig(
            lambda_conflict_handler_arn=lambda_conflict_handler_arn
        )

        return typing.cast(None, jsii.invoke(self, "putLambdaConflictHandlerConfig", [value]))

    @jsii.member(jsii_name="resetConflictDetection")
    def reset_conflict_detection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConflictDetection", []))

    @jsii.member(jsii_name="resetConflictHandler")
    def reset_conflict_handler(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConflictHandler", []))

    @jsii.member(jsii_name="resetLambdaConflictHandlerConfig")
    def reset_lambda_conflict_handler_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaConflictHandlerConfig", []))

    @builtins.property
    @jsii.member(jsii_name="lambdaConflictHandlerConfig")
    def lambda_conflict_handler_config(
        self,
    ) -> AppsyncFunctionSyncConfigLambdaConflictHandlerConfigOutputReference:
        return typing.cast(AppsyncFunctionSyncConfigLambdaConflictHandlerConfigOutputReference, jsii.get(self, "lambdaConflictHandlerConfig"))

    @builtins.property
    @jsii.member(jsii_name="conflictDetectionInput")
    def conflict_detection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conflictDetectionInput"))

    @builtins.property
    @jsii.member(jsii_name="conflictHandlerInput")
    def conflict_handler_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conflictHandlerInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaConflictHandlerConfigInput")
    def lambda_conflict_handler_config_input(
        self,
    ) -> typing.Optional[AppsyncFunctionSyncConfigLambdaConflictHandlerConfig]:
        return typing.cast(typing.Optional[AppsyncFunctionSyncConfigLambdaConflictHandlerConfig], jsii.get(self, "lambdaConflictHandlerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="conflictDetection")
    def conflict_detection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conflictDetection"))

    @conflict_detection.setter
    def conflict_detection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15743b5a69e9f6d34395ece391c6c5dda1233fd8ae322f0522317735644cf6df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conflictDetection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="conflictHandler")
    def conflict_handler(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conflictHandler"))

    @conflict_handler.setter
    def conflict_handler(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e1faf5a187ba264c7f162a41e2e1480ae3f71bf79c75088c984e1a51eb2503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conflictHandler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppsyncFunctionSyncConfig]:
        return typing.cast(typing.Optional[AppsyncFunctionSyncConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AppsyncFunctionSyncConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd2f3d72d3ea80c27e90f7f9884a7e79ac78d8d074b6b841aaee00f65218aa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppsyncFunction",
    "AppsyncFunctionConfig",
    "AppsyncFunctionRuntime",
    "AppsyncFunctionRuntimeOutputReference",
    "AppsyncFunctionSyncConfig",
    "AppsyncFunctionSyncConfigLambdaConflictHandlerConfig",
    "AppsyncFunctionSyncConfigLambdaConflictHandlerConfigOutputReference",
    "AppsyncFunctionSyncConfigOutputReference",
]

publication.publish()

def _typecheckingstub__17d73923a51e9f964e2f07064bda096e8e71808c1eef0fcd8c35fded8c002328(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    api_id: builtins.str,
    data_source: builtins.str,
    name: builtins.str,
    code: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    function_version: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    max_batch_size: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    request_mapping_template: typing.Optional[builtins.str] = None,
    response_mapping_template: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[typing.Union[AppsyncFunctionRuntime, typing.Dict[builtins.str, typing.Any]]] = None,
    sync_config: typing.Optional[typing.Union[AppsyncFunctionSyncConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8903f2ab2778c2e67731eba214f2cbb3903c656bcb05f3989ae79340789ba656(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae59e3d0356ec7514c5a177413048ce0fefd111b41b640f53e34d111dfc57b79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a0c703519f7c694662e7ca5d93e3492867560e6e030dd43bbebfe56f08d98c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23400292df0377f3708b59c30c2b1919d629291cc5c77e2af0b8f860a838607d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee8bb39f2b55c0ba2c7659c26fa84fb10d37f91938f718fb31a360ecb21f158(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8777baea348f046332661ee1c39d5e627399d489d23146718ae49a16c088e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a006fb115616df0fc1c76fc1f83fecfcf40f34084a8883ebccda1f922dba70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511e03051facbd46d3a64275b164991b6fd316758362930aff150c7e73f6b5d2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0714bcec271a76dda8780d19a184cc6ea7a3aa4c5e08f6ea103a456d0a472e94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5017b2c6c5f935394de70950b91b1ad61b5cc1ab46713fc6a6e3cad4087e61c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5953d237a177620d96f18ec20b12d343c7708c9dc8fa08ac6b3c3569e472936(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca810a3fc9ec915a0a7f5d19c6b4e235badfc7e80854d44771dc92633006dea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7288b6a21947f30aa07e4bf991fedada205ecfa0a691a036b0d969b40aa72ae8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    api_id: builtins.str,
    data_source: builtins.str,
    name: builtins.str,
    code: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    function_version: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    max_batch_size: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    request_mapping_template: typing.Optional[builtins.str] = None,
    response_mapping_template: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[typing.Union[AppsyncFunctionRuntime, typing.Dict[builtins.str, typing.Any]]] = None,
    sync_config: typing.Optional[typing.Union[AppsyncFunctionSyncConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d9cc96115f8cca6fb687a881260a630762800cd92de97f0a35c51349ccff57d(
    *,
    name: builtins.str,
    runtime_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73343d71c3bd24df0c62f5dabc59c343dfac93facf173eacbf800a962adfd743(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3040aeaa442b8c64958bae42bc010f263e979f65660d63b91b9999f7bfd1d120(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca43cf5abdf5b8b464294c7cd9c71c363d16c7b28ab386fa506e8e1e11dc255(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834a686118a09a18eddc2d4f4bd39e2d898a44b58e82f75251ea4ed861a24896(
    value: typing.Optional[AppsyncFunctionRuntime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd56ba9d1b6f0db6c14f3990814f73bfa63b4878c326b042f5fe50a1cff89eb(
    *,
    conflict_detection: typing.Optional[builtins.str] = None,
    conflict_handler: typing.Optional[builtins.str] = None,
    lambda_conflict_handler_config: typing.Optional[typing.Union[AppsyncFunctionSyncConfigLambdaConflictHandlerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc0b47feca44288070c36aa8e624e3fe4068456ddec9374cfa83a9deb4bfbc6f(
    *,
    lambda_conflict_handler_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__576672d2a4d9db786f578dbe97fa009873f0a495386f88c7c86004f2902c40c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d530118651c24d0b1ea3cb3c3222416336cd85cf48661337a4f282f7bb6ecad7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a588ba3266a36a7038172195692523a714a2c2c939cc336b4e28749cd9d97e41(
    value: typing.Optional[AppsyncFunctionSyncConfigLambdaConflictHandlerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c433ca4357b3d1550667da308c0f0ed6dbfad19e262e574fa984ed3c1168934(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15743b5a69e9f6d34395ece391c6c5dda1233fd8ae322f0522317735644cf6df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e1faf5a187ba264c7f162a41e2e1480ae3f71bf79c75088c984e1a51eb2503(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd2f3d72d3ea80c27e90f7f9884a7e79ac78d8d074b6b841aaee00f65218aa6(
    value: typing.Optional[AppsyncFunctionSyncConfig],
) -> None:
    """Type checking stubs"""
    pass
