r'''
# `aws_sagemaker_endpoint`

Refer to the Terraform Registry for docs: [`aws_sagemaker_endpoint`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint).
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


class SagemakerEndpoint(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpoint",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint aws_sagemaker_endpoint}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        endpoint_config_name: builtins.str,
        deployment_config: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint aws_sagemaker_endpoint} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param endpoint_config_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#endpoint_config_name SagemakerEndpoint#endpoint_config_name}.
        :param deployment_config: deployment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#deployment_config SagemakerEndpoint#deployment_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#id SagemakerEndpoint#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#name SagemakerEndpoint#name}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#region SagemakerEndpoint#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#tags SagemakerEndpoint#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#tags_all SagemakerEndpoint#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed5e6b90d57b4912a4131d4df5a81faca91930eb50479371667b59235348038)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SagemakerEndpointConfig(
            endpoint_config_name=endpoint_config_name,
            deployment_config=deployment_config,
            id=id,
            name=name,
            region=region,
            tags=tags,
            tags_all=tags_all,
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
        '''Generates CDKTF code for importing a SagemakerEndpoint resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SagemakerEndpoint to import.
        :param import_from_id: The id of the existing SagemakerEndpoint that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SagemakerEndpoint to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d67a22e74ed31296d9f5d2867b5b85846debde34f45ec77a01e40d8ba15ad52)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDeploymentConfig")
    def put_deployment_config(
        self,
        *,
        auto_rollback_configuration: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigAutoRollbackConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        blue_green_update_policy: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        rolling_update_policy: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigRollingUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto_rollback_configuration: auto_rollback_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#auto_rollback_configuration SagemakerEndpoint#auto_rollback_configuration}
        :param blue_green_update_policy: blue_green_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#blue_green_update_policy SagemakerEndpoint#blue_green_update_policy}
        :param rolling_update_policy: rolling_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#rolling_update_policy SagemakerEndpoint#rolling_update_policy}
        '''
        value = SagemakerEndpointDeploymentConfig(
            auto_rollback_configuration=auto_rollback_configuration,
            blue_green_update_policy=blue_green_update_policy,
            rolling_update_policy=rolling_update_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putDeploymentConfig", [value]))

    @jsii.member(jsii_name="resetDeploymentConfig")
    def reset_deployment_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "SagemakerEndpointDeploymentConfigOutputReference":
        return typing.cast("SagemakerEndpointDeploymentConfigOutputReference", jsii.get(self, "deploymentConfig"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigInput")
    def deployment_config_input(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfig"]:
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfig"], jsii.get(self, "deploymentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointConfigNameInput")
    def endpoint_config_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointConfigNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

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
    @jsii.member(jsii_name="endpointConfigName")
    def endpoint_config_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointConfigName"))

    @endpoint_config_name.setter
    def endpoint_config_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd07bf7e05125daf4cd3b5f6a49d668d202c567d1e343ec4fc5ce18ac776696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointConfigName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__994a436f8da07d53fb8f9be9cc8381c6b7db59e8fdd722bafa17caa13516fe5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2dfd77c6f8739e058adc1e130ad2b1fe6913c1bbe7ca9db6e589b76d2511727)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9967ea9ecbb5997ef2434699a89d148935070bc40acf89bc0800dd3358db17b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825ada93a8b74dfe39af9784ec1a3178b2bf931bb48b033a23697ed23037c364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37f9591e2bcbdad43a1765d13def2cc1b0546dccae6d6f6c0a0778e05fcaebe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "endpoint_config_name": "endpointConfigName",
        "deployment_config": "deploymentConfig",
        "id": "id",
        "name": "name",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class SagemakerEndpointConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        endpoint_config_name: builtins.str,
        deployment_config: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param endpoint_config_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#endpoint_config_name SagemakerEndpoint#endpoint_config_name}.
        :param deployment_config: deployment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#deployment_config SagemakerEndpoint#deployment_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#id SagemakerEndpoint#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#name SagemakerEndpoint#name}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#region SagemakerEndpoint#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#tags SagemakerEndpoint#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#tags_all SagemakerEndpoint#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(deployment_config, dict):
            deployment_config = SagemakerEndpointDeploymentConfig(**deployment_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1058fcab6074a85a0ffc00b3dda1007e7c0586f6aad8fb977fe053de8e1ddd5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument endpoint_config_name", value=endpoint_config_name, expected_type=type_hints["endpoint_config_name"])
            check_type(argname="argument deployment_config", value=deployment_config, expected_type=type_hints["deployment_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint_config_name": endpoint_config_name,
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
        if deployment_config is not None:
            self._values["deployment_config"] = deployment_config
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
    def endpoint_config_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#endpoint_config_name SagemakerEndpoint#endpoint_config_name}.'''
        result = self._values.get("endpoint_config_name")
        assert result is not None, "Required property 'endpoint_config_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployment_config(self) -> typing.Optional["SagemakerEndpointDeploymentConfig"]:
        '''deployment_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#deployment_config SagemakerEndpoint#deployment_config}
        '''
        result = self._values.get("deployment_config")
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#id SagemakerEndpoint#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#name SagemakerEndpoint#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#region SagemakerEndpoint#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#tags SagemakerEndpoint#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#tags_all SagemakerEndpoint#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfig",
    jsii_struct_bases=[],
    name_mapping={
        "auto_rollback_configuration": "autoRollbackConfiguration",
        "blue_green_update_policy": "blueGreenUpdatePolicy",
        "rolling_update_policy": "rollingUpdatePolicy",
    },
)
class SagemakerEndpointDeploymentConfig:
    def __init__(
        self,
        *,
        auto_rollback_configuration: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigAutoRollbackConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        blue_green_update_policy: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        rolling_update_policy: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigRollingUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto_rollback_configuration: auto_rollback_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#auto_rollback_configuration SagemakerEndpoint#auto_rollback_configuration}
        :param blue_green_update_policy: blue_green_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#blue_green_update_policy SagemakerEndpoint#blue_green_update_policy}
        :param rolling_update_policy: rolling_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#rolling_update_policy SagemakerEndpoint#rolling_update_policy}
        '''
        if isinstance(auto_rollback_configuration, dict):
            auto_rollback_configuration = SagemakerEndpointDeploymentConfigAutoRollbackConfiguration(**auto_rollback_configuration)
        if isinstance(blue_green_update_policy, dict):
            blue_green_update_policy = SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy(**blue_green_update_policy)
        if isinstance(rolling_update_policy, dict):
            rolling_update_policy = SagemakerEndpointDeploymentConfigRollingUpdatePolicy(**rolling_update_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96cadbb11a9bc0b82e567b324911715202dc1ee25f725983ea516871187dd93)
            check_type(argname="argument auto_rollback_configuration", value=auto_rollback_configuration, expected_type=type_hints["auto_rollback_configuration"])
            check_type(argname="argument blue_green_update_policy", value=blue_green_update_policy, expected_type=type_hints["blue_green_update_policy"])
            check_type(argname="argument rolling_update_policy", value=rolling_update_policy, expected_type=type_hints["rolling_update_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_rollback_configuration is not None:
            self._values["auto_rollback_configuration"] = auto_rollback_configuration
        if blue_green_update_policy is not None:
            self._values["blue_green_update_policy"] = blue_green_update_policy
        if rolling_update_policy is not None:
            self._values["rolling_update_policy"] = rolling_update_policy

    @builtins.property
    def auto_rollback_configuration(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfigAutoRollbackConfiguration"]:
        '''auto_rollback_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#auto_rollback_configuration SagemakerEndpoint#auto_rollback_configuration}
        '''
        result = self._values.get("auto_rollback_configuration")
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfigAutoRollbackConfiguration"], result)

    @builtins.property
    def blue_green_update_policy(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy"]:
        '''blue_green_update_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#blue_green_update_policy SagemakerEndpoint#blue_green_update_policy}
        '''
        result = self._values.get("blue_green_update_policy")
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy"], result)

    @builtins.property
    def rolling_update_policy(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfigRollingUpdatePolicy"]:
        '''rolling_update_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#rolling_update_policy SagemakerEndpoint#rolling_update_policy}
        '''
        result = self._values.get("rolling_update_policy")
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfigRollingUpdatePolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigAutoRollbackConfiguration",
    jsii_struct_bases=[],
    name_mapping={"alarms": "alarms"},
)
class SagemakerEndpointDeploymentConfigAutoRollbackConfiguration:
    def __init__(
        self,
        *,
        alarms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param alarms: alarms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#alarms SagemakerEndpoint#alarms}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d472fa4cfc3d9d67f2dd11bb71ff18aab03a7922954c8c670fa9887e3b557ba)
            check_type(argname="argument alarms", value=alarms, expected_type=type_hints["alarms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarms is not None:
            self._values["alarms"] = alarms

    @builtins.property
    def alarms(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms"]]]:
        '''alarms block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#alarms SagemakerEndpoint#alarms}
        '''
        result = self._values.get("alarms")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfigAutoRollbackConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms",
    jsii_struct_bases=[],
    name_mapping={"alarm_name": "alarmName"},
)
class SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms:
    def __init__(self, *, alarm_name: builtins.str) -> None:
        '''
        :param alarm_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#alarm_name SagemakerEndpoint#alarm_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb2d156854d821a98194c3c0cf37a60d0c7744ad1f566193a10306c984f986d)
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alarm_name": alarm_name,
        }

    @builtins.property
    def alarm_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#alarm_name SagemakerEndpoint#alarm_name}.'''
        result = self._values.get("alarm_name")
        assert result is not None, "Required property 'alarm_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b1f07b4f440adc7c64f207e947ffdc56c698c80d09b8d1c7093225c3ebe91d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed26d57948bbbe65c4d1d52475414ef128af0f8134151d79998374e3f5d3d075)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aad6c3730160ee6423bf74d9bf7e5f63532db1c959906194f18edba10839b4a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e008a8f7eeaf7e0514aeea183bd48d2c76ec5621388d15faa3ba1455ba5b3278)
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
            type_hints = typing.get_type_hints(_typecheckingstub__064398f199282bef7dc1c1a1e3051286051e32a0c1560fc681907f91cd28c62f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__790ac8b44c797586b3b497b5df77e0399efb0d562add5814c22ca20417ddcc7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f2f5bf5c86c5e20a46c9ee44ccbb8dffd78a24c8a4fd021f1839d7d0e560938)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="alarmNameInput")
    def alarm_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmNameInput"))

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alarmName"))

    @alarm_name.setter
    def alarm_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe0b26badfb46173b75010f7ceaadcd63273d54e82f1498aa0633adba63ba1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d17aace0429c19a5aa39659560f48f077da11ad1d0043699afa16ed22d585a9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointDeploymentConfigAutoRollbackConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigAutoRollbackConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da6ee148b8d8c7519214e069f7c3efec5d0e42208f0bde099964aa84b9e801e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAlarms")
    def put_alarms(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a7993cc7e005ee745ae2c12b149d84a2bce6f96a1d9194eee7026d62a75e4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAlarms", [value]))

    @jsii.member(jsii_name="resetAlarms")
    def reset_alarms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlarms", []))

    @builtins.property
    @jsii.member(jsii_name="alarms")
    def alarms(
        self,
    ) -> SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsList:
        return typing.cast(SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsList, jsii.get(self, "alarms"))

    @builtins.property
    @jsii.member(jsii_name="alarmsInput")
    def alarms_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]]], jsii.get(self, "alarmsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigAutoRollbackConfiguration]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigAutoRollbackConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointDeploymentConfigAutoRollbackConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92cab95602df8243cae36c09b2685eddb251130472e32c082af08f265441ef18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "traffic_routing_configuration": "trafficRoutingConfiguration",
        "maximum_execution_timeout_in_seconds": "maximumExecutionTimeoutInSeconds",
        "termination_wait_in_seconds": "terminationWaitInSeconds",
    },
)
class SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy:
    def __init__(
        self,
        *,
        traffic_routing_configuration: typing.Union["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration", typing.Dict[builtins.str, typing.Any]],
        maximum_execution_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        termination_wait_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param traffic_routing_configuration: traffic_routing_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#traffic_routing_configuration SagemakerEndpoint#traffic_routing_configuration}
        :param maximum_execution_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#maximum_execution_timeout_in_seconds SagemakerEndpoint#maximum_execution_timeout_in_seconds}.
        :param termination_wait_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#termination_wait_in_seconds SagemakerEndpoint#termination_wait_in_seconds}.
        '''
        if isinstance(traffic_routing_configuration, dict):
            traffic_routing_configuration = SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration(**traffic_routing_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2c48db96e8d40c6c16bce828ad35ab875a8ec363885ab4180c2e8fe209612e6)
            check_type(argname="argument traffic_routing_configuration", value=traffic_routing_configuration, expected_type=type_hints["traffic_routing_configuration"])
            check_type(argname="argument maximum_execution_timeout_in_seconds", value=maximum_execution_timeout_in_seconds, expected_type=type_hints["maximum_execution_timeout_in_seconds"])
            check_type(argname="argument termination_wait_in_seconds", value=termination_wait_in_seconds, expected_type=type_hints["termination_wait_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "traffic_routing_configuration": traffic_routing_configuration,
        }
        if maximum_execution_timeout_in_seconds is not None:
            self._values["maximum_execution_timeout_in_seconds"] = maximum_execution_timeout_in_seconds
        if termination_wait_in_seconds is not None:
            self._values["termination_wait_in_seconds"] = termination_wait_in_seconds

    @builtins.property
    def traffic_routing_configuration(
        self,
    ) -> "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration":
        '''traffic_routing_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#traffic_routing_configuration SagemakerEndpoint#traffic_routing_configuration}
        '''
        result = self._values.get("traffic_routing_configuration")
        assert result is not None, "Required property 'traffic_routing_configuration' is missing"
        return typing.cast("SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration", result)

    @builtins.property
    def maximum_execution_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#maximum_execution_timeout_in_seconds SagemakerEndpoint#maximum_execution_timeout_in_seconds}.'''
        result = self._values.get("maximum_execution_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def termination_wait_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#termination_wait_in_seconds SagemakerEndpoint#termination_wait_in_seconds}.'''
        result = self._values.get("termination_wait_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e40129c5bc42882e14facaf3028900100de05120cb50f5f06b538f0755af06a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTrafficRoutingConfiguration")
    def put_traffic_routing_configuration(
        self,
        *,
        type: builtins.str,
        wait_interval_in_seconds: jsii.Number,
        canary_size: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize", typing.Dict[builtins.str, typing.Any]]] = None,
        linear_step_size: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param wait_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#wait_interval_in_seconds SagemakerEndpoint#wait_interval_in_seconds}.
        :param canary_size: canary_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#canary_size SagemakerEndpoint#canary_size}
        :param linear_step_size: linear_step_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#linear_step_size SagemakerEndpoint#linear_step_size}
        '''
        value = SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration(
            type=type,
            wait_interval_in_seconds=wait_interval_in_seconds,
            canary_size=canary_size,
            linear_step_size=linear_step_size,
        )

        return typing.cast(None, jsii.invoke(self, "putTrafficRoutingConfiguration", [value]))

    @jsii.member(jsii_name="resetMaximumExecutionTimeoutInSeconds")
    def reset_maximum_execution_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumExecutionTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetTerminationWaitInSeconds")
    def reset_termination_wait_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminationWaitInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="trafficRoutingConfiguration")
    def traffic_routing_configuration(
        self,
    ) -> "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationOutputReference":
        return typing.cast("SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationOutputReference", jsii.get(self, "trafficRoutingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="maximumExecutionTimeoutInSecondsInput")
    def maximum_execution_timeout_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumExecutionTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="terminationWaitInSecondsInput")
    def termination_wait_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "terminationWaitInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficRoutingConfigurationInput")
    def traffic_routing_configuration_input(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration"]:
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration"], jsii.get(self, "trafficRoutingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumExecutionTimeoutInSeconds")
    def maximum_execution_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumExecutionTimeoutInSeconds"))

    @maximum_execution_timeout_in_seconds.setter
    def maximum_execution_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e99466a3c00e9194bee1f968cd8eb903adb719b79afcc2ebe5e7ea0066f6f7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumExecutionTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terminationWaitInSeconds")
    def termination_wait_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "terminationWaitInSeconds"))

    @termination_wait_in_seconds.setter
    def termination_wait_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edaf97839c5b40b92252a46fe6dcf35b7f5bd15941afcbee2fcfb4367e6025c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminationWaitInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef93cd914e8b422bc95a7f1358f5f9768fe9ef9cee09bf86c935c02401707ca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "wait_interval_in_seconds": "waitIntervalInSeconds",
        "canary_size": "canarySize",
        "linear_step_size": "linearStepSize",
    },
)
class SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration:
    def __init__(
        self,
        *,
        type: builtins.str,
        wait_interval_in_seconds: jsii.Number,
        canary_size: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize", typing.Dict[builtins.str, typing.Any]]] = None,
        linear_step_size: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param wait_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#wait_interval_in_seconds SagemakerEndpoint#wait_interval_in_seconds}.
        :param canary_size: canary_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#canary_size SagemakerEndpoint#canary_size}
        :param linear_step_size: linear_step_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#linear_step_size SagemakerEndpoint#linear_step_size}
        '''
        if isinstance(canary_size, dict):
            canary_size = SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize(**canary_size)
        if isinstance(linear_step_size, dict):
            linear_step_size = SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize(**linear_step_size)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a033ef090a1439be1c9234bc33ff4798c9fc0064915517b59131baf597027e0)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument wait_interval_in_seconds", value=wait_interval_in_seconds, expected_type=type_hints["wait_interval_in_seconds"])
            check_type(argname="argument canary_size", value=canary_size, expected_type=type_hints["canary_size"])
            check_type(argname="argument linear_step_size", value=linear_step_size, expected_type=type_hints["linear_step_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "wait_interval_in_seconds": wait_interval_in_seconds,
        }
        if canary_size is not None:
            self._values["canary_size"] = canary_size
        if linear_step_size is not None:
            self._values["linear_step_size"] = linear_step_size

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def wait_interval_in_seconds(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#wait_interval_in_seconds SagemakerEndpoint#wait_interval_in_seconds}.'''
        result = self._values.get("wait_interval_in_seconds")
        assert result is not None, "Required property 'wait_interval_in_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def canary_size(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize"]:
        '''canary_size block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#canary_size SagemakerEndpoint#canary_size}
        '''
        result = self._values.get("canary_size")
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize"], result)

    @builtins.property
    def linear_step_size(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize"]:
        '''linear_step_size block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#linear_step_size SagemakerEndpoint#linear_step_size}
        '''
        result = self._values.get("linear_step_size")
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize:
    def __init__(self, *, type: builtins.str, value: jsii.Number) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd408a528b64d56dc3b637eaf20345f398ea24c5de19ebe490cf8109e3bd410f)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySizeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySizeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a8d76984a0a52005634e751e5635771469e8a3d0765c591ec891d339ed5d7a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__86d13cff7d95eab2ccbc869e82d48aba434b43515729cb41cd76c804a6ec7efd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14bc7ae0d29b323520d36d04a6beced79da68aae572e9620a18b4e3752664bc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87ee009057924fe76f87110323ae297a174b996596f1228594479ae3b74c512c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize:
    def __init__(self, *, type: builtins.str, value: jsii.Number) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a5622f7bf38a1e6bcfe343e654397cc30d27f52cd9398ea007d23ecbbd10a9a)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSizeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSizeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b010e2785d1b0c2244d3f68050b8ce1c08980b893bc285a6ba17bb321a4393ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__6318c3c5ee00ab0dc48c8fe55727a09c010b95af2d9a71710211b6b5a1bc2354)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5fe5c72544dc30a0bc8e538d9dd84131024635fd362237f8807f257e26618c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43811b7dff01b2a8935bea5153ee48c865c77d16615054e4d267e544bf83507a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e47ac2b203455363849fb7240d0021a9cc03f6d83d800e920364107b41989aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCanarySize")
    def put_canary_size(self, *, type: builtins.str, value: jsii.Number) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.
        '''
        value_ = SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize(
            type=type, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putCanarySize", [value_]))

    @jsii.member(jsii_name="putLinearStepSize")
    def put_linear_step_size(self, *, type: builtins.str, value: jsii.Number) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.
        '''
        value_ = SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize(
            type=type, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putLinearStepSize", [value_]))

    @jsii.member(jsii_name="resetCanarySize")
    def reset_canary_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCanarySize", []))

    @jsii.member(jsii_name="resetLinearStepSize")
    def reset_linear_step_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinearStepSize", []))

    @builtins.property
    @jsii.member(jsii_name="canarySize")
    def canary_size(
        self,
    ) -> SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySizeOutputReference:
        return typing.cast(SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySizeOutputReference, jsii.get(self, "canarySize"))

    @builtins.property
    @jsii.member(jsii_name="linearStepSize")
    def linear_step_size(
        self,
    ) -> SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSizeOutputReference:
        return typing.cast(SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSizeOutputReference, jsii.get(self, "linearStepSize"))

    @builtins.property
    @jsii.member(jsii_name="canarySizeInput")
    def canary_size_input(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize], jsii.get(self, "canarySizeInput"))

    @builtins.property
    @jsii.member(jsii_name="linearStepSizeInput")
    def linear_step_size_input(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize], jsii.get(self, "linearStepSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="waitIntervalInSecondsInput")
    def wait_interval_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "waitIntervalInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b53bbde605dcf4e22102ffc971dc486609825a7d60d22f23c400f26adaba76a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitIntervalInSeconds")
    def wait_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "waitIntervalInSeconds"))

    @wait_interval_in_seconds.setter
    def wait_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c173343b24b5bd11952e7a3e0946ad736b53518b43afaa91fca92c9429622051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__472485b1b21e6668c34d7fca43228d7f35e4e362043a025c100915a0999cd5a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointDeploymentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7661ba3f0fd5cca9ac6c3d3a62880a5a8c541a6ff8dbb2efce9abf759b3c84b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoRollbackConfiguration")
    def put_auto_rollback_configuration(
        self,
        *,
        alarms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param alarms: alarms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#alarms SagemakerEndpoint#alarms}
        '''
        value = SagemakerEndpointDeploymentConfigAutoRollbackConfiguration(
            alarms=alarms
        )

        return typing.cast(None, jsii.invoke(self, "putAutoRollbackConfiguration", [value]))

    @jsii.member(jsii_name="putBlueGreenUpdatePolicy")
    def put_blue_green_update_policy(
        self,
        *,
        traffic_routing_configuration: typing.Union[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration, typing.Dict[builtins.str, typing.Any]],
        maximum_execution_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        termination_wait_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param traffic_routing_configuration: traffic_routing_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#traffic_routing_configuration SagemakerEndpoint#traffic_routing_configuration}
        :param maximum_execution_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#maximum_execution_timeout_in_seconds SagemakerEndpoint#maximum_execution_timeout_in_seconds}.
        :param termination_wait_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#termination_wait_in_seconds SagemakerEndpoint#termination_wait_in_seconds}.
        '''
        value = SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy(
            traffic_routing_configuration=traffic_routing_configuration,
            maximum_execution_timeout_in_seconds=maximum_execution_timeout_in_seconds,
            termination_wait_in_seconds=termination_wait_in_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putBlueGreenUpdatePolicy", [value]))

    @jsii.member(jsii_name="putRollingUpdatePolicy")
    def put_rolling_update_policy(
        self,
        *,
        maximum_batch_size: typing.Union["SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize", typing.Dict[builtins.str, typing.Any]],
        wait_interval_in_seconds: jsii.Number,
        maximum_execution_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        rollback_maximum_batch_size: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param maximum_batch_size: maximum_batch_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#maximum_batch_size SagemakerEndpoint#maximum_batch_size}
        :param wait_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#wait_interval_in_seconds SagemakerEndpoint#wait_interval_in_seconds}.
        :param maximum_execution_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#maximum_execution_timeout_in_seconds SagemakerEndpoint#maximum_execution_timeout_in_seconds}.
        :param rollback_maximum_batch_size: rollback_maximum_batch_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#rollback_maximum_batch_size SagemakerEndpoint#rollback_maximum_batch_size}
        '''
        value = SagemakerEndpointDeploymentConfigRollingUpdatePolicy(
            maximum_batch_size=maximum_batch_size,
            wait_interval_in_seconds=wait_interval_in_seconds,
            maximum_execution_timeout_in_seconds=maximum_execution_timeout_in_seconds,
            rollback_maximum_batch_size=rollback_maximum_batch_size,
        )

        return typing.cast(None, jsii.invoke(self, "putRollingUpdatePolicy", [value]))

    @jsii.member(jsii_name="resetAutoRollbackConfiguration")
    def reset_auto_rollback_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoRollbackConfiguration", []))

    @jsii.member(jsii_name="resetBlueGreenUpdatePolicy")
    def reset_blue_green_update_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlueGreenUpdatePolicy", []))

    @jsii.member(jsii_name="resetRollingUpdatePolicy")
    def reset_rolling_update_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRollingUpdatePolicy", []))

    @builtins.property
    @jsii.member(jsii_name="autoRollbackConfiguration")
    def auto_rollback_configuration(
        self,
    ) -> SagemakerEndpointDeploymentConfigAutoRollbackConfigurationOutputReference:
        return typing.cast(SagemakerEndpointDeploymentConfigAutoRollbackConfigurationOutputReference, jsii.get(self, "autoRollbackConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="blueGreenUpdatePolicy")
    def blue_green_update_policy(
        self,
    ) -> SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyOutputReference:
        return typing.cast(SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyOutputReference, jsii.get(self, "blueGreenUpdatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="rollingUpdatePolicy")
    def rolling_update_policy(
        self,
    ) -> "SagemakerEndpointDeploymentConfigRollingUpdatePolicyOutputReference":
        return typing.cast("SagemakerEndpointDeploymentConfigRollingUpdatePolicyOutputReference", jsii.get(self, "rollingUpdatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="autoRollbackConfigurationInput")
    def auto_rollback_configuration_input(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigAutoRollbackConfiguration]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigAutoRollbackConfiguration], jsii.get(self, "autoRollbackConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="blueGreenUpdatePolicyInput")
    def blue_green_update_policy_input(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy], jsii.get(self, "blueGreenUpdatePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="rollingUpdatePolicyInput")
    def rolling_update_policy_input(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfigRollingUpdatePolicy"]:
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfigRollingUpdatePolicy"], jsii.get(self, "rollingUpdatePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerEndpointDeploymentConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointDeploymentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7217f302f2c6c9e52bea16fd1b29956fcd2444f09af7875c307807f8c521825e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigRollingUpdatePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "maximum_batch_size": "maximumBatchSize",
        "wait_interval_in_seconds": "waitIntervalInSeconds",
        "maximum_execution_timeout_in_seconds": "maximumExecutionTimeoutInSeconds",
        "rollback_maximum_batch_size": "rollbackMaximumBatchSize",
    },
)
class SagemakerEndpointDeploymentConfigRollingUpdatePolicy:
    def __init__(
        self,
        *,
        maximum_batch_size: typing.Union["SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize", typing.Dict[builtins.str, typing.Any]],
        wait_interval_in_seconds: jsii.Number,
        maximum_execution_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        rollback_maximum_batch_size: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param maximum_batch_size: maximum_batch_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#maximum_batch_size SagemakerEndpoint#maximum_batch_size}
        :param wait_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#wait_interval_in_seconds SagemakerEndpoint#wait_interval_in_seconds}.
        :param maximum_execution_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#maximum_execution_timeout_in_seconds SagemakerEndpoint#maximum_execution_timeout_in_seconds}.
        :param rollback_maximum_batch_size: rollback_maximum_batch_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#rollback_maximum_batch_size SagemakerEndpoint#rollback_maximum_batch_size}
        '''
        if isinstance(maximum_batch_size, dict):
            maximum_batch_size = SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize(**maximum_batch_size)
        if isinstance(rollback_maximum_batch_size, dict):
            rollback_maximum_batch_size = SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize(**rollback_maximum_batch_size)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2de60d02857521ba34a477e6123706c68998d231d71fdadf8d0ce62631e6f745)
            check_type(argname="argument maximum_batch_size", value=maximum_batch_size, expected_type=type_hints["maximum_batch_size"])
            check_type(argname="argument wait_interval_in_seconds", value=wait_interval_in_seconds, expected_type=type_hints["wait_interval_in_seconds"])
            check_type(argname="argument maximum_execution_timeout_in_seconds", value=maximum_execution_timeout_in_seconds, expected_type=type_hints["maximum_execution_timeout_in_seconds"])
            check_type(argname="argument rollback_maximum_batch_size", value=rollback_maximum_batch_size, expected_type=type_hints["rollback_maximum_batch_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "maximum_batch_size": maximum_batch_size,
            "wait_interval_in_seconds": wait_interval_in_seconds,
        }
        if maximum_execution_timeout_in_seconds is not None:
            self._values["maximum_execution_timeout_in_seconds"] = maximum_execution_timeout_in_seconds
        if rollback_maximum_batch_size is not None:
            self._values["rollback_maximum_batch_size"] = rollback_maximum_batch_size

    @builtins.property
    def maximum_batch_size(
        self,
    ) -> "SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize":
        '''maximum_batch_size block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#maximum_batch_size SagemakerEndpoint#maximum_batch_size}
        '''
        result = self._values.get("maximum_batch_size")
        assert result is not None, "Required property 'maximum_batch_size' is missing"
        return typing.cast("SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize", result)

    @builtins.property
    def wait_interval_in_seconds(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#wait_interval_in_seconds SagemakerEndpoint#wait_interval_in_seconds}.'''
        result = self._values.get("wait_interval_in_seconds")
        assert result is not None, "Required property 'wait_interval_in_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def maximum_execution_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#maximum_execution_timeout_in_seconds SagemakerEndpoint#maximum_execution_timeout_in_seconds}.'''
        result = self._values.get("maximum_execution_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rollback_maximum_batch_size(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize"]:
        '''rollback_maximum_batch_size block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#rollback_maximum_batch_size SagemakerEndpoint#rollback_maximum_batch_size}
        '''
        result = self._values.get("rollback_maximum_batch_size")
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfigRollingUpdatePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize:
    def __init__(self, *, type: builtins.str, value: jsii.Number) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1653f9f3adccb6b3d05456ec1b067300123eb3656ae040484af22a9ded76fc7a)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSizeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSizeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__883227fb1040b266f849951873519c3b80071bc8209c21018dacabfd4665a837)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__3229fb3d50ec68015f0d015c4405fca1e9852e6b5bc15f516330b47e5a4c9f92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9dbd38a63ae259717a0fb5fe1622e46d4d5c7ef3bee3a2a6ec188898ffa9cb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f070f31161898accf4907095f0f8a4ab57eb2ec0b0ae9cecc4acdfda182896d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointDeploymentConfigRollingUpdatePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigRollingUpdatePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d098c6b5e6507875bcf3b85a24ec482db99c94020658b2254ca97c2ae7b0ad99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMaximumBatchSize")
    def put_maximum_batch_size(self, *, type: builtins.str, value: jsii.Number) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.
        '''
        value_ = SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize(
            type=type, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putMaximumBatchSize", [value_]))

    @jsii.member(jsii_name="putRollbackMaximumBatchSize")
    def put_rollback_maximum_batch_size(
        self,
        *,
        type: builtins.str,
        value: jsii.Number,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.
        '''
        value_ = SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize(
            type=type, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putRollbackMaximumBatchSize", [value_]))

    @jsii.member(jsii_name="resetMaximumExecutionTimeoutInSeconds")
    def reset_maximum_execution_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumExecutionTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetRollbackMaximumBatchSize")
    def reset_rollback_maximum_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRollbackMaximumBatchSize", []))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchSize")
    def maximum_batch_size(
        self,
    ) -> SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSizeOutputReference:
        return typing.cast(SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSizeOutputReference, jsii.get(self, "maximumBatchSize"))

    @builtins.property
    @jsii.member(jsii_name="rollbackMaximumBatchSize")
    def rollback_maximum_batch_size(
        self,
    ) -> "SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSizeOutputReference":
        return typing.cast("SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSizeOutputReference", jsii.get(self, "rollbackMaximumBatchSize"))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchSizeInput")
    def maximum_batch_size_input(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize], jsii.get(self, "maximumBatchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumExecutionTimeoutInSecondsInput")
    def maximum_execution_timeout_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumExecutionTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="rollbackMaximumBatchSizeInput")
    def rollback_maximum_batch_size_input(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize"]:
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize"], jsii.get(self, "rollbackMaximumBatchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="waitIntervalInSecondsInput")
    def wait_interval_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "waitIntervalInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumExecutionTimeoutInSeconds")
    def maximum_execution_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumExecutionTimeoutInSeconds"))

    @maximum_execution_timeout_in_seconds.setter
    def maximum_execution_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03ff63813c2962d724cad062b48bb3f966aab331e23f534c8a91a44ac0cccd70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumExecutionTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitIntervalInSeconds")
    def wait_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "waitIntervalInSeconds"))

    @wait_interval_in_seconds.setter
    def wait_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e315a4aed04d895f105e475bdfb72aea685964e58f937140b565b2d7b1004605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicy]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0a076549147066764eb038080088825dab0c148dff2f33c6b2a89fc465201f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize:
    def __init__(self, *, type: builtins.str, value: jsii.Number) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6332e41d6cf3aad01d51eba071a3a9b1445f2066527416e60e11e09784d9fb56)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSizeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSizeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9e48bf847230921c73110ec8585428baa9808889435ae56540862bad2e4397c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__634f1fe4b4ea06e4249ef97dfd9b89229a225ec0cb7de3f5c4a628680817b3bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da7ddff27036652eb0906d2935a4852007ff9fb90ead6953e180d330f5814cc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a22e01a9f58fd2f85e073e6c33a6e4083f89e7f6f9d8d80572b162ddac0380e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SagemakerEndpoint",
    "SagemakerEndpointConfig",
    "SagemakerEndpointDeploymentConfig",
    "SagemakerEndpointDeploymentConfigAutoRollbackConfiguration",
    "SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms",
    "SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsList",
    "SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsOutputReference",
    "SagemakerEndpointDeploymentConfigAutoRollbackConfigurationOutputReference",
    "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy",
    "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyOutputReference",
    "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration",
    "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize",
    "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySizeOutputReference",
    "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize",
    "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSizeOutputReference",
    "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationOutputReference",
    "SagemakerEndpointDeploymentConfigOutputReference",
    "SagemakerEndpointDeploymentConfigRollingUpdatePolicy",
    "SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize",
    "SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSizeOutputReference",
    "SagemakerEndpointDeploymentConfigRollingUpdatePolicyOutputReference",
    "SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize",
    "SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSizeOutputReference",
]

publication.publish()

def _typecheckingstub__1ed5e6b90d57b4912a4131d4df5a81faca91930eb50479371667b59235348038(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    endpoint_config_name: builtins.str,
    deployment_config: typing.Optional[typing.Union[SagemakerEndpointDeploymentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__9d67a22e74ed31296d9f5d2867b5b85846debde34f45ec77a01e40d8ba15ad52(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd07bf7e05125daf4cd3b5f6a49d668d202c567d1e343ec4fc5ce18ac776696(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__994a436f8da07d53fb8f9be9cc8381c6b7db59e8fdd722bafa17caa13516fe5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2dfd77c6f8739e058adc1e130ad2b1fe6913c1bbe7ca9db6e589b76d2511727(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9967ea9ecbb5997ef2434699a89d148935070bc40acf89bc0800dd3358db17b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825ada93a8b74dfe39af9784ec1a3178b2bf931bb48b033a23697ed23037c364(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f9591e2bcbdad43a1765d13def2cc1b0546dccae6d6f6c0a0778e05fcaebe3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1058fcab6074a85a0ffc00b3dda1007e7c0586f6aad8fb977fe053de8e1ddd5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    endpoint_config_name: builtins.str,
    deployment_config: typing.Optional[typing.Union[SagemakerEndpointDeploymentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96cadbb11a9bc0b82e567b324911715202dc1ee25f725983ea516871187dd93(
    *,
    auto_rollback_configuration: typing.Optional[typing.Union[SagemakerEndpointDeploymentConfigAutoRollbackConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    blue_green_update_policy: typing.Optional[typing.Union[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    rolling_update_policy: typing.Optional[typing.Union[SagemakerEndpointDeploymentConfigRollingUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d472fa4cfc3d9d67f2dd11bb71ff18aab03a7922954c8c670fa9887e3b557ba(
    *,
    alarms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb2d156854d821a98194c3c0cf37a60d0c7744ad1f566193a10306c984f986d(
    *,
    alarm_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b1f07b4f440adc7c64f207e947ffdc56c698c80d09b8d1c7093225c3ebe91d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed26d57948bbbe65c4d1d52475414ef128af0f8134151d79998374e3f5d3d075(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aad6c3730160ee6423bf74d9bf7e5f63532db1c959906194f18edba10839b4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e008a8f7eeaf7e0514aeea183bd48d2c76ec5621388d15faa3ba1455ba5b3278(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__064398f199282bef7dc1c1a1e3051286051e32a0c1560fc681907f91cd28c62f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__790ac8b44c797586b3b497b5df77e0399efb0d562add5814c22ca20417ddcc7b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2f5bf5c86c5e20a46c9ee44ccbb8dffd78a24c8a4fd021f1839d7d0e560938(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe0b26badfb46173b75010f7ceaadcd63273d54e82f1498aa0633adba63ba1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17aace0429c19a5aa39659560f48f077da11ad1d0043699afa16ed22d585a9b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da6ee148b8d8c7519214e069f7c3efec5d0e42208f0bde099964aa84b9e801e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a7993cc7e005ee745ae2c12b149d84a2bce6f96a1d9194eee7026d62a75e4b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92cab95602df8243cae36c09b2685eddb251130472e32c082af08f265441ef18(
    value: typing.Optional[SagemakerEndpointDeploymentConfigAutoRollbackConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c48db96e8d40c6c16bce828ad35ab875a8ec363885ab4180c2e8fe209612e6(
    *,
    traffic_routing_configuration: typing.Union[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration, typing.Dict[builtins.str, typing.Any]],
    maximum_execution_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    termination_wait_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e40129c5bc42882e14facaf3028900100de05120cb50f5f06b538f0755af06a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e99466a3c00e9194bee1f968cd8eb903adb719b79afcc2ebe5e7ea0066f6f7c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edaf97839c5b40b92252a46fe6dcf35b7f5bd15941afcbee2fcfb4367e6025c1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef93cd914e8b422bc95a7f1358f5f9768fe9ef9cee09bf86c935c02401707ca5(
    value: typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a033ef090a1439be1c9234bc33ff4798c9fc0064915517b59131baf597027e0(
    *,
    type: builtins.str,
    wait_interval_in_seconds: jsii.Number,
    canary_size: typing.Optional[typing.Union[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize, typing.Dict[builtins.str, typing.Any]]] = None,
    linear_step_size: typing.Optional[typing.Union[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd408a528b64d56dc3b637eaf20345f398ea24c5de19ebe490cf8109e3bd410f(
    *,
    type: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a8d76984a0a52005634e751e5635771469e8a3d0765c591ec891d339ed5d7a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d13cff7d95eab2ccbc869e82d48aba434b43515729cb41cd76c804a6ec7efd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14bc7ae0d29b323520d36d04a6beced79da68aae572e9620a18b4e3752664bc5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ee009057924fe76f87110323ae297a174b996596f1228594479ae3b74c512c(
    value: typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5622f7bf38a1e6bcfe343e654397cc30d27f52cd9398ea007d23ecbbd10a9a(
    *,
    type: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b010e2785d1b0c2244d3f68050b8ce1c08980b893bc285a6ba17bb321a4393ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6318c3c5ee00ab0dc48c8fe55727a09c010b95af2d9a71710211b6b5a1bc2354(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5fe5c72544dc30a0bc8e538d9dd84131024635fd362237f8807f257e26618c7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43811b7dff01b2a8935bea5153ee48c865c77d16615054e4d267e544bf83507a(
    value: typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e47ac2b203455363849fb7240d0021a9cc03f6d83d800e920364107b41989aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b53bbde605dcf4e22102ffc971dc486609825a7d60d22f23c400f26adaba76a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c173343b24b5bd11952e7a3e0946ad736b53518b43afaa91fca92c9429622051(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472485b1b21e6668c34d7fca43228d7f35e4e362043a025c100915a0999cd5a9(
    value: typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7661ba3f0fd5cca9ac6c3d3a62880a5a8c541a6ff8dbb2efce9abf759b3c84b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7217f302f2c6c9e52bea16fd1b29956fcd2444f09af7875c307807f8c521825e(
    value: typing.Optional[SagemakerEndpointDeploymentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de60d02857521ba34a477e6123706c68998d231d71fdadf8d0ce62631e6f745(
    *,
    maximum_batch_size: typing.Union[SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize, typing.Dict[builtins.str, typing.Any]],
    wait_interval_in_seconds: jsii.Number,
    maximum_execution_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    rollback_maximum_batch_size: typing.Optional[typing.Union[SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1653f9f3adccb6b3d05456ec1b067300123eb3656ae040484af22a9ded76fc7a(
    *,
    type: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883227fb1040b266f849951873519c3b80071bc8209c21018dacabfd4665a837(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3229fb3d50ec68015f0d015c4405fca1e9852e6b5bc15f516330b47e5a4c9f92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9dbd38a63ae259717a0fb5fe1622e46d4d5c7ef3bee3a2a6ec188898ffa9cb6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f070f31161898accf4907095f0f8a4ab57eb2ec0b0ae9cecc4acdfda182896d(
    value: typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d098c6b5e6507875bcf3b85a24ec482db99c94020658b2254ca97c2ae7b0ad99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ff63813c2962d724cad062b48bb3f966aab331e23f534c8a91a44ac0cccd70(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e315a4aed04d895f105e475bdfb72aea685964e58f937140b565b2d7b1004605(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a076549147066764eb038080088825dab0c148dff2f33c6b2a89fc465201f3(
    value: typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6332e41d6cf3aad01d51eba071a3a9b1445f2066527416e60e11e09784d9fb56(
    *,
    type: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e48bf847230921c73110ec8585428baa9808889435ae56540862bad2e4397c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__634f1fe4b4ea06e4249ef97dfd9b89229a225ec0cb7de3f5c4a628680817b3bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da7ddff27036652eb0906d2935a4852007ff9fb90ead6953e180d330f5814cc3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a22e01a9f58fd2f85e073e6c33a6e4083f89e7f6f9d8d80572b162ddac0380e(
    value: typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize],
) -> None:
    """Type checking stubs"""
    pass
