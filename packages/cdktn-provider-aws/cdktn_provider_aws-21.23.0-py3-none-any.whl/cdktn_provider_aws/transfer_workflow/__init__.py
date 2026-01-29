r'''
# `aws_transfer_workflow`

Refer to the Terraform Registry for docs: [`aws_transfer_workflow`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow).
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


class TransferWorkflow(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflow",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow aws_transfer_workflow}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        steps: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TransferWorkflowSteps", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        on_exception_steps: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TransferWorkflowOnExceptionSteps", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow aws_transfer_workflow} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param steps: steps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#steps TransferWorkflow#steps}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#description TransferWorkflow#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#id TransferWorkflow#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param on_exception_steps: on_exception_steps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#on_exception_steps TransferWorkflow#on_exception_steps}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#region TransferWorkflow#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#tags TransferWorkflow#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#tags_all TransferWorkflow#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de4fb654950bf7aac05bbf1efdb2604967af9b4bdb53a5d3ae31d522f3bb168f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = TransferWorkflowConfig(
            steps=steps,
            description=description,
            id=id,
            on_exception_steps=on_exception_steps,
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
        '''Generates CDKTF code for importing a TransferWorkflow resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the TransferWorkflow to import.
        :param import_from_id: The id of the existing TransferWorkflow that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the TransferWorkflow to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2216c99c9cc80e7a74abf5a4f985abd4fdc0a4ad1d9ac6ff42136659c1911e5a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putOnExceptionSteps")
    def put_on_exception_steps(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TransferWorkflowOnExceptionSteps", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c07d6555b061dddbec876aeb52ebd569524658334664d1f17272d9c8d30fd98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOnExceptionSteps", [value]))

    @jsii.member(jsii_name="putSteps")
    def put_steps(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TransferWorkflowSteps", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd9b70fb54ca13fa6f2c7520fc6fa657c49866990521e3b2e4cf8ac09f1860ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSteps", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOnExceptionSteps")
    def reset_on_exception_steps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnExceptionSteps", []))

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
    @jsii.member(jsii_name="onExceptionSteps")
    def on_exception_steps(self) -> "TransferWorkflowOnExceptionStepsList":
        return typing.cast("TransferWorkflowOnExceptionStepsList", jsii.get(self, "onExceptionSteps"))

    @builtins.property
    @jsii.member(jsii_name="steps")
    def steps(self) -> "TransferWorkflowStepsList":
        return typing.cast("TransferWorkflowStepsList", jsii.get(self, "steps"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="onExceptionStepsInput")
    def on_exception_steps_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TransferWorkflowOnExceptionSteps"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TransferWorkflowOnExceptionSteps"]]], jsii.get(self, "onExceptionStepsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="stepsInput")
    def steps_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TransferWorkflowSteps"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TransferWorkflowSteps"]]], jsii.get(self, "stepsInput"))

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
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__794a5cbc5fe9a0166a0a66fc76f33df54c2075b824e01e30cb038e7bd761ba87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd25e8f126dd3ec26ee4753c86975a04ea526188a89e7718de0193d89e07d2ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db32c726bc7d627b8c69eb2f9adeba7f2e753bc2dd758fcd01e448ff60de76e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f798c8a9e51df96941e7d82c4e48b6b43077ed37f875c604aceb89119d78325d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d283eb80b909cd4805f2cd81a73d185006ae1fccbb61f31dd909fb25b760cee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "steps": "steps",
        "description": "description",
        "id": "id",
        "on_exception_steps": "onExceptionSteps",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class TransferWorkflowConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        steps: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TransferWorkflowSteps", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        on_exception_steps: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TransferWorkflowOnExceptionSteps", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param steps: steps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#steps TransferWorkflow#steps}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#description TransferWorkflow#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#id TransferWorkflow#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param on_exception_steps: on_exception_steps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#on_exception_steps TransferWorkflow#on_exception_steps}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#region TransferWorkflow#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#tags TransferWorkflow#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#tags_all TransferWorkflow#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a85814f3c6b4b3a1f805518fa071d99164969560adcf456c3662cb957af63b8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument on_exception_steps", value=on_exception_steps, expected_type=type_hints["on_exception_steps"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "steps": steps,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if on_exception_steps is not None:
            self._values["on_exception_steps"] = on_exception_steps
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
    def steps(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TransferWorkflowSteps"]]:
        '''steps block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#steps TransferWorkflow#steps}
        '''
        result = self._values.get("steps")
        assert result is not None, "Required property 'steps' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TransferWorkflowSteps"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#description TransferWorkflow#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#id TransferWorkflow#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_exception_steps(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TransferWorkflowOnExceptionSteps"]]]:
        '''on_exception_steps block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#on_exception_steps TransferWorkflow#on_exception_steps}
        '''
        result = self._values.get("on_exception_steps")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TransferWorkflowOnExceptionSteps"]]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#region TransferWorkflow#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#tags TransferWorkflow#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#tags_all TransferWorkflow#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionSteps",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "copy_step_details": "copyStepDetails",
        "custom_step_details": "customStepDetails",
        "decrypt_step_details": "decryptStepDetails",
        "delete_step_details": "deleteStepDetails",
        "tag_step_details": "tagStepDetails",
    },
)
class TransferWorkflowOnExceptionSteps:
    def __init__(
        self,
        *,
        type: builtins.str,
        copy_step_details: typing.Optional[typing.Union["TransferWorkflowOnExceptionStepsCopyStepDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_step_details: typing.Optional[typing.Union["TransferWorkflowOnExceptionStepsCustomStepDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        decrypt_step_details: typing.Optional[typing.Union["TransferWorkflowOnExceptionStepsDecryptStepDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        delete_step_details: typing.Optional[typing.Union["TransferWorkflowOnExceptionStepsDeleteStepDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_step_details: typing.Optional[typing.Union["TransferWorkflowOnExceptionStepsTagStepDetails", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#type TransferWorkflow#type}.
        :param copy_step_details: copy_step_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#copy_step_details TransferWorkflow#copy_step_details}
        :param custom_step_details: custom_step_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#custom_step_details TransferWorkflow#custom_step_details}
        :param decrypt_step_details: decrypt_step_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#decrypt_step_details TransferWorkflow#decrypt_step_details}
        :param delete_step_details: delete_step_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#delete_step_details TransferWorkflow#delete_step_details}
        :param tag_step_details: tag_step_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#tag_step_details TransferWorkflow#tag_step_details}
        '''
        if isinstance(copy_step_details, dict):
            copy_step_details = TransferWorkflowOnExceptionStepsCopyStepDetails(**copy_step_details)
        if isinstance(custom_step_details, dict):
            custom_step_details = TransferWorkflowOnExceptionStepsCustomStepDetails(**custom_step_details)
        if isinstance(decrypt_step_details, dict):
            decrypt_step_details = TransferWorkflowOnExceptionStepsDecryptStepDetails(**decrypt_step_details)
        if isinstance(delete_step_details, dict):
            delete_step_details = TransferWorkflowOnExceptionStepsDeleteStepDetails(**delete_step_details)
        if isinstance(tag_step_details, dict):
            tag_step_details = TransferWorkflowOnExceptionStepsTagStepDetails(**tag_step_details)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3499701a3d25fe40ec6df9c68def9710800aa1cd43c6e1ac769810436560d8b)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument copy_step_details", value=copy_step_details, expected_type=type_hints["copy_step_details"])
            check_type(argname="argument custom_step_details", value=custom_step_details, expected_type=type_hints["custom_step_details"])
            check_type(argname="argument decrypt_step_details", value=decrypt_step_details, expected_type=type_hints["decrypt_step_details"])
            check_type(argname="argument delete_step_details", value=delete_step_details, expected_type=type_hints["delete_step_details"])
            check_type(argname="argument tag_step_details", value=tag_step_details, expected_type=type_hints["tag_step_details"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if copy_step_details is not None:
            self._values["copy_step_details"] = copy_step_details
        if custom_step_details is not None:
            self._values["custom_step_details"] = custom_step_details
        if decrypt_step_details is not None:
            self._values["decrypt_step_details"] = decrypt_step_details
        if delete_step_details is not None:
            self._values["delete_step_details"] = delete_step_details
        if tag_step_details is not None:
            self._values["tag_step_details"] = tag_step_details

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#type TransferWorkflow#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def copy_step_details(
        self,
    ) -> typing.Optional["TransferWorkflowOnExceptionStepsCopyStepDetails"]:
        '''copy_step_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#copy_step_details TransferWorkflow#copy_step_details}
        '''
        result = self._values.get("copy_step_details")
        return typing.cast(typing.Optional["TransferWorkflowOnExceptionStepsCopyStepDetails"], result)

    @builtins.property
    def custom_step_details(
        self,
    ) -> typing.Optional["TransferWorkflowOnExceptionStepsCustomStepDetails"]:
        '''custom_step_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#custom_step_details TransferWorkflow#custom_step_details}
        '''
        result = self._values.get("custom_step_details")
        return typing.cast(typing.Optional["TransferWorkflowOnExceptionStepsCustomStepDetails"], result)

    @builtins.property
    def decrypt_step_details(
        self,
    ) -> typing.Optional["TransferWorkflowOnExceptionStepsDecryptStepDetails"]:
        '''decrypt_step_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#decrypt_step_details TransferWorkflow#decrypt_step_details}
        '''
        result = self._values.get("decrypt_step_details")
        return typing.cast(typing.Optional["TransferWorkflowOnExceptionStepsDecryptStepDetails"], result)

    @builtins.property
    def delete_step_details(
        self,
    ) -> typing.Optional["TransferWorkflowOnExceptionStepsDeleteStepDetails"]:
        '''delete_step_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#delete_step_details TransferWorkflow#delete_step_details}
        '''
        result = self._values.get("delete_step_details")
        return typing.cast(typing.Optional["TransferWorkflowOnExceptionStepsDeleteStepDetails"], result)

    @builtins.property
    def tag_step_details(
        self,
    ) -> typing.Optional["TransferWorkflowOnExceptionStepsTagStepDetails"]:
        '''tag_step_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#tag_step_details TransferWorkflow#tag_step_details}
        '''
        result = self._values.get("tag_step_details")
        return typing.cast(typing.Optional["TransferWorkflowOnExceptionStepsTagStepDetails"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowOnExceptionSteps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsCopyStepDetails",
    jsii_struct_bases=[],
    name_mapping={
        "destination_file_location": "destinationFileLocation",
        "name": "name",
        "overwrite_existing": "overwriteExisting",
        "source_file_location": "sourceFileLocation",
    },
)
class TransferWorkflowOnExceptionStepsCopyStepDetails:
    def __init__(
        self,
        *,
        destination_file_location: typing.Optional[typing.Union["TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        overwrite_existing: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination_file_location: destination_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#destination_file_location TransferWorkflow#destination_file_location}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param overwrite_existing: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#overwrite_existing TransferWorkflow#overwrite_existing}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        '''
        if isinstance(destination_file_location, dict):
            destination_file_location = TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocation(**destination_file_location)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54afa8429b00a0c9fcf26dc0006212101c1553fb2fe3f425251e9a776dc11153)
            check_type(argname="argument destination_file_location", value=destination_file_location, expected_type=type_hints["destination_file_location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument overwrite_existing", value=overwrite_existing, expected_type=type_hints["overwrite_existing"])
            check_type(argname="argument source_file_location", value=source_file_location, expected_type=type_hints["source_file_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination_file_location is not None:
            self._values["destination_file_location"] = destination_file_location
        if name is not None:
            self._values["name"] = name
        if overwrite_existing is not None:
            self._values["overwrite_existing"] = overwrite_existing
        if source_file_location is not None:
            self._values["source_file_location"] = source_file_location

    @builtins.property
    def destination_file_location(
        self,
    ) -> typing.Optional["TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocation"]:
        '''destination_file_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#destination_file_location TransferWorkflow#destination_file_location}
        '''
        result = self._values.get("destination_file_location")
        return typing.cast(typing.Optional["TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocation"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def overwrite_existing(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#overwrite_existing TransferWorkflow#overwrite_existing}.'''
        result = self._values.get("overwrite_existing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_file_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.'''
        result = self._values.get("source_file_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowOnExceptionStepsCopyStepDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocation",
    jsii_struct_bases=[],
    name_mapping={
        "efs_file_location": "efsFileLocation",
        "s3_file_location": "s3FileLocation",
    },
)
class TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocation:
    def __init__(
        self,
        *,
        efs_file_location: typing.Optional[typing.Union["TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_file_location: typing.Optional[typing.Union["TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param efs_file_location: efs_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#efs_file_location TransferWorkflow#efs_file_location}
        :param s3_file_location: s3_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#s3_file_location TransferWorkflow#s3_file_location}
        '''
        if isinstance(efs_file_location, dict):
            efs_file_location = TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocation(**efs_file_location)
        if isinstance(s3_file_location, dict):
            s3_file_location = TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocation(**s3_file_location)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b18803fe80686d3513e424845073c5f48688a6cffc955365afc13d329e30d375)
            check_type(argname="argument efs_file_location", value=efs_file_location, expected_type=type_hints["efs_file_location"])
            check_type(argname="argument s3_file_location", value=s3_file_location, expected_type=type_hints["s3_file_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if efs_file_location is not None:
            self._values["efs_file_location"] = efs_file_location
        if s3_file_location is not None:
            self._values["s3_file_location"] = s3_file_location

    @builtins.property
    def efs_file_location(
        self,
    ) -> typing.Optional["TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocation"]:
        '''efs_file_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#efs_file_location TransferWorkflow#efs_file_location}
        '''
        result = self._values.get("efs_file_location")
        return typing.cast(typing.Optional["TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocation"], result)

    @builtins.property
    def s3_file_location(
        self,
    ) -> typing.Optional["TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocation"]:
        '''s3_file_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#s3_file_location TransferWorkflow#s3_file_location}
        '''
        result = self._values.get("s3_file_location")
        return typing.cast(typing.Optional["TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocation",
    jsii_struct_bases=[],
    name_mapping={"file_system_id": "fileSystemId", "path": "path"},
)
class TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocation:
    def __init__(
        self,
        *,
        file_system_id: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_system_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#file_system_id TransferWorkflow#file_system_id}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#path TransferWorkflow#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4219ba881c73d99011d32e3a96a3d86225c8e1a27f42bb0c8aa3323fb1f92883)
            check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file_system_id is not None:
            self._values["file_system_id"] = file_system_id
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def file_system_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#file_system_id TransferWorkflow#file_system_id}.'''
        result = self._values.get("file_system_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#path TransferWorkflow#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ecb399bfbdcc4728b45c704f39226ed2038a4dffa4480e118a842c051380ec4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFileSystemId")
    def reset_file_system_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileSystemId", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="fileSystemIdInput")
    def file_system_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileSystemIdInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileSystemId"))

    @file_system_id.setter
    def file_system_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__681cee368434708d2c66d6cf07ccd00ea6472642571301d104861670249cd56e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileSystemId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__261bb972e38fc133c6536f7e644e36a76637d8357e6140380b487a3e68aa19a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc96713bebc9fe988a5e76c30b9b711044937b749f9b7abb2e1ac9ca76efd403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe706f65079cafc8de90ad5ec9a517034e65518e400ef02d85e2c76b706700e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEfsFileLocation")
    def put_efs_file_location(
        self,
        *,
        file_system_id: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_system_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#file_system_id TransferWorkflow#file_system_id}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#path TransferWorkflow#path}.
        '''
        value = TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocation(
            file_system_id=file_system_id, path=path
        )

        return typing.cast(None, jsii.invoke(self, "putEfsFileLocation", [value]))

    @jsii.member(jsii_name="putS3FileLocation")
    def put_s3_file_location(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#bucket TransferWorkflow#bucket}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#key TransferWorkflow#key}.
        '''
        value = TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocation(
            bucket=bucket, key=key
        )

        return typing.cast(None, jsii.invoke(self, "putS3FileLocation", [value]))

    @jsii.member(jsii_name="resetEfsFileLocation")
    def reset_efs_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEfsFileLocation", []))

    @jsii.member(jsii_name="resetS3FileLocation")
    def reset_s3_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3FileLocation", []))

    @builtins.property
    @jsii.member(jsii_name="efsFileLocation")
    def efs_file_location(
        self,
    ) -> TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocationOutputReference:
        return typing.cast(TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocationOutputReference, jsii.get(self, "efsFileLocation"))

    @builtins.property
    @jsii.member(jsii_name="s3FileLocation")
    def s3_file_location(
        self,
    ) -> "TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocationOutputReference":
        return typing.cast("TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocationOutputReference", jsii.get(self, "s3FileLocation"))

    @builtins.property
    @jsii.member(jsii_name="efsFileLocationInput")
    def efs_file_location_input(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocation], jsii.get(self, "efsFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="s3FileLocationInput")
    def s3_file_location_input(
        self,
    ) -> typing.Optional["TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocation"]:
        return typing.cast(typing.Optional["TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocation"], jsii.get(self, "s3FileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd803a51316fcfd674ebaaecd24d9c27b76dc7c80ed37d6ebd2edd65dd439862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocation",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "key": "key"},
)
class TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocation:
    def __init__(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#bucket TransferWorkflow#bucket}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#key TransferWorkflow#key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fdfd293ca19493239eec7780abb0998cdcf3e0948057e7e9919b79f659c7d50)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if key is not None:
            self._values["key"] = key

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#bucket TransferWorkflow#bucket}.'''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#key TransferWorkflow#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0b03977935ba9bc8af87cfca01ea0def3d97356245b67e5da1cd25aae91e82d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucket")
    def reset_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucket", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a57552a7075a8bbab9e2180436edf675e79db801bb087ad8090b3f6c2437f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02709721fcb20cb8fdd0836cbb6ea02160fef653a90e1125ffc15e8a9f459b08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b7d1764f177aae96a193a6e542e8650b05445473cf87ca0968c96e8fb0d7acf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TransferWorkflowOnExceptionStepsCopyStepDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsCopyStepDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba79f499d5964273c9e1d1560be620e5070d45a87c76d89fd9959d46ed54aea5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDestinationFileLocation")
    def put_destination_file_location(
        self,
        *,
        efs_file_location: typing.Optional[typing.Union[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
        s3_file_location: typing.Optional[typing.Union[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param efs_file_location: efs_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#efs_file_location TransferWorkflow#efs_file_location}
        :param s3_file_location: s3_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#s3_file_location TransferWorkflow#s3_file_location}
        '''
        value = TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocation(
            efs_file_location=efs_file_location, s3_file_location=s3_file_location
        )

        return typing.cast(None, jsii.invoke(self, "putDestinationFileLocation", [value]))

    @jsii.member(jsii_name="resetDestinationFileLocation")
    def reset_destination_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationFileLocation", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOverwriteExisting")
    def reset_overwrite_existing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwriteExisting", []))

    @jsii.member(jsii_name="resetSourceFileLocation")
    def reset_source_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFileLocation", []))

    @builtins.property
    @jsii.member(jsii_name="destinationFileLocation")
    def destination_file_location(
        self,
    ) -> TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationOutputReference:
        return typing.cast(TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationOutputReference, jsii.get(self, "destinationFileLocation"))

    @builtins.property
    @jsii.member(jsii_name="destinationFileLocationInput")
    def destination_file_location_input(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocation], jsii.get(self, "destinationFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteExistingInput")
    def overwrite_existing_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "overwriteExistingInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocationInput")
    def source_file_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c72c25e5638ff013cca4a7141156caa2cbba7884e14c05a052509bfc2757b80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overwriteExisting")
    def overwrite_existing(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "overwriteExisting"))

    @overwrite_existing.setter
    def overwrite_existing(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6754defcee7619011d6943fac24c6bf7fec00969949b1916f8071a3118443229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwriteExisting", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocation")
    def source_file_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFileLocation"))

    @source_file_location.setter
    def source_file_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dc6964b2317001b8bab4544ebf66b823a2569d2cc5b635c15d0fb1861c871cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFileLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetails]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d588a8d0fe4c0a7c43fc9d24aa4fe28c19332545b0db80f11bdc09c848875e92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsCustomStepDetails",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "source_file_location": "sourceFileLocation",
        "target": "target",
        "timeout_seconds": "timeoutSeconds",
    },
)
class TransferWorkflowOnExceptionStepsCustomStepDetails:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#target TransferWorkflow#target}.
        :param timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#timeout_seconds TransferWorkflow#timeout_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9610f1055760504ab7ad86ba654cf82062c8bf06ae80a48edc7de863218981bc)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source_file_location", value=source_file_location, expected_type=type_hints["source_file_location"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if source_file_location is not None:
            self._values["source_file_location"] = source_file_location
        if target is not None:
            self._values["target"] = target
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_file_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.'''
        result = self._values.get("source_file_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#target TransferWorkflow#target}.'''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#timeout_seconds TransferWorkflow#timeout_seconds}.'''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowOnExceptionStepsCustomStepDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferWorkflowOnExceptionStepsCustomStepDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsCustomStepDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07f0b482862da9464829adc26adbd6dfb448b1937569f07d6e9377b1d07bf9bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSourceFileLocation")
    def reset_source_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFileLocation", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @jsii.member(jsii_name="resetTimeoutSeconds")
    def reset_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocationInput")
    def source_file_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecondsInput")
    def timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a7154792844c4a361a21126229f1d16e010971358743c9a15fcc479cf65ae1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocation")
    def source_file_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFileLocation"))

    @source_file_location.setter
    def source_file_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5691e13f11fc23417d76e58ad7e9d9d76c17df62ede47cd52c7233fd1b22e854)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFileLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce107777d70cdea29db0c1f4cb56ed444903210f877932709e97c9da716a951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c3bb7787e7db459bf2a2be396da177958cd9cf17ffd768d41030fc15647fc57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsCustomStepDetails]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsCustomStepDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowOnExceptionStepsCustomStepDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f028375f3e1f46624863246b648cf913310dcc63826e0b8fb0061cecfe1799a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsDecryptStepDetails",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "destination_file_location": "destinationFileLocation",
        "name": "name",
        "overwrite_existing": "overwriteExisting",
        "source_file_location": "sourceFileLocation",
    },
)
class TransferWorkflowOnExceptionStepsDecryptStepDetails:
    def __init__(
        self,
        *,
        type: builtins.str,
        destination_file_location: typing.Optional[typing.Union["TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        overwrite_existing: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#type TransferWorkflow#type}.
        :param destination_file_location: destination_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#destination_file_location TransferWorkflow#destination_file_location}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param overwrite_existing: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#overwrite_existing TransferWorkflow#overwrite_existing}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        '''
        if isinstance(destination_file_location, dict):
            destination_file_location = TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocation(**destination_file_location)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17b55cfcd07a3b341ba1300cd7e9bb256e027195df6cc19ba9d3043a0e4db387)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument destination_file_location", value=destination_file_location, expected_type=type_hints["destination_file_location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument overwrite_existing", value=overwrite_existing, expected_type=type_hints["overwrite_existing"])
            check_type(argname="argument source_file_location", value=source_file_location, expected_type=type_hints["source_file_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if destination_file_location is not None:
            self._values["destination_file_location"] = destination_file_location
        if name is not None:
            self._values["name"] = name
        if overwrite_existing is not None:
            self._values["overwrite_existing"] = overwrite_existing
        if source_file_location is not None:
            self._values["source_file_location"] = source_file_location

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#type TransferWorkflow#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_file_location(
        self,
    ) -> typing.Optional["TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocation"]:
        '''destination_file_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#destination_file_location TransferWorkflow#destination_file_location}
        '''
        result = self._values.get("destination_file_location")
        return typing.cast(typing.Optional["TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocation"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def overwrite_existing(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#overwrite_existing TransferWorkflow#overwrite_existing}.'''
        result = self._values.get("overwrite_existing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_file_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.'''
        result = self._values.get("source_file_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowOnExceptionStepsDecryptStepDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocation",
    jsii_struct_bases=[],
    name_mapping={
        "efs_file_location": "efsFileLocation",
        "s3_file_location": "s3FileLocation",
    },
)
class TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocation:
    def __init__(
        self,
        *,
        efs_file_location: typing.Optional[typing.Union["TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_file_location: typing.Optional[typing.Union["TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param efs_file_location: efs_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#efs_file_location TransferWorkflow#efs_file_location}
        :param s3_file_location: s3_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#s3_file_location TransferWorkflow#s3_file_location}
        '''
        if isinstance(efs_file_location, dict):
            efs_file_location = TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation(**efs_file_location)
        if isinstance(s3_file_location, dict):
            s3_file_location = TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocation(**s3_file_location)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9ff2d44bc5cb0c560ce5484884cf6a81deaa243077d8a2db0ade3c56567261)
            check_type(argname="argument efs_file_location", value=efs_file_location, expected_type=type_hints["efs_file_location"])
            check_type(argname="argument s3_file_location", value=s3_file_location, expected_type=type_hints["s3_file_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if efs_file_location is not None:
            self._values["efs_file_location"] = efs_file_location
        if s3_file_location is not None:
            self._values["s3_file_location"] = s3_file_location

    @builtins.property
    def efs_file_location(
        self,
    ) -> typing.Optional["TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation"]:
        '''efs_file_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#efs_file_location TransferWorkflow#efs_file_location}
        '''
        result = self._values.get("efs_file_location")
        return typing.cast(typing.Optional["TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation"], result)

    @builtins.property
    def s3_file_location(
        self,
    ) -> typing.Optional["TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocation"]:
        '''s3_file_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#s3_file_location TransferWorkflow#s3_file_location}
        '''
        result = self._values.get("s3_file_location")
        return typing.cast(typing.Optional["TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation",
    jsii_struct_bases=[],
    name_mapping={"file_system_id": "fileSystemId", "path": "path"},
)
class TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation:
    def __init__(
        self,
        *,
        file_system_id: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_system_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#file_system_id TransferWorkflow#file_system_id}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#path TransferWorkflow#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af3fc9f246354b8e061a855f14e5c1c58fafa8298ef2ae940f6103f64122b076)
            check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file_system_id is not None:
            self._values["file_system_id"] = file_system_id
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def file_system_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#file_system_id TransferWorkflow#file_system_id}.'''
        result = self._values.get("file_system_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#path TransferWorkflow#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1f481168180d396fec4d87f139c93e5b8796ae71654cef57a93761e789754a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFileSystemId")
    def reset_file_system_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileSystemId", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="fileSystemIdInput")
    def file_system_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileSystemIdInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileSystemId"))

    @file_system_id.setter
    def file_system_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf304a1cd8c5451434b093e8788c786ca7203b263b9d6b8da418a2733a7e214d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileSystemId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e391f927bb3b12268fa2a60e9a502e4e5e564a0c35ca1f9e581321324ab34ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ace535763a6b9ed88184980e6e4544bf00dd340319d297f5a496608660495ad3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__589502ee97b794abc045c068f20cd3e23eeeae8c245aef8ccae42b2efc689f0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEfsFileLocation")
    def put_efs_file_location(
        self,
        *,
        file_system_id: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_system_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#file_system_id TransferWorkflow#file_system_id}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#path TransferWorkflow#path}.
        '''
        value = TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation(
            file_system_id=file_system_id, path=path
        )

        return typing.cast(None, jsii.invoke(self, "putEfsFileLocation", [value]))

    @jsii.member(jsii_name="putS3FileLocation")
    def put_s3_file_location(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#bucket TransferWorkflow#bucket}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#key TransferWorkflow#key}.
        '''
        value = TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocation(
            bucket=bucket, key=key
        )

        return typing.cast(None, jsii.invoke(self, "putS3FileLocation", [value]))

    @jsii.member(jsii_name="resetEfsFileLocation")
    def reset_efs_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEfsFileLocation", []))

    @jsii.member(jsii_name="resetS3FileLocation")
    def reset_s3_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3FileLocation", []))

    @builtins.property
    @jsii.member(jsii_name="efsFileLocation")
    def efs_file_location(
        self,
    ) -> TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocationOutputReference:
        return typing.cast(TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocationOutputReference, jsii.get(self, "efsFileLocation"))

    @builtins.property
    @jsii.member(jsii_name="s3FileLocation")
    def s3_file_location(
        self,
    ) -> "TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocationOutputReference":
        return typing.cast("TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocationOutputReference", jsii.get(self, "s3FileLocation"))

    @builtins.property
    @jsii.member(jsii_name="efsFileLocationInput")
    def efs_file_location_input(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation], jsii.get(self, "efsFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="s3FileLocationInput")
    def s3_file_location_input(
        self,
    ) -> typing.Optional["TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocation"]:
        return typing.cast(typing.Optional["TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocation"], jsii.get(self, "s3FileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6165ea4c93488e4655acc42cc3d12175b373390ea80fab6cd0d3592c57e63350)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocation",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "key": "key"},
)
class TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocation:
    def __init__(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#bucket TransferWorkflow#bucket}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#key TransferWorkflow#key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__273944b679315ee172a4e628de5809a466c001080c57f069ae014b4e5ded06bc)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if key is not None:
            self._values["key"] = key

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#bucket TransferWorkflow#bucket}.'''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#key TransferWorkflow#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c9bb64fbbff9cd66e73f78ff5fde606d9cb177a6511d13944066d5246498a5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucket")
    def reset_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucket", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d629ad3cd92d221b566b4d52610bdb32c72728a624728578e3f897016c495232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2f052c638dcf9f1096b6764ef7b4e34e796b8bc865226527832c91d3d88a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ce42210de92ec12c9978182a5aa282742a6fefe3b8507a0f722a6df2d5f24e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TransferWorkflowOnExceptionStepsDecryptStepDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsDecryptStepDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cb6548dd834b434e1ef9b3bfaae2cc819aac7dd1e3a5f599e18b3e10080f6d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDestinationFileLocation")
    def put_destination_file_location(
        self,
        *,
        efs_file_location: typing.Optional[typing.Union[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
        s3_file_location: typing.Optional[typing.Union[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param efs_file_location: efs_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#efs_file_location TransferWorkflow#efs_file_location}
        :param s3_file_location: s3_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#s3_file_location TransferWorkflow#s3_file_location}
        '''
        value = TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocation(
            efs_file_location=efs_file_location, s3_file_location=s3_file_location
        )

        return typing.cast(None, jsii.invoke(self, "putDestinationFileLocation", [value]))

    @jsii.member(jsii_name="resetDestinationFileLocation")
    def reset_destination_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationFileLocation", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOverwriteExisting")
    def reset_overwrite_existing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwriteExisting", []))

    @jsii.member(jsii_name="resetSourceFileLocation")
    def reset_source_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFileLocation", []))

    @builtins.property
    @jsii.member(jsii_name="destinationFileLocation")
    def destination_file_location(
        self,
    ) -> TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationOutputReference:
        return typing.cast(TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationOutputReference, jsii.get(self, "destinationFileLocation"))

    @builtins.property
    @jsii.member(jsii_name="destinationFileLocationInput")
    def destination_file_location_input(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocation], jsii.get(self, "destinationFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteExistingInput")
    def overwrite_existing_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "overwriteExistingInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocationInput")
    def source_file_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1190b0eee23326baf2b8b5e385ef9a4a45867bc9f2f5ee9763cccc06e20afdc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overwriteExisting")
    def overwrite_existing(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "overwriteExisting"))

    @overwrite_existing.setter
    def overwrite_existing(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ef68e3eef28b7e2cd2f6ff862fa01ce9a7a28387a4ca9ebb4a48ac78f02abb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwriteExisting", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocation")
    def source_file_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFileLocation"))

    @source_file_location.setter
    def source_file_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6013a0047a8a9ec43479653ae286ccc15770b943c484e0427cd0348765d8758d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFileLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84f5478bc035baad60068bf727d457f6b5d934f3a93b4cfdffe8e1b29510a95a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetails]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc7bdb88412147649262b67b1e51ead251a530a53c21023c946277c50161abe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsDeleteStepDetails",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "source_file_location": "sourceFileLocation"},
)
class TransferWorkflowOnExceptionStepsDeleteStepDetails:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85761cec8e4f3b25c0d8935ba6ca3fa6beaea63670c87e3feccd05bd50b8d464)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source_file_location", value=source_file_location, expected_type=type_hints["source_file_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if source_file_location is not None:
            self._values["source_file_location"] = source_file_location

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_file_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.'''
        result = self._values.get("source_file_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowOnExceptionStepsDeleteStepDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferWorkflowOnExceptionStepsDeleteStepDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsDeleteStepDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b079b97d902558b7be26eda4d22d47a34fdc96ed329ec8be60ba5c3749cfa99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSourceFileLocation")
    def reset_source_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFileLocation", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocationInput")
    def source_file_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e8c895ab410bf30250ecfddebcbc1620cbd16bc74ca351eccf55e562b383ed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocation")
    def source_file_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFileLocation"))

    @source_file_location.setter
    def source_file_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__965987ae8b648a6861f6ee7a85bd17d0104f95bc6a39dfc8899f323db8bd9bd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFileLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsDeleteStepDetails]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsDeleteStepDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowOnExceptionStepsDeleteStepDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4923eb86d43193bc51cd27c9b90f7991095106270075aad2e27cb48dcbd46c6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TransferWorkflowOnExceptionStepsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff53d76cd9ea94947a5681538f36079ed18c6de15f9d42cf5ada8c170ad2c059)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TransferWorkflowOnExceptionStepsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c568f1972f5a655db9e5d47acb25fbc4936651c79dca8b08c14f58526ce6cd1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TransferWorkflowOnExceptionStepsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441f603a47ba3f3057c6a3cf9c2bce6bb085c18b2ebe5544492117a6f662925c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca4faba0407fa59e758a15a55573f894b5bace84fe8979154ec8bed1e7618617)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b8f43c152c96ba08c32a9c844f59506690ef07ae7e26371790466cda1cd31b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TransferWorkflowOnExceptionSteps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TransferWorkflowOnExceptionSteps]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TransferWorkflowOnExceptionSteps]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__628664ef380a4510bb486c9299f684c48e1d9bca7ff5a7d1517bc731d6ed1319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TransferWorkflowOnExceptionStepsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a677e71e6b60aeee10932258744ff8f037d89b989a3aa03272ea412634c327f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCopyStepDetails")
    def put_copy_step_details(
        self,
        *,
        destination_file_location: typing.Optional[typing.Union[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        overwrite_existing: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination_file_location: destination_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#destination_file_location TransferWorkflow#destination_file_location}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param overwrite_existing: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#overwrite_existing TransferWorkflow#overwrite_existing}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        '''
        value = TransferWorkflowOnExceptionStepsCopyStepDetails(
            destination_file_location=destination_file_location,
            name=name,
            overwrite_existing=overwrite_existing,
            source_file_location=source_file_location,
        )

        return typing.cast(None, jsii.invoke(self, "putCopyStepDetails", [value]))

    @jsii.member(jsii_name="putCustomStepDetails")
    def put_custom_step_details(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#target TransferWorkflow#target}.
        :param timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#timeout_seconds TransferWorkflow#timeout_seconds}.
        '''
        value = TransferWorkflowOnExceptionStepsCustomStepDetails(
            name=name,
            source_file_location=source_file_location,
            target=target,
            timeout_seconds=timeout_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomStepDetails", [value]))

    @jsii.member(jsii_name="putDecryptStepDetails")
    def put_decrypt_step_details(
        self,
        *,
        type: builtins.str,
        destination_file_location: typing.Optional[typing.Union[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        overwrite_existing: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#type TransferWorkflow#type}.
        :param destination_file_location: destination_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#destination_file_location TransferWorkflow#destination_file_location}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param overwrite_existing: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#overwrite_existing TransferWorkflow#overwrite_existing}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        '''
        value = TransferWorkflowOnExceptionStepsDecryptStepDetails(
            type=type,
            destination_file_location=destination_file_location,
            name=name,
            overwrite_existing=overwrite_existing,
            source_file_location=source_file_location,
        )

        return typing.cast(None, jsii.invoke(self, "putDecryptStepDetails", [value]))

    @jsii.member(jsii_name="putDeleteStepDetails")
    def put_delete_step_details(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        '''
        value = TransferWorkflowOnExceptionStepsDeleteStepDetails(
            name=name, source_file_location=source_file_location
        )

        return typing.cast(None, jsii.invoke(self, "putDeleteStepDetails", [value]))

    @jsii.member(jsii_name="putTagStepDetails")
    def put_tag_step_details(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TransferWorkflowOnExceptionStepsTagStepDetailsTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        :param tags: tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#tags TransferWorkflow#tags}
        '''
        value = TransferWorkflowOnExceptionStepsTagStepDetails(
            name=name, source_file_location=source_file_location, tags=tags
        )

        return typing.cast(None, jsii.invoke(self, "putTagStepDetails", [value]))

    @jsii.member(jsii_name="resetCopyStepDetails")
    def reset_copy_step_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyStepDetails", []))

    @jsii.member(jsii_name="resetCustomStepDetails")
    def reset_custom_step_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomStepDetails", []))

    @jsii.member(jsii_name="resetDecryptStepDetails")
    def reset_decrypt_step_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDecryptStepDetails", []))

    @jsii.member(jsii_name="resetDeleteStepDetails")
    def reset_delete_step_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteStepDetails", []))

    @jsii.member(jsii_name="resetTagStepDetails")
    def reset_tag_step_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagStepDetails", []))

    @builtins.property
    @jsii.member(jsii_name="copyStepDetails")
    def copy_step_details(
        self,
    ) -> TransferWorkflowOnExceptionStepsCopyStepDetailsOutputReference:
        return typing.cast(TransferWorkflowOnExceptionStepsCopyStepDetailsOutputReference, jsii.get(self, "copyStepDetails"))

    @builtins.property
    @jsii.member(jsii_name="customStepDetails")
    def custom_step_details(
        self,
    ) -> TransferWorkflowOnExceptionStepsCustomStepDetailsOutputReference:
        return typing.cast(TransferWorkflowOnExceptionStepsCustomStepDetailsOutputReference, jsii.get(self, "customStepDetails"))

    @builtins.property
    @jsii.member(jsii_name="decryptStepDetails")
    def decrypt_step_details(
        self,
    ) -> TransferWorkflowOnExceptionStepsDecryptStepDetailsOutputReference:
        return typing.cast(TransferWorkflowOnExceptionStepsDecryptStepDetailsOutputReference, jsii.get(self, "decryptStepDetails"))

    @builtins.property
    @jsii.member(jsii_name="deleteStepDetails")
    def delete_step_details(
        self,
    ) -> TransferWorkflowOnExceptionStepsDeleteStepDetailsOutputReference:
        return typing.cast(TransferWorkflowOnExceptionStepsDeleteStepDetailsOutputReference, jsii.get(self, "deleteStepDetails"))

    @builtins.property
    @jsii.member(jsii_name="tagStepDetails")
    def tag_step_details(
        self,
    ) -> "TransferWorkflowOnExceptionStepsTagStepDetailsOutputReference":
        return typing.cast("TransferWorkflowOnExceptionStepsTagStepDetailsOutputReference", jsii.get(self, "tagStepDetails"))

    @builtins.property
    @jsii.member(jsii_name="copyStepDetailsInput")
    def copy_step_details_input(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetails]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetails], jsii.get(self, "copyStepDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="customStepDetailsInput")
    def custom_step_details_input(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsCustomStepDetails]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsCustomStepDetails], jsii.get(self, "customStepDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="decryptStepDetailsInput")
    def decrypt_step_details_input(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetails]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetails], jsii.get(self, "decryptStepDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteStepDetailsInput")
    def delete_step_details_input(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsDeleteStepDetails]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsDeleteStepDetails], jsii.get(self, "deleteStepDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagStepDetailsInput")
    def tag_step_details_input(
        self,
    ) -> typing.Optional["TransferWorkflowOnExceptionStepsTagStepDetails"]:
        return typing.cast(typing.Optional["TransferWorkflowOnExceptionStepsTagStepDetails"], jsii.get(self, "tagStepDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af4205fd68b08603eb6126aee4d66855ac74c184205eb390436a595f2595286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferWorkflowOnExceptionSteps]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferWorkflowOnExceptionSteps]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferWorkflowOnExceptionSteps]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81dbff235d1972e4f380708b88a6f7ae1569f611e45cd3e5aa8278d1c1982cd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsTagStepDetails",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "source_file_location": "sourceFileLocation",
        "tags": "tags",
    },
)
class TransferWorkflowOnExceptionStepsTagStepDetails:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TransferWorkflowOnExceptionStepsTagStepDetailsTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        :param tags: tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#tags TransferWorkflow#tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72f930725aecde9b821bb634a350f7364b94896c16597235b6b171841ef78cf1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source_file_location", value=source_file_location, expected_type=type_hints["source_file_location"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if source_file_location is not None:
            self._values["source_file_location"] = source_file_location
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_file_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.'''
        result = self._values.get("source_file_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TransferWorkflowOnExceptionStepsTagStepDetailsTags"]]]:
        '''tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#tags TransferWorkflow#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TransferWorkflowOnExceptionStepsTagStepDetailsTags"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowOnExceptionStepsTagStepDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferWorkflowOnExceptionStepsTagStepDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsTagStepDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8382266883c5f4c6c1599ea841ef44793c79b179b16bf07d742e22fa74e2d93)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTags")
    def put_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TransferWorkflowOnExceptionStepsTagStepDetailsTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b66cb300c6c43985e1acf70e8cd042f2aadd4ff23a4f5ef0992d8240eb69db5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTags", [value]))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSourceFileLocation")
    def reset_source_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFileLocation", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "TransferWorkflowOnExceptionStepsTagStepDetailsTagsList":
        return typing.cast("TransferWorkflowOnExceptionStepsTagStepDetailsTagsList", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocationInput")
    def source_file_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TransferWorkflowOnExceptionStepsTagStepDetailsTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TransferWorkflowOnExceptionStepsTagStepDetailsTags"]]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b355b7b099a5606a0733acde22b883eeba51682eca74afadfe998dba98fd37de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocation")
    def source_file_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFileLocation"))

    @source_file_location.setter
    def source_file_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffab372db67695e331f3c1da5bf78936dc8333de1ac3dd9163d6558925476133)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFileLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferWorkflowOnExceptionStepsTagStepDetails]:
        return typing.cast(typing.Optional[TransferWorkflowOnExceptionStepsTagStepDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowOnExceptionStepsTagStepDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4e6ed0df0422e1a3ed12bce3d5268c205acdf3b6300280dfea45c6a83e02c8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsTagStepDetailsTags",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class TransferWorkflowOnExceptionStepsTagStepDetailsTags:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#key TransferWorkflow#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#value TransferWorkflow#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7989c3a1936d743f744ee82818116ede42617b2c7e632e37738c08ae5def8062)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#key TransferWorkflow#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#value TransferWorkflow#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowOnExceptionStepsTagStepDetailsTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferWorkflowOnExceptionStepsTagStepDetailsTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsTagStepDetailsTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4be91b91099e2e8d219ec475f3471e150b3820da8ed49f462d88af8b66ca0be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TransferWorkflowOnExceptionStepsTagStepDetailsTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef565794854e710dc37acd449de584aca9a0d68b5ab8f9964d74df6f453e41f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TransferWorkflowOnExceptionStepsTagStepDetailsTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb68d931b193b455efe91d32427ab4107fe4a81502fd27f2d433fafbf466b87e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18dee0446e4cc26b34cb56001e024bcff60e9b9f28ac9b28d207f10a5ce6a165)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3597e80d0a580bad8ec4e6e9f2e97094c8d1f6a8091aa72e43700d3a7b5b941e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TransferWorkflowOnExceptionStepsTagStepDetailsTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TransferWorkflowOnExceptionStepsTagStepDetailsTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TransferWorkflowOnExceptionStepsTagStepDetailsTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7d0e75b40fc9f79caa767057e872c3651ff0413d41aef8a289455b27947f2fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TransferWorkflowOnExceptionStepsTagStepDetailsTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowOnExceptionStepsTagStepDetailsTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7da78451e80a8f95c2083d7c180e4b3d5377b27b0443fe3023cd02547d57f28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__759efe1b718b49db425b3ce56ac3eb42381fc4bf3f2544ca84b85a52953f32ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af3d612177bfe2dfa6fac8bee72e42cad1b350e514b073915722498e532ad997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferWorkflowOnExceptionStepsTagStepDetailsTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferWorkflowOnExceptionStepsTagStepDetailsTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferWorkflowOnExceptionStepsTagStepDetailsTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e753982f1d20160e8da3ec95650e8b907358e9a9031a3a8ea506bca9de3eda0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowSteps",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "copy_step_details": "copyStepDetails",
        "custom_step_details": "customStepDetails",
        "decrypt_step_details": "decryptStepDetails",
        "delete_step_details": "deleteStepDetails",
        "tag_step_details": "tagStepDetails",
    },
)
class TransferWorkflowSteps:
    def __init__(
        self,
        *,
        type: builtins.str,
        copy_step_details: typing.Optional[typing.Union["TransferWorkflowStepsCopyStepDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_step_details: typing.Optional[typing.Union["TransferWorkflowStepsCustomStepDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        decrypt_step_details: typing.Optional[typing.Union["TransferWorkflowStepsDecryptStepDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        delete_step_details: typing.Optional[typing.Union["TransferWorkflowStepsDeleteStepDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_step_details: typing.Optional[typing.Union["TransferWorkflowStepsTagStepDetails", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#type TransferWorkflow#type}.
        :param copy_step_details: copy_step_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#copy_step_details TransferWorkflow#copy_step_details}
        :param custom_step_details: custom_step_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#custom_step_details TransferWorkflow#custom_step_details}
        :param decrypt_step_details: decrypt_step_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#decrypt_step_details TransferWorkflow#decrypt_step_details}
        :param delete_step_details: delete_step_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#delete_step_details TransferWorkflow#delete_step_details}
        :param tag_step_details: tag_step_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#tag_step_details TransferWorkflow#tag_step_details}
        '''
        if isinstance(copy_step_details, dict):
            copy_step_details = TransferWorkflowStepsCopyStepDetails(**copy_step_details)
        if isinstance(custom_step_details, dict):
            custom_step_details = TransferWorkflowStepsCustomStepDetails(**custom_step_details)
        if isinstance(decrypt_step_details, dict):
            decrypt_step_details = TransferWorkflowStepsDecryptStepDetails(**decrypt_step_details)
        if isinstance(delete_step_details, dict):
            delete_step_details = TransferWorkflowStepsDeleteStepDetails(**delete_step_details)
        if isinstance(tag_step_details, dict):
            tag_step_details = TransferWorkflowStepsTagStepDetails(**tag_step_details)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fbe3a6f53b1e25f1ed3af20e563acebb5cb739986799c3593cebbc02e1054e0)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument copy_step_details", value=copy_step_details, expected_type=type_hints["copy_step_details"])
            check_type(argname="argument custom_step_details", value=custom_step_details, expected_type=type_hints["custom_step_details"])
            check_type(argname="argument decrypt_step_details", value=decrypt_step_details, expected_type=type_hints["decrypt_step_details"])
            check_type(argname="argument delete_step_details", value=delete_step_details, expected_type=type_hints["delete_step_details"])
            check_type(argname="argument tag_step_details", value=tag_step_details, expected_type=type_hints["tag_step_details"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if copy_step_details is not None:
            self._values["copy_step_details"] = copy_step_details
        if custom_step_details is not None:
            self._values["custom_step_details"] = custom_step_details
        if decrypt_step_details is not None:
            self._values["decrypt_step_details"] = decrypt_step_details
        if delete_step_details is not None:
            self._values["delete_step_details"] = delete_step_details
        if tag_step_details is not None:
            self._values["tag_step_details"] = tag_step_details

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#type TransferWorkflow#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def copy_step_details(
        self,
    ) -> typing.Optional["TransferWorkflowStepsCopyStepDetails"]:
        '''copy_step_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#copy_step_details TransferWorkflow#copy_step_details}
        '''
        result = self._values.get("copy_step_details")
        return typing.cast(typing.Optional["TransferWorkflowStepsCopyStepDetails"], result)

    @builtins.property
    def custom_step_details(
        self,
    ) -> typing.Optional["TransferWorkflowStepsCustomStepDetails"]:
        '''custom_step_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#custom_step_details TransferWorkflow#custom_step_details}
        '''
        result = self._values.get("custom_step_details")
        return typing.cast(typing.Optional["TransferWorkflowStepsCustomStepDetails"], result)

    @builtins.property
    def decrypt_step_details(
        self,
    ) -> typing.Optional["TransferWorkflowStepsDecryptStepDetails"]:
        '''decrypt_step_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#decrypt_step_details TransferWorkflow#decrypt_step_details}
        '''
        result = self._values.get("decrypt_step_details")
        return typing.cast(typing.Optional["TransferWorkflowStepsDecryptStepDetails"], result)

    @builtins.property
    def delete_step_details(
        self,
    ) -> typing.Optional["TransferWorkflowStepsDeleteStepDetails"]:
        '''delete_step_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#delete_step_details TransferWorkflow#delete_step_details}
        '''
        result = self._values.get("delete_step_details")
        return typing.cast(typing.Optional["TransferWorkflowStepsDeleteStepDetails"], result)

    @builtins.property
    def tag_step_details(
        self,
    ) -> typing.Optional["TransferWorkflowStepsTagStepDetails"]:
        '''tag_step_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#tag_step_details TransferWorkflow#tag_step_details}
        '''
        result = self._values.get("tag_step_details")
        return typing.cast(typing.Optional["TransferWorkflowStepsTagStepDetails"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowSteps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsCopyStepDetails",
    jsii_struct_bases=[],
    name_mapping={
        "destination_file_location": "destinationFileLocation",
        "name": "name",
        "overwrite_existing": "overwriteExisting",
        "source_file_location": "sourceFileLocation",
    },
)
class TransferWorkflowStepsCopyStepDetails:
    def __init__(
        self,
        *,
        destination_file_location: typing.Optional[typing.Union["TransferWorkflowStepsCopyStepDetailsDestinationFileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        overwrite_existing: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination_file_location: destination_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#destination_file_location TransferWorkflow#destination_file_location}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param overwrite_existing: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#overwrite_existing TransferWorkflow#overwrite_existing}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        '''
        if isinstance(destination_file_location, dict):
            destination_file_location = TransferWorkflowStepsCopyStepDetailsDestinationFileLocation(**destination_file_location)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864d8b015c2812b80992ac5df59512ecf866996f4d322a44727177393f864288)
            check_type(argname="argument destination_file_location", value=destination_file_location, expected_type=type_hints["destination_file_location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument overwrite_existing", value=overwrite_existing, expected_type=type_hints["overwrite_existing"])
            check_type(argname="argument source_file_location", value=source_file_location, expected_type=type_hints["source_file_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination_file_location is not None:
            self._values["destination_file_location"] = destination_file_location
        if name is not None:
            self._values["name"] = name
        if overwrite_existing is not None:
            self._values["overwrite_existing"] = overwrite_existing
        if source_file_location is not None:
            self._values["source_file_location"] = source_file_location

    @builtins.property
    def destination_file_location(
        self,
    ) -> typing.Optional["TransferWorkflowStepsCopyStepDetailsDestinationFileLocation"]:
        '''destination_file_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#destination_file_location TransferWorkflow#destination_file_location}
        '''
        result = self._values.get("destination_file_location")
        return typing.cast(typing.Optional["TransferWorkflowStepsCopyStepDetailsDestinationFileLocation"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def overwrite_existing(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#overwrite_existing TransferWorkflow#overwrite_existing}.'''
        result = self._values.get("overwrite_existing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_file_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.'''
        result = self._values.get("source_file_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowStepsCopyStepDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsCopyStepDetailsDestinationFileLocation",
    jsii_struct_bases=[],
    name_mapping={
        "efs_file_location": "efsFileLocation",
        "s3_file_location": "s3FileLocation",
    },
)
class TransferWorkflowStepsCopyStepDetailsDestinationFileLocation:
    def __init__(
        self,
        *,
        efs_file_location: typing.Optional[typing.Union["TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_file_location: typing.Optional[typing.Union["TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param efs_file_location: efs_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#efs_file_location TransferWorkflow#efs_file_location}
        :param s3_file_location: s3_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#s3_file_location TransferWorkflow#s3_file_location}
        '''
        if isinstance(efs_file_location, dict):
            efs_file_location = TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocation(**efs_file_location)
        if isinstance(s3_file_location, dict):
            s3_file_location = TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocation(**s3_file_location)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c4016c970fa4f1159c3a00a17ad375e8a528ab48ddf979bb63ee5ea0ea982d)
            check_type(argname="argument efs_file_location", value=efs_file_location, expected_type=type_hints["efs_file_location"])
            check_type(argname="argument s3_file_location", value=s3_file_location, expected_type=type_hints["s3_file_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if efs_file_location is not None:
            self._values["efs_file_location"] = efs_file_location
        if s3_file_location is not None:
            self._values["s3_file_location"] = s3_file_location

    @builtins.property
    def efs_file_location(
        self,
    ) -> typing.Optional["TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocation"]:
        '''efs_file_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#efs_file_location TransferWorkflow#efs_file_location}
        '''
        result = self._values.get("efs_file_location")
        return typing.cast(typing.Optional["TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocation"], result)

    @builtins.property
    def s3_file_location(
        self,
    ) -> typing.Optional["TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocation"]:
        '''s3_file_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#s3_file_location TransferWorkflow#s3_file_location}
        '''
        result = self._values.get("s3_file_location")
        return typing.cast(typing.Optional["TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowStepsCopyStepDetailsDestinationFileLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocation",
    jsii_struct_bases=[],
    name_mapping={"file_system_id": "fileSystemId", "path": "path"},
)
class TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocation:
    def __init__(
        self,
        *,
        file_system_id: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_system_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#file_system_id TransferWorkflow#file_system_id}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#path TransferWorkflow#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd9d4401fddb4e1cc575f5dc636b0efb79326e6a7a2f06987e21dd7eac056e95)
            check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file_system_id is not None:
            self._values["file_system_id"] = file_system_id
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def file_system_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#file_system_id TransferWorkflow#file_system_id}.'''
        result = self._values.get("file_system_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#path TransferWorkflow#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5590d912b40bc45b6e1cdbcbe8dd9ea0bc2d1aa7de440c1b67f0eb5754f6853)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFileSystemId")
    def reset_file_system_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileSystemId", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="fileSystemIdInput")
    def file_system_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileSystemIdInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileSystemId"))

    @file_system_id.setter
    def file_system_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b951ec1b26df4279837c59c661e71bbf11f6e6187e7a2aa4aa790a8de1d054b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileSystemId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b65751f4cb5dee2f6ec85dd4c7a381222d98621fa48445c826491f7f9fd76ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489eab017dd4f7b22766aed2954131c183b7a2bb393b5e64530cdbafe55dab0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TransferWorkflowStepsCopyStepDetailsDestinationFileLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsCopyStepDetailsDestinationFileLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a32bbe3253dac661038f5b38c27e0f19ee44f7e9276c2ca6511376d2bb800d5f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEfsFileLocation")
    def put_efs_file_location(
        self,
        *,
        file_system_id: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_system_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#file_system_id TransferWorkflow#file_system_id}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#path TransferWorkflow#path}.
        '''
        value = TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocation(
            file_system_id=file_system_id, path=path
        )

        return typing.cast(None, jsii.invoke(self, "putEfsFileLocation", [value]))

    @jsii.member(jsii_name="putS3FileLocation")
    def put_s3_file_location(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#bucket TransferWorkflow#bucket}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#key TransferWorkflow#key}.
        '''
        value = TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocation(
            bucket=bucket, key=key
        )

        return typing.cast(None, jsii.invoke(self, "putS3FileLocation", [value]))

    @jsii.member(jsii_name="resetEfsFileLocation")
    def reset_efs_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEfsFileLocation", []))

    @jsii.member(jsii_name="resetS3FileLocation")
    def reset_s3_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3FileLocation", []))

    @builtins.property
    @jsii.member(jsii_name="efsFileLocation")
    def efs_file_location(
        self,
    ) -> TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocationOutputReference:
        return typing.cast(TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocationOutputReference, jsii.get(self, "efsFileLocation"))

    @builtins.property
    @jsii.member(jsii_name="s3FileLocation")
    def s3_file_location(
        self,
    ) -> "TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocationOutputReference":
        return typing.cast("TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocationOutputReference", jsii.get(self, "s3FileLocation"))

    @builtins.property
    @jsii.member(jsii_name="efsFileLocationInput")
    def efs_file_location_input(
        self,
    ) -> typing.Optional[TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocation], jsii.get(self, "efsFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="s3FileLocationInput")
    def s3_file_location_input(
        self,
    ) -> typing.Optional["TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocation"]:
        return typing.cast(typing.Optional["TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocation"], jsii.get(self, "s3FileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferWorkflowStepsCopyStepDetailsDestinationFileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowStepsCopyStepDetailsDestinationFileLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowStepsCopyStepDetailsDestinationFileLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67a74b2230bd89df0a0f999d63f047d5aba845b63f473f4b77af680aa1aa02bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocation",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "key": "key"},
)
class TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocation:
    def __init__(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#bucket TransferWorkflow#bucket}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#key TransferWorkflow#key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361f501a04314127ac3568a580b673325c0579984ee6696e33e5b407ac156caf)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if key is not None:
            self._values["key"] = key

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#bucket TransferWorkflow#bucket}.'''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#key TransferWorkflow#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f917a15f3454747496d56b036aec72a7f7081bb13d3620eaefb7f4ea06d564e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucket")
    def reset_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucket", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__603172c2e4e4c93edc99b8063bb4d2f5bf05abb059bcd297bab9f5169a17ff0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec466f66555f5579118fc8d27ae1116591bf44b065392536b9c8693790daa74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc986ef371f763b12ad076c968d5fb6bb92357d662e41749d78a7e6b723e27f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TransferWorkflowStepsCopyStepDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsCopyStepDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1293814843ac3749a8be7f0c5d7cf0b0c71289706fbcf54e745be3aa51f283ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDestinationFileLocation")
    def put_destination_file_location(
        self,
        *,
        efs_file_location: typing.Optional[typing.Union[TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
        s3_file_location: typing.Optional[typing.Union[TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param efs_file_location: efs_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#efs_file_location TransferWorkflow#efs_file_location}
        :param s3_file_location: s3_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#s3_file_location TransferWorkflow#s3_file_location}
        '''
        value = TransferWorkflowStepsCopyStepDetailsDestinationFileLocation(
            efs_file_location=efs_file_location, s3_file_location=s3_file_location
        )

        return typing.cast(None, jsii.invoke(self, "putDestinationFileLocation", [value]))

    @jsii.member(jsii_name="resetDestinationFileLocation")
    def reset_destination_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationFileLocation", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOverwriteExisting")
    def reset_overwrite_existing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwriteExisting", []))

    @jsii.member(jsii_name="resetSourceFileLocation")
    def reset_source_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFileLocation", []))

    @builtins.property
    @jsii.member(jsii_name="destinationFileLocation")
    def destination_file_location(
        self,
    ) -> TransferWorkflowStepsCopyStepDetailsDestinationFileLocationOutputReference:
        return typing.cast(TransferWorkflowStepsCopyStepDetailsDestinationFileLocationOutputReference, jsii.get(self, "destinationFileLocation"))

    @builtins.property
    @jsii.member(jsii_name="destinationFileLocationInput")
    def destination_file_location_input(
        self,
    ) -> typing.Optional[TransferWorkflowStepsCopyStepDetailsDestinationFileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowStepsCopyStepDetailsDestinationFileLocation], jsii.get(self, "destinationFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteExistingInput")
    def overwrite_existing_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "overwriteExistingInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocationInput")
    def source_file_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfbe5ee1e34d8d49b8b57d6c8a6210519d4d73554f7482a6693ea48b16a4bd6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overwriteExisting")
    def overwrite_existing(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "overwriteExisting"))

    @overwrite_existing.setter
    def overwrite_existing(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd5c4c3849e6334f918a64c35c7e757dd5605c5351e894eba8d8bf83c25d5bc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwriteExisting", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocation")
    def source_file_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFileLocation"))

    @source_file_location.setter
    def source_file_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f836d78110ddac07eb32d32b48415bb0f552a7cb8eef0abdfd14041ca21323d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFileLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TransferWorkflowStepsCopyStepDetails]:
        return typing.cast(typing.Optional[TransferWorkflowStepsCopyStepDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowStepsCopyStepDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b83c76ce2d518d2861f7a952df7b7ee1b68c6b5120797d65e457f70cc6c1da70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsCustomStepDetails",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "source_file_location": "sourceFileLocation",
        "target": "target",
        "timeout_seconds": "timeoutSeconds",
    },
)
class TransferWorkflowStepsCustomStepDetails:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#target TransferWorkflow#target}.
        :param timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#timeout_seconds TransferWorkflow#timeout_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55d34f9bcaeb3ecb212796caa7753f3e12eb296ad098dc685aab12d4589265a5)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source_file_location", value=source_file_location, expected_type=type_hints["source_file_location"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if source_file_location is not None:
            self._values["source_file_location"] = source_file_location
        if target is not None:
            self._values["target"] = target
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_file_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.'''
        result = self._values.get("source_file_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#target TransferWorkflow#target}.'''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#timeout_seconds TransferWorkflow#timeout_seconds}.'''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowStepsCustomStepDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferWorkflowStepsCustomStepDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsCustomStepDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76e059ebc5ad7f84b1e7d17e72b56746c71dc365d5bbe54ce25f66aba8d8f827)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSourceFileLocation")
    def reset_source_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFileLocation", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @jsii.member(jsii_name="resetTimeoutSeconds")
    def reset_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocationInput")
    def source_file_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecondsInput")
    def timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a84fc6675144571b1847a0bde89defac6b6781493dabaf57b08369e2d4ec1388)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocation")
    def source_file_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFileLocation"))

    @source_file_location.setter
    def source_file_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cf22a08704dcf9f244cc83c8e14e81b187960f868f5978da6ccdb45738bc399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFileLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c302dc08edcad6076632d5c3b0ab2cf01ef6273de13fe239bd11554b3bc2898)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a7715bc8d74a788993c6c04fe42080a8598f4876ee0e4380c63bfbc875069f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TransferWorkflowStepsCustomStepDetails]:
        return typing.cast(typing.Optional[TransferWorkflowStepsCustomStepDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowStepsCustomStepDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d677f1f453ab48cbc77f26e8e6cc274f3012d80146e713422855243a4a5783)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsDecryptStepDetails",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "destination_file_location": "destinationFileLocation",
        "name": "name",
        "overwrite_existing": "overwriteExisting",
        "source_file_location": "sourceFileLocation",
    },
)
class TransferWorkflowStepsDecryptStepDetails:
    def __init__(
        self,
        *,
        type: builtins.str,
        destination_file_location: typing.Optional[typing.Union["TransferWorkflowStepsDecryptStepDetailsDestinationFileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        overwrite_existing: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#type TransferWorkflow#type}.
        :param destination_file_location: destination_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#destination_file_location TransferWorkflow#destination_file_location}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param overwrite_existing: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#overwrite_existing TransferWorkflow#overwrite_existing}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        '''
        if isinstance(destination_file_location, dict):
            destination_file_location = TransferWorkflowStepsDecryptStepDetailsDestinationFileLocation(**destination_file_location)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aa2de7888d8477f870803c4e9e3f6bd84489260562cd840be7e92174ef36f17)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument destination_file_location", value=destination_file_location, expected_type=type_hints["destination_file_location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument overwrite_existing", value=overwrite_existing, expected_type=type_hints["overwrite_existing"])
            check_type(argname="argument source_file_location", value=source_file_location, expected_type=type_hints["source_file_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if destination_file_location is not None:
            self._values["destination_file_location"] = destination_file_location
        if name is not None:
            self._values["name"] = name
        if overwrite_existing is not None:
            self._values["overwrite_existing"] = overwrite_existing
        if source_file_location is not None:
            self._values["source_file_location"] = source_file_location

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#type TransferWorkflow#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_file_location(
        self,
    ) -> typing.Optional["TransferWorkflowStepsDecryptStepDetailsDestinationFileLocation"]:
        '''destination_file_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#destination_file_location TransferWorkflow#destination_file_location}
        '''
        result = self._values.get("destination_file_location")
        return typing.cast(typing.Optional["TransferWorkflowStepsDecryptStepDetailsDestinationFileLocation"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def overwrite_existing(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#overwrite_existing TransferWorkflow#overwrite_existing}.'''
        result = self._values.get("overwrite_existing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_file_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.'''
        result = self._values.get("source_file_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowStepsDecryptStepDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsDecryptStepDetailsDestinationFileLocation",
    jsii_struct_bases=[],
    name_mapping={
        "efs_file_location": "efsFileLocation",
        "s3_file_location": "s3FileLocation",
    },
)
class TransferWorkflowStepsDecryptStepDetailsDestinationFileLocation:
    def __init__(
        self,
        *,
        efs_file_location: typing.Optional[typing.Union["TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_file_location: typing.Optional[typing.Union["TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param efs_file_location: efs_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#efs_file_location TransferWorkflow#efs_file_location}
        :param s3_file_location: s3_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#s3_file_location TransferWorkflow#s3_file_location}
        '''
        if isinstance(efs_file_location, dict):
            efs_file_location = TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation(**efs_file_location)
        if isinstance(s3_file_location, dict):
            s3_file_location = TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocation(**s3_file_location)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce7961031a68a29bd90bda967bc7178f12e0173c5f8b1a0c03f59a93040ccd3)
            check_type(argname="argument efs_file_location", value=efs_file_location, expected_type=type_hints["efs_file_location"])
            check_type(argname="argument s3_file_location", value=s3_file_location, expected_type=type_hints["s3_file_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if efs_file_location is not None:
            self._values["efs_file_location"] = efs_file_location
        if s3_file_location is not None:
            self._values["s3_file_location"] = s3_file_location

    @builtins.property
    def efs_file_location(
        self,
    ) -> typing.Optional["TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation"]:
        '''efs_file_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#efs_file_location TransferWorkflow#efs_file_location}
        '''
        result = self._values.get("efs_file_location")
        return typing.cast(typing.Optional["TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation"], result)

    @builtins.property
    def s3_file_location(
        self,
    ) -> typing.Optional["TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocation"]:
        '''s3_file_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#s3_file_location TransferWorkflow#s3_file_location}
        '''
        result = self._values.get("s3_file_location")
        return typing.cast(typing.Optional["TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowStepsDecryptStepDetailsDestinationFileLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation",
    jsii_struct_bases=[],
    name_mapping={"file_system_id": "fileSystemId", "path": "path"},
)
class TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation:
    def __init__(
        self,
        *,
        file_system_id: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_system_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#file_system_id TransferWorkflow#file_system_id}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#path TransferWorkflow#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f633f311fad0ac4a79741c0f0b57eaf2e80a3a5e1d397ee997b60ab77208a841)
            check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file_system_id is not None:
            self._values["file_system_id"] = file_system_id
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def file_system_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#file_system_id TransferWorkflow#file_system_id}.'''
        result = self._values.get("file_system_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#path TransferWorkflow#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67eff449c75c426d59a5d9cf72f6e0a8f013afccf1d6a84a21becc45d4769795)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFileSystemId")
    def reset_file_system_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileSystemId", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="fileSystemIdInput")
    def file_system_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileSystemIdInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileSystemId"))

    @file_system_id.setter
    def file_system_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__def8c0e591aaf6d3716a8e38390519d08a93fcaa0196a41529895dcdd99378c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileSystemId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8733187f81d23dfcd343d3d630b7b9befdfa0b2eb3eab8b9992dda609d389b1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d11c3c75a8413040ebb430e966c9e1173aa8c90df2596ba4ec1b2cb7047a03e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41adb286af3bba820040e5c2465b34d6ff2f6176ef5b7bb829ee794b192c7848)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEfsFileLocation")
    def put_efs_file_location(
        self,
        *,
        file_system_id: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_system_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#file_system_id TransferWorkflow#file_system_id}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#path TransferWorkflow#path}.
        '''
        value = TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation(
            file_system_id=file_system_id, path=path
        )

        return typing.cast(None, jsii.invoke(self, "putEfsFileLocation", [value]))

    @jsii.member(jsii_name="putS3FileLocation")
    def put_s3_file_location(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#bucket TransferWorkflow#bucket}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#key TransferWorkflow#key}.
        '''
        value = TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocation(
            bucket=bucket, key=key
        )

        return typing.cast(None, jsii.invoke(self, "putS3FileLocation", [value]))

    @jsii.member(jsii_name="resetEfsFileLocation")
    def reset_efs_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEfsFileLocation", []))

    @jsii.member(jsii_name="resetS3FileLocation")
    def reset_s3_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3FileLocation", []))

    @builtins.property
    @jsii.member(jsii_name="efsFileLocation")
    def efs_file_location(
        self,
    ) -> TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocationOutputReference:
        return typing.cast(TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocationOutputReference, jsii.get(self, "efsFileLocation"))

    @builtins.property
    @jsii.member(jsii_name="s3FileLocation")
    def s3_file_location(
        self,
    ) -> "TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocationOutputReference":
        return typing.cast("TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocationOutputReference", jsii.get(self, "s3FileLocation"))

    @builtins.property
    @jsii.member(jsii_name="efsFileLocationInput")
    def efs_file_location_input(
        self,
    ) -> typing.Optional[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation], jsii.get(self, "efsFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="s3FileLocationInput")
    def s3_file_location_input(
        self,
    ) -> typing.Optional["TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocation"]:
        return typing.cast(typing.Optional["TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocation"], jsii.get(self, "s3FileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ad12afd944cebea9acfcfbc4c53a86e54547333b282352fee4fd1ada564b789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocation",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "key": "key"},
)
class TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocation:
    def __init__(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#bucket TransferWorkflow#bucket}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#key TransferWorkflow#key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52d421448fe9fb615d2151f1f7362fd78a93c776271d8613ae1ab3dc8acaba3e)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if key is not None:
            self._values["key"] = key

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#bucket TransferWorkflow#bucket}.'''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#key TransferWorkflow#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6baf1e273f42a58be4a623cf87d32c542ec797c2d6eddb6a8d0e45b62ccbb401)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucket")
    def reset_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucket", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22076ad48d54f9e2a19febeffad4916b3dfeb7c05c6a369334a54ada9b443236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8960a4d1dd456b4ba1ab332a3d3f6cf4c36ea2a644ad0234d955fea65f4f1a30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9863114db568668949824f765f302e1e4472c2ee462ad2b81db3d1ba5f6da9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TransferWorkflowStepsDecryptStepDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsDecryptStepDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a89e129e90a0f4bddd7893b9798c79ca447519e473a79ab3bd309beda00559b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDestinationFileLocation")
    def put_destination_file_location(
        self,
        *,
        efs_file_location: typing.Optional[typing.Union[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
        s3_file_location: typing.Optional[typing.Union[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param efs_file_location: efs_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#efs_file_location TransferWorkflow#efs_file_location}
        :param s3_file_location: s3_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#s3_file_location TransferWorkflow#s3_file_location}
        '''
        value = TransferWorkflowStepsDecryptStepDetailsDestinationFileLocation(
            efs_file_location=efs_file_location, s3_file_location=s3_file_location
        )

        return typing.cast(None, jsii.invoke(self, "putDestinationFileLocation", [value]))

    @jsii.member(jsii_name="resetDestinationFileLocation")
    def reset_destination_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationFileLocation", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOverwriteExisting")
    def reset_overwrite_existing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwriteExisting", []))

    @jsii.member(jsii_name="resetSourceFileLocation")
    def reset_source_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFileLocation", []))

    @builtins.property
    @jsii.member(jsii_name="destinationFileLocation")
    def destination_file_location(
        self,
    ) -> TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationOutputReference:
        return typing.cast(TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationOutputReference, jsii.get(self, "destinationFileLocation"))

    @builtins.property
    @jsii.member(jsii_name="destinationFileLocationInput")
    def destination_file_location_input(
        self,
    ) -> typing.Optional[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocation]:
        return typing.cast(typing.Optional[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocation], jsii.get(self, "destinationFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteExistingInput")
    def overwrite_existing_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "overwriteExistingInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocationInput")
    def source_file_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9979330f10c0c55daa0c5be7cb36d9c960c08b2345520612cf2873b91f03e630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overwriteExisting")
    def overwrite_existing(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "overwriteExisting"))

    @overwrite_existing.setter
    def overwrite_existing(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b2270396f7986631a5dc841767a9bec449fc793a23acd0329988003ab811370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwriteExisting", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocation")
    def source_file_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFileLocation"))

    @source_file_location.setter
    def source_file_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faf9e608f38135712b54f3d11f0983b67723cbce0cc94387fa332e29690d0dd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFileLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf19c2e2e94da3c1f98d6e8685d300cff24de2108b90cf500d89b06a88af6bbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferWorkflowStepsDecryptStepDetails]:
        return typing.cast(typing.Optional[TransferWorkflowStepsDecryptStepDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowStepsDecryptStepDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cbc2ec83ea1370a0b9acf2f2cb533a683bb1f35e881a206774d4bba8116f49c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsDeleteStepDetails",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "source_file_location": "sourceFileLocation"},
)
class TransferWorkflowStepsDeleteStepDetails:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9da5b25cdab7c44f611e4086e2ca45c068709e8aaf1e95b5e6309ff86cef5122)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source_file_location", value=source_file_location, expected_type=type_hints["source_file_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if source_file_location is not None:
            self._values["source_file_location"] = source_file_location

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_file_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.'''
        result = self._values.get("source_file_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowStepsDeleteStepDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferWorkflowStepsDeleteStepDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsDeleteStepDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a69b8ea8f22defba16ad070122b496bb8e7d0a53075e21945afc32205d5f1a14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSourceFileLocation")
    def reset_source_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFileLocation", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocationInput")
    def source_file_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c09e5f22aab935232cb2144fa6cc63d68977564ff2e5830d83ca66e6e19808d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocation")
    def source_file_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFileLocation"))

    @source_file_location.setter
    def source_file_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0cf5d457964a949c4152ae3e15eb24d2d7a3e03aad0278bc5dc50df8ff4d394)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFileLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TransferWorkflowStepsDeleteStepDetails]:
        return typing.cast(typing.Optional[TransferWorkflowStepsDeleteStepDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowStepsDeleteStepDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c3f8f53406fff9691037fafdf825f33dbafaad26d8bec270e9c9f93f8d1362b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TransferWorkflowStepsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9079d3be583151fa79bc0f194330f293ddfd33597077351ce13d90b6a32fb0cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TransferWorkflowStepsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b997875ade4c53edf47e0a77d6ad07c364bc1b5d986d1b9fe9322acfe48b82ba)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TransferWorkflowStepsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fbde61a586ddb2d98b790633aa8b0c860192d714fcef6f890adef50cd1f981e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4108b583d410b21d961205cbbb01a27d16989ab34a7bc59f9bcefd317b4cf8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18edc15e53a677070215a78fbf34590fc38700bac1eecc358613b0a23a6d6092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TransferWorkflowSteps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TransferWorkflowSteps]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TransferWorkflowSteps]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d7873d23bdbff3f83852464941926e9df1fc759c3d9cfd7d1c469ffd4bca5b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TransferWorkflowStepsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__468b262a22d3e123cbb02fc93c099ebbfd5e8082118a4ed0209ce897449f0d0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCopyStepDetails")
    def put_copy_step_details(
        self,
        *,
        destination_file_location: typing.Optional[typing.Union[TransferWorkflowStepsCopyStepDetailsDestinationFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        overwrite_existing: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination_file_location: destination_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#destination_file_location TransferWorkflow#destination_file_location}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param overwrite_existing: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#overwrite_existing TransferWorkflow#overwrite_existing}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        '''
        value = TransferWorkflowStepsCopyStepDetails(
            destination_file_location=destination_file_location,
            name=name,
            overwrite_existing=overwrite_existing,
            source_file_location=source_file_location,
        )

        return typing.cast(None, jsii.invoke(self, "putCopyStepDetails", [value]))

    @jsii.member(jsii_name="putCustomStepDetails")
    def put_custom_step_details(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#target TransferWorkflow#target}.
        :param timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#timeout_seconds TransferWorkflow#timeout_seconds}.
        '''
        value = TransferWorkflowStepsCustomStepDetails(
            name=name,
            source_file_location=source_file_location,
            target=target,
            timeout_seconds=timeout_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomStepDetails", [value]))

    @jsii.member(jsii_name="putDecryptStepDetails")
    def put_decrypt_step_details(
        self,
        *,
        type: builtins.str,
        destination_file_location: typing.Optional[typing.Union[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        overwrite_existing: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#type TransferWorkflow#type}.
        :param destination_file_location: destination_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#destination_file_location TransferWorkflow#destination_file_location}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param overwrite_existing: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#overwrite_existing TransferWorkflow#overwrite_existing}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        '''
        value = TransferWorkflowStepsDecryptStepDetails(
            type=type,
            destination_file_location=destination_file_location,
            name=name,
            overwrite_existing=overwrite_existing,
            source_file_location=source_file_location,
        )

        return typing.cast(None, jsii.invoke(self, "putDecryptStepDetails", [value]))

    @jsii.member(jsii_name="putDeleteStepDetails")
    def put_delete_step_details(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        '''
        value = TransferWorkflowStepsDeleteStepDetails(
            name=name, source_file_location=source_file_location
        )

        return typing.cast(None, jsii.invoke(self, "putDeleteStepDetails", [value]))

    @jsii.member(jsii_name="putTagStepDetails")
    def put_tag_step_details(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TransferWorkflowStepsTagStepDetailsTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        :param tags: tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#tags TransferWorkflow#tags}
        '''
        value = TransferWorkflowStepsTagStepDetails(
            name=name, source_file_location=source_file_location, tags=tags
        )

        return typing.cast(None, jsii.invoke(self, "putTagStepDetails", [value]))

    @jsii.member(jsii_name="resetCopyStepDetails")
    def reset_copy_step_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyStepDetails", []))

    @jsii.member(jsii_name="resetCustomStepDetails")
    def reset_custom_step_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomStepDetails", []))

    @jsii.member(jsii_name="resetDecryptStepDetails")
    def reset_decrypt_step_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDecryptStepDetails", []))

    @jsii.member(jsii_name="resetDeleteStepDetails")
    def reset_delete_step_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteStepDetails", []))

    @jsii.member(jsii_name="resetTagStepDetails")
    def reset_tag_step_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagStepDetails", []))

    @builtins.property
    @jsii.member(jsii_name="copyStepDetails")
    def copy_step_details(self) -> TransferWorkflowStepsCopyStepDetailsOutputReference:
        return typing.cast(TransferWorkflowStepsCopyStepDetailsOutputReference, jsii.get(self, "copyStepDetails"))

    @builtins.property
    @jsii.member(jsii_name="customStepDetails")
    def custom_step_details(
        self,
    ) -> TransferWorkflowStepsCustomStepDetailsOutputReference:
        return typing.cast(TransferWorkflowStepsCustomStepDetailsOutputReference, jsii.get(self, "customStepDetails"))

    @builtins.property
    @jsii.member(jsii_name="decryptStepDetails")
    def decrypt_step_details(
        self,
    ) -> TransferWorkflowStepsDecryptStepDetailsOutputReference:
        return typing.cast(TransferWorkflowStepsDecryptStepDetailsOutputReference, jsii.get(self, "decryptStepDetails"))

    @builtins.property
    @jsii.member(jsii_name="deleteStepDetails")
    def delete_step_details(
        self,
    ) -> TransferWorkflowStepsDeleteStepDetailsOutputReference:
        return typing.cast(TransferWorkflowStepsDeleteStepDetailsOutputReference, jsii.get(self, "deleteStepDetails"))

    @builtins.property
    @jsii.member(jsii_name="tagStepDetails")
    def tag_step_details(self) -> "TransferWorkflowStepsTagStepDetailsOutputReference":
        return typing.cast("TransferWorkflowStepsTagStepDetailsOutputReference", jsii.get(self, "tagStepDetails"))

    @builtins.property
    @jsii.member(jsii_name="copyStepDetailsInput")
    def copy_step_details_input(
        self,
    ) -> typing.Optional[TransferWorkflowStepsCopyStepDetails]:
        return typing.cast(typing.Optional[TransferWorkflowStepsCopyStepDetails], jsii.get(self, "copyStepDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="customStepDetailsInput")
    def custom_step_details_input(
        self,
    ) -> typing.Optional[TransferWorkflowStepsCustomStepDetails]:
        return typing.cast(typing.Optional[TransferWorkflowStepsCustomStepDetails], jsii.get(self, "customStepDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="decryptStepDetailsInput")
    def decrypt_step_details_input(
        self,
    ) -> typing.Optional[TransferWorkflowStepsDecryptStepDetails]:
        return typing.cast(typing.Optional[TransferWorkflowStepsDecryptStepDetails], jsii.get(self, "decryptStepDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteStepDetailsInput")
    def delete_step_details_input(
        self,
    ) -> typing.Optional[TransferWorkflowStepsDeleteStepDetails]:
        return typing.cast(typing.Optional[TransferWorkflowStepsDeleteStepDetails], jsii.get(self, "deleteStepDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagStepDetailsInput")
    def tag_step_details_input(
        self,
    ) -> typing.Optional["TransferWorkflowStepsTagStepDetails"]:
        return typing.cast(typing.Optional["TransferWorkflowStepsTagStepDetails"], jsii.get(self, "tagStepDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__907057ed2a0aabaac1283d234dbc3735ca480f775d1c7acc684b9e5f56227f0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferWorkflowSteps]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferWorkflowSteps]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferWorkflowSteps]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924e4c0cf565e56e30eff8a296fc852bb290a9904f2e4ce123955e5ec85abdf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsTagStepDetails",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "source_file_location": "sourceFileLocation",
        "tags": "tags",
    },
)
class TransferWorkflowStepsTagStepDetails:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        source_file_location: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TransferWorkflowStepsTagStepDetailsTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.
        :param source_file_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.
        :param tags: tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#tags TransferWorkflow#tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ab94c6812a2e0e8aab82c9d96454eae4d4ee47d1740004585b8fc4bfb92e8fe)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source_file_location", value=source_file_location, expected_type=type_hints["source_file_location"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if source_file_location is not None:
            self._values["source_file_location"] = source_file_location
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#name TransferWorkflow#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_file_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#source_file_location TransferWorkflow#source_file_location}.'''
        result = self._values.get("source_file_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TransferWorkflowStepsTagStepDetailsTags"]]]:
        '''tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#tags TransferWorkflow#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TransferWorkflowStepsTagStepDetailsTags"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowStepsTagStepDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferWorkflowStepsTagStepDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsTagStepDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bf72b27a5e9b5e6db85bf30e36b263386b75bd5de4de4d206c3f84cffa0af3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTags")
    def put_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TransferWorkflowStepsTagStepDetailsTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a0eabf898c53ab777efd6ad99b14389b6fd4c5fddc623f9fe6f2949536506b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTags", [value]))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSourceFileLocation")
    def reset_source_file_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFileLocation", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "TransferWorkflowStepsTagStepDetailsTagsList":
        return typing.cast("TransferWorkflowStepsTagStepDetailsTagsList", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocationInput")
    def source_file_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TransferWorkflowStepsTagStepDetailsTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TransferWorkflowStepsTagStepDetailsTags"]]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1efbd0ffccac3ad96d4efa362f1866cf401037bd378791a4a1cb9ef5edb103d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFileLocation")
    def source_file_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFileLocation"))

    @source_file_location.setter
    def source_file_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af1e6e90f892f6d9406d294d06252ef20caf3b654e10ffe0f32cb692000203c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFileLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TransferWorkflowStepsTagStepDetails]:
        return typing.cast(typing.Optional[TransferWorkflowStepsTagStepDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferWorkflowStepsTagStepDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7f02a705103c98d7ea19a523f97c5404638e1ea265c2929394a23ebef073ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsTagStepDetailsTags",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class TransferWorkflowStepsTagStepDetailsTags:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#key TransferWorkflow#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#value TransferWorkflow#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f720dd3bb49bbfb79b79a2b4239a7c7827a23557348400d0bdda4bdfd82ff8)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#key TransferWorkflow#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_workflow#value TransferWorkflow#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferWorkflowStepsTagStepDetailsTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferWorkflowStepsTagStepDetailsTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsTagStepDetailsTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__738e2a2f080c5b438d951078ee67c2c74f8e0e9cc9b2d84bf2bc3f8fc9312896)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TransferWorkflowStepsTagStepDetailsTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c9075429cd860fba84c37b5316c726946b10c09f17fb4063a6961bc27e64165)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TransferWorkflowStepsTagStepDetailsTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11595575434aba2e6f034879791e861ef50d2a99354f862f35a643391d9d1ab6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2928b3ee7ccc814a88efe7735c8597ffe0fb5ceb960de61012b7d578d6fba20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08140272cb02c64c153a92983509bbe97c08b9ddb8e4432ee1487ce8ce2197bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TransferWorkflowStepsTagStepDetailsTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TransferWorkflowStepsTagStepDetailsTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TransferWorkflowStepsTagStepDetailsTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d449f97a03f859182d591bfaac2797352ace5770ee478aad5c38c8b96280b750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TransferWorkflowStepsTagStepDetailsTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferWorkflow.TransferWorkflowStepsTagStepDetailsTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__392e2880a352b4a5eb449ee4fa18e5ec92aab7a3ea955c3dd5f4386a5a4e32e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06f44d57ceead395e7c674f5d4d363a069b8691b1dc6934213ed8328c288104e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195cb0c483fd9156574e0696f5f532a4658030f53561a7ccf67014db46c988cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferWorkflowStepsTagStepDetailsTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferWorkflowStepsTagStepDetailsTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferWorkflowStepsTagStepDetailsTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__806ed38c5e4d6073fe80c157f85752c4f3f0b2fcc7db5bde161dd958ba50d35a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "TransferWorkflow",
    "TransferWorkflowConfig",
    "TransferWorkflowOnExceptionSteps",
    "TransferWorkflowOnExceptionStepsCopyStepDetails",
    "TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocation",
    "TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocation",
    "TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocationOutputReference",
    "TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationOutputReference",
    "TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocation",
    "TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocationOutputReference",
    "TransferWorkflowOnExceptionStepsCopyStepDetailsOutputReference",
    "TransferWorkflowOnExceptionStepsCustomStepDetails",
    "TransferWorkflowOnExceptionStepsCustomStepDetailsOutputReference",
    "TransferWorkflowOnExceptionStepsDecryptStepDetails",
    "TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocation",
    "TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation",
    "TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocationOutputReference",
    "TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationOutputReference",
    "TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocation",
    "TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocationOutputReference",
    "TransferWorkflowOnExceptionStepsDecryptStepDetailsOutputReference",
    "TransferWorkflowOnExceptionStepsDeleteStepDetails",
    "TransferWorkflowOnExceptionStepsDeleteStepDetailsOutputReference",
    "TransferWorkflowOnExceptionStepsList",
    "TransferWorkflowOnExceptionStepsOutputReference",
    "TransferWorkflowOnExceptionStepsTagStepDetails",
    "TransferWorkflowOnExceptionStepsTagStepDetailsOutputReference",
    "TransferWorkflowOnExceptionStepsTagStepDetailsTags",
    "TransferWorkflowOnExceptionStepsTagStepDetailsTagsList",
    "TransferWorkflowOnExceptionStepsTagStepDetailsTagsOutputReference",
    "TransferWorkflowSteps",
    "TransferWorkflowStepsCopyStepDetails",
    "TransferWorkflowStepsCopyStepDetailsDestinationFileLocation",
    "TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocation",
    "TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocationOutputReference",
    "TransferWorkflowStepsCopyStepDetailsDestinationFileLocationOutputReference",
    "TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocation",
    "TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocationOutputReference",
    "TransferWorkflowStepsCopyStepDetailsOutputReference",
    "TransferWorkflowStepsCustomStepDetails",
    "TransferWorkflowStepsCustomStepDetailsOutputReference",
    "TransferWorkflowStepsDecryptStepDetails",
    "TransferWorkflowStepsDecryptStepDetailsDestinationFileLocation",
    "TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation",
    "TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocationOutputReference",
    "TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationOutputReference",
    "TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocation",
    "TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocationOutputReference",
    "TransferWorkflowStepsDecryptStepDetailsOutputReference",
    "TransferWorkflowStepsDeleteStepDetails",
    "TransferWorkflowStepsDeleteStepDetailsOutputReference",
    "TransferWorkflowStepsList",
    "TransferWorkflowStepsOutputReference",
    "TransferWorkflowStepsTagStepDetails",
    "TransferWorkflowStepsTagStepDetailsOutputReference",
    "TransferWorkflowStepsTagStepDetailsTags",
    "TransferWorkflowStepsTagStepDetailsTagsList",
    "TransferWorkflowStepsTagStepDetailsTagsOutputReference",
]

publication.publish()

def _typecheckingstub__de4fb654950bf7aac05bbf1efdb2604967af9b4bdb53a5d3ae31d522f3bb168f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    steps: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TransferWorkflowSteps, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    on_exception_steps: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TransferWorkflowOnExceptionSteps, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__2216c99c9cc80e7a74abf5a4f985abd4fdc0a4ad1d9ac6ff42136659c1911e5a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c07d6555b061dddbec876aeb52ebd569524658334664d1f17272d9c8d30fd98(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TransferWorkflowOnExceptionSteps, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9b70fb54ca13fa6f2c7520fc6fa657c49866990521e3b2e4cf8ac09f1860ae(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TransferWorkflowSteps, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794a5cbc5fe9a0166a0a66fc76f33df54c2075b824e01e30cb038e7bd761ba87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd25e8f126dd3ec26ee4753c86975a04ea526188a89e7718de0193d89e07d2ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db32c726bc7d627b8c69eb2f9adeba7f2e753bc2dd758fcd01e448ff60de76e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f798c8a9e51df96941e7d82c4e48b6b43077ed37f875c604aceb89119d78325d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d283eb80b909cd4805f2cd81a73d185006ae1fccbb61f31dd909fb25b760cee(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a85814f3c6b4b3a1f805518fa071d99164969560adcf456c3662cb957af63b8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    steps: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TransferWorkflowSteps, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    on_exception_steps: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TransferWorkflowOnExceptionSteps, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3499701a3d25fe40ec6df9c68def9710800aa1cd43c6e1ac769810436560d8b(
    *,
    type: builtins.str,
    copy_step_details: typing.Optional[typing.Union[TransferWorkflowOnExceptionStepsCopyStepDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_step_details: typing.Optional[typing.Union[TransferWorkflowOnExceptionStepsCustomStepDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    decrypt_step_details: typing.Optional[typing.Union[TransferWorkflowOnExceptionStepsDecryptStepDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_step_details: typing.Optional[typing.Union[TransferWorkflowOnExceptionStepsDeleteStepDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_step_details: typing.Optional[typing.Union[TransferWorkflowOnExceptionStepsTagStepDetails, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54afa8429b00a0c9fcf26dc0006212101c1553fb2fe3f425251e9a776dc11153(
    *,
    destination_file_location: typing.Optional[typing.Union[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    overwrite_existing: typing.Optional[builtins.str] = None,
    source_file_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18803fe80686d3513e424845073c5f48688a6cffc955365afc13d329e30d375(
    *,
    efs_file_location: typing.Optional[typing.Union[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_file_location: typing.Optional[typing.Union[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4219ba881c73d99011d32e3a96a3d86225c8e1a27f42bb0c8aa3323fb1f92883(
    *,
    file_system_id: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ecb399bfbdcc4728b45c704f39226ed2038a4dffa4480e118a842c051380ec4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__681cee368434708d2c66d6cf07ccd00ea6472642571301d104861670249cd56e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261bb972e38fc133c6536f7e644e36a76637d8357e6140380b487a3e68aa19a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc96713bebc9fe988a5e76c30b9b711044937b749f9b7abb2e1ac9ca76efd403(
    value: typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationEfsFileLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe706f65079cafc8de90ad5ec9a517034e65518e400ef02d85e2c76b706700e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd803a51316fcfd674ebaaecd24d9c27b76dc7c80ed37d6ebd2edd65dd439862(
    value: typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fdfd293ca19493239eec7780abb0998cdcf3e0948057e7e9919b79f659c7d50(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b03977935ba9bc8af87cfca01ea0def3d97356245b67e5da1cd25aae91e82d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a57552a7075a8bbab9e2180436edf675e79db801bb087ad8090b3f6c2437f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02709721fcb20cb8fdd0836cbb6ea02160fef653a90e1125ffc15e8a9f459b08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7d1764f177aae96a193a6e542e8650b05445473cf87ca0968c96e8fb0d7acf(
    value: typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetailsDestinationFileLocationS3FileLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba79f499d5964273c9e1d1560be620e5070d45a87c76d89fd9959d46ed54aea5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c72c25e5638ff013cca4a7141156caa2cbba7884e14c05a052509bfc2757b80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6754defcee7619011d6943fac24c6bf7fec00969949b1916f8071a3118443229(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dc6964b2317001b8bab4544ebf66b823a2569d2cc5b635c15d0fb1861c871cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d588a8d0fe4c0a7c43fc9d24aa4fe28c19332545b0db80f11bdc09c848875e92(
    value: typing.Optional[TransferWorkflowOnExceptionStepsCopyStepDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9610f1055760504ab7ad86ba654cf82062c8bf06ae80a48edc7de863218981bc(
    *,
    name: typing.Optional[builtins.str] = None,
    source_file_location: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f0b482862da9464829adc26adbd6dfb448b1937569f07d6e9377b1d07bf9bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a7154792844c4a361a21126229f1d16e010971358743c9a15fcc479cf65ae1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5691e13f11fc23417d76e58ad7e9d9d76c17df62ede47cd52c7233fd1b22e854(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce107777d70cdea29db0c1f4cb56ed444903210f877932709e97c9da716a951(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c3bb7787e7db459bf2a2be396da177958cd9cf17ffd768d41030fc15647fc57(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f028375f3e1f46624863246b648cf913310dcc63826e0b8fb0061cecfe1799a(
    value: typing.Optional[TransferWorkflowOnExceptionStepsCustomStepDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b55cfcd07a3b341ba1300cd7e9bb256e027195df6cc19ba9d3043a0e4db387(
    *,
    type: builtins.str,
    destination_file_location: typing.Optional[typing.Union[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    overwrite_existing: typing.Optional[builtins.str] = None,
    source_file_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9ff2d44bc5cb0c560ce5484884cf6a81deaa243077d8a2db0ade3c56567261(
    *,
    efs_file_location: typing.Optional[typing.Union[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_file_location: typing.Optional[typing.Union[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3fc9f246354b8e061a855f14e5c1c58fafa8298ef2ae940f6103f64122b076(
    *,
    file_system_id: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f481168180d396fec4d87f139c93e5b8796ae71654cef57a93761e789754a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf304a1cd8c5451434b093e8788c786ca7203b263b9d6b8da418a2733a7e214d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e391f927bb3b12268fa2a60e9a502e4e5e564a0c35ca1f9e581321324ab34ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace535763a6b9ed88184980e6e4544bf00dd340319d297f5a496608660495ad3(
    value: typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__589502ee97b794abc045c068f20cd3e23eeeae8c245aef8ccae42b2efc689f0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6165ea4c93488e4655acc42cc3d12175b373390ea80fab6cd0d3592c57e63350(
    value: typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__273944b679315ee172a4e628de5809a466c001080c57f069ae014b4e5ded06bc(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9bb64fbbff9cd66e73f78ff5fde606d9cb177a6511d13944066d5246498a5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d629ad3cd92d221b566b4d52610bdb32c72728a624728578e3f897016c495232(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2f052c638dcf9f1096b6764ef7b4e34e796b8bc865226527832c91d3d88a3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ce42210de92ec12c9978182a5aa282742a6fefe3b8507a0f722a6df2d5f24e(
    value: typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetailsDestinationFileLocationS3FileLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb6548dd834b434e1ef9b3bfaae2cc819aac7dd1e3a5f599e18b3e10080f6d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1190b0eee23326baf2b8b5e385ef9a4a45867bc9f2f5ee9763cccc06e20afdc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef68e3eef28b7e2cd2f6ff862fa01ce9a7a28387a4ca9ebb4a48ac78f02abb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6013a0047a8a9ec43479653ae286ccc15770b943c484e0427cd0348765d8758d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f5478bc035baad60068bf727d457f6b5d934f3a93b4cfdffe8e1b29510a95a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc7bdb88412147649262b67b1e51ead251a530a53c21023c946277c50161abe0(
    value: typing.Optional[TransferWorkflowOnExceptionStepsDecryptStepDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85761cec8e4f3b25c0d8935ba6ca3fa6beaea63670c87e3feccd05bd50b8d464(
    *,
    name: typing.Optional[builtins.str] = None,
    source_file_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b079b97d902558b7be26eda4d22d47a34fdc96ed329ec8be60ba5c3749cfa99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e8c895ab410bf30250ecfddebcbc1620cbd16bc74ca351eccf55e562b383ed8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965987ae8b648a6861f6ee7a85bd17d0104f95bc6a39dfc8899f323db8bd9bd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4923eb86d43193bc51cd27c9b90f7991095106270075aad2e27cb48dcbd46c6f(
    value: typing.Optional[TransferWorkflowOnExceptionStepsDeleteStepDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff53d76cd9ea94947a5681538f36079ed18c6de15f9d42cf5ada8c170ad2c059(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c568f1972f5a655db9e5d47acb25fbc4936651c79dca8b08c14f58526ce6cd1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441f603a47ba3f3057c6a3cf9c2bce6bb085c18b2ebe5544492117a6f662925c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4faba0407fa59e758a15a55573f894b5bace84fe8979154ec8bed1e7618617(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8f43c152c96ba08c32a9c844f59506690ef07ae7e26371790466cda1cd31b5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__628664ef380a4510bb486c9299f684c48e1d9bca7ff5a7d1517bc731d6ed1319(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TransferWorkflowOnExceptionSteps]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a677e71e6b60aeee10932258744ff8f037d89b989a3aa03272ea412634c327f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af4205fd68b08603eb6126aee4d66855ac74c184205eb390436a595f2595286(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81dbff235d1972e4f380708b88a6f7ae1569f611e45cd3e5aa8278d1c1982cd1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferWorkflowOnExceptionSteps]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f930725aecde9b821bb634a350f7364b94896c16597235b6b171841ef78cf1(
    *,
    name: typing.Optional[builtins.str] = None,
    source_file_location: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TransferWorkflowOnExceptionStepsTagStepDetailsTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8382266883c5f4c6c1599ea841ef44793c79b179b16bf07d742e22fa74e2d93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66cb300c6c43985e1acf70e8cd042f2aadd4ff23a4f5ef0992d8240eb69db5a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TransferWorkflowOnExceptionStepsTagStepDetailsTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b355b7b099a5606a0733acde22b883eeba51682eca74afadfe998dba98fd37de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffab372db67695e331f3c1da5bf78936dc8333de1ac3dd9163d6558925476133(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4e6ed0df0422e1a3ed12bce3d5268c205acdf3b6300280dfea45c6a83e02c8e(
    value: typing.Optional[TransferWorkflowOnExceptionStepsTagStepDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7989c3a1936d743f744ee82818116ede42617b2c7e632e37738c08ae5def8062(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4be91b91099e2e8d219ec475f3471e150b3820da8ed49f462d88af8b66ca0be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef565794854e710dc37acd449de584aca9a0d68b5ab8f9964d74df6f453e41f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb68d931b193b455efe91d32427ab4107fe4a81502fd27f2d433fafbf466b87e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18dee0446e4cc26b34cb56001e024bcff60e9b9f28ac9b28d207f10a5ce6a165(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3597e80d0a580bad8ec4e6e9f2e97094c8d1f6a8091aa72e43700d3a7b5b941e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d0e75b40fc9f79caa767057e872c3651ff0413d41aef8a289455b27947f2fa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TransferWorkflowOnExceptionStepsTagStepDetailsTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7da78451e80a8f95c2083d7c180e4b3d5377b27b0443fe3023cd02547d57f28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759efe1b718b49db425b3ce56ac3eb42381fc4bf3f2544ca84b85a52953f32ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3d612177bfe2dfa6fac8bee72e42cad1b350e514b073915722498e532ad997(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e753982f1d20160e8da3ec95650e8b907358e9a9031a3a8ea506bca9de3eda0a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferWorkflowOnExceptionStepsTagStepDetailsTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fbe3a6f53b1e25f1ed3af20e563acebb5cb739986799c3593cebbc02e1054e0(
    *,
    type: builtins.str,
    copy_step_details: typing.Optional[typing.Union[TransferWorkflowStepsCopyStepDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_step_details: typing.Optional[typing.Union[TransferWorkflowStepsCustomStepDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    decrypt_step_details: typing.Optional[typing.Union[TransferWorkflowStepsDecryptStepDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_step_details: typing.Optional[typing.Union[TransferWorkflowStepsDeleteStepDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_step_details: typing.Optional[typing.Union[TransferWorkflowStepsTagStepDetails, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864d8b015c2812b80992ac5df59512ecf866996f4d322a44727177393f864288(
    *,
    destination_file_location: typing.Optional[typing.Union[TransferWorkflowStepsCopyStepDetailsDestinationFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    overwrite_existing: typing.Optional[builtins.str] = None,
    source_file_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c4016c970fa4f1159c3a00a17ad375e8a528ab48ddf979bb63ee5ea0ea982d(
    *,
    efs_file_location: typing.Optional[typing.Union[TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_file_location: typing.Optional[typing.Union[TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9d4401fddb4e1cc575f5dc636b0efb79326e6a7a2f06987e21dd7eac056e95(
    *,
    file_system_id: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5590d912b40bc45b6e1cdbcbe8dd9ea0bc2d1aa7de440c1b67f0eb5754f6853(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b951ec1b26df4279837c59c661e71bbf11f6e6187e7a2aa4aa790a8de1d054b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b65751f4cb5dee2f6ec85dd4c7a381222d98621fa48445c826491f7f9fd76ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489eab017dd4f7b22766aed2954131c183b7a2bb393b5e64530cdbafe55dab0e(
    value: typing.Optional[TransferWorkflowStepsCopyStepDetailsDestinationFileLocationEfsFileLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32bbe3253dac661038f5b38c27e0f19ee44f7e9276c2ca6511376d2bb800d5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a74b2230bd89df0a0f999d63f047d5aba845b63f473f4b77af680aa1aa02bf(
    value: typing.Optional[TransferWorkflowStepsCopyStepDetailsDestinationFileLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361f501a04314127ac3568a580b673325c0579984ee6696e33e5b407ac156caf(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f917a15f3454747496d56b036aec72a7f7081bb13d3620eaefb7f4ea06d564e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__603172c2e4e4c93edc99b8063bb4d2f5bf05abb059bcd297bab9f5169a17ff0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec466f66555f5579118fc8d27ae1116591bf44b065392536b9c8693790daa74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc986ef371f763b12ad076c968d5fb6bb92357d662e41749d78a7e6b723e27f6(
    value: typing.Optional[TransferWorkflowStepsCopyStepDetailsDestinationFileLocationS3FileLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1293814843ac3749a8be7f0c5d7cf0b0c71289706fbcf54e745be3aa51f283ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfbe5ee1e34d8d49b8b57d6c8a6210519d4d73554f7482a6693ea48b16a4bd6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd5c4c3849e6334f918a64c35c7e757dd5605c5351e894eba8d8bf83c25d5bc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f836d78110ddac07eb32d32b48415bb0f552a7cb8eef0abdfd14041ca21323d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83c76ce2d518d2861f7a952df7b7ee1b68c6b5120797d65e457f70cc6c1da70(
    value: typing.Optional[TransferWorkflowStepsCopyStepDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55d34f9bcaeb3ecb212796caa7753f3e12eb296ad098dc685aab12d4589265a5(
    *,
    name: typing.Optional[builtins.str] = None,
    source_file_location: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e059ebc5ad7f84b1e7d17e72b56746c71dc365d5bbe54ce25f66aba8d8f827(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84fc6675144571b1847a0bde89defac6b6781493dabaf57b08369e2d4ec1388(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf22a08704dcf9f244cc83c8e14e81b187960f868f5978da6ccdb45738bc399(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c302dc08edcad6076632d5c3b0ab2cf01ef6273de13fe239bd11554b3bc2898(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7715bc8d74a788993c6c04fe42080a8598f4876ee0e4380c63bfbc875069f2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d677f1f453ab48cbc77f26e8e6cc274f3012d80146e713422855243a4a5783(
    value: typing.Optional[TransferWorkflowStepsCustomStepDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aa2de7888d8477f870803c4e9e3f6bd84489260562cd840be7e92174ef36f17(
    *,
    type: builtins.str,
    destination_file_location: typing.Optional[typing.Union[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    overwrite_existing: typing.Optional[builtins.str] = None,
    source_file_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce7961031a68a29bd90bda967bc7178f12e0173c5f8b1a0c03f59a93040ccd3(
    *,
    efs_file_location: typing.Optional[typing.Union[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_file_location: typing.Optional[typing.Union[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f633f311fad0ac4a79741c0f0b57eaf2e80a3a5e1d397ee997b60ab77208a841(
    *,
    file_system_id: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67eff449c75c426d59a5d9cf72f6e0a8f013afccf1d6a84a21becc45d4769795(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def8c0e591aaf6d3716a8e38390519d08a93fcaa0196a41529895dcdd99378c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8733187f81d23dfcd343d3d630b7b9befdfa0b2eb3eab8b9992dda609d389b1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d11c3c75a8413040ebb430e966c9e1173aa8c90df2596ba4ec1b2cb7047a03e(
    value: typing.Optional[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationEfsFileLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41adb286af3bba820040e5c2465b34d6ff2f6176ef5b7bb829ee794b192c7848(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad12afd944cebea9acfcfbc4c53a86e54547333b282352fee4fd1ada564b789(
    value: typing.Optional[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d421448fe9fb615d2151f1f7362fd78a93c776271d8613ae1ab3dc8acaba3e(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6baf1e273f42a58be4a623cf87d32c542ec797c2d6eddb6a8d0e45b62ccbb401(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22076ad48d54f9e2a19febeffad4916b3dfeb7c05c6a369334a54ada9b443236(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8960a4d1dd456b4ba1ab332a3d3f6cf4c36ea2a644ad0234d955fea65f4f1a30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9863114db568668949824f765f302e1e4472c2ee462ad2b81db3d1ba5f6da9e(
    value: typing.Optional[TransferWorkflowStepsDecryptStepDetailsDestinationFileLocationS3FileLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a89e129e90a0f4bddd7893b9798c79ca447519e473a79ab3bd309beda00559b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9979330f10c0c55daa0c5be7cb36d9c960c08b2345520612cf2873b91f03e630(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2270396f7986631a5dc841767a9bec449fc793a23acd0329988003ab811370(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faf9e608f38135712b54f3d11f0983b67723cbce0cc94387fa332e29690d0dd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf19c2e2e94da3c1f98d6e8685d300cff24de2108b90cf500d89b06a88af6bbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cbc2ec83ea1370a0b9acf2f2cb533a683bb1f35e881a206774d4bba8116f49c(
    value: typing.Optional[TransferWorkflowStepsDecryptStepDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da5b25cdab7c44f611e4086e2ca45c068709e8aaf1e95b5e6309ff86cef5122(
    *,
    name: typing.Optional[builtins.str] = None,
    source_file_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69b8ea8f22defba16ad070122b496bb8e7d0a53075e21945afc32205d5f1a14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c09e5f22aab935232cb2144fa6cc63d68977564ff2e5830d83ca66e6e19808d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0cf5d457964a949c4152ae3e15eb24d2d7a3e03aad0278bc5dc50df8ff4d394(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c3f8f53406fff9691037fafdf825f33dbafaad26d8bec270e9c9f93f8d1362b(
    value: typing.Optional[TransferWorkflowStepsDeleteStepDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9079d3be583151fa79bc0f194330f293ddfd33597077351ce13d90b6a32fb0cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b997875ade4c53edf47e0a77d6ad07c364bc1b5d986d1b9fe9322acfe48b82ba(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fbde61a586ddb2d98b790633aa8b0c860192d714fcef6f890adef50cd1f981e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4108b583d410b21d961205cbbb01a27d16989ab34a7bc59f9bcefd317b4cf8c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18edc15e53a677070215a78fbf34590fc38700bac1eecc358613b0a23a6d6092(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d7873d23bdbff3f83852464941926e9df1fc759c3d9cfd7d1c469ffd4bca5b3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TransferWorkflowSteps]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468b262a22d3e123cbb02fc93c099ebbfd5e8082118a4ed0209ce897449f0d0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__907057ed2a0aabaac1283d234dbc3735ca480f775d1c7acc684b9e5f56227f0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924e4c0cf565e56e30eff8a296fc852bb290a9904f2e4ce123955e5ec85abdf3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferWorkflowSteps]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab94c6812a2e0e8aab82c9d96454eae4d4ee47d1740004585b8fc4bfb92e8fe(
    *,
    name: typing.Optional[builtins.str] = None,
    source_file_location: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TransferWorkflowStepsTagStepDetailsTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf72b27a5e9b5e6db85bf30e36b263386b75bd5de4de4d206c3f84cffa0af3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a0eabf898c53ab777efd6ad99b14389b6fd4c5fddc623f9fe6f2949536506b2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TransferWorkflowStepsTagStepDetailsTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1efbd0ffccac3ad96d4efa362f1866cf401037bd378791a4a1cb9ef5edb103d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1e6e90f892f6d9406d294d06252ef20caf3b654e10ffe0f32cb692000203c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7f02a705103c98d7ea19a523f97c5404638e1ea265c2929394a23ebef073ed(
    value: typing.Optional[TransferWorkflowStepsTagStepDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f720dd3bb49bbfb79b79a2b4239a7c7827a23557348400d0bdda4bdfd82ff8(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__738e2a2f080c5b438d951078ee67c2c74f8e0e9cc9b2d84bf2bc3f8fc9312896(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9075429cd860fba84c37b5316c726946b10c09f17fb4063a6961bc27e64165(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11595575434aba2e6f034879791e861ef50d2a99354f862f35a643391d9d1ab6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2928b3ee7ccc814a88efe7735c8597ffe0fb5ceb960de61012b7d578d6fba20(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08140272cb02c64c153a92983509bbe97c08b9ddb8e4432ee1487ce8ce2197bb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d449f97a03f859182d591bfaac2797352ace5770ee478aad5c38c8b96280b750(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TransferWorkflowStepsTagStepDetailsTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392e2880a352b4a5eb449ee4fa18e5ec92aab7a3ea955c3dd5f4386a5a4e32e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f44d57ceead395e7c674f5d4d363a069b8691b1dc6934213ed8328c288104e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195cb0c483fd9156574e0696f5f532a4658030f53561a7ccf67014db46c988cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806ed38c5e4d6073fe80c157f85752c4f3f0b2fcc7db5bde161dd958ba50d35a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TransferWorkflowStepsTagStepDetailsTags]],
) -> None:
    """Type checking stubs"""
    pass
