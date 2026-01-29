r'''
# `aws_appmesh_virtual_node`

Refer to the Terraform Registry for docs: [`aws_appmesh_virtual_node`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node).
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


class AppmeshVirtualNode(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNode",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node aws_appmesh_virtual_node}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        mesh_name: builtins.str,
        name: builtins.str,
        spec: typing.Union["AppmeshVirtualNodeSpec", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        mesh_owner: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node aws_appmesh_virtual_node} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param mesh_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#mesh_name AppmeshVirtualNode#mesh_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#name AppmeshVirtualNode#name}.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#spec AppmeshVirtualNode#spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#id AppmeshVirtualNode#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mesh_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#mesh_owner AppmeshVirtualNode#mesh_owner}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#region AppmeshVirtualNode#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tags AppmeshVirtualNode#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tags_all AppmeshVirtualNode#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5172288e5618603275da7a129ce2c33bfdb6d64cdc79753460b0d75c9f09b815)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppmeshVirtualNodeConfig(
            mesh_name=mesh_name,
            name=name,
            spec=spec,
            id=id,
            mesh_owner=mesh_owner,
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
        '''Generates CDKTF code for importing a AppmeshVirtualNode resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppmeshVirtualNode to import.
        :param import_from_id: The id of the existing AppmeshVirtualNode that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppmeshVirtualNode to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50d95e439e0830896ed0f36b9f7d80cb70cec9f2d2b37fece1d9b1f98950a13f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshVirtualNodeSpecBackend", typing.Dict[builtins.str, typing.Any]]]]] = None,
        backend_defaults: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendDefaults", typing.Dict[builtins.str, typing.Any]]] = None,
        listener: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshVirtualNodeSpecListener", typing.Dict[builtins.str, typing.Any]]]]] = None,
        logging: typing.Optional[typing.Union["AppmeshVirtualNodeSpecLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        service_discovery: typing.Optional[typing.Union["AppmeshVirtualNodeSpecServiceDiscovery", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param backend: backend block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#backend AppmeshVirtualNode#backend}
        :param backend_defaults: backend_defaults block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#backend_defaults AppmeshVirtualNode#backend_defaults}
        :param listener: listener block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#listener AppmeshVirtualNode#listener}
        :param logging: logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#logging AppmeshVirtualNode#logging}
        :param service_discovery: service_discovery block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#service_discovery AppmeshVirtualNode#service_discovery}
        '''
        value = AppmeshVirtualNodeSpec(
            backend=backend,
            backend_defaults=backend_defaults,
            listener=listener,
            logging=logging,
            service_discovery=service_discovery,
        )

        return typing.cast(None, jsii.invoke(self, "putSpec", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMeshOwner")
    def reset_mesh_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMeshOwner", []))

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
    @jsii.member(jsii_name="createdDate")
    def created_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdDate"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdatedDate")
    def last_updated_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdatedDate"))

    @builtins.property
    @jsii.member(jsii_name="resourceOwner")
    def resource_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceOwner"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "AppmeshVirtualNodeSpecOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="meshNameInput")
    def mesh_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "meshNameInput"))

    @builtins.property
    @jsii.member(jsii_name="meshOwnerInput")
    def mesh_owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "meshOwnerInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="specInput")
    def spec_input(self) -> typing.Optional["AppmeshVirtualNodeSpec"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpec"], jsii.get(self, "specInput"))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce963d2efec943ec5501b4b5d04104d986cdfb13f502087789974aa8b6c37bf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "meshName"))

    @mesh_name.setter
    def mesh_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70e094899f10368d6842a1a923ba3a02c86107862d2bea3786c848ad33c06eeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "meshName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="meshOwner")
    def mesh_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "meshOwner"))

    @mesh_owner.setter
    def mesh_owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4822a7d1c04a3f787345cf69a4b5f15476a140a7f4584e1007febee8cc309af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "meshOwner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d843d85067b59a7b2c3a73b2872991ff2a93c31c35a6cd33a4f1ab3ba068011f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f6fc608c9b24144a8d089171900b7d4a6c89b4ab608f8cb245cd32544e6e52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91176d8b65b7d306333342e03a6958ac614635c29038edc42875fbbef46c54a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f003ad776c786ac2d620dd9397e3e1ae1d2cecbffec457172bcfb853cfd36ed6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "mesh_name": "meshName",
        "name": "name",
        "spec": "spec",
        "id": "id",
        "mesh_owner": "meshOwner",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class AppmeshVirtualNodeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        mesh_name: builtins.str,
        name: builtins.str,
        spec: typing.Union["AppmeshVirtualNodeSpec", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        mesh_owner: typing.Optional[builtins.str] = None,
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
        :param mesh_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#mesh_name AppmeshVirtualNode#mesh_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#name AppmeshVirtualNode#name}.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#spec AppmeshVirtualNode#spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#id AppmeshVirtualNode#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mesh_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#mesh_owner AppmeshVirtualNode#mesh_owner}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#region AppmeshVirtualNode#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tags AppmeshVirtualNode#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tags_all AppmeshVirtualNode#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(spec, dict):
            spec = AppmeshVirtualNodeSpec(**spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7ab6abfc8bf5ae852b956a9a27185f830830809376fbac4fc779c0ce20e559a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument mesh_name", value=mesh_name, expected_type=type_hints["mesh_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument mesh_owner", value=mesh_owner, expected_type=type_hints["mesh_owner"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mesh_name": mesh_name,
            "name": name,
            "spec": spec,
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
        if id is not None:
            self._values["id"] = id
        if mesh_owner is not None:
            self._values["mesh_owner"] = mesh_owner
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
    def mesh_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#mesh_name AppmeshVirtualNode#mesh_name}.'''
        result = self._values.get("mesh_name")
        assert result is not None, "Required property 'mesh_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#name AppmeshVirtualNode#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spec(self) -> "AppmeshVirtualNodeSpec":
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#spec AppmeshVirtualNode#spec}
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast("AppmeshVirtualNodeSpec", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#id AppmeshVirtualNode#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#mesh_owner AppmeshVirtualNode#mesh_owner}.'''
        result = self._values.get("mesh_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#region AppmeshVirtualNode#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tags AppmeshVirtualNode#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tags_all AppmeshVirtualNode#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpec",
    jsii_struct_bases=[],
    name_mapping={
        "backend": "backend",
        "backend_defaults": "backendDefaults",
        "listener": "listener",
        "logging": "logging",
        "service_discovery": "serviceDiscovery",
    },
)
class AppmeshVirtualNodeSpec:
    def __init__(
        self,
        *,
        backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshVirtualNodeSpecBackend", typing.Dict[builtins.str, typing.Any]]]]] = None,
        backend_defaults: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendDefaults", typing.Dict[builtins.str, typing.Any]]] = None,
        listener: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshVirtualNodeSpecListener", typing.Dict[builtins.str, typing.Any]]]]] = None,
        logging: typing.Optional[typing.Union["AppmeshVirtualNodeSpecLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        service_discovery: typing.Optional[typing.Union["AppmeshVirtualNodeSpecServiceDiscovery", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param backend: backend block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#backend AppmeshVirtualNode#backend}
        :param backend_defaults: backend_defaults block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#backend_defaults AppmeshVirtualNode#backend_defaults}
        :param listener: listener block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#listener AppmeshVirtualNode#listener}
        :param logging: logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#logging AppmeshVirtualNode#logging}
        :param service_discovery: service_discovery block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#service_discovery AppmeshVirtualNode#service_discovery}
        '''
        if isinstance(backend_defaults, dict):
            backend_defaults = AppmeshVirtualNodeSpecBackendDefaults(**backend_defaults)
        if isinstance(logging, dict):
            logging = AppmeshVirtualNodeSpecLogging(**logging)
        if isinstance(service_discovery, dict):
            service_discovery = AppmeshVirtualNodeSpecServiceDiscovery(**service_discovery)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb3670928005760dd0de1ce79f1c2d5168518892756da39d9c5131ffe8823e84)
            check_type(argname="argument backend", value=backend, expected_type=type_hints["backend"])
            check_type(argname="argument backend_defaults", value=backend_defaults, expected_type=type_hints["backend_defaults"])
            check_type(argname="argument listener", value=listener, expected_type=type_hints["listener"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument service_discovery", value=service_discovery, expected_type=type_hints["service_discovery"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backend is not None:
            self._values["backend"] = backend
        if backend_defaults is not None:
            self._values["backend_defaults"] = backend_defaults
        if listener is not None:
            self._values["listener"] = listener
        if logging is not None:
            self._values["logging"] = logging
        if service_discovery is not None:
            self._values["service_discovery"] = service_discovery

    @builtins.property
    def backend(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshVirtualNodeSpecBackend"]]]:
        '''backend block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#backend AppmeshVirtualNode#backend}
        '''
        result = self._values.get("backend")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshVirtualNodeSpecBackend"]]], result)

    @builtins.property
    def backend_defaults(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendDefaults"]:
        '''backend_defaults block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#backend_defaults AppmeshVirtualNode#backend_defaults}
        '''
        result = self._values.get("backend_defaults")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendDefaults"], result)

    @builtins.property
    def listener(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshVirtualNodeSpecListener"]]]:
        '''listener block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#listener AppmeshVirtualNode#listener}
        '''
        result = self._values.get("listener")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshVirtualNodeSpecListener"]]], result)

    @builtins.property
    def logging(self) -> typing.Optional["AppmeshVirtualNodeSpecLogging"]:
        '''logging block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#logging AppmeshVirtualNode#logging}
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecLogging"], result)

    @builtins.property
    def service_discovery(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecServiceDiscovery"]:
        '''service_discovery block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#service_discovery AppmeshVirtualNode#service_discovery}
        '''
        result = self._values.get("service_discovery")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecServiceDiscovery"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackend",
    jsii_struct_bases=[],
    name_mapping={"virtual_service": "virtualService"},
)
class AppmeshVirtualNodeSpecBackend:
    def __init__(
        self,
        *,
        virtual_service: typing.Union["AppmeshVirtualNodeSpecBackendVirtualService", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param virtual_service: virtual_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#virtual_service AppmeshVirtualNode#virtual_service}
        '''
        if isinstance(virtual_service, dict):
            virtual_service = AppmeshVirtualNodeSpecBackendVirtualService(**virtual_service)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d32520f73281c67a6cd2419ec79267a8e8c19cee0d5b66f15006f4695c779cc)
            check_type(argname="argument virtual_service", value=virtual_service, expected_type=type_hints["virtual_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_service": virtual_service,
        }

    @builtins.property
    def virtual_service(self) -> "AppmeshVirtualNodeSpecBackendVirtualService":
        '''virtual_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#virtual_service AppmeshVirtualNode#virtual_service}
        '''
        result = self._values.get("virtual_service")
        assert result is not None, "Required property 'virtual_service' is missing"
        return typing.cast("AppmeshVirtualNodeSpecBackendVirtualService", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackend(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaults",
    jsii_struct_bases=[],
    name_mapping={"client_policy": "clientPolicy"},
)
class AppmeshVirtualNodeSpecBackendDefaults:
    def __init__(
        self,
        *,
        client_policy: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_policy: client_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#client_policy AppmeshVirtualNode#client_policy}
        '''
        if isinstance(client_policy, dict):
            client_policy = AppmeshVirtualNodeSpecBackendDefaultsClientPolicy(**client_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd33021a513758747438c149a283732e7766db464da1908774b32979cd07b3ad)
            check_type(argname="argument client_policy", value=client_policy, expected_type=type_hints["client_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_policy is not None:
            self._values["client_policy"] = client_policy

    @builtins.property
    def client_policy(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicy"]:
        '''client_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#client_policy AppmeshVirtualNode#client_policy}
        '''
        result = self._values.get("client_policy")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendDefaults(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicy",
    jsii_struct_bases=[],
    name_mapping={"tls": "tls"},
)
class AppmeshVirtualNodeSpecBackendDefaultsClientPolicy:
    def __init__(
        self,
        *,
        tls: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTls", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param tls: tls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tls AppmeshVirtualNode#tls}
        '''
        if isinstance(tls, dict):
            tls = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTls(**tls)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48cd84ee72f9a9393ecb780a9bd50771dd3f615313fccf78d63991635f6df76d)
            check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tls is not None:
            self._values["tls"] = tls

    @builtins.property
    def tls(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTls"]:
        '''tls block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tls AppmeshVirtualNode#tls}
        '''
        result = self._values.get("tls")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTls"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendDefaultsClientPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e019bf5f23d13b34b7983b1096f72891b1e5d6c5230125ccee7b9bc4f66bbd11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTls")
    def put_tls(
        self,
        *,
        validation: typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidation", typing.Dict[builtins.str, typing.Any]],
        certificate: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param validation: validation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#validation AppmeshVirtualNode#validation}
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate AppmeshVirtualNode#certificate}
        :param enforce: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#enforce AppmeshVirtualNode#enforce}.
        :param ports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#ports AppmeshVirtualNode#ports}.
        '''
        value = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTls(
            validation=validation,
            certificate=certificate,
            enforce=enforce,
            ports=ports,
        )

        return typing.cast(None, jsii.invoke(self, "putTls", [value]))

    @jsii.member(jsii_name="resetTls")
    def reset_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTls", []))

    @builtins.property
    @jsii.member(jsii_name="tls")
    def tls(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsOutputReference", jsii.get(self, "tls"))

    @builtins.property
    @jsii.member(jsii_name="tlsInput")
    def tls_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTls"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTls"], jsii.get(self, "tlsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicy]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__106b169ca54cf898a21e9bf0f4dd6eb6de22aecd63e38d882a91e9b4bba68dc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTls",
    jsii_struct_bases=[],
    name_mapping={
        "validation": "validation",
        "certificate": "certificate",
        "enforce": "enforce",
        "ports": "ports",
    },
)
class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTls:
    def __init__(
        self,
        *,
        validation: typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidation", typing.Dict[builtins.str, typing.Any]],
        certificate: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param validation: validation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#validation AppmeshVirtualNode#validation}
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate AppmeshVirtualNode#certificate}
        :param enforce: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#enforce AppmeshVirtualNode#enforce}.
        :param ports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#ports AppmeshVirtualNode#ports}.
        '''
        if isinstance(validation, dict):
            validation = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidation(**validation)
        if isinstance(certificate, dict):
            certificate = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificate(**certificate)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8ffad650a7d594789bbe2b6cb03a444fad78409fcb16533a248c4a23c7ced97)
            check_type(argname="argument validation", value=validation, expected_type=type_hints["validation"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument enforce", value=enforce, expected_type=type_hints["enforce"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "validation": validation,
        }
        if certificate is not None:
            self._values["certificate"] = certificate
        if enforce is not None:
            self._values["enforce"] = enforce
        if ports is not None:
            self._values["ports"] = ports

    @builtins.property
    def validation(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidation":
        '''validation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#validation AppmeshVirtualNode#validation}
        '''
        result = self._values.get("validation")
        assert result is not None, "Required property 'validation' is missing"
        return typing.cast("AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidation", result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificate"]:
        '''certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate AppmeshVirtualNode#certificate}
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificate"], result)

    @builtins.property
    def enforce(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#enforce AppmeshVirtualNode#enforce}.'''
        result = self._values.get("enforce")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#ports AppmeshVirtualNode#ports}.'''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificate",
    jsii_struct_bases=[],
    name_mapping={"file": "file", "sds": "sds"},
)
class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificate:
    def __init__(
        self,
        *,
        file: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFile", typing.Dict[builtins.str, typing.Any]]] = None,
        sds: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSds", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        :param sds: sds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#sds AppmeshVirtualNode#sds}
        '''
        if isinstance(file, dict):
            file = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFile(**file)
        if isinstance(sds, dict):
            sds = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSds(**sds)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19a7ca3ee1dbe54b9d1bff36effb8a69e9404bf3207cd8e8fc2be9a3938e4f36)
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument sds", value=sds, expected_type=type_hints["sds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file is not None:
            self._values["file"] = file
        if sds is not None:
            self._values["sds"] = sds

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFile"], result)

    @builtins.property
    def sds(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSds"]:
        '''sds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#sds AppmeshVirtualNode#sds}
        '''
        result = self._values.get("sds")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSds"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFile",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_chain": "certificateChain",
        "private_key": "privateKey",
    },
)
class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFile:
    def __init__(
        self,
        *,
        certificate_chain: builtins.str,
        private_key: builtins.str,
    ) -> None:
        '''
        :param certificate_chain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_chain AppmeshVirtualNode#certificate_chain}.
        :param private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#private_key AppmeshVirtualNode#private_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aaf37ec87517ea7d5b1cc5fff355189e3240d330cc1cbd0fa5bf92490533679)
            check_type(argname="argument certificate_chain", value=certificate_chain, expected_type=type_hints["certificate_chain"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_chain": certificate_chain,
            "private_key": private_key,
        }

    @builtins.property
    def certificate_chain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_chain AppmeshVirtualNode#certificate_chain}.'''
        result = self._values.get("certificate_chain")
        assert result is not None, "Required property 'certificate_chain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def private_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#private_key AppmeshVirtualNode#private_key}.'''
        result = self._values.get("private_key")
        assert result is not None, "Required property 'private_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__517309efa9fa546a6205c45172ee9381f9e668ec77a054276e84b670b24222c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="certificateChainInput")
    def certificate_chain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateChainInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyInput")
    def private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateChain")
    def certificate_chain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateChain"))

    @certificate_chain.setter
    def certificate_chain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__318eb6bb5c288ee05af2dcedf11bdfaac94601e33b09278ced698f1150cf90a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateChain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c4491ab2f0fdcafa407522517c48aae87ea0f700e360ab1915f0c6c074a1c4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFile]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__815e74f988ad73a9e5c0e32f50b2ba667ff5fdcfe56a712aa65baecc88184361)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0442697b2f95d0f87fd75f76bfcd155313fdbe838ddd07aa570930ff0bc432e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        certificate_chain: builtins.str,
        private_key: builtins.str,
    ) -> None:
        '''
        :param certificate_chain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_chain AppmeshVirtualNode#certificate_chain}.
        :param private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#private_key AppmeshVirtualNode#private_key}.
        '''
        value = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFile(
            certificate_chain=certificate_chain, private_key=private_key
        )

        return typing.cast(None, jsii.invoke(self, "putFile", [value]))

    @jsii.member(jsii_name="putSds")
    def put_sds(self, *, secret_name: builtins.str) -> None:
        '''
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#secret_name AppmeshVirtualNode#secret_name}.
        '''
        value = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSds(
            secret_name=secret_name
        )

        return typing.cast(None, jsii.invoke(self, "putSds", [value]))

    @jsii.member(jsii_name="resetFile")
    def reset_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFile", []))

    @jsii.member(jsii_name="resetSds")
    def reset_sds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSds", []))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(
        self,
    ) -> AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFileOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="sds")
    def sds(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSdsOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSdsOutputReference", jsii.get(self, "sds"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFile]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFile], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="sdsInput")
    def sds_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSds"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSds"], jsii.get(self, "sdsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificate]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85abbe0adcb67fc57d0ce27c04737b3c05ab072af253385631cab24be431b0e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSds",
    jsii_struct_bases=[],
    name_mapping={"secret_name": "secretName"},
)
class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSds:
    def __init__(self, *, secret_name: builtins.str) -> None:
        '''
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#secret_name AppmeshVirtualNode#secret_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635d855d0edb6ef7acaab392b973833cb5b96cb0caa05f84585136f79bd42f45)
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_name": secret_name,
        }

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#secret_name AppmeshVirtualNode#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b925886256fdf896462d51e5b5c0d44586f67bbe3bbcb8809c4851882d827f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__887ac4834ec91e3021e9f400769c5e5cadab78876b8ddabcbe22b9b467cde638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSds]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ee46dc18be4a92668f70126a88af9e403a59bbe0ffef1ee2d9445466495137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9534d26d71ae836081c286ac59730443d1849065da29346fa770393da8711820)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCertificate")
    def put_certificate(
        self,
        *,
        file: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFile, typing.Dict[builtins.str, typing.Any]]] = None,
        sds: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSds, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        :param sds: sds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#sds AppmeshVirtualNode#sds}
        '''
        value = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificate(
            file=file, sds=sds
        )

        return typing.cast(None, jsii.invoke(self, "putCertificate", [value]))

    @jsii.member(jsii_name="putValidation")
    def put_validation(
        self,
        *,
        trust: typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrust", typing.Dict[builtins.str, typing.Any]],
        subject_alternative_names: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNames", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param trust: trust block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#trust AppmeshVirtualNode#trust}
        :param subject_alternative_names: subject_alternative_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#subject_alternative_names AppmeshVirtualNode#subject_alternative_names}
        '''
        value = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidation(
            trust=trust, subject_alternative_names=subject_alternative_names
        )

        return typing.cast(None, jsii.invoke(self, "putValidation", [value]))

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetEnforce")
    def reset_enforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforce", []))

    @jsii.member(jsii_name="resetPorts")
    def reset_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPorts", []))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(
        self,
    ) -> AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateOutputReference, jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="validation")
    def validation(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationOutputReference", jsii.get(self, "validation"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificate]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificate], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="validationInput")
    def validation_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidation"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidation"], jsii.get(self, "validationInput"))

    @builtins.property
    @jsii.member(jsii_name="enforce")
    def enforce(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforce"))

    @enforce.setter
    def enforce(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c74d46ad473e13122a53e5490509218d836a8f6b248aaeaa49d96117f7c52f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d528f9437080ca0fccdc4a2357274844de2c6e9d533e227a40b3b6b8c71023d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTls]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTls], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTls],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53e32d8c2e96fdee87aed0d583903b2861f58db42907edc5ed38b5a221b6064c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidation",
    jsii_struct_bases=[],
    name_mapping={
        "trust": "trust",
        "subject_alternative_names": "subjectAlternativeNames",
    },
)
class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidation:
    def __init__(
        self,
        *,
        trust: typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrust", typing.Dict[builtins.str, typing.Any]],
        subject_alternative_names: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNames", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param trust: trust block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#trust AppmeshVirtualNode#trust}
        :param subject_alternative_names: subject_alternative_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#subject_alternative_names AppmeshVirtualNode#subject_alternative_names}
        '''
        if isinstance(trust, dict):
            trust = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrust(**trust)
        if isinstance(subject_alternative_names, dict):
            subject_alternative_names = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNames(**subject_alternative_names)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc22af273546981bf1a31eff9e1d787cc2534e1eafe67a7b3be66376a4e9c53e)
            check_type(argname="argument trust", value=trust, expected_type=type_hints["trust"])
            check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trust": trust,
        }
        if subject_alternative_names is not None:
            self._values["subject_alternative_names"] = subject_alternative_names

    @builtins.property
    def trust(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrust":
        '''trust block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#trust AppmeshVirtualNode#trust}
        '''
        result = self._values.get("trust")
        assert result is not None, "Required property 'trust' is missing"
        return typing.cast("AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrust", result)

    @builtins.property
    def subject_alternative_names(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNames"]:
        '''subject_alternative_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#subject_alternative_names AppmeshVirtualNode#subject_alternative_names}
        '''
        result = self._values.get("subject_alternative_names")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNames"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1719597d0286fe4402517fd8be212c30d2b8cf6022b816e7bb4b2c02380cb210)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSubjectAlternativeNames")
    def put_subject_alternative_names(
        self,
        *,
        match: typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatch", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#match AppmeshVirtualNode#match}
        '''
        value = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNames(
            match=match
        )

        return typing.cast(None, jsii.invoke(self, "putSubjectAlternativeNames", [value]))

    @jsii.member(jsii_name="putTrust")
    def put_trust(
        self,
        *,
        acm: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcm", typing.Dict[builtins.str, typing.Any]]] = None,
        file: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFile", typing.Dict[builtins.str, typing.Any]]] = None,
        sds: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSds", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param acm: acm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#acm AppmeshVirtualNode#acm}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        :param sds: sds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#sds AppmeshVirtualNode#sds}
        '''
        value = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrust(
            acm=acm, file=file, sds=sds
        )

        return typing.cast(None, jsii.invoke(self, "putTrust", [value]))

    @jsii.member(jsii_name="resetSubjectAlternativeNames")
    def reset_subject_alternative_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectAlternativeNames", []))

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeNames")
    def subject_alternative_names(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesOutputReference", jsii.get(self, "subjectAlternativeNames"))

    @builtins.property
    @jsii.member(jsii_name="trust")
    def trust(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustOutputReference", jsii.get(self, "trust"))

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeNamesInput")
    def subject_alternative_names_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNames"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNames"], jsii.get(self, "subjectAlternativeNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="trustInput")
    def trust_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrust"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrust"], jsii.get(self, "trustInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidation]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73797900476fad92ec59919c3dea51ef619915a20b4ad6ce5c07b7f86e88d863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNames",
    jsii_struct_bases=[],
    name_mapping={"match": "match"},
)
class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNames:
    def __init__(
        self,
        *,
        match: typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatch", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#match AppmeshVirtualNode#match}
        '''
        if isinstance(match, dict):
            match = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36e57b54d9166e817f334d93cde771d07252c0b1ff8ae44a2c55f7483c901881)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match": match,
        }

    @builtins.property
    def match(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatch":
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#match AppmeshVirtualNode#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatch", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatch",
    jsii_struct_bases=[],
    name_mapping={"exact": "exact"},
)
class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatch:
    def __init__(self, *, exact: typing.Sequence[builtins.str]) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#exact AppmeshVirtualNode#exact}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1419ff5226d4ed1dafe5bb14ccf1d54586e40cf21bedffc8ca8fd04edb32664)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "exact": exact,
        }

    @builtins.property
    def exact(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#exact AppmeshVirtualNode#exact}.'''
        result = self._values.get("exact")
        assert result is not None, "Required property 'exact' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93432844e7f980123477d73a54997639ae497f709e5b018909bc44d8e18d1fa2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64dfca17f0c8760593659a0973a47143aae737b004e0d5fb5c0452fc33a7a159)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatch]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c3bc738c5eb46220677d58539b0bcffeeac3db18d66777a402f56c88730b083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2435dac827fde8d8157e21eea4e2da469d27fe216eca847b944e8e8504ce03a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMatch")
    def put_match(self, *, exact: typing.Sequence[builtins.str]) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#exact AppmeshVirtualNode#exact}.
        '''
        value = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatch(
            exact=exact
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(
        self,
    ) -> AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatchOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatch]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNames]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNames], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNames],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44252b818b779626eff76f36063e46bee38fe6882b45d1d7160ace1302c03c4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrust",
    jsii_struct_bases=[],
    name_mapping={"acm": "acm", "file": "file", "sds": "sds"},
)
class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrust:
    def __init__(
        self,
        *,
        acm: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcm", typing.Dict[builtins.str, typing.Any]]] = None,
        file: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFile", typing.Dict[builtins.str, typing.Any]]] = None,
        sds: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSds", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param acm: acm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#acm AppmeshVirtualNode#acm}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        :param sds: sds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#sds AppmeshVirtualNode#sds}
        '''
        if isinstance(acm, dict):
            acm = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcm(**acm)
        if isinstance(file, dict):
            file = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFile(**file)
        if isinstance(sds, dict):
            sds = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSds(**sds)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e16b470e76136ee369e35c40c934e2f12c2b510553b2bcc6fc49590b1801273)
            check_type(argname="argument acm", value=acm, expected_type=type_hints["acm"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument sds", value=sds, expected_type=type_hints["sds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if acm is not None:
            self._values["acm"] = acm
        if file is not None:
            self._values["file"] = file
        if sds is not None:
            self._values["sds"] = sds

    @builtins.property
    def acm(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcm"]:
        '''acm block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#acm AppmeshVirtualNode#acm}
        '''
        result = self._values.get("acm")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcm"], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFile"], result)

    @builtins.property
    def sds(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSds"]:
        '''sds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#sds AppmeshVirtualNode#sds}
        '''
        result = self._values.get("sds")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSds"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrust(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcm",
    jsii_struct_bases=[],
    name_mapping={"certificate_authority_arns": "certificateAuthorityArns"},
)
class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcm:
    def __init__(
        self,
        *,
        certificate_authority_arns: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param certificate_authority_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_authority_arns AppmeshVirtualNode#certificate_authority_arns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b6538d1437f2ffea5c8607bef33e77816bd952990d2e45d7dcdf192f3225880)
            check_type(argname="argument certificate_authority_arns", value=certificate_authority_arns, expected_type=type_hints["certificate_authority_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_authority_arns": certificate_authority_arns,
        }

    @builtins.property
    def certificate_authority_arns(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_authority_arns AppmeshVirtualNode#certificate_authority_arns}.'''
        result = self._values.get("certificate_authority_arns")
        assert result is not None, "Required property 'certificate_authority_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcmOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcmOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7cd0d762e4f5edecb066da5813ed2404a88591884e870dda35473b365c93df6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityArnsInput")
    def certificate_authority_arns_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "certificateAuthorityArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityArns")
    def certificate_authority_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "certificateAuthorityArns"))

    @certificate_authority_arns.setter
    def certificate_authority_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f149bbe3b0d7ade15afe279ff3581d9b214abae95c62e5df295a2d6be73b516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateAuthorityArns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcm]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3844ef822d04d070a3746690e70438d7e0f4ff6c1e39d3cf723d5015aebfc4f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFile",
    jsii_struct_bases=[],
    name_mapping={"certificate_chain": "certificateChain"},
)
class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFile:
    def __init__(self, *, certificate_chain: builtins.str) -> None:
        '''
        :param certificate_chain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_chain AppmeshVirtualNode#certificate_chain}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b19fe038617776975a77d91ce46c75f93072cc4fd1a6d9f1df858f35e8e8976)
            check_type(argname="argument certificate_chain", value=certificate_chain, expected_type=type_hints["certificate_chain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_chain": certificate_chain,
        }

    @builtins.property
    def certificate_chain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_chain AppmeshVirtualNode#certificate_chain}.'''
        result = self._values.get("certificate_chain")
        assert result is not None, "Required property 'certificate_chain' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80680ff1cefe20e72a434038ed9534051975914b25d1d90b186fe9b54bdc188b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="certificateChainInput")
    def certificate_chain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateChainInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateChain")
    def certificate_chain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateChain"))

    @certificate_chain.setter
    def certificate_chain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__268c047408d1016b18d0a77063ef3cf233d73ec2b74998d0f40589f3e90e3a2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateChain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFile]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3acaba05a4dda01e34052963e169738fdeca5441bd9af5992fba926ffd6020f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2b790162650c87a8cee2a9a205a79876a55578df769ad0ebc226b71e215cd05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAcm")
    def put_acm(
        self,
        *,
        certificate_authority_arns: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param certificate_authority_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_authority_arns AppmeshVirtualNode#certificate_authority_arns}.
        '''
        value = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcm(
            certificate_authority_arns=certificate_authority_arns
        )

        return typing.cast(None, jsii.invoke(self, "putAcm", [value]))

    @jsii.member(jsii_name="putFile")
    def put_file(self, *, certificate_chain: builtins.str) -> None:
        '''
        :param certificate_chain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_chain AppmeshVirtualNode#certificate_chain}.
        '''
        value = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFile(
            certificate_chain=certificate_chain
        )

        return typing.cast(None, jsii.invoke(self, "putFile", [value]))

    @jsii.member(jsii_name="putSds")
    def put_sds(self, *, secret_name: builtins.str) -> None:
        '''
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#secret_name AppmeshVirtualNode#secret_name}.
        '''
        value = AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSds(
            secret_name=secret_name
        )

        return typing.cast(None, jsii.invoke(self, "putSds", [value]))

    @jsii.member(jsii_name="resetAcm")
    def reset_acm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcm", []))

    @jsii.member(jsii_name="resetFile")
    def reset_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFile", []))

    @jsii.member(jsii_name="resetSds")
    def reset_sds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSds", []))

    @builtins.property
    @jsii.member(jsii_name="acm")
    def acm(
        self,
    ) -> AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcmOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcmOutputReference, jsii.get(self, "acm"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(
        self,
    ) -> AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFileOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="sds")
    def sds(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSdsOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSdsOutputReference", jsii.get(self, "sds"))

    @builtins.property
    @jsii.member(jsii_name="acmInput")
    def acm_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcm]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcm], jsii.get(self, "acmInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFile]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFile], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="sdsInput")
    def sds_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSds"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSds"], jsii.get(self, "sdsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrust]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrust], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrust],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf1eb3f231ce2587c22cef2b12597bb55362e0501c9746c82539bfac9e87e141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSds",
    jsii_struct_bases=[],
    name_mapping={"secret_name": "secretName"},
)
class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSds:
    def __init__(self, *, secret_name: builtins.str) -> None:
        '''
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#secret_name AppmeshVirtualNode#secret_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0c7779a137dd298d0cc0a9e2479e8ece96c29da94ba28ac2f5bcad22f7b634)
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_name": secret_name,
        }

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#secret_name AppmeshVirtualNode#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9867bbd527aeb05631a7876e890cf24d7a92a1b4980c9beb7f67ad726dce7cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__194730bcd1d931eac156bef92f4c15fed5bcca90a069ff148fd842602b9ea45c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSds]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f320eab480bf8547961df17ff8e07ee519ffe8ad2aeb06fbbd8ccb4fbedcf8a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecBackendDefaultsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendDefaultsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a74197984ad540fbe31cb721b95f5c02bfb74c76fc371562feb3b8ed850db527)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientPolicy")
    def put_client_policy(
        self,
        *,
        tls: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTls, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param tls: tls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tls AppmeshVirtualNode#tls}
        '''
        value = AppmeshVirtualNodeSpecBackendDefaultsClientPolicy(tls=tls)

        return typing.cast(None, jsii.invoke(self, "putClientPolicy", [value]))

    @jsii.member(jsii_name="resetClientPolicy")
    def reset_client_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="clientPolicy")
    def client_policy(
        self,
    ) -> AppmeshVirtualNodeSpecBackendDefaultsClientPolicyOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecBackendDefaultsClientPolicyOutputReference, jsii.get(self, "clientPolicy"))

    @builtins.property
    @jsii.member(jsii_name="clientPolicyInput")
    def client_policy_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicy]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicy], jsii.get(self, "clientPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaults]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaults], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaults],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__949b65fa643e8a33bc2a4bdc252c6eefa3e7d8fec2c49d4c0069bf9db04dda21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecBackendList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__846d08fff3865e2782f4baf44e6b55fce3dc3cadd52c987fd8f28a56463977e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AppmeshVirtualNodeSpecBackendOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46cd71bf3ad64774d78f11df0139c65d0183b7fda436104be6cc598e8415a617)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshVirtualNodeSpecBackendOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a330114425792bb26f60faa00231f2bb58ed95351d1f63274cec575186f56a72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aab4f3d55eb0fa52e1bd90ca0089775f676e5d7278620aa76e34dfd847300945)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2e36970f41d5693888b62f8f53622ef16872b78ca592aa0045b263957096e72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecBackend]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecBackend]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecBackend]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__295497814b9b03dfe8e569715516fb2eeae0bc0c1b1c511acacceccc95d2816b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecBackendOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5482d91ab7e70f3d4638387c96e076178a1163605ae3285204dd2b3453440e81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putVirtualService")
    def put_virtual_service(
        self,
        *,
        virtual_service_name: builtins.str,
        client_policy: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param virtual_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#virtual_service_name AppmeshVirtualNode#virtual_service_name}.
        :param client_policy: client_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#client_policy AppmeshVirtualNode#client_policy}
        '''
        value = AppmeshVirtualNodeSpecBackendVirtualService(
            virtual_service_name=virtual_service_name, client_policy=client_policy
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualService", [value]))

    @builtins.property
    @jsii.member(jsii_name="virtualService")
    def virtual_service(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendVirtualServiceOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecBackendVirtualServiceOutputReference", jsii.get(self, "virtualService"))

    @builtins.property
    @jsii.member(jsii_name="virtualServiceInput")
    def virtual_service_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendVirtualService"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendVirtualService"], jsii.get(self, "virtualServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecBackend]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecBackend]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecBackend]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e6726c71bfaa2a7e65f87e7885124aca0cc746ed4c5542e50ddaa5a36279d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualService",
    jsii_struct_bases=[],
    name_mapping={
        "virtual_service_name": "virtualServiceName",
        "client_policy": "clientPolicy",
    },
)
class AppmeshVirtualNodeSpecBackendVirtualService:
    def __init__(
        self,
        *,
        virtual_service_name: builtins.str,
        client_policy: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param virtual_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#virtual_service_name AppmeshVirtualNode#virtual_service_name}.
        :param client_policy: client_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#client_policy AppmeshVirtualNode#client_policy}
        '''
        if isinstance(client_policy, dict):
            client_policy = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicy(**client_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f4d312da85b87a536a8875c6aab1c1dd89f47c6ffb19f1ae8da669c13084ef)
            check_type(argname="argument virtual_service_name", value=virtual_service_name, expected_type=type_hints["virtual_service_name"])
            check_type(argname="argument client_policy", value=client_policy, expected_type=type_hints["client_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_service_name": virtual_service_name,
        }
        if client_policy is not None:
            self._values["client_policy"] = client_policy

    @builtins.property
    def virtual_service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#virtual_service_name AppmeshVirtualNode#virtual_service_name}.'''
        result = self._values.get("virtual_service_name")
        assert result is not None, "Required property 'virtual_service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_policy(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicy"]:
        '''client_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#client_policy AppmeshVirtualNode#client_policy}
        '''
        result = self._values.get("client_policy")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendVirtualService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicy",
    jsii_struct_bases=[],
    name_mapping={"tls": "tls"},
)
class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicy:
    def __init__(
        self,
        *,
        tls: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTls", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param tls: tls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tls AppmeshVirtualNode#tls}
        '''
        if isinstance(tls, dict):
            tls = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTls(**tls)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__775fc1aa60f57f5ace1c7515a4df3912fd83cb78168342e06d5668038ef82028)
            check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tls is not None:
            self._values["tls"] = tls

    @builtins.property
    def tls(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTls"]:
        '''tls block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tls AppmeshVirtualNode#tls}
        '''
        result = self._values.get("tls")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTls"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b6c6b67381d596d301f0c9abbd044218268a8a7e6d44326d36a790853aca4f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTls")
    def put_tls(
        self,
        *,
        validation: typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidation", typing.Dict[builtins.str, typing.Any]],
        certificate: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param validation: validation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#validation AppmeshVirtualNode#validation}
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate AppmeshVirtualNode#certificate}
        :param enforce: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#enforce AppmeshVirtualNode#enforce}.
        :param ports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#ports AppmeshVirtualNode#ports}.
        '''
        value = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTls(
            validation=validation,
            certificate=certificate,
            enforce=enforce,
            ports=ports,
        )

        return typing.cast(None, jsii.invoke(self, "putTls", [value]))

    @jsii.member(jsii_name="resetTls")
    def reset_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTls", []))

    @builtins.property
    @jsii.member(jsii_name="tls")
    def tls(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsOutputReference", jsii.get(self, "tls"))

    @builtins.property
    @jsii.member(jsii_name="tlsInput")
    def tls_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTls"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTls"], jsii.get(self, "tlsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicy]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0451640a4e83ff92a38bf279ed9e69e1d58c31ac426d007e0bc281f6429a890a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTls",
    jsii_struct_bases=[],
    name_mapping={
        "validation": "validation",
        "certificate": "certificate",
        "enforce": "enforce",
        "ports": "ports",
    },
)
class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTls:
    def __init__(
        self,
        *,
        validation: typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidation", typing.Dict[builtins.str, typing.Any]],
        certificate: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param validation: validation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#validation AppmeshVirtualNode#validation}
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate AppmeshVirtualNode#certificate}
        :param enforce: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#enforce AppmeshVirtualNode#enforce}.
        :param ports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#ports AppmeshVirtualNode#ports}.
        '''
        if isinstance(validation, dict):
            validation = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidation(**validation)
        if isinstance(certificate, dict):
            certificate = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificate(**certificate)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1526cec49cfb192e2f8617340468da15ee2c3afa005fb4b4d307d56f6070be62)
            check_type(argname="argument validation", value=validation, expected_type=type_hints["validation"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument enforce", value=enforce, expected_type=type_hints["enforce"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "validation": validation,
        }
        if certificate is not None:
            self._values["certificate"] = certificate
        if enforce is not None:
            self._values["enforce"] = enforce
        if ports is not None:
            self._values["ports"] = ports

    @builtins.property
    def validation(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidation":
        '''validation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#validation AppmeshVirtualNode#validation}
        '''
        result = self._values.get("validation")
        assert result is not None, "Required property 'validation' is missing"
        return typing.cast("AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidation", result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificate"]:
        '''certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate AppmeshVirtualNode#certificate}
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificate"], result)

    @builtins.property
    def enforce(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#enforce AppmeshVirtualNode#enforce}.'''
        result = self._values.get("enforce")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#ports AppmeshVirtualNode#ports}.'''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificate",
    jsii_struct_bases=[],
    name_mapping={"file": "file", "sds": "sds"},
)
class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificate:
    def __init__(
        self,
        *,
        file: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFile", typing.Dict[builtins.str, typing.Any]]] = None,
        sds: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSds", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        :param sds: sds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#sds AppmeshVirtualNode#sds}
        '''
        if isinstance(file, dict):
            file = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFile(**file)
        if isinstance(sds, dict):
            sds = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSds(**sds)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d8dd0725190f46b919604a90660e9515e91ab7080f846559ed376c24bcf5d65)
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument sds", value=sds, expected_type=type_hints["sds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file is not None:
            self._values["file"] = file
        if sds is not None:
            self._values["sds"] = sds

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFile"], result)

    @builtins.property
    def sds(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSds"]:
        '''sds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#sds AppmeshVirtualNode#sds}
        '''
        result = self._values.get("sds")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSds"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFile",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_chain": "certificateChain",
        "private_key": "privateKey",
    },
)
class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFile:
    def __init__(
        self,
        *,
        certificate_chain: builtins.str,
        private_key: builtins.str,
    ) -> None:
        '''
        :param certificate_chain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_chain AppmeshVirtualNode#certificate_chain}.
        :param private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#private_key AppmeshVirtualNode#private_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e393e077d51e815c2046f7ef4b46a3d90802d9d45a151176d2dec4419d5c42cc)
            check_type(argname="argument certificate_chain", value=certificate_chain, expected_type=type_hints["certificate_chain"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_chain": certificate_chain,
            "private_key": private_key,
        }

    @builtins.property
    def certificate_chain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_chain AppmeshVirtualNode#certificate_chain}.'''
        result = self._values.get("certificate_chain")
        assert result is not None, "Required property 'certificate_chain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def private_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#private_key AppmeshVirtualNode#private_key}.'''
        result = self._values.get("private_key")
        assert result is not None, "Required property 'private_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18460e055ae4a6c34641122028a298bfffe32152a0ba6b98cd02719acea7d3fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="certificateChainInput")
    def certificate_chain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateChainInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyInput")
    def private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateChain")
    def certificate_chain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateChain"))

    @certificate_chain.setter
    def certificate_chain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5aa248349b8894e0b7e64e8eadd1840adc889436d4f0a236f8e00463ebfdaf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateChain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0927540cd8978b9c4795a649819a46a4aee6614b3f607479a3ad8671de4e4a8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFile]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95fb331bc3f44f8a99a4e4e7ec6f1fb23d14fe24214bcff5458e7c4484609c7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f6e8ffc8b3f9791cdd5b2de841f59e3060ef33cafbec3dae14059b8f08d64a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        certificate_chain: builtins.str,
        private_key: builtins.str,
    ) -> None:
        '''
        :param certificate_chain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_chain AppmeshVirtualNode#certificate_chain}.
        :param private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#private_key AppmeshVirtualNode#private_key}.
        '''
        value = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFile(
            certificate_chain=certificate_chain, private_key=private_key
        )

        return typing.cast(None, jsii.invoke(self, "putFile", [value]))

    @jsii.member(jsii_name="putSds")
    def put_sds(self, *, secret_name: builtins.str) -> None:
        '''
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#secret_name AppmeshVirtualNode#secret_name}.
        '''
        value = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSds(
            secret_name=secret_name
        )

        return typing.cast(None, jsii.invoke(self, "putSds", [value]))

    @jsii.member(jsii_name="resetFile")
    def reset_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFile", []))

    @jsii.member(jsii_name="resetSds")
    def reset_sds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSds", []))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(
        self,
    ) -> AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFileOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="sds")
    def sds(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSdsOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSdsOutputReference", jsii.get(self, "sds"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFile]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFile], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="sdsInput")
    def sds_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSds"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSds"], jsii.get(self, "sdsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificate]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a2e3a7db8586b2d77652ec963c9c182641d2cce8cc7fb50cc1a6551b824d6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSds",
    jsii_struct_bases=[],
    name_mapping={"secret_name": "secretName"},
)
class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSds:
    def __init__(self, *, secret_name: builtins.str) -> None:
        '''
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#secret_name AppmeshVirtualNode#secret_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5470222945e75caa1b29e0feef2eaf2a484f96450a3d68a706abbf8cf55651a9)
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_name": secret_name,
        }

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#secret_name AppmeshVirtualNode#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83bcffd9228f83bd1860005fd335ef4e9fb60d9d050bdd712fc1da2220919b43)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebdbfb109eaa9cbab82b00d1f16e12593ad286944841aeecc13fde2290634ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSds]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2333cf273c824f793ea32163592dd659b11ab1c1250981904ea8a0b8a8e0d5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ff03d13d6e5dad00a2a4722813d7a732ffc125097b7dbbf97a0596161cd6fbd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCertificate")
    def put_certificate(
        self,
        *,
        file: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFile, typing.Dict[builtins.str, typing.Any]]] = None,
        sds: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSds, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        :param sds: sds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#sds AppmeshVirtualNode#sds}
        '''
        value = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificate(
            file=file, sds=sds
        )

        return typing.cast(None, jsii.invoke(self, "putCertificate", [value]))

    @jsii.member(jsii_name="putValidation")
    def put_validation(
        self,
        *,
        trust: typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrust", typing.Dict[builtins.str, typing.Any]],
        subject_alternative_names: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNames", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param trust: trust block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#trust AppmeshVirtualNode#trust}
        :param subject_alternative_names: subject_alternative_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#subject_alternative_names AppmeshVirtualNode#subject_alternative_names}
        '''
        value = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidation(
            trust=trust, subject_alternative_names=subject_alternative_names
        )

        return typing.cast(None, jsii.invoke(self, "putValidation", [value]))

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetEnforce")
    def reset_enforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforce", []))

    @jsii.member(jsii_name="resetPorts")
    def reset_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPorts", []))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(
        self,
    ) -> AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateOutputReference, jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="validation")
    def validation(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationOutputReference", jsii.get(self, "validation"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificate]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificate], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="validationInput")
    def validation_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidation"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidation"], jsii.get(self, "validationInput"))

    @builtins.property
    @jsii.member(jsii_name="enforce")
    def enforce(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforce"))

    @enforce.setter
    def enforce(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45b2be19d0305e24dfc1c66afbe7f114772e320eaa8635844fa2d40d8171a54c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ba02b28e4bd0d3b998b7718afb5a7e26349168780051b85bceaa87582c4b1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTls]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTls], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTls],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdfec02b9bad6a1aff766d51c89f0ca17a2013ba2739ad6aa5e5bf65b0e080aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidation",
    jsii_struct_bases=[],
    name_mapping={
        "trust": "trust",
        "subject_alternative_names": "subjectAlternativeNames",
    },
)
class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidation:
    def __init__(
        self,
        *,
        trust: typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrust", typing.Dict[builtins.str, typing.Any]],
        subject_alternative_names: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNames", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param trust: trust block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#trust AppmeshVirtualNode#trust}
        :param subject_alternative_names: subject_alternative_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#subject_alternative_names AppmeshVirtualNode#subject_alternative_names}
        '''
        if isinstance(trust, dict):
            trust = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrust(**trust)
        if isinstance(subject_alternative_names, dict):
            subject_alternative_names = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNames(**subject_alternative_names)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c1469043d2d41b6388729253eb5e711e779d0a8ba4af5a4ed6ecd8f6cf87e3c)
            check_type(argname="argument trust", value=trust, expected_type=type_hints["trust"])
            check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trust": trust,
        }
        if subject_alternative_names is not None:
            self._values["subject_alternative_names"] = subject_alternative_names

    @builtins.property
    def trust(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrust":
        '''trust block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#trust AppmeshVirtualNode#trust}
        '''
        result = self._values.get("trust")
        assert result is not None, "Required property 'trust' is missing"
        return typing.cast("AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrust", result)

    @builtins.property
    def subject_alternative_names(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNames"]:
        '''subject_alternative_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#subject_alternative_names AppmeshVirtualNode#subject_alternative_names}
        '''
        result = self._values.get("subject_alternative_names")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNames"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ab5bae7e6a2f303fad030d1be235f2f9ba5e212852df3e69e5187e106977c8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSubjectAlternativeNames")
    def put_subject_alternative_names(
        self,
        *,
        match: typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatch", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#match AppmeshVirtualNode#match}
        '''
        value = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNames(
            match=match
        )

        return typing.cast(None, jsii.invoke(self, "putSubjectAlternativeNames", [value]))

    @jsii.member(jsii_name="putTrust")
    def put_trust(
        self,
        *,
        acm: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcm", typing.Dict[builtins.str, typing.Any]]] = None,
        file: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFile", typing.Dict[builtins.str, typing.Any]]] = None,
        sds: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSds", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param acm: acm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#acm AppmeshVirtualNode#acm}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        :param sds: sds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#sds AppmeshVirtualNode#sds}
        '''
        value = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrust(
            acm=acm, file=file, sds=sds
        )

        return typing.cast(None, jsii.invoke(self, "putTrust", [value]))

    @jsii.member(jsii_name="resetSubjectAlternativeNames")
    def reset_subject_alternative_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectAlternativeNames", []))

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeNames")
    def subject_alternative_names(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesOutputReference", jsii.get(self, "subjectAlternativeNames"))

    @builtins.property
    @jsii.member(jsii_name="trust")
    def trust(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustOutputReference", jsii.get(self, "trust"))

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeNamesInput")
    def subject_alternative_names_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNames"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNames"], jsii.get(self, "subjectAlternativeNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="trustInput")
    def trust_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrust"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrust"], jsii.get(self, "trustInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidation]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c427c48774bf4db3d65c27b440f830dfc6628ffc74fd0597ba6f5df0cecc2d5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNames",
    jsii_struct_bases=[],
    name_mapping={"match": "match"},
)
class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNames:
    def __init__(
        self,
        *,
        match: typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatch", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#match AppmeshVirtualNode#match}
        '''
        if isinstance(match, dict):
            match = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2faad516a91946fd71e7883add8638663e7d678cd500b42211bdbcc587ea3a)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match": match,
        }

    @builtins.property
    def match(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatch":
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#match AppmeshVirtualNode#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatch", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatch",
    jsii_struct_bases=[],
    name_mapping={"exact": "exact"},
)
class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatch:
    def __init__(self, *, exact: typing.Sequence[builtins.str]) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#exact AppmeshVirtualNode#exact}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5f2ee50c4681f7381af10bcaed2a169b8cb8211a46690c6c74d921ec225236)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "exact": exact,
        }

    @builtins.property
    def exact(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#exact AppmeshVirtualNode#exact}.'''
        result = self._values.get("exact")
        assert result is not None, "Required property 'exact' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f21a2744a3ea44861f697c5c6cd3c98171382445e09eb6498b5409ef6c9453e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__922522833177aacd4026e2be619f6ff80712d32d2fa3affded8cc0240180b464)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatch]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d3e1d133f7d75c6d3f748956544fcb0cba9c65cf0c42723e6356af9969f47b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3a11961755ea0808f73ec2b56f8479b95d68c696ab9e5f10b45ae401da9982d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMatch")
    def put_match(self, *, exact: typing.Sequence[builtins.str]) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#exact AppmeshVirtualNode#exact}.
        '''
        value = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatch(
            exact=exact
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(
        self,
    ) -> AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatchOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatch]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNames]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNames], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNames],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a55257f574576600529746acae425ea36274f73581b838308b3825bc5eb9d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrust",
    jsii_struct_bases=[],
    name_mapping={"acm": "acm", "file": "file", "sds": "sds"},
)
class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrust:
    def __init__(
        self,
        *,
        acm: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcm", typing.Dict[builtins.str, typing.Any]]] = None,
        file: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFile", typing.Dict[builtins.str, typing.Any]]] = None,
        sds: typing.Optional[typing.Union["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSds", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param acm: acm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#acm AppmeshVirtualNode#acm}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        :param sds: sds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#sds AppmeshVirtualNode#sds}
        '''
        if isinstance(acm, dict):
            acm = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcm(**acm)
        if isinstance(file, dict):
            file = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFile(**file)
        if isinstance(sds, dict):
            sds = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSds(**sds)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__902566a25f335d452a4cb5beab0f1427ca21a2423f3744592c1262f0ce3bb150)
            check_type(argname="argument acm", value=acm, expected_type=type_hints["acm"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument sds", value=sds, expected_type=type_hints["sds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if acm is not None:
            self._values["acm"] = acm
        if file is not None:
            self._values["file"] = file
        if sds is not None:
            self._values["sds"] = sds

    @builtins.property
    def acm(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcm"]:
        '''acm block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#acm AppmeshVirtualNode#acm}
        '''
        result = self._values.get("acm")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcm"], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFile"], result)

    @builtins.property
    def sds(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSds"]:
        '''sds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#sds AppmeshVirtualNode#sds}
        '''
        result = self._values.get("sds")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSds"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrust(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcm",
    jsii_struct_bases=[],
    name_mapping={"certificate_authority_arns": "certificateAuthorityArns"},
)
class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcm:
    def __init__(
        self,
        *,
        certificate_authority_arns: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param certificate_authority_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_authority_arns AppmeshVirtualNode#certificate_authority_arns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e471341ada4d946d4bc2d08752d910916e317c294455c7d4a58f90e602dfa70)
            check_type(argname="argument certificate_authority_arns", value=certificate_authority_arns, expected_type=type_hints["certificate_authority_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_authority_arns": certificate_authority_arns,
        }

    @builtins.property
    def certificate_authority_arns(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_authority_arns AppmeshVirtualNode#certificate_authority_arns}.'''
        result = self._values.get("certificate_authority_arns")
        assert result is not None, "Required property 'certificate_authority_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcmOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcmOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad3ba2e86c451e14d52a36b0aecacefcc87d28871a9f9c37dc29ee9629b06118)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityArnsInput")
    def certificate_authority_arns_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "certificateAuthorityArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityArns")
    def certificate_authority_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "certificateAuthorityArns"))

    @certificate_authority_arns.setter
    def certificate_authority_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd4fae775a4c4e9980e95e512ad5e3edac465b9f5effd6db1d0f98c6df05f2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateAuthorityArns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcm]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0cb072c7d7088fbdf555be7efea808af6e1bbad04e22947fb5bc93b425409df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFile",
    jsii_struct_bases=[],
    name_mapping={"certificate_chain": "certificateChain"},
)
class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFile:
    def __init__(self, *, certificate_chain: builtins.str) -> None:
        '''
        :param certificate_chain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_chain AppmeshVirtualNode#certificate_chain}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87020fefaaf68ce26a570fb41ec040d243ba528210743dd54d4cd0106c2ec8dc)
            check_type(argname="argument certificate_chain", value=certificate_chain, expected_type=type_hints["certificate_chain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_chain": certificate_chain,
        }

    @builtins.property
    def certificate_chain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_chain AppmeshVirtualNode#certificate_chain}.'''
        result = self._values.get("certificate_chain")
        assert result is not None, "Required property 'certificate_chain' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10dc30d8a2c34396f37e68e618097a9bce4255c1f04d50e8cd0393c6fc7516be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="certificateChainInput")
    def certificate_chain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateChainInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateChain")
    def certificate_chain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateChain"))

    @certificate_chain.setter
    def certificate_chain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__121de9584e9375fcffa55702785e73a52f0bd917be093af6fea2f573bb0e7d3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateChain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFile]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3839ccd190ed67ef0e7704d85962830e455c2eb914ed21c3740f1da2fe03dacd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db9863588a4a3947b6feb327a22e8e0ae5455d25331cc95b7e1f491b5b34f1bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAcm")
    def put_acm(
        self,
        *,
        certificate_authority_arns: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param certificate_authority_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_authority_arns AppmeshVirtualNode#certificate_authority_arns}.
        '''
        value = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcm(
            certificate_authority_arns=certificate_authority_arns
        )

        return typing.cast(None, jsii.invoke(self, "putAcm", [value]))

    @jsii.member(jsii_name="putFile")
    def put_file(self, *, certificate_chain: builtins.str) -> None:
        '''
        :param certificate_chain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_chain AppmeshVirtualNode#certificate_chain}.
        '''
        value = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFile(
            certificate_chain=certificate_chain
        )

        return typing.cast(None, jsii.invoke(self, "putFile", [value]))

    @jsii.member(jsii_name="putSds")
    def put_sds(self, *, secret_name: builtins.str) -> None:
        '''
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#secret_name AppmeshVirtualNode#secret_name}.
        '''
        value = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSds(
            secret_name=secret_name
        )

        return typing.cast(None, jsii.invoke(self, "putSds", [value]))

    @jsii.member(jsii_name="resetAcm")
    def reset_acm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcm", []))

    @jsii.member(jsii_name="resetFile")
    def reset_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFile", []))

    @jsii.member(jsii_name="resetSds")
    def reset_sds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSds", []))

    @builtins.property
    @jsii.member(jsii_name="acm")
    def acm(
        self,
    ) -> AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcmOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcmOutputReference, jsii.get(self, "acm"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(
        self,
    ) -> AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFileOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="sds")
    def sds(
        self,
    ) -> "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSdsOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSdsOutputReference", jsii.get(self, "sds"))

    @builtins.property
    @jsii.member(jsii_name="acmInput")
    def acm_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcm]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcm], jsii.get(self, "acmInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFile]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFile], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="sdsInput")
    def sds_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSds"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSds"], jsii.get(self, "sdsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrust]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrust], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrust],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a18442cab100a7dff0896835744ee34b778c6023acdaf0c57bb9da7ef1549a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSds",
    jsii_struct_bases=[],
    name_mapping={"secret_name": "secretName"},
)
class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSds:
    def __init__(self, *, secret_name: builtins.str) -> None:
        '''
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#secret_name AppmeshVirtualNode#secret_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32ae7a895ac0787b4fe99fe127a16e863061bf492472f0525a932372908cf2f5)
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_name": secret_name,
        }

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#secret_name AppmeshVirtualNode#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72dab4b57c830efec642b6277d8ea4ca552afb03830c46510224051916fc4d16)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__956690f54bb1a7ba44f0eea89c5deb40d6ceaf3b6041a3056e6cccddf375c663)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSds]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efbeee29f6594b043d3aa7db58a8119c3d8635ab33fd5afe55de63bea7a0b058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecBackendVirtualServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecBackendVirtualServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37fb2e096f7eed12132d9a56c5f0112760305eef60b8b3bb7a868f0fb3856915)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientPolicy")
    def put_client_policy(
        self,
        *,
        tls: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTls, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param tls: tls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tls AppmeshVirtualNode#tls}
        '''
        value = AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicy(tls=tls)

        return typing.cast(None, jsii.invoke(self, "putClientPolicy", [value]))

    @jsii.member(jsii_name="resetClientPolicy")
    def reset_client_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="clientPolicy")
    def client_policy(
        self,
    ) -> AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyOutputReference, jsii.get(self, "clientPolicy"))

    @builtins.property
    @jsii.member(jsii_name="clientPolicyInput")
    def client_policy_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicy]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicy], jsii.get(self, "clientPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualServiceNameInput")
    def virtual_service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualServiceName")
    def virtual_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualServiceName"))

    @virtual_service_name.setter
    def virtual_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e8b1c6580fd4b1fa7517c289a2727bfc2c99efbf9e740f935e4f8a2b76bc427)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendVirtualService]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendVirtualService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab96276caf119bd05f756ff982c777e222b288d50b29ef826695114819d6c178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListener",
    jsii_struct_bases=[],
    name_mapping={
        "port_mapping": "portMapping",
        "connection_pool": "connectionPool",
        "health_check": "healthCheck",
        "outlier_detection": "outlierDetection",
        "timeout": "timeout",
        "tls": "tls",
    },
)
class AppmeshVirtualNodeSpecListener:
    def __init__(
        self,
        *,
        port_mapping: typing.Union["AppmeshVirtualNodeSpecListenerPortMapping", typing.Dict[builtins.str, typing.Any]],
        connection_pool: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerConnectionPool", typing.Dict[builtins.str, typing.Any]]] = None,
        health_check: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        outlier_detection: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerOutlierDetection", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
        tls: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTls", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param port_mapping: port_mapping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#port_mapping AppmeshVirtualNode#port_mapping}
        :param connection_pool: connection_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#connection_pool AppmeshVirtualNode#connection_pool}
        :param health_check: health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#health_check AppmeshVirtualNode#health_check}
        :param outlier_detection: outlier_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#outlier_detection AppmeshVirtualNode#outlier_detection}
        :param timeout: timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#timeout AppmeshVirtualNode#timeout}
        :param tls: tls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tls AppmeshVirtualNode#tls}
        '''
        if isinstance(port_mapping, dict):
            port_mapping = AppmeshVirtualNodeSpecListenerPortMapping(**port_mapping)
        if isinstance(connection_pool, dict):
            connection_pool = AppmeshVirtualNodeSpecListenerConnectionPool(**connection_pool)
        if isinstance(health_check, dict):
            health_check = AppmeshVirtualNodeSpecListenerHealthCheck(**health_check)
        if isinstance(outlier_detection, dict):
            outlier_detection = AppmeshVirtualNodeSpecListenerOutlierDetection(**outlier_detection)
        if isinstance(timeout, dict):
            timeout = AppmeshVirtualNodeSpecListenerTimeout(**timeout)
        if isinstance(tls, dict):
            tls = AppmeshVirtualNodeSpecListenerTls(**tls)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aea8038318bff130d5d658f590a0a37973ccc243c270c91faeeeeca28ce7187)
            check_type(argname="argument port_mapping", value=port_mapping, expected_type=type_hints["port_mapping"])
            check_type(argname="argument connection_pool", value=connection_pool, expected_type=type_hints["connection_pool"])
            check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
            check_type(argname="argument outlier_detection", value=outlier_detection, expected_type=type_hints["outlier_detection"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port_mapping": port_mapping,
        }
        if connection_pool is not None:
            self._values["connection_pool"] = connection_pool
        if health_check is not None:
            self._values["health_check"] = health_check
        if outlier_detection is not None:
            self._values["outlier_detection"] = outlier_detection
        if timeout is not None:
            self._values["timeout"] = timeout
        if tls is not None:
            self._values["tls"] = tls

    @builtins.property
    def port_mapping(self) -> "AppmeshVirtualNodeSpecListenerPortMapping":
        '''port_mapping block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#port_mapping AppmeshVirtualNode#port_mapping}
        '''
        result = self._values.get("port_mapping")
        assert result is not None, "Required property 'port_mapping' is missing"
        return typing.cast("AppmeshVirtualNodeSpecListenerPortMapping", result)

    @builtins.property
    def connection_pool(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerConnectionPool"]:
        '''connection_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#connection_pool AppmeshVirtualNode#connection_pool}
        '''
        result = self._values.get("connection_pool")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerConnectionPool"], result)

    @builtins.property
    def health_check(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerHealthCheck"]:
        '''health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#health_check AppmeshVirtualNode#health_check}
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerHealthCheck"], result)

    @builtins.property
    def outlier_detection(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerOutlierDetection"]:
        '''outlier_detection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#outlier_detection AppmeshVirtualNode#outlier_detection}
        '''
        result = self._values.get("outlier_detection")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerOutlierDetection"], result)

    @builtins.property
    def timeout(self) -> typing.Optional["AppmeshVirtualNodeSpecListenerTimeout"]:
        '''timeout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#timeout AppmeshVirtualNode#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTimeout"], result)

    @builtins.property
    def tls(self) -> typing.Optional["AppmeshVirtualNodeSpecListenerTls"]:
        '''tls block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tls AppmeshVirtualNode#tls}
        '''
        result = self._values.get("tls")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTls"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListener(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerConnectionPool",
    jsii_struct_bases=[],
    name_mapping={"grpc": "grpc", "http": "http", "http2": "http2", "tcp": "tcp"},
)
class AppmeshVirtualNodeSpecListenerConnectionPool:
    def __init__(
        self,
        *,
        grpc: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerConnectionPoolGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshVirtualNodeSpecListenerConnectionPoolHttp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http2: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshVirtualNodeSpecListenerConnectionPoolHttp2", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tcp: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshVirtualNodeSpecListenerConnectionPoolTcp", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#grpc AppmeshVirtualNode#grpc}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#http AppmeshVirtualNode#http}
        :param http2: http2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#http2 AppmeshVirtualNode#http2}
        :param tcp: tcp block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tcp AppmeshVirtualNode#tcp}
        '''
        if isinstance(grpc, dict):
            grpc = AppmeshVirtualNodeSpecListenerConnectionPoolGrpc(**grpc)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ea32c907c44c415ecc019e66bdbea78de97ed87fe938818d232b515fc6fe86)
            check_type(argname="argument grpc", value=grpc, expected_type=type_hints["grpc"])
            check_type(argname="argument http", value=http, expected_type=type_hints["http"])
            check_type(argname="argument http2", value=http2, expected_type=type_hints["http2"])
            check_type(argname="argument tcp", value=tcp, expected_type=type_hints["tcp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if grpc is not None:
            self._values["grpc"] = grpc
        if http is not None:
            self._values["http"] = http
        if http2 is not None:
            self._values["http2"] = http2
        if tcp is not None:
            self._values["tcp"] = tcp

    @builtins.property
    def grpc(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerConnectionPoolGrpc"]:
        '''grpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#grpc AppmeshVirtualNode#grpc}
        '''
        result = self._values.get("grpc")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerConnectionPoolGrpc"], result)

    @builtins.property
    def http(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshVirtualNodeSpecListenerConnectionPoolHttp"]]]:
        '''http block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#http AppmeshVirtualNode#http}
        '''
        result = self._values.get("http")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshVirtualNodeSpecListenerConnectionPoolHttp"]]], result)

    @builtins.property
    def http2(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshVirtualNodeSpecListenerConnectionPoolHttp2"]]]:
        '''http2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#http2 AppmeshVirtualNode#http2}
        '''
        result = self._values.get("http2")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshVirtualNodeSpecListenerConnectionPoolHttp2"]]], result)

    @builtins.property
    def tcp(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshVirtualNodeSpecListenerConnectionPoolTcp"]]]:
        '''tcp block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tcp AppmeshVirtualNode#tcp}
        '''
        result = self._values.get("tcp")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshVirtualNodeSpecListenerConnectionPoolTcp"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerConnectionPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerConnectionPoolGrpc",
    jsii_struct_bases=[],
    name_mapping={"max_requests": "maxRequests"},
)
class AppmeshVirtualNodeSpecListenerConnectionPoolGrpc:
    def __init__(self, *, max_requests: jsii.Number) -> None:
        '''
        :param max_requests: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#max_requests AppmeshVirtualNode#max_requests}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2d614fa081e6102e7eb5137e1ad148c9079759d739808a7faba950beac7980)
            check_type(argname="argument max_requests", value=max_requests, expected_type=type_hints["max_requests"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_requests": max_requests,
        }

    @builtins.property
    def max_requests(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#max_requests AppmeshVirtualNode#max_requests}.'''
        result = self._values.get("max_requests")
        assert result is not None, "Required property 'max_requests' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerConnectionPoolGrpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerConnectionPoolGrpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerConnectionPoolGrpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__917fb3f725aff8daae81da8c6060cd31ba7b7e5403a37b8a5aec320f1ae3a910)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maxRequestsInput")
    def max_requests_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRequestsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRequests")
    def max_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRequests"))

    @max_requests.setter
    def max_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8919047292285f7612f634f9889fbcf9076791f3da868f401b803b9953f279a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerConnectionPoolGrpc]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerConnectionPoolGrpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerConnectionPoolGrpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__951eb92239a0f1d416b32d4da23f2c376dab2f8a4122cd4b48da36aef51ffa19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerConnectionPoolHttp",
    jsii_struct_bases=[],
    name_mapping={
        "max_connections": "maxConnections",
        "max_pending_requests": "maxPendingRequests",
    },
)
class AppmeshVirtualNodeSpecListenerConnectionPoolHttp:
    def __init__(
        self,
        *,
        max_connections: jsii.Number,
        max_pending_requests: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_connections: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#max_connections AppmeshVirtualNode#max_connections}.
        :param max_pending_requests: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#max_pending_requests AppmeshVirtualNode#max_pending_requests}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f34b42558abed1bf46bd1217b972fead89b015a89e308d378cc5768b5d7d61a)
            check_type(argname="argument max_connections", value=max_connections, expected_type=type_hints["max_connections"])
            check_type(argname="argument max_pending_requests", value=max_pending_requests, expected_type=type_hints["max_pending_requests"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_connections": max_connections,
        }
        if max_pending_requests is not None:
            self._values["max_pending_requests"] = max_pending_requests

    @builtins.property
    def max_connections(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#max_connections AppmeshVirtualNode#max_connections}.'''
        result = self._values.get("max_connections")
        assert result is not None, "Required property 'max_connections' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_pending_requests(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#max_pending_requests AppmeshVirtualNode#max_pending_requests}.'''
        result = self._values.get("max_pending_requests")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerConnectionPoolHttp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerConnectionPoolHttp2",
    jsii_struct_bases=[],
    name_mapping={"max_requests": "maxRequests"},
)
class AppmeshVirtualNodeSpecListenerConnectionPoolHttp2:
    def __init__(self, *, max_requests: jsii.Number) -> None:
        '''
        :param max_requests: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#max_requests AppmeshVirtualNode#max_requests}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ba5903882d9fe88fb0a675c700703c36880f574e54bcec0165c890116ad138a)
            check_type(argname="argument max_requests", value=max_requests, expected_type=type_hints["max_requests"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_requests": max_requests,
        }

    @builtins.property
    def max_requests(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#max_requests AppmeshVirtualNode#max_requests}.'''
        result = self._values.get("max_requests")
        assert result is not None, "Required property 'max_requests' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerConnectionPoolHttp2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerConnectionPoolHttp2List(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerConnectionPoolHttp2List",
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
            type_hints = typing.get_type_hints(_typecheckingstub__300bc440b62ffea8b45ece5ee0fc669a38dc06fd9b42b758dbb07e64d09a0bd6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppmeshVirtualNodeSpecListenerConnectionPoolHttp2OutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87fbdf228f4f88e92c9f1ce5e1608bcd9c040e0acef0e770dfb310cef2be6d04)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshVirtualNodeSpecListenerConnectionPoolHttp2OutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdb7f59a195f6c2bad6c887023247917fd136e57d5384240cf71146fde04eeca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fb976d114550cb62a4adffb679197e4bfe93653c8689a006eb91f13ef89735a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__456c3f5a4cf37c85d69ab48f6622dd4e3e040d13ef325a698a67d9a096808433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListenerConnectionPoolHttp2]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListenerConnectionPoolHttp2]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListenerConnectionPoolHttp2]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9c042b5686d09d34894afd72f0e884c013ddef2fd414c822cfd43855a7e4aa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecListenerConnectionPoolHttp2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerConnectionPoolHttp2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__907092f47eecb9e084c3e66bd6371f51bf4b0c695a3d01c8c591c5c6d3a7667b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="maxRequestsInput")
    def max_requests_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRequestsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRequests")
    def max_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRequests"))

    @max_requests.setter
    def max_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d2f740689f1d88f769758db56ef6e3bdb1dcc0b30401ca6d8e7f599d3a8023e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecListenerConnectionPoolHttp2]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecListenerConnectionPoolHttp2]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecListenerConnectionPoolHttp2]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17331c7e129e848abde07a19f595be87c0ad39da98327d32e05563fa690babaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecListenerConnectionPoolHttpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerConnectionPoolHttpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbc5993d9dcd1ac329cf356b9bcae778b5fd4110a0d8d74833a7b552269a06fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppmeshVirtualNodeSpecListenerConnectionPoolHttpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a75527128704c8de14fd264e6f330b371e67af80329cb7ecef2c7bd4580f29)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshVirtualNodeSpecListenerConnectionPoolHttpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eccc261fe0737d88c481274f78debf7f5759022b8ba1b40d4a7ebfeed21733f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cd5748bcf2be6d42a55add58e4c8c478d273d4b502a8f63e82deced0e45b09f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e352145892ef47bd76f9fa1425f0e3691799b2a9820ec66a0240b1463c826fb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListenerConnectionPoolHttp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListenerConnectionPoolHttp]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListenerConnectionPoolHttp]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4234c80159704a370a1d7cdfc5faf97e9267af69c28bd591512310f9fe03392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecListenerConnectionPoolHttpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerConnectionPoolHttpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fec6dcf01169f0574ad664c7e00ccab8d8d84f0e23f87aabcbff96d7642652c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMaxPendingRequests")
    def reset_max_pending_requests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPendingRequests", []))

    @builtins.property
    @jsii.member(jsii_name="maxConnectionsInput")
    def max_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPendingRequestsInput")
    def max_pending_requests_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPendingRequestsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnections")
    def max_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnections"))

    @max_connections.setter
    def max_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f00ecc140d05cd6ea0d38bb5953c4374578979c0197e8cf1583cd62db083fb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPendingRequests")
    def max_pending_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPendingRequests"))

    @max_pending_requests.setter
    def max_pending_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d59fb070c9999a5dab86ce8ac1354bd7efb645dc181b9e4bfc72c629e1ae6dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPendingRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecListenerConnectionPoolHttp]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecListenerConnectionPoolHttp]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecListenerConnectionPoolHttp]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ebba2bb518e77fbe0e107dae5d50d8bef4ddb9d94f3d80774320050078899a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecListenerConnectionPoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerConnectionPoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__415876b3fc51480ae1ab8f078e367af26fee31abaad771cc42a394d44d0b3547)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGrpc")
    def put_grpc(self, *, max_requests: jsii.Number) -> None:
        '''
        :param max_requests: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#max_requests AppmeshVirtualNode#max_requests}.
        '''
        value = AppmeshVirtualNodeSpecListenerConnectionPoolGrpc(
            max_requests=max_requests
        )

        return typing.cast(None, jsii.invoke(self, "putGrpc", [value]))

    @jsii.member(jsii_name="putHttp")
    def put_http(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecListenerConnectionPoolHttp, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9927633eedf112caf459eabe82f7659c19cf64de16cac78eea000e793e2633c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttp", [value]))

    @jsii.member(jsii_name="putHttp2")
    def put_http2(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecListenerConnectionPoolHttp2, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__781e759142de1e3fd2513c3b734eb97d5c3d9b5b1bb999ef18741bcbeaca6657)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttp2", [value]))

    @jsii.member(jsii_name="putTcp")
    def put_tcp(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshVirtualNodeSpecListenerConnectionPoolTcp", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae9cac6da59f29b1bb5b6d27d5315fd2c21da6cc4ad1ef2f20a44492c1d5730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTcp", [value]))

    @jsii.member(jsii_name="resetGrpc")
    def reset_grpc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpc", []))

    @jsii.member(jsii_name="resetHttp")
    def reset_http(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp", []))

    @jsii.member(jsii_name="resetHttp2")
    def reset_http2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp2", []))

    @jsii.member(jsii_name="resetTcp")
    def reset_tcp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcp", []))

    @builtins.property
    @jsii.member(jsii_name="grpc")
    def grpc(self) -> AppmeshVirtualNodeSpecListenerConnectionPoolGrpcOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecListenerConnectionPoolGrpcOutputReference, jsii.get(self, "grpc"))

    @builtins.property
    @jsii.member(jsii_name="http")
    def http(self) -> AppmeshVirtualNodeSpecListenerConnectionPoolHttpList:
        return typing.cast(AppmeshVirtualNodeSpecListenerConnectionPoolHttpList, jsii.get(self, "http"))

    @builtins.property
    @jsii.member(jsii_name="http2")
    def http2(self) -> AppmeshVirtualNodeSpecListenerConnectionPoolHttp2List:
        return typing.cast(AppmeshVirtualNodeSpecListenerConnectionPoolHttp2List, jsii.get(self, "http2"))

    @builtins.property
    @jsii.member(jsii_name="tcp")
    def tcp(self) -> "AppmeshVirtualNodeSpecListenerConnectionPoolTcpList":
        return typing.cast("AppmeshVirtualNodeSpecListenerConnectionPoolTcpList", jsii.get(self, "tcp"))

    @builtins.property
    @jsii.member(jsii_name="grpcInput")
    def grpc_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerConnectionPoolGrpc]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerConnectionPoolGrpc], jsii.get(self, "grpcInput"))

    @builtins.property
    @jsii.member(jsii_name="http2Input")
    def http2_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListenerConnectionPoolHttp2]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListenerConnectionPoolHttp2]]], jsii.get(self, "http2Input"))

    @builtins.property
    @jsii.member(jsii_name="httpInput")
    def http_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListenerConnectionPoolHttp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListenerConnectionPoolHttp]]], jsii.get(self, "httpInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpInput")
    def tcp_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshVirtualNodeSpecListenerConnectionPoolTcp"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshVirtualNodeSpecListenerConnectionPoolTcp"]]], jsii.get(self, "tcpInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerConnectionPool]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerConnectionPool], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerConnectionPool],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cece5e28ee7cebe9b6afb461e8f16cf1a7cf68147f7dcd1a38bcd8a648a488b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerConnectionPoolTcp",
    jsii_struct_bases=[],
    name_mapping={"max_connections": "maxConnections"},
)
class AppmeshVirtualNodeSpecListenerConnectionPoolTcp:
    def __init__(self, *, max_connections: jsii.Number) -> None:
        '''
        :param max_connections: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#max_connections AppmeshVirtualNode#max_connections}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1daabf9db4ed7214bf52ab8d60f32b14a0cfa1f5227326a63e9ad0d425da1e3c)
            check_type(argname="argument max_connections", value=max_connections, expected_type=type_hints["max_connections"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_connections": max_connections,
        }

    @builtins.property
    def max_connections(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#max_connections AppmeshVirtualNode#max_connections}.'''
        result = self._values.get("max_connections")
        assert result is not None, "Required property 'max_connections' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerConnectionPoolTcp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerConnectionPoolTcpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerConnectionPoolTcpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5835ea8c0ab745b4aa8a3fe9841cc775368ca1708afc313e981cda5e3a3ca83f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppmeshVirtualNodeSpecListenerConnectionPoolTcpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72fb8f01bee7a9b072349eb006d91f8a5358d6e9f373e167df1f23fd543345ea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshVirtualNodeSpecListenerConnectionPoolTcpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1096bc9856c0f132a8e73b4cffd2d676df1b5dd77d9f2fa3fb173c02db3a3192)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc29fd206276e628423cc2918033e9c10bc62ee6bf0a6544c9e9b6b1a3d4f774)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a2949ceda5d5155df47b566eaf8b1648aebbe00d9c76ac15ac5e1bb4b882fc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListenerConnectionPoolTcp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListenerConnectionPoolTcp]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListenerConnectionPoolTcp]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dbdc90ef05ef2ad7e92b97cb1c3b296edc23847c6a01d95dab7a7cde62061e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecListenerConnectionPoolTcpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerConnectionPoolTcpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d3efd60247b2223fd09de9b6b1c3438870ea38f63afdabcba329eb79de64e3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="maxConnectionsInput")
    def max_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnections")
    def max_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnections"))

    @max_connections.setter
    def max_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__122a1cd444f30ab87ca4856e1f05f2dd262c574d2f6f7862656d6808ced14668)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecListenerConnectionPoolTcp]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecListenerConnectionPoolTcp]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecListenerConnectionPoolTcp]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a3a2a1e21c6ebeea0400826f9f6607f41b0e2f1f0280d2b9fa5009b33e0b446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerHealthCheck",
    jsii_struct_bases=[],
    name_mapping={
        "healthy_threshold": "healthyThreshold",
        "interval_millis": "intervalMillis",
        "protocol": "protocol",
        "timeout_millis": "timeoutMillis",
        "unhealthy_threshold": "unhealthyThreshold",
        "path": "path",
        "port": "port",
    },
)
class AppmeshVirtualNodeSpecListenerHealthCheck:
    def __init__(
        self,
        *,
        healthy_threshold: jsii.Number,
        interval_millis: jsii.Number,
        protocol: builtins.str,
        timeout_millis: jsii.Number,
        unhealthy_threshold: jsii.Number,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param healthy_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#healthy_threshold AppmeshVirtualNode#healthy_threshold}.
        :param interval_millis: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#interval_millis AppmeshVirtualNode#interval_millis}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#protocol AppmeshVirtualNode#protocol}.
        :param timeout_millis: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#timeout_millis AppmeshVirtualNode#timeout_millis}.
        :param unhealthy_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unhealthy_threshold AppmeshVirtualNode#unhealthy_threshold}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#path AppmeshVirtualNode#path}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#port AppmeshVirtualNode#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d85f643d8d3b5c4563f3fad129a21467cfb050601dfd9612f13469c81b59a91e)
            check_type(argname="argument healthy_threshold", value=healthy_threshold, expected_type=type_hints["healthy_threshold"])
            check_type(argname="argument interval_millis", value=interval_millis, expected_type=type_hints["interval_millis"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument timeout_millis", value=timeout_millis, expected_type=type_hints["timeout_millis"])
            check_type(argname="argument unhealthy_threshold", value=unhealthy_threshold, expected_type=type_hints["unhealthy_threshold"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "healthy_threshold": healthy_threshold,
            "interval_millis": interval_millis,
            "protocol": protocol,
            "timeout_millis": timeout_millis,
            "unhealthy_threshold": unhealthy_threshold,
        }
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def healthy_threshold(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#healthy_threshold AppmeshVirtualNode#healthy_threshold}.'''
        result = self._values.get("healthy_threshold")
        assert result is not None, "Required property 'healthy_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def interval_millis(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#interval_millis AppmeshVirtualNode#interval_millis}.'''
        result = self._values.get("interval_millis")
        assert result is not None, "Required property 'interval_millis' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#protocol AppmeshVirtualNode#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timeout_millis(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#timeout_millis AppmeshVirtualNode#timeout_millis}.'''
        result = self._values.get("timeout_millis")
        assert result is not None, "Required property 'timeout_millis' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def unhealthy_threshold(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unhealthy_threshold AppmeshVirtualNode#unhealthy_threshold}.'''
        result = self._values.get("unhealthy_threshold")
        assert result is not None, "Required property 'unhealthy_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#path AppmeshVirtualNode#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#port AppmeshVirtualNode#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerHealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerHealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerHealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc83897da947fba66ca2bce770c8eee15b0b6add30ae2986463fa7d96fa8401e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="healthyThresholdInput")
    def healthy_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthyThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalMillisInput")
    def interval_millis_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalMillisInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutMillisInput")
    def timeout_millis_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutMillisInput"))

    @builtins.property
    @jsii.member(jsii_name="unhealthyThresholdInput")
    def unhealthy_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "unhealthyThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="healthyThreshold")
    def healthy_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "healthyThreshold"))

    @healthy_threshold.setter
    def healthy_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7acd1c99b728928436e14cfef907f0d540effcc1e4cdb0cbb1d4c542363e7de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthyThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalMillis")
    def interval_millis(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalMillis"))

    @interval_millis.setter
    def interval_millis(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c586e2ab06c2bea6be6dd245ea0395713bb7457498998c111017a4a2a0722b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalMillis", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb73014deb379d3f9dcde455db8dd65b81a2be9bb3918ee32cf680df1ec2da4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9921f60d1d6266c1e1172747ebab5479807f45188ba733eade3c20c71824b6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9b548fad1b683448e07b88b401a7791af48e3d756be57efd36e8e0c8723cff1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutMillis")
    def timeout_millis(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutMillis"))

    @timeout_millis.setter
    def timeout_millis(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09c9742a070b0633178cb7d252a632e2f4f75a385b42b2bafceb3bdd1efb69eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutMillis", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unhealthyThreshold")
    def unhealthy_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unhealthyThreshold"))

    @unhealthy_threshold.setter
    def unhealthy_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70addfdbd6c473a2e34649fc14c016211856cbf588344295d1252f804ebf4449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unhealthyThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerHealthCheck]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerHealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerHealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90de23ec2a87403b95095ac9999ae9130d815b8264822aa3cbcf51f24dc35615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecListenerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3e75df8ddb205a18005405f1e71b4637caf6845e18fecdda8ce59f5f6937986)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppmeshVirtualNodeSpecListenerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42b765d692159cadcb49f8bcebfcada0c48dcf449c5ef8982d7055f16794a2b5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshVirtualNodeSpecListenerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9208d189a894751a2f8743902d67c7daa577cfeb9a108db3b7006ba46c01dfb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91ccd5b2844e929079474dea8438fcd5b40acea6c43667bb6cc980349047db10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7966bb181d7d7dc923e4b302ed19f0aeeb8030b157e97bf8cd6547f02de19218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListener]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListener]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListener]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__442d2e2d5ae3ffa9b92d61c7c90f00cc074c54d26afe7ccc020a056bd4c54368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerOutlierDetection",
    jsii_struct_bases=[],
    name_mapping={
        "base_ejection_duration": "baseEjectionDuration",
        "interval": "interval",
        "max_ejection_percent": "maxEjectionPercent",
        "max_server_errors": "maxServerErrors",
    },
)
class AppmeshVirtualNodeSpecListenerOutlierDetection:
    def __init__(
        self,
        *,
        base_ejection_duration: typing.Union["AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDuration", typing.Dict[builtins.str, typing.Any]],
        interval: typing.Union["AppmeshVirtualNodeSpecListenerOutlierDetectionInterval", typing.Dict[builtins.str, typing.Any]],
        max_ejection_percent: jsii.Number,
        max_server_errors: jsii.Number,
    ) -> None:
        '''
        :param base_ejection_duration: base_ejection_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#base_ejection_duration AppmeshVirtualNode#base_ejection_duration}
        :param interval: interval block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#interval AppmeshVirtualNode#interval}
        :param max_ejection_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#max_ejection_percent AppmeshVirtualNode#max_ejection_percent}.
        :param max_server_errors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#max_server_errors AppmeshVirtualNode#max_server_errors}.
        '''
        if isinstance(base_ejection_duration, dict):
            base_ejection_duration = AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDuration(**base_ejection_duration)
        if isinstance(interval, dict):
            interval = AppmeshVirtualNodeSpecListenerOutlierDetectionInterval(**interval)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__690e93ef7bd28ae3e60f0ab649c2ab9b2b900792bf1db31c987ca9edd2877202)
            check_type(argname="argument base_ejection_duration", value=base_ejection_duration, expected_type=type_hints["base_ejection_duration"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument max_ejection_percent", value=max_ejection_percent, expected_type=type_hints["max_ejection_percent"])
            check_type(argname="argument max_server_errors", value=max_server_errors, expected_type=type_hints["max_server_errors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_ejection_duration": base_ejection_duration,
            "interval": interval,
            "max_ejection_percent": max_ejection_percent,
            "max_server_errors": max_server_errors,
        }

    @builtins.property
    def base_ejection_duration(
        self,
    ) -> "AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDuration":
        '''base_ejection_duration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#base_ejection_duration AppmeshVirtualNode#base_ejection_duration}
        '''
        result = self._values.get("base_ejection_duration")
        assert result is not None, "Required property 'base_ejection_duration' is missing"
        return typing.cast("AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDuration", result)

    @builtins.property
    def interval(self) -> "AppmeshVirtualNodeSpecListenerOutlierDetectionInterval":
        '''interval block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#interval AppmeshVirtualNode#interval}
        '''
        result = self._values.get("interval")
        assert result is not None, "Required property 'interval' is missing"
        return typing.cast("AppmeshVirtualNodeSpecListenerOutlierDetectionInterval", result)

    @builtins.property
    def max_ejection_percent(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#max_ejection_percent AppmeshVirtualNode#max_ejection_percent}.'''
        result = self._values.get("max_ejection_percent")
        assert result is not None, "Required property 'max_ejection_percent' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_server_errors(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#max_server_errors AppmeshVirtualNode#max_server_errors}.'''
        result = self._values.get("max_server_errors")
        assert result is not None, "Required property 'max_server_errors' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerOutlierDetection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDuration",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDuration:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f802836bc379bfd9b425ea3e35685362edf326b7b5e6131cbc91f25b294b9e28)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9ead37a9a8a6a011f062ee91f60673320b3bccc38229a709d1c717b808aa041)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f89ebc62f4c60e047189e7570b28b4db96c5f738ad019c17783e93f1fa3f74e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ca3f79215e97f94448e1e801b4cb5a62b56e56d1a8d2fa86fa401610da0f00c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDuration]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27ec5aa8b77fa3776c5028b067be6eeadacc8e7bb4e2788f8bd27c441cf8b7f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerOutlierDetectionInterval",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshVirtualNodeSpecListenerOutlierDetectionInterval:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__606ec4b20c12614d7bc452e3554b3ffe7c6d3a164285beacb533e8cef9721876)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerOutlierDetectionInterval(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerOutlierDetectionIntervalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerOutlierDetectionIntervalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16547425888639a057f8223a558aa7a7393ee0196be9925cd03a579dee30d6f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccf716140f7279c41759bf4c06032bb7ec8f1bf1f10b42cd3a404e0a73dc4af4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f624742ce97fc68f47196c74f0f745cc29002a8d8a0ca49522a53a53f6c83188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerOutlierDetectionInterval]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerOutlierDetectionInterval], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerOutlierDetectionInterval],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68dbc9b097ee50f9ebdc8656243445a8798ea9381a0c5faae418ab5d7f2b7330)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecListenerOutlierDetectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerOutlierDetectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d661e5f26d8425ae1e58b9e56ad93fdc5a9d678ab7bd128cbb35a27d89aa3f2f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBaseEjectionDuration")
    def put_base_ejection_duration(
        self,
        *,
        unit: builtins.str,
        value: jsii.Number,
    ) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        value_ = AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDuration(
            unit=unit, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putBaseEjectionDuration", [value_]))

    @jsii.member(jsii_name="putInterval")
    def put_interval(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        value_ = AppmeshVirtualNodeSpecListenerOutlierDetectionInterval(
            unit=unit, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putInterval", [value_]))

    @builtins.property
    @jsii.member(jsii_name="baseEjectionDuration")
    def base_ejection_duration(
        self,
    ) -> AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDurationOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDurationOutputReference, jsii.get(self, "baseEjectionDuration"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(
        self,
    ) -> AppmeshVirtualNodeSpecListenerOutlierDetectionIntervalOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecListenerOutlierDetectionIntervalOutputReference, jsii.get(self, "interval"))

    @builtins.property
    @jsii.member(jsii_name="baseEjectionDurationInput")
    def base_ejection_duration_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDuration]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDuration], jsii.get(self, "baseEjectionDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerOutlierDetectionInterval]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerOutlierDetectionInterval], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="maxEjectionPercentInput")
    def max_ejection_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxEjectionPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="maxServerErrorsInput")
    def max_server_errors_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxServerErrorsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxEjectionPercent")
    def max_ejection_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxEjectionPercent"))

    @max_ejection_percent.setter
    def max_ejection_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e236bb669e860db01a485e7e56f8044de29939afa816167144f16a8f4a8e8a49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxEjectionPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxServerErrors")
    def max_server_errors(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxServerErrors"))

    @max_server_errors.setter
    def max_server_errors(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4e34bc5de4297ca4d3290ea80a52ae80f4d7f715028f53bb2c9f931f4398b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxServerErrors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerOutlierDetection]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerOutlierDetection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerOutlierDetection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30d1428fc674f010bb81e1f81eeb13c89965878fddd4fcdfd35bc901215ddfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecListenerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd55217b93e40911d1ecda11d71c59dc1d70980217014e9e7994c50947d8f32c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putConnectionPool")
    def put_connection_pool(
        self,
        *,
        grpc: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerConnectionPoolGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
        http: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecListenerConnectionPoolHttp, typing.Dict[builtins.str, typing.Any]]]]] = None,
        http2: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecListenerConnectionPoolHttp2, typing.Dict[builtins.str, typing.Any]]]]] = None,
        tcp: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecListenerConnectionPoolTcp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#grpc AppmeshVirtualNode#grpc}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#http AppmeshVirtualNode#http}
        :param http2: http2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#http2 AppmeshVirtualNode#http2}
        :param tcp: tcp block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tcp AppmeshVirtualNode#tcp}
        '''
        value = AppmeshVirtualNodeSpecListenerConnectionPool(
            grpc=grpc, http=http, http2=http2, tcp=tcp
        )

        return typing.cast(None, jsii.invoke(self, "putConnectionPool", [value]))

    @jsii.member(jsii_name="putHealthCheck")
    def put_health_check(
        self,
        *,
        healthy_threshold: jsii.Number,
        interval_millis: jsii.Number,
        protocol: builtins.str,
        timeout_millis: jsii.Number,
        unhealthy_threshold: jsii.Number,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param healthy_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#healthy_threshold AppmeshVirtualNode#healthy_threshold}.
        :param interval_millis: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#interval_millis AppmeshVirtualNode#interval_millis}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#protocol AppmeshVirtualNode#protocol}.
        :param timeout_millis: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#timeout_millis AppmeshVirtualNode#timeout_millis}.
        :param unhealthy_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unhealthy_threshold AppmeshVirtualNode#unhealthy_threshold}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#path AppmeshVirtualNode#path}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#port AppmeshVirtualNode#port}.
        '''
        value = AppmeshVirtualNodeSpecListenerHealthCheck(
            healthy_threshold=healthy_threshold,
            interval_millis=interval_millis,
            protocol=protocol,
            timeout_millis=timeout_millis,
            unhealthy_threshold=unhealthy_threshold,
            path=path,
            port=port,
        )

        return typing.cast(None, jsii.invoke(self, "putHealthCheck", [value]))

    @jsii.member(jsii_name="putOutlierDetection")
    def put_outlier_detection(
        self,
        *,
        base_ejection_duration: typing.Union[AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDuration, typing.Dict[builtins.str, typing.Any]],
        interval: typing.Union[AppmeshVirtualNodeSpecListenerOutlierDetectionInterval, typing.Dict[builtins.str, typing.Any]],
        max_ejection_percent: jsii.Number,
        max_server_errors: jsii.Number,
    ) -> None:
        '''
        :param base_ejection_duration: base_ejection_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#base_ejection_duration AppmeshVirtualNode#base_ejection_duration}
        :param interval: interval block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#interval AppmeshVirtualNode#interval}
        :param max_ejection_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#max_ejection_percent AppmeshVirtualNode#max_ejection_percent}.
        :param max_server_errors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#max_server_errors AppmeshVirtualNode#max_server_errors}.
        '''
        value = AppmeshVirtualNodeSpecListenerOutlierDetection(
            base_ejection_duration=base_ejection_duration,
            interval=interval,
            max_ejection_percent=max_ejection_percent,
            max_server_errors=max_server_errors,
        )

        return typing.cast(None, jsii.invoke(self, "putOutlierDetection", [value]))

    @jsii.member(jsii_name="putPortMapping")
    def put_port_mapping(self, *, port: jsii.Number, protocol: builtins.str) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#port AppmeshVirtualNode#port}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#protocol AppmeshVirtualNode#protocol}.
        '''
        value = AppmeshVirtualNodeSpecListenerPortMapping(port=port, protocol=protocol)

        return typing.cast(None, jsii.invoke(self, "putPortMapping", [value]))

    @jsii.member(jsii_name="putTimeout")
    def put_timeout(
        self,
        *,
        grpc: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTimeoutGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTimeoutHttp", typing.Dict[builtins.str, typing.Any]]] = None,
        http2: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTimeoutHttp2", typing.Dict[builtins.str, typing.Any]]] = None,
        tcp: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTimeoutTcp", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#grpc AppmeshVirtualNode#grpc}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#http AppmeshVirtualNode#http}
        :param http2: http2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#http2 AppmeshVirtualNode#http2}
        :param tcp: tcp block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tcp AppmeshVirtualNode#tcp}
        '''
        value = AppmeshVirtualNodeSpecListenerTimeout(
            grpc=grpc, http=http, http2=http2, tcp=tcp
        )

        return typing.cast(None, jsii.invoke(self, "putTimeout", [value]))

    @jsii.member(jsii_name="putTls")
    def put_tls(
        self,
        *,
        certificate: typing.Union["AppmeshVirtualNodeSpecListenerTlsCertificate", typing.Dict[builtins.str, typing.Any]],
        mode: builtins.str,
        validation: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTlsValidation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate AppmeshVirtualNode#certificate}
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#mode AppmeshVirtualNode#mode}.
        :param validation: validation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#validation AppmeshVirtualNode#validation}
        '''
        value = AppmeshVirtualNodeSpecListenerTls(
            certificate=certificate, mode=mode, validation=validation
        )

        return typing.cast(None, jsii.invoke(self, "putTls", [value]))

    @jsii.member(jsii_name="resetConnectionPool")
    def reset_connection_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionPool", []))

    @jsii.member(jsii_name="resetHealthCheck")
    def reset_health_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheck", []))

    @jsii.member(jsii_name="resetOutlierDetection")
    def reset_outlier_detection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutlierDetection", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetTls")
    def reset_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTls", []))

    @builtins.property
    @jsii.member(jsii_name="connectionPool")
    def connection_pool(
        self,
    ) -> AppmeshVirtualNodeSpecListenerConnectionPoolOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecListenerConnectionPoolOutputReference, jsii.get(self, "connectionPool"))

    @builtins.property
    @jsii.member(jsii_name="healthCheck")
    def health_check(self) -> AppmeshVirtualNodeSpecListenerHealthCheckOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecListenerHealthCheckOutputReference, jsii.get(self, "healthCheck"))

    @builtins.property
    @jsii.member(jsii_name="outlierDetection")
    def outlier_detection(
        self,
    ) -> AppmeshVirtualNodeSpecListenerOutlierDetectionOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecListenerOutlierDetectionOutputReference, jsii.get(self, "outlierDetection"))

    @builtins.property
    @jsii.member(jsii_name="portMapping")
    def port_mapping(
        self,
    ) -> "AppmeshVirtualNodeSpecListenerPortMappingOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecListenerPortMappingOutputReference", jsii.get(self, "portMapping"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> "AppmeshVirtualNodeSpecListenerTimeoutOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecListenerTimeoutOutputReference", jsii.get(self, "timeout"))

    @builtins.property
    @jsii.member(jsii_name="tls")
    def tls(self) -> "AppmeshVirtualNodeSpecListenerTlsOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecListenerTlsOutputReference", jsii.get(self, "tls"))

    @builtins.property
    @jsii.member(jsii_name="connectionPoolInput")
    def connection_pool_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerConnectionPool]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerConnectionPool], jsii.get(self, "connectionPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckInput")
    def health_check_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerHealthCheck]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerHealthCheck], jsii.get(self, "healthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="outlierDetectionInput")
    def outlier_detection_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerOutlierDetection]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerOutlierDetection], jsii.get(self, "outlierDetectionInput"))

    @builtins.property
    @jsii.member(jsii_name="portMappingInput")
    def port_mapping_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerPortMapping"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerPortMapping"], jsii.get(self, "portMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional["AppmeshVirtualNodeSpecListenerTimeout"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTimeout"], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsInput")
    def tls_input(self) -> typing.Optional["AppmeshVirtualNodeSpecListenerTls"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTls"], jsii.get(self, "tlsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecListener]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecListener]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecListener]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7619ef86bb0ddb51984c6ebc9badfb2ebc8cec28727d05be496f06fd9822c0f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerPortMapping",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "protocol": "protocol"},
)
class AppmeshVirtualNodeSpecListenerPortMapping:
    def __init__(self, *, port: jsii.Number, protocol: builtins.str) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#port AppmeshVirtualNode#port}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#protocol AppmeshVirtualNode#protocol}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6c1c21670687f0f070a441165738cd45499f4b3d09912695d30bf79ad5b0508)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "protocol": protocol,
        }

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#port AppmeshVirtualNode#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#protocol AppmeshVirtualNode#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerPortMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerPortMappingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerPortMappingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c77257dc7c528076c91f1092713d792faa9d0ae7fbab190c080cacd9db2a95a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b22de44f453447d36e295b5757a218b0ea2618d846420d7e08d3de6aaf0ce35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be6dc8742326d85e251bab26d255b693e247596d1b8e65f508fb3e8718cfc72b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerPortMapping]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerPortMapping], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerPortMapping],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b104cf7648b7fb7a29c82a82c5d219d542981444d98db4e2a86690450bb3ff1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeout",
    jsii_struct_bases=[],
    name_mapping={"grpc": "grpc", "http": "http", "http2": "http2", "tcp": "tcp"},
)
class AppmeshVirtualNodeSpecListenerTimeout:
    def __init__(
        self,
        *,
        grpc: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTimeoutGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTimeoutHttp", typing.Dict[builtins.str, typing.Any]]] = None,
        http2: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTimeoutHttp2", typing.Dict[builtins.str, typing.Any]]] = None,
        tcp: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTimeoutTcp", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#grpc AppmeshVirtualNode#grpc}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#http AppmeshVirtualNode#http}
        :param http2: http2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#http2 AppmeshVirtualNode#http2}
        :param tcp: tcp block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tcp AppmeshVirtualNode#tcp}
        '''
        if isinstance(grpc, dict):
            grpc = AppmeshVirtualNodeSpecListenerTimeoutGrpc(**grpc)
        if isinstance(http, dict):
            http = AppmeshVirtualNodeSpecListenerTimeoutHttp(**http)
        if isinstance(http2, dict):
            http2 = AppmeshVirtualNodeSpecListenerTimeoutHttp2(**http2)
        if isinstance(tcp, dict):
            tcp = AppmeshVirtualNodeSpecListenerTimeoutTcp(**tcp)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__707a95db1e3acdd56aff29deb72e18760e0e36c6427ca80d3e27a07372cbd8cb)
            check_type(argname="argument grpc", value=grpc, expected_type=type_hints["grpc"])
            check_type(argname="argument http", value=http, expected_type=type_hints["http"])
            check_type(argname="argument http2", value=http2, expected_type=type_hints["http2"])
            check_type(argname="argument tcp", value=tcp, expected_type=type_hints["tcp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if grpc is not None:
            self._values["grpc"] = grpc
        if http is not None:
            self._values["http"] = http
        if http2 is not None:
            self._values["http2"] = http2
        if tcp is not None:
            self._values["tcp"] = tcp

    @builtins.property
    def grpc(self) -> typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutGrpc"]:
        '''grpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#grpc AppmeshVirtualNode#grpc}
        '''
        result = self._values.get("grpc")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutGrpc"], result)

    @builtins.property
    def http(self) -> typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutHttp"]:
        '''http block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#http AppmeshVirtualNode#http}
        '''
        result = self._values.get("http")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutHttp"], result)

    @builtins.property
    def http2(self) -> typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutHttp2"]:
        '''http2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#http2 AppmeshVirtualNode#http2}
        '''
        result = self._values.get("http2")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutHttp2"], result)

    @builtins.property
    def tcp(self) -> typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutTcp"]:
        '''tcp block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#tcp AppmeshVirtualNode#tcp}
        '''
        result = self._values.get("tcp")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutTcp"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutGrpc",
    jsii_struct_bases=[],
    name_mapping={"idle": "idle", "per_request": "perRequest"},
)
class AppmeshVirtualNodeSpecListenerTimeoutGrpc:
    def __init__(
        self,
        *,
        idle: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTimeoutGrpcIdle", typing.Dict[builtins.str, typing.Any]]] = None,
        per_request: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param idle: idle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#idle AppmeshVirtualNode#idle}
        :param per_request: per_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#per_request AppmeshVirtualNode#per_request}
        '''
        if isinstance(idle, dict):
            idle = AppmeshVirtualNodeSpecListenerTimeoutGrpcIdle(**idle)
        if isinstance(per_request, dict):
            per_request = AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequest(**per_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5010307f3157802a5b1a459151324f99d4ebca3a8c54fb87e024072838047086)
            check_type(argname="argument idle", value=idle, expected_type=type_hints["idle"])
            check_type(argname="argument per_request", value=per_request, expected_type=type_hints["per_request"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if idle is not None:
            self._values["idle"] = idle
        if per_request is not None:
            self._values["per_request"] = per_request

    @builtins.property
    def idle(self) -> typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutGrpcIdle"]:
        '''idle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#idle AppmeshVirtualNode#idle}
        '''
        result = self._values.get("idle")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutGrpcIdle"], result)

    @builtins.property
    def per_request(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequest"]:
        '''per_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#per_request AppmeshVirtualNode#per_request}
        '''
        result = self._values.get("per_request")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequest"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTimeoutGrpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutGrpcIdle",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshVirtualNodeSpecListenerTimeoutGrpcIdle:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ebb1815705321677556f7bd18a92416c07efb7f4e3798c4e3864de0439bec5)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTimeoutGrpcIdle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerTimeoutGrpcIdleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutGrpcIdleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68979f9e310de626f542e4879829255d1cef3783a3e8c92d18b828fba6993970)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ec0dd9a7da54ec48e9e1c103b4fc6bbccea5681745c98c34268d88270fdfd24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__992676e144eedb5e45249f40440cea4764eef22c8e3175fa9088c8bb8de306b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutGrpcIdle]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutGrpcIdle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutGrpcIdle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__174e7e09c9477093e242cc4aaf31c4e385f33cee56a3fa15c143be65f4225664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecListenerTimeoutGrpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutGrpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47acb1cb0095eee4643fd6126194ef644e550fc79f38225c5d5f5e96e862ec31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIdle")
    def put_idle(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        value_ = AppmeshVirtualNodeSpecListenerTimeoutGrpcIdle(unit=unit, value=value)

        return typing.cast(None, jsii.invoke(self, "putIdle", [value_]))

    @jsii.member(jsii_name="putPerRequest")
    def put_per_request(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        value_ = AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequest(
            unit=unit, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putPerRequest", [value_]))

    @jsii.member(jsii_name="resetIdle")
    def reset_idle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdle", []))

    @jsii.member(jsii_name="resetPerRequest")
    def reset_per_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerRequest", []))

    @builtins.property
    @jsii.member(jsii_name="idle")
    def idle(self) -> AppmeshVirtualNodeSpecListenerTimeoutGrpcIdleOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecListenerTimeoutGrpcIdleOutputReference, jsii.get(self, "idle"))

    @builtins.property
    @jsii.member(jsii_name="perRequest")
    def per_request(
        self,
    ) -> "AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequestOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequestOutputReference", jsii.get(self, "perRequest"))

    @builtins.property
    @jsii.member(jsii_name="idleInput")
    def idle_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutGrpcIdle]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutGrpcIdle], jsii.get(self, "idleInput"))

    @builtins.property
    @jsii.member(jsii_name="perRequestInput")
    def per_request_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequest"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequest"], jsii.get(self, "perRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutGrpc]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutGrpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutGrpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a430edceb53a611b2495696e948a04c32d2debb54312d4139fb7f1269f51d28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequest",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequest:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13dc0c135eb1f47ef5a791fc98e26d4df5c28b6d80818d1c27fe24e2991ec451)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0320183d1b8cc5abe0841644492fea4cf0aa166052e0d750168b38c57ace8a5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77bbde38e2eb0bf85010e3227e482c31f1f498dff73218925ab353ce3c80ae55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d8a9840f81b9452b155ef20fbdf5bd854755faeccd6836e65867be67aa854d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequest]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__513bfbbb87665b64fb806c1ced08d93663bfcf67343ec67b1c5ea771b8780e02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutHttp",
    jsii_struct_bases=[],
    name_mapping={"idle": "idle", "per_request": "perRequest"},
)
class AppmeshVirtualNodeSpecListenerTimeoutHttp:
    def __init__(
        self,
        *,
        idle: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTimeoutHttpIdle", typing.Dict[builtins.str, typing.Any]]] = None,
        per_request: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param idle: idle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#idle AppmeshVirtualNode#idle}
        :param per_request: per_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#per_request AppmeshVirtualNode#per_request}
        '''
        if isinstance(idle, dict):
            idle = AppmeshVirtualNodeSpecListenerTimeoutHttpIdle(**idle)
        if isinstance(per_request, dict):
            per_request = AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequest(**per_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__601839862576df9110eea01502746d98b6a9df02c4ea524d8ea00e0f50723850)
            check_type(argname="argument idle", value=idle, expected_type=type_hints["idle"])
            check_type(argname="argument per_request", value=per_request, expected_type=type_hints["per_request"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if idle is not None:
            self._values["idle"] = idle
        if per_request is not None:
            self._values["per_request"] = per_request

    @builtins.property
    def idle(self) -> typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutHttpIdle"]:
        '''idle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#idle AppmeshVirtualNode#idle}
        '''
        result = self._values.get("idle")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutHttpIdle"], result)

    @builtins.property
    def per_request(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequest"]:
        '''per_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#per_request AppmeshVirtualNode#per_request}
        '''
        result = self._values.get("per_request")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequest"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTimeoutHttp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutHttp2",
    jsii_struct_bases=[],
    name_mapping={"idle": "idle", "per_request": "perRequest"},
)
class AppmeshVirtualNodeSpecListenerTimeoutHttp2:
    def __init__(
        self,
        *,
        idle: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTimeoutHttp2Idle", typing.Dict[builtins.str, typing.Any]]] = None,
        per_request: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param idle: idle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#idle AppmeshVirtualNode#idle}
        :param per_request: per_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#per_request AppmeshVirtualNode#per_request}
        '''
        if isinstance(idle, dict):
            idle = AppmeshVirtualNodeSpecListenerTimeoutHttp2Idle(**idle)
        if isinstance(per_request, dict):
            per_request = AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequest(**per_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5c5a575035359b65c266bcde9f1d9c0209aca73f40eef7716568d24d208a74d)
            check_type(argname="argument idle", value=idle, expected_type=type_hints["idle"])
            check_type(argname="argument per_request", value=per_request, expected_type=type_hints["per_request"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if idle is not None:
            self._values["idle"] = idle
        if per_request is not None:
            self._values["per_request"] = per_request

    @builtins.property
    def idle(self) -> typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutHttp2Idle"]:
        '''idle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#idle AppmeshVirtualNode#idle}
        '''
        result = self._values.get("idle")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutHttp2Idle"], result)

    @builtins.property
    def per_request(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequest"]:
        '''per_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#per_request AppmeshVirtualNode#per_request}
        '''
        result = self._values.get("per_request")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequest"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTimeoutHttp2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutHttp2Idle",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshVirtualNodeSpecListenerTimeoutHttp2Idle:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30476edec9a9ad78f6e0746b78e07810362346ced0f10e341a118b375f61466c)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTimeoutHttp2Idle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerTimeoutHttp2IdleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutHttp2IdleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f64f2d002ccf274db0f13068384f1d13957f34c48e28927c59867e6550e5f685)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fef0f31e3917dcf9bdc9d0ac08dad97da596725b797a6183cf8cfe36bfc02e9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a83c22e49d297f4d2be6f54916587f17a812b118ab2f58a804ee8e71b18f407a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp2Idle]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp2Idle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp2Idle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac15d1c3ed0d8fd8cb22d5242a1f92776cd4f9cfeed7f6a799eaffd00c36b1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecListenerTimeoutHttp2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutHttp2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__041f4efc8991afb2c8bbb7da16b2326ab7f8575f641d57ac2156b05370b6f46b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIdle")
    def put_idle(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        value_ = AppmeshVirtualNodeSpecListenerTimeoutHttp2Idle(unit=unit, value=value)

        return typing.cast(None, jsii.invoke(self, "putIdle", [value_]))

    @jsii.member(jsii_name="putPerRequest")
    def put_per_request(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        value_ = AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequest(
            unit=unit, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putPerRequest", [value_]))

    @jsii.member(jsii_name="resetIdle")
    def reset_idle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdle", []))

    @jsii.member(jsii_name="resetPerRequest")
    def reset_per_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerRequest", []))

    @builtins.property
    @jsii.member(jsii_name="idle")
    def idle(self) -> AppmeshVirtualNodeSpecListenerTimeoutHttp2IdleOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecListenerTimeoutHttp2IdleOutputReference, jsii.get(self, "idle"))

    @builtins.property
    @jsii.member(jsii_name="perRequest")
    def per_request(
        self,
    ) -> "AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequestOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequestOutputReference", jsii.get(self, "perRequest"))

    @builtins.property
    @jsii.member(jsii_name="idleInput")
    def idle_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp2Idle]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp2Idle], jsii.get(self, "idleInput"))

    @builtins.property
    @jsii.member(jsii_name="perRequestInput")
    def per_request_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequest"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequest"], jsii.get(self, "perRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp2]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d742bd1e52273c6052834d63f1f26e076cdf09f06c2d0e708b47dbf2f70560d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequest",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequest:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee78dffe70fbe3a5a52a6777677d1dd254ca1404adfa5ece5df14288a98bbcf1)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18bdb8561d417fd6faf74afde077d8c76acbdc5e861fd95e5932274b1095e8a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ec66165dd3782a49d680edd1af4f3e97feb5e631dd7ac91567e6e3e011be3b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8798140b1c0cf9986f23ac10b953ae1b7819e1d2c28cd4a98d5e089ef78d5a57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequest]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f814b8cad6ffdb08a9da52ed1ddcbcf54a8011a509709afa8a7d3a89e0bcf389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutHttpIdle",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshVirtualNodeSpecListenerTimeoutHttpIdle:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c657ee4dde23aad2d9fd5c2e28eb505ed40e55872093e6024fdcfa69efba55f)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTimeoutHttpIdle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerTimeoutHttpIdleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutHttpIdleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24c13424b42a248eec2268cbfae0b0da69215f1ed551cdbdf618d08a86528a87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58cac95dfd8e29de08d5d080350e64a3b4dfd8d2d6e7b3e1f3ed925a4e30087f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b243303a170e632aadd3be8aa4827501ceff56c0ce50f7b0a043eb20a09f1b29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttpIdle]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttpIdle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttpIdle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6360349cec12b28e78535887b53a154ae6771dae66ceb76f93bf2d52254e13a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecListenerTimeoutHttpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutHttpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bb6d02002fc2418b0f5c123cbdf8096519cef88f88987eed4cdc531004e26cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIdle")
    def put_idle(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        value_ = AppmeshVirtualNodeSpecListenerTimeoutHttpIdle(unit=unit, value=value)

        return typing.cast(None, jsii.invoke(self, "putIdle", [value_]))

    @jsii.member(jsii_name="putPerRequest")
    def put_per_request(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        value_ = AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequest(
            unit=unit, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putPerRequest", [value_]))

    @jsii.member(jsii_name="resetIdle")
    def reset_idle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdle", []))

    @jsii.member(jsii_name="resetPerRequest")
    def reset_per_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerRequest", []))

    @builtins.property
    @jsii.member(jsii_name="idle")
    def idle(self) -> AppmeshVirtualNodeSpecListenerTimeoutHttpIdleOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecListenerTimeoutHttpIdleOutputReference, jsii.get(self, "idle"))

    @builtins.property
    @jsii.member(jsii_name="perRequest")
    def per_request(
        self,
    ) -> "AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequestOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequestOutputReference", jsii.get(self, "perRequest"))

    @builtins.property
    @jsii.member(jsii_name="idleInput")
    def idle_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttpIdle]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttpIdle], jsii.get(self, "idleInput"))

    @builtins.property
    @jsii.member(jsii_name="perRequestInput")
    def per_request_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequest"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequest"], jsii.get(self, "perRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9d62a69e2ba32eca35d9ee3e864ed47384b6ec69153b7900a9396738ebc65b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequest",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequest:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d2c15b1b093bd7f4b0ec55b6dc6dcb42dbdfe530de4f2b2c55f856a641c02cc)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50fe3c9e47e98b087efe2064c864f4f598b8018eed314bbe662cccb42d2c0943)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff714090fa8fd9e95d80003623a333ded332ccaeeb130fd106d0fad0f89b06bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b0131a2730ed9a05fb417553d1ac62ffcef6bd45e4449fc86d88162fe396b9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequest]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6816e40befc4d7c7203a300d63c947fa070bd71d887ec70dd913f3a32230ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecListenerTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc1817705d9c341502beb77690d845d7a546b18bc5eaaa70a218be99841e5900)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGrpc")
    def put_grpc(
        self,
        *,
        idle: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTimeoutGrpcIdle, typing.Dict[builtins.str, typing.Any]]] = None,
        per_request: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param idle: idle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#idle AppmeshVirtualNode#idle}
        :param per_request: per_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#per_request AppmeshVirtualNode#per_request}
        '''
        value = AppmeshVirtualNodeSpecListenerTimeoutGrpc(
            idle=idle, per_request=per_request
        )

        return typing.cast(None, jsii.invoke(self, "putGrpc", [value]))

    @jsii.member(jsii_name="putHttp")
    def put_http(
        self,
        *,
        idle: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTimeoutHttpIdle, typing.Dict[builtins.str, typing.Any]]] = None,
        per_request: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param idle: idle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#idle AppmeshVirtualNode#idle}
        :param per_request: per_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#per_request AppmeshVirtualNode#per_request}
        '''
        value = AppmeshVirtualNodeSpecListenerTimeoutHttp(
            idle=idle, per_request=per_request
        )

        return typing.cast(None, jsii.invoke(self, "putHttp", [value]))

    @jsii.member(jsii_name="putHttp2")
    def put_http2(
        self,
        *,
        idle: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTimeoutHttp2Idle, typing.Dict[builtins.str, typing.Any]]] = None,
        per_request: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param idle: idle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#idle AppmeshVirtualNode#idle}
        :param per_request: per_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#per_request AppmeshVirtualNode#per_request}
        '''
        value = AppmeshVirtualNodeSpecListenerTimeoutHttp2(
            idle=idle, per_request=per_request
        )

        return typing.cast(None, jsii.invoke(self, "putHttp2", [value]))

    @jsii.member(jsii_name="putTcp")
    def put_tcp(
        self,
        *,
        idle: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTimeoutTcpIdle", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param idle: idle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#idle AppmeshVirtualNode#idle}
        '''
        value = AppmeshVirtualNodeSpecListenerTimeoutTcp(idle=idle)

        return typing.cast(None, jsii.invoke(self, "putTcp", [value]))

    @jsii.member(jsii_name="resetGrpc")
    def reset_grpc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpc", []))

    @jsii.member(jsii_name="resetHttp")
    def reset_http(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp", []))

    @jsii.member(jsii_name="resetHttp2")
    def reset_http2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp2", []))

    @jsii.member(jsii_name="resetTcp")
    def reset_tcp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcp", []))

    @builtins.property
    @jsii.member(jsii_name="grpc")
    def grpc(self) -> AppmeshVirtualNodeSpecListenerTimeoutGrpcOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecListenerTimeoutGrpcOutputReference, jsii.get(self, "grpc"))

    @builtins.property
    @jsii.member(jsii_name="http")
    def http(self) -> AppmeshVirtualNodeSpecListenerTimeoutHttpOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecListenerTimeoutHttpOutputReference, jsii.get(self, "http"))

    @builtins.property
    @jsii.member(jsii_name="http2")
    def http2(self) -> AppmeshVirtualNodeSpecListenerTimeoutHttp2OutputReference:
        return typing.cast(AppmeshVirtualNodeSpecListenerTimeoutHttp2OutputReference, jsii.get(self, "http2"))

    @builtins.property
    @jsii.member(jsii_name="tcp")
    def tcp(self) -> "AppmeshVirtualNodeSpecListenerTimeoutTcpOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecListenerTimeoutTcpOutputReference", jsii.get(self, "tcp"))

    @builtins.property
    @jsii.member(jsii_name="grpcInput")
    def grpc_input(self) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutGrpc]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutGrpc], jsii.get(self, "grpcInput"))

    @builtins.property
    @jsii.member(jsii_name="http2Input")
    def http2_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp2]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp2], jsii.get(self, "http2Input"))

    @builtins.property
    @jsii.member(jsii_name="httpInput")
    def http_input(self) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp], jsii.get(self, "httpInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpInput")
    def tcp_input(self) -> typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutTcp"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutTcp"], jsii.get(self, "tcpInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeout]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405a488a3b470935e01ecf995c7e71347d02cdd28335a14f673fa28d36f2274b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutTcp",
    jsii_struct_bases=[],
    name_mapping={"idle": "idle"},
)
class AppmeshVirtualNodeSpecListenerTimeoutTcp:
    def __init__(
        self,
        *,
        idle: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTimeoutTcpIdle", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param idle: idle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#idle AppmeshVirtualNode#idle}
        '''
        if isinstance(idle, dict):
            idle = AppmeshVirtualNodeSpecListenerTimeoutTcpIdle(**idle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce095d021bcab6e83045da7fba962bd64b7849953aca23a6d3f0f60bfed87879)
            check_type(argname="argument idle", value=idle, expected_type=type_hints["idle"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if idle is not None:
            self._values["idle"] = idle

    @builtins.property
    def idle(self) -> typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutTcpIdle"]:
        '''idle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#idle AppmeshVirtualNode#idle}
        '''
        result = self._values.get("idle")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTimeoutTcpIdle"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTimeoutTcp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutTcpIdle",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshVirtualNodeSpecListenerTimeoutTcpIdle:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eefd315f8342b82ceb436942ca903e88e49f109364d4f82c268440cb8f19c01e)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTimeoutTcpIdle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerTimeoutTcpIdleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutTcpIdleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5610bcffd3483037363f6e5bf604ac4bd734854ea2881b80d0c52ae1fb99c40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__637a355710d0e1125f58ced96921e002fa0e4a2cb2553b1d404b169f1b0ba856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__558fb09fa49486272487075cf63d5c2237a14fd1ac81f3de2e3def202516805d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutTcpIdle]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutTcpIdle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutTcpIdle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25eb16c6c94514c62f5d63dc8c825246031244e44a46dc51688736abba16b673)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecListenerTimeoutTcpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTimeoutTcpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc1944e848642d3b456ace5210683395721fd838e850cf49ebf0ad986b2b3d9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIdle")
    def put_idle(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#unit AppmeshVirtualNode#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        value_ = AppmeshVirtualNodeSpecListenerTimeoutTcpIdle(unit=unit, value=value)

        return typing.cast(None, jsii.invoke(self, "putIdle", [value_]))

    @jsii.member(jsii_name="resetIdle")
    def reset_idle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdle", []))

    @builtins.property
    @jsii.member(jsii_name="idle")
    def idle(self) -> AppmeshVirtualNodeSpecListenerTimeoutTcpIdleOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecListenerTimeoutTcpIdleOutputReference, jsii.get(self, "idle"))

    @builtins.property
    @jsii.member(jsii_name="idleInput")
    def idle_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutTcpIdle]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutTcpIdle], jsii.get(self, "idleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutTcp]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutTcp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutTcp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dc714be83374164ab58837c3280a9a005a64b83301a0e2f43a0e6a459af3354)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTls",
    jsii_struct_bases=[],
    name_mapping={
        "certificate": "certificate",
        "mode": "mode",
        "validation": "validation",
    },
)
class AppmeshVirtualNodeSpecListenerTls:
    def __init__(
        self,
        *,
        certificate: typing.Union["AppmeshVirtualNodeSpecListenerTlsCertificate", typing.Dict[builtins.str, typing.Any]],
        mode: builtins.str,
        validation: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTlsValidation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate AppmeshVirtualNode#certificate}
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#mode AppmeshVirtualNode#mode}.
        :param validation: validation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#validation AppmeshVirtualNode#validation}
        '''
        if isinstance(certificate, dict):
            certificate = AppmeshVirtualNodeSpecListenerTlsCertificate(**certificate)
        if isinstance(validation, dict):
            validation = AppmeshVirtualNodeSpecListenerTlsValidation(**validation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf6de424d1fcd8acf772a6de338466e362120abdd55fa063ee5c3c06151bfa7)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument validation", value=validation, expected_type=type_hints["validation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate": certificate,
            "mode": mode,
        }
        if validation is not None:
            self._values["validation"] = validation

    @builtins.property
    def certificate(self) -> "AppmeshVirtualNodeSpecListenerTlsCertificate":
        '''certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate AppmeshVirtualNode#certificate}
        '''
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return typing.cast("AppmeshVirtualNodeSpecListenerTlsCertificate", result)

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#mode AppmeshVirtualNode#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def validation(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerTlsValidation"]:
        '''validation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#validation AppmeshVirtualNode#validation}
        '''
        result = self._values.get("validation")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTlsValidation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsCertificate",
    jsii_struct_bases=[],
    name_mapping={"acm": "acm", "file": "file", "sds": "sds"},
)
class AppmeshVirtualNodeSpecListenerTlsCertificate:
    def __init__(
        self,
        *,
        acm: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTlsCertificateAcm", typing.Dict[builtins.str, typing.Any]]] = None,
        file: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTlsCertificateFile", typing.Dict[builtins.str, typing.Any]]] = None,
        sds: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTlsCertificateSds", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param acm: acm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#acm AppmeshVirtualNode#acm}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        :param sds: sds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#sds AppmeshVirtualNode#sds}
        '''
        if isinstance(acm, dict):
            acm = AppmeshVirtualNodeSpecListenerTlsCertificateAcm(**acm)
        if isinstance(file, dict):
            file = AppmeshVirtualNodeSpecListenerTlsCertificateFile(**file)
        if isinstance(sds, dict):
            sds = AppmeshVirtualNodeSpecListenerTlsCertificateSds(**sds)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b4b719aec6cc2a4f5d6cc7a54b2d2aa4e77e0de939cd1d7d2c58b8995fbf18d)
            check_type(argname="argument acm", value=acm, expected_type=type_hints["acm"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument sds", value=sds, expected_type=type_hints["sds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if acm is not None:
            self._values["acm"] = acm
        if file is not None:
            self._values["file"] = file
        if sds is not None:
            self._values["sds"] = sds

    @builtins.property
    def acm(self) -> typing.Optional["AppmeshVirtualNodeSpecListenerTlsCertificateAcm"]:
        '''acm block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#acm AppmeshVirtualNode#acm}
        '''
        result = self._values.get("acm")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTlsCertificateAcm"], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerTlsCertificateFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTlsCertificateFile"], result)

    @builtins.property
    def sds(self) -> typing.Optional["AppmeshVirtualNodeSpecListenerTlsCertificateSds"]:
        '''sds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#sds AppmeshVirtualNode#sds}
        '''
        result = self._values.get("sds")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTlsCertificateSds"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTlsCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsCertificateAcm",
    jsii_struct_bases=[],
    name_mapping={"certificate_arn": "certificateArn"},
)
class AppmeshVirtualNodeSpecListenerTlsCertificateAcm:
    def __init__(self, *, certificate_arn: builtins.str) -> None:
        '''
        :param certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_arn AppmeshVirtualNode#certificate_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a671216257ea7674c0a41da6f94ce94819789a641d84c572da4af4da95ccb021)
            check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_arn": certificate_arn,
        }

    @builtins.property
    def certificate_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_arn AppmeshVirtualNode#certificate_arn}.'''
        result = self._values.get("certificate_arn")
        assert result is not None, "Required property 'certificate_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTlsCertificateAcm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerTlsCertificateAcmOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsCertificateAcmOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__535b3fae09737d1c53671cdeab7c34934498f75e5b3ac1e51c6ef4e63a98466a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="certificateArnInput")
    def certificate_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateArnInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateArn"))

    @certificate_arn.setter
    def certificate_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9b17cc259d829f18e97365726a42dcc5f45a3fa494097198bd0789d32f8f520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificateAcm]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificateAcm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificateAcm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d07bb4f91c6f44006c215d58d6c236fe3e09ee247fc75299de035836f730cd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsCertificateFile",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_chain": "certificateChain",
        "private_key": "privateKey",
    },
)
class AppmeshVirtualNodeSpecListenerTlsCertificateFile:
    def __init__(
        self,
        *,
        certificate_chain: builtins.str,
        private_key: builtins.str,
    ) -> None:
        '''
        :param certificate_chain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_chain AppmeshVirtualNode#certificate_chain}.
        :param private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#private_key AppmeshVirtualNode#private_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186828500702a7b2f6466b6cf824e8df0cef7828750305030d8400cdc1b3b406)
            check_type(argname="argument certificate_chain", value=certificate_chain, expected_type=type_hints["certificate_chain"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_chain": certificate_chain,
            "private_key": private_key,
        }

    @builtins.property
    def certificate_chain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_chain AppmeshVirtualNode#certificate_chain}.'''
        result = self._values.get("certificate_chain")
        assert result is not None, "Required property 'certificate_chain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def private_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#private_key AppmeshVirtualNode#private_key}.'''
        result = self._values.get("private_key")
        assert result is not None, "Required property 'private_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTlsCertificateFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerTlsCertificateFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsCertificateFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14ce07f769fcf43206ce2dcb4c78ebd8824c50a20342508f0d88ef49f144f380)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="certificateChainInput")
    def certificate_chain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateChainInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyInput")
    def private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateChain")
    def certificate_chain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateChain"))

    @certificate_chain.setter
    def certificate_chain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5154b833173ccc8231c97357021869e33ae7a35a5774cf9f587267e80a772103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateChain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36de67039b45dcb00eb42561b2d0c3fc68e158c89e08e71f7196579f9eded353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificateFile]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificateFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificateFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a53e9ab10c659e290dce972365cb02ac759d2dd9b3731dbc180859945d2798a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecListenerTlsCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72c872f656bcce6068f45ad5b2a88c7d93c7f96118d8f514d6217191a1a4aca2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAcm")
    def put_acm(self, *, certificate_arn: builtins.str) -> None:
        '''
        :param certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_arn AppmeshVirtualNode#certificate_arn}.
        '''
        value = AppmeshVirtualNodeSpecListenerTlsCertificateAcm(
            certificate_arn=certificate_arn
        )

        return typing.cast(None, jsii.invoke(self, "putAcm", [value]))

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        certificate_chain: builtins.str,
        private_key: builtins.str,
    ) -> None:
        '''
        :param certificate_chain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_chain AppmeshVirtualNode#certificate_chain}.
        :param private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#private_key AppmeshVirtualNode#private_key}.
        '''
        value = AppmeshVirtualNodeSpecListenerTlsCertificateFile(
            certificate_chain=certificate_chain, private_key=private_key
        )

        return typing.cast(None, jsii.invoke(self, "putFile", [value]))

    @jsii.member(jsii_name="putSds")
    def put_sds(self, *, secret_name: builtins.str) -> None:
        '''
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#secret_name AppmeshVirtualNode#secret_name}.
        '''
        value = AppmeshVirtualNodeSpecListenerTlsCertificateSds(
            secret_name=secret_name
        )

        return typing.cast(None, jsii.invoke(self, "putSds", [value]))

    @jsii.member(jsii_name="resetAcm")
    def reset_acm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcm", []))

    @jsii.member(jsii_name="resetFile")
    def reset_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFile", []))

    @jsii.member(jsii_name="resetSds")
    def reset_sds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSds", []))

    @builtins.property
    @jsii.member(jsii_name="acm")
    def acm(self) -> AppmeshVirtualNodeSpecListenerTlsCertificateAcmOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecListenerTlsCertificateAcmOutputReference, jsii.get(self, "acm"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> AppmeshVirtualNodeSpecListenerTlsCertificateFileOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecListenerTlsCertificateFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="sds")
    def sds(self) -> "AppmeshVirtualNodeSpecListenerTlsCertificateSdsOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecListenerTlsCertificateSdsOutputReference", jsii.get(self, "sds"))

    @builtins.property
    @jsii.member(jsii_name="acmInput")
    def acm_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificateAcm]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificateAcm], jsii.get(self, "acmInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificateFile]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificateFile], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="sdsInput")
    def sds_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerTlsCertificateSds"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTlsCertificateSds"], jsii.get(self, "sdsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificate]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6baeeb183c4089c18d0eadffd060f6d3b64a3243ad9663768ea450c248ee9ef2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsCertificateSds",
    jsii_struct_bases=[],
    name_mapping={"secret_name": "secretName"},
)
class AppmeshVirtualNodeSpecListenerTlsCertificateSds:
    def __init__(self, *, secret_name: builtins.str) -> None:
        '''
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#secret_name AppmeshVirtualNode#secret_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d16e5887610ce342e6114abd83e3adb62e5abb9a070e8e74046767e0b990e137)
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_name": secret_name,
        }

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#secret_name AppmeshVirtualNode#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTlsCertificateSds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerTlsCertificateSdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsCertificateSdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd39c9dc24689828a9c927520ece9e0cf7fae7fecd028c530d7418f6256273e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a77f77842546bb6378b37eee62a95dcd6205e5fa176c9680ce037464127000cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificateSds]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificateSds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificateSds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2354f3cc5ff5c4049fa95cc414acc3f4ce30f99964568d58363a8a1db1710429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecListenerTlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0856f9064d64260e779ee36bf974472c1ac6abbfc266ab405831e7b95958799e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCertificate")
    def put_certificate(
        self,
        *,
        acm: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTlsCertificateAcm, typing.Dict[builtins.str, typing.Any]]] = None,
        file: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTlsCertificateFile, typing.Dict[builtins.str, typing.Any]]] = None,
        sds: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTlsCertificateSds, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param acm: acm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#acm AppmeshVirtualNode#acm}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        :param sds: sds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#sds AppmeshVirtualNode#sds}
        '''
        value = AppmeshVirtualNodeSpecListenerTlsCertificate(
            acm=acm, file=file, sds=sds
        )

        return typing.cast(None, jsii.invoke(self, "putCertificate", [value]))

    @jsii.member(jsii_name="putValidation")
    def put_validation(
        self,
        *,
        trust: typing.Union["AppmeshVirtualNodeSpecListenerTlsValidationTrust", typing.Dict[builtins.str, typing.Any]],
        subject_alternative_names: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNames", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param trust: trust block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#trust AppmeshVirtualNode#trust}
        :param subject_alternative_names: subject_alternative_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#subject_alternative_names AppmeshVirtualNode#subject_alternative_names}
        '''
        value = AppmeshVirtualNodeSpecListenerTlsValidation(
            trust=trust, subject_alternative_names=subject_alternative_names
        )

        return typing.cast(None, jsii.invoke(self, "putValidation", [value]))

    @jsii.member(jsii_name="resetValidation")
    def reset_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidation", []))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(
        self,
    ) -> AppmeshVirtualNodeSpecListenerTlsCertificateOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecListenerTlsCertificateOutputReference, jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="validation")
    def validation(
        self,
    ) -> "AppmeshVirtualNodeSpecListenerTlsValidationOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecListenerTlsValidationOutputReference", jsii.get(self, "validation"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificate]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificate], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="validationInput")
    def validation_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerTlsValidation"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTlsValidation"], jsii.get(self, "validationInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2f859ca82cd8fbb5aadd435ba3e4838e6bbc29872a0d7230c95ba8d3dddccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshVirtualNodeSpecListenerTls]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTls], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTls],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5121c8c419313027f13a74bd4ae42a54d740f1af4423442a0f00fb6485c65456)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsValidation",
    jsii_struct_bases=[],
    name_mapping={
        "trust": "trust",
        "subject_alternative_names": "subjectAlternativeNames",
    },
)
class AppmeshVirtualNodeSpecListenerTlsValidation:
    def __init__(
        self,
        *,
        trust: typing.Union["AppmeshVirtualNodeSpecListenerTlsValidationTrust", typing.Dict[builtins.str, typing.Any]],
        subject_alternative_names: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNames", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param trust: trust block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#trust AppmeshVirtualNode#trust}
        :param subject_alternative_names: subject_alternative_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#subject_alternative_names AppmeshVirtualNode#subject_alternative_names}
        '''
        if isinstance(trust, dict):
            trust = AppmeshVirtualNodeSpecListenerTlsValidationTrust(**trust)
        if isinstance(subject_alternative_names, dict):
            subject_alternative_names = AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNames(**subject_alternative_names)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__518bd6376c329f12f2fda55a6d16b4ed328bacaf056e13886b700f9216238a2f)
            check_type(argname="argument trust", value=trust, expected_type=type_hints["trust"])
            check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trust": trust,
        }
        if subject_alternative_names is not None:
            self._values["subject_alternative_names"] = subject_alternative_names

    @builtins.property
    def trust(self) -> "AppmeshVirtualNodeSpecListenerTlsValidationTrust":
        '''trust block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#trust AppmeshVirtualNode#trust}
        '''
        result = self._values.get("trust")
        assert result is not None, "Required property 'trust' is missing"
        return typing.cast("AppmeshVirtualNodeSpecListenerTlsValidationTrust", result)

    @builtins.property
    def subject_alternative_names(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNames"]:
        '''subject_alternative_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#subject_alternative_names AppmeshVirtualNode#subject_alternative_names}
        '''
        result = self._values.get("subject_alternative_names")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNames"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTlsValidation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerTlsValidationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsValidationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f40f806c5d356169e137df37785163d789392e7956d45d52ecca5e008b21844d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSubjectAlternativeNames")
    def put_subject_alternative_names(
        self,
        *,
        match: typing.Union["AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatch", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#match AppmeshVirtualNode#match}
        '''
        value = AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNames(
            match=match
        )

        return typing.cast(None, jsii.invoke(self, "putSubjectAlternativeNames", [value]))

    @jsii.member(jsii_name="putTrust")
    def put_trust(
        self,
        *,
        file: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTlsValidationTrustFile", typing.Dict[builtins.str, typing.Any]]] = None,
        sds: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTlsValidationTrustSds", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        :param sds: sds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#sds AppmeshVirtualNode#sds}
        '''
        value = AppmeshVirtualNodeSpecListenerTlsValidationTrust(file=file, sds=sds)

        return typing.cast(None, jsii.invoke(self, "putTrust", [value]))

    @jsii.member(jsii_name="resetSubjectAlternativeNames")
    def reset_subject_alternative_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectAlternativeNames", []))

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeNames")
    def subject_alternative_names(
        self,
    ) -> "AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesOutputReference", jsii.get(self, "subjectAlternativeNames"))

    @builtins.property
    @jsii.member(jsii_name="trust")
    def trust(
        self,
    ) -> "AppmeshVirtualNodeSpecListenerTlsValidationTrustOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecListenerTlsValidationTrustOutputReference", jsii.get(self, "trust"))

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeNamesInput")
    def subject_alternative_names_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNames"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNames"], jsii.get(self, "subjectAlternativeNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="trustInput")
    def trust_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerTlsValidationTrust"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTlsValidationTrust"], jsii.get(self, "trustInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidation]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__970effe4f426be89eb86210fd037a1c4d6e326b1be29b4715720d02189c1b63b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNames",
    jsii_struct_bases=[],
    name_mapping={"match": "match"},
)
class AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNames:
    def __init__(
        self,
        *,
        match: typing.Union["AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatch", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#match AppmeshVirtualNode#match}
        '''
        if isinstance(match, dict):
            match = AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fe1488fe05ecfee31abe64385a366cde9884276143bcaace8ff68e0fa7ad582)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match": match,
        }

    @builtins.property
    def match(
        self,
    ) -> "AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatch":
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#match AppmeshVirtualNode#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatch", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatch",
    jsii_struct_bases=[],
    name_mapping={"exact": "exact"},
)
class AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatch:
    def __init__(self, *, exact: typing.Sequence[builtins.str]) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#exact AppmeshVirtualNode#exact}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b159023ca6dddf90287e68de492ddde382ae9e0761ceed04dad00cf5c788b3ab)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "exact": exact,
        }

    @builtins.property
    def exact(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#exact AppmeshVirtualNode#exact}.'''
        result = self._values.get("exact")
        assert result is not None, "Required property 'exact' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__805f81d218d290c1469cafa93b806ea0f9808618feac3d7e6b3f17a2f5bab927)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31cc28bad873b3727a8155d0ec29c1d22f9a25548f3aec99af4ff51ded777b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatch]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77021ea2c406770b80574cf789f38e9ec0987b22b294c3c22bd53ccf790b0f7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e5fdab551e6ec6391171f063b509d60207509315438041a5c6c236877a6867c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMatch")
    def put_match(self, *, exact: typing.Sequence[builtins.str]) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#exact AppmeshVirtualNode#exact}.
        '''
        value = AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatch(
            exact=exact
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(
        self,
    ) -> AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatchOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatch]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNames]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNames], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNames],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6227324ffff2ab7dd34d819bf152b09e120fccd121430b46ee9bfdbbce02db4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsValidationTrust",
    jsii_struct_bases=[],
    name_mapping={"file": "file", "sds": "sds"},
)
class AppmeshVirtualNodeSpecListenerTlsValidationTrust:
    def __init__(
        self,
        *,
        file: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTlsValidationTrustFile", typing.Dict[builtins.str, typing.Any]]] = None,
        sds: typing.Optional[typing.Union["AppmeshVirtualNodeSpecListenerTlsValidationTrustSds", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        :param sds: sds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#sds AppmeshVirtualNode#sds}
        '''
        if isinstance(file, dict):
            file = AppmeshVirtualNodeSpecListenerTlsValidationTrustFile(**file)
        if isinstance(sds, dict):
            sds = AppmeshVirtualNodeSpecListenerTlsValidationTrustSds(**sds)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eff3c6f6c6abddc1afaba37ce4cd324d3361c9381c423d77997f0ccc758d7631)
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument sds", value=sds, expected_type=type_hints["sds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file is not None:
            self._values["file"] = file
        if sds is not None:
            self._values["sds"] = sds

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerTlsValidationTrustFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTlsValidationTrustFile"], result)

    @builtins.property
    def sds(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerTlsValidationTrustSds"]:
        '''sds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#sds AppmeshVirtualNode#sds}
        '''
        result = self._values.get("sds")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTlsValidationTrustSds"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTlsValidationTrust(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsValidationTrustFile",
    jsii_struct_bases=[],
    name_mapping={"certificate_chain": "certificateChain"},
)
class AppmeshVirtualNodeSpecListenerTlsValidationTrustFile:
    def __init__(self, *, certificate_chain: builtins.str) -> None:
        '''
        :param certificate_chain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_chain AppmeshVirtualNode#certificate_chain}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f1e3458672d50d85e4e02c2ad8cecaa56027bbf8b0249dddda2f5bc90941f5e)
            check_type(argname="argument certificate_chain", value=certificate_chain, expected_type=type_hints["certificate_chain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_chain": certificate_chain,
        }

    @builtins.property
    def certificate_chain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_chain AppmeshVirtualNode#certificate_chain}.'''
        result = self._values.get("certificate_chain")
        assert result is not None, "Required property 'certificate_chain' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTlsValidationTrustFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerTlsValidationTrustFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsValidationTrustFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__375aa6d60ef3496d0f1d9cb46ac483e4a35cdfa36018615ffb5e4066fc0b5b9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="certificateChainInput")
    def certificate_chain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateChainInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateChain")
    def certificate_chain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateChain"))

    @certificate_chain.setter
    def certificate_chain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daae9348044505676185cc0db3b40a873e4d6a85b9a72aa6b775d1ba49a8bd47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateChain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationTrustFile]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationTrustFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationTrustFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__954717ab823ebd5475bae9638d66f4325647547979dc796643a0e59df0e6de03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecListenerTlsValidationTrustOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsValidationTrustOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__133c9391b1138d9526befe10dd7012a0b14358d7a54925503d737b52bce34af6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(self, *, certificate_chain: builtins.str) -> None:
        '''
        :param certificate_chain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#certificate_chain AppmeshVirtualNode#certificate_chain}.
        '''
        value = AppmeshVirtualNodeSpecListenerTlsValidationTrustFile(
            certificate_chain=certificate_chain
        )

        return typing.cast(None, jsii.invoke(self, "putFile", [value]))

    @jsii.member(jsii_name="putSds")
    def put_sds(self, *, secret_name: builtins.str) -> None:
        '''
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#secret_name AppmeshVirtualNode#secret_name}.
        '''
        value = AppmeshVirtualNodeSpecListenerTlsValidationTrustSds(
            secret_name=secret_name
        )

        return typing.cast(None, jsii.invoke(self, "putSds", [value]))

    @jsii.member(jsii_name="resetFile")
    def reset_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFile", []))

    @jsii.member(jsii_name="resetSds")
    def reset_sds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSds", []))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(
        self,
    ) -> AppmeshVirtualNodeSpecListenerTlsValidationTrustFileOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecListenerTlsValidationTrustFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="sds")
    def sds(
        self,
    ) -> "AppmeshVirtualNodeSpecListenerTlsValidationTrustSdsOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecListenerTlsValidationTrustSdsOutputReference", jsii.get(self, "sds"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationTrustFile]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationTrustFile], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="sdsInput")
    def sds_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecListenerTlsValidationTrustSds"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecListenerTlsValidationTrustSds"], jsii.get(self, "sdsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationTrust]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationTrust], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationTrust],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4baeb1f3f84c8cf32c8f822209f7d60bd1f4a42f3ad9aecef0d6796e9ae8cebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsValidationTrustSds",
    jsii_struct_bases=[],
    name_mapping={"secret_name": "secretName"},
)
class AppmeshVirtualNodeSpecListenerTlsValidationTrustSds:
    def __init__(self, *, secret_name: builtins.str) -> None:
        '''
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#secret_name AppmeshVirtualNode#secret_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5fc50a3e346769122ea48e89997f981d4ab20d622a40b554fddb6e831aa6c42)
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_name": secret_name,
        }

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#secret_name AppmeshVirtualNode#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecListenerTlsValidationTrustSds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecListenerTlsValidationTrustSdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecListenerTlsValidationTrustSdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89e34aab2bc4d844fd5fa5e6dbac8d27f7fb746a33be82144177818c85910f86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__434d82beced3be62259436409d4dc5dad232213be473a6017781a3a9e7de8ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationTrustSds]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationTrustSds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationTrustSds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c9714ac784ed88e06ef5441d4d8fd0908bb1e4bdd75c6b9021fca52623018bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecLogging",
    jsii_struct_bases=[],
    name_mapping={"access_log": "accessLog"},
)
class AppmeshVirtualNodeSpecLogging:
    def __init__(
        self,
        *,
        access_log: typing.Optional[typing.Union["AppmeshVirtualNodeSpecLoggingAccessLog", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_log: access_log block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#access_log AppmeshVirtualNode#access_log}
        '''
        if isinstance(access_log, dict):
            access_log = AppmeshVirtualNodeSpecLoggingAccessLog(**access_log)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dece958470d6700b67c466feeec007a9b81d013d132a2690516a3ca1239663c)
            check_type(argname="argument access_log", value=access_log, expected_type=type_hints["access_log"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_log is not None:
            self._values["access_log"] = access_log

    @builtins.property
    def access_log(self) -> typing.Optional["AppmeshVirtualNodeSpecLoggingAccessLog"]:
        '''access_log block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#access_log AppmeshVirtualNode#access_log}
        '''
        result = self._values.get("access_log")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecLoggingAccessLog"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecLogging(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecLoggingAccessLog",
    jsii_struct_bases=[],
    name_mapping={"file": "file"},
)
class AppmeshVirtualNodeSpecLoggingAccessLog:
    def __init__(
        self,
        *,
        file: typing.Optional[typing.Union["AppmeshVirtualNodeSpecLoggingAccessLogFile", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        '''
        if isinstance(file, dict):
            file = AppmeshVirtualNodeSpecLoggingAccessLogFile(**file)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37a77467a093cd3c6c3ae386c05d8e47d624c5ec44eee821b32c874c3b85f527)
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file is not None:
            self._values["file"] = file

    @builtins.property
    def file(self) -> typing.Optional["AppmeshVirtualNodeSpecLoggingAccessLogFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecLoggingAccessLogFile"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecLoggingAccessLog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecLoggingAccessLogFile",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "format": "format"},
)
class AppmeshVirtualNodeSpecLoggingAccessLogFile:
    def __init__(
        self,
        *,
        path: builtins.str,
        format: typing.Optional[typing.Union["AppmeshVirtualNodeSpecLoggingAccessLogFileFormat", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#path AppmeshVirtualNode#path}.
        :param format: format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#format AppmeshVirtualNode#format}
        '''
        if isinstance(format, dict):
            format = AppmeshVirtualNodeSpecLoggingAccessLogFileFormat(**format)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edccd1650586ebc2d11d181dccb094d55ec80e00a46eaf6ea8a466f4379b155e)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if format is not None:
            self._values["format"] = format

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#path AppmeshVirtualNode#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def format(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecLoggingAccessLogFileFormat"]:
        '''format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#format AppmeshVirtualNode#format}
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecLoggingAccessLogFileFormat"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecLoggingAccessLogFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecLoggingAccessLogFileFormat",
    jsii_struct_bases=[],
    name_mapping={"json": "json", "text": "text"},
)
class AppmeshVirtualNodeSpecLoggingAccessLogFileFormat:
    def __init__(
        self,
        *,
        json: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson", typing.Dict[builtins.str, typing.Any]]]]] = None,
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#json AppmeshVirtualNode#json}
        :param text: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#text AppmeshVirtualNode#text}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b5ae4168c4ae5b3d276016fb1f7c2e2a46053381881e8bb4cb9ee2a4a41c1f6)
            check_type(argname="argument json", value=json, expected_type=type_hints["json"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if json is not None:
            self._values["json"] = json
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def json(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson"]]]:
        '''json block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#json AppmeshVirtualNode#json}
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson"]]], result)

    @builtins.property
    def text(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#text AppmeshVirtualNode#text}.'''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecLoggingAccessLogFileFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#key AppmeshVirtualNode#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b00d0079832070fefa149922c999da01361faf1719e42b3e69103109a67fbbd)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#key AppmeshVirtualNode#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#value AppmeshVirtualNode#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJsonList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJsonList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c05d761429eac7f7678a5ef8035d1153c4f35be6fc34e1461d617ce535b3be42)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJsonOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe95824c88e67d095fe52a2d808c3ee9063aa741822bd8aea70e90c0164da4f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJsonOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51ba327b53147156674ada72a1614bb6a5e7a9fd682cafc8e92c3670fd753597)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4317b213509c9f4fe3090849367a2e2ffa7a0be5cc4735dcbf114c933db6038)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69d1ee3429988c982c787035bd8e93a2a278da51884f5ffa1dbe5c1f7ec979fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea4d9abbb8e28494fec38ff4cecb17e0794873f0aa044ab1590f5a8a99d92c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJsonOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJsonOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d00198adc5d7fc081cb843326cb33955bc16e6129619c9591838d4ae693ab04)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e59b3deb8f54570cd2a25c573b53f36e5b91788afb4a854e9e1a1443b88db26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db62a454b8490bdebe53711cdcc7f1e882927760a9edba511729000ce23beb73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99f388ac2c6327db1c899089a7d388a35c47987a929a826e65ea00c369ec8fc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecLoggingAccessLogFileFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecLoggingAccessLogFileFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a98c817e1b519d1ca526a6a84c8c943408dfb0bfbbbb4150148e22a91daa8d34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putJson")
    def put_json(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64aee2fd0143743888229b78f0328b1a38c02706daf2e866bee15c98d2971b38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putJson", [value]))

    @jsii.member(jsii_name="resetJson")
    def reset_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJson", []))

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(self) -> AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJsonList:
        return typing.cast(AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJsonList, jsii.get(self, "json"))

    @builtins.property
    @jsii.member(jsii_name="jsonInput")
    def json_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson]]], jsii.get(self, "jsonInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7756ee7d0dba5df783d939db04370c76adcc80b3c5360b6ef8df2ad5be315d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecLoggingAccessLogFileFormat]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecLoggingAccessLogFileFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecLoggingAccessLogFileFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02abf7095df8107d99faade0141f7d45dc823380ea2917183b0011c4abbe8819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecLoggingAccessLogFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecLoggingAccessLogFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__371b9871810ac596a63d9aab4a376b2afa8d36b66871b9dac048fbc36f58c5d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFormat")
    def put_format(
        self,
        *,
        json: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson, typing.Dict[builtins.str, typing.Any]]]]] = None,
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#json AppmeshVirtualNode#json}
        :param text: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#text AppmeshVirtualNode#text}.
        '''
        value = AppmeshVirtualNodeSpecLoggingAccessLogFileFormat(json=json, text=text)

        return typing.cast(None, jsii.invoke(self, "putFormat", [value]))

    @jsii.member(jsii_name="resetFormat")
    def reset_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFormat", []))

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> AppmeshVirtualNodeSpecLoggingAccessLogFileFormatOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecLoggingAccessLogFileFormatOutputReference, jsii.get(self, "format"))

    @builtins.property
    @jsii.member(jsii_name="formatInput")
    def format_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecLoggingAccessLogFileFormat]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecLoggingAccessLogFileFormat], jsii.get(self, "formatInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b606d497cb473cd835ee956ae9ae04c1f0b1c803e068fd9d01816edaf4359b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecLoggingAccessLogFile]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecLoggingAccessLogFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecLoggingAccessLogFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__840978a44ced820f0191b0e5d9fb3f08d5a807d75b8f8a232dd0627675877dcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecLoggingAccessLogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecLoggingAccessLogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb93f28cba7dd0f2ef37b0105630822ad53722fc6181676c73ec359f495d2c96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        path: builtins.str,
        format: typing.Optional[typing.Union[AppmeshVirtualNodeSpecLoggingAccessLogFileFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#path AppmeshVirtualNode#path}.
        :param format: format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#format AppmeshVirtualNode#format}
        '''
        value = AppmeshVirtualNodeSpecLoggingAccessLogFile(path=path, format=format)

        return typing.cast(None, jsii.invoke(self, "putFile", [value]))

    @jsii.member(jsii_name="resetFile")
    def reset_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFile", []))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> AppmeshVirtualNodeSpecLoggingAccessLogFileOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecLoggingAccessLogFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(self) -> typing.Optional[AppmeshVirtualNodeSpecLoggingAccessLogFile]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecLoggingAccessLogFile], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshVirtualNodeSpecLoggingAccessLog]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecLoggingAccessLog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecLoggingAccessLog],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32b749db6f87d6f17920ac30aa152f2cffb106b2f572dfcc9be4dfcca47b011b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecLoggingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecLoggingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97db36f59a7d52f1f4db51fa90e2459df4881fa16a5f7dac9bc112c3f3cd3f87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccessLog")
    def put_access_log(
        self,
        *,
        file: typing.Optional[typing.Union[AppmeshVirtualNodeSpecLoggingAccessLogFile, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#file AppmeshVirtualNode#file}
        '''
        value = AppmeshVirtualNodeSpecLoggingAccessLog(file=file)

        return typing.cast(None, jsii.invoke(self, "putAccessLog", [value]))

    @jsii.member(jsii_name="resetAccessLog")
    def reset_access_log(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLog", []))

    @builtins.property
    @jsii.member(jsii_name="accessLog")
    def access_log(self) -> AppmeshVirtualNodeSpecLoggingAccessLogOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecLoggingAccessLogOutputReference, jsii.get(self, "accessLog"))

    @builtins.property
    @jsii.member(jsii_name="accessLogInput")
    def access_log_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecLoggingAccessLog]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecLoggingAccessLog], jsii.get(self, "accessLogInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshVirtualNodeSpecLogging]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecLogging], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecLogging],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f24dadc95f3f8cd551acc4276bcf04a7d8175f46299d3e2ae8b93599bc2df1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa09647374b70aa19e94530936edc89bae8ea5136b236910363c9b0dbd9360ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBackend")
    def put_backend(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecBackend, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72eff2cc5ba6da8554708c813252bea14ef79fd9d84b5f4e0a56c82e72be720f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackend", [value]))

    @jsii.member(jsii_name="putBackendDefaults")
    def put_backend_defaults(
        self,
        *,
        client_policy: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendDefaultsClientPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_policy: client_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#client_policy AppmeshVirtualNode#client_policy}
        '''
        value = AppmeshVirtualNodeSpecBackendDefaults(client_policy=client_policy)

        return typing.cast(None, jsii.invoke(self, "putBackendDefaults", [value]))

    @jsii.member(jsii_name="putListener")
    def put_listener(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecListener, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d404752c5f6889f8bf94616b3c17fa76f1961b08b39d2830de3529c5e9ad52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putListener", [value]))

    @jsii.member(jsii_name="putLogging")
    def put_logging(
        self,
        *,
        access_log: typing.Optional[typing.Union[AppmeshVirtualNodeSpecLoggingAccessLog, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_log: access_log block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#access_log AppmeshVirtualNode#access_log}
        '''
        value = AppmeshVirtualNodeSpecLogging(access_log=access_log)

        return typing.cast(None, jsii.invoke(self, "putLogging", [value]))

    @jsii.member(jsii_name="putServiceDiscovery")
    def put_service_discovery(
        self,
        *,
        aws_cloud_map: typing.Optional[typing.Union["AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMap", typing.Dict[builtins.str, typing.Any]]] = None,
        dns: typing.Optional[typing.Union["AppmeshVirtualNodeSpecServiceDiscoveryDns", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_cloud_map: aws_cloud_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#aws_cloud_map AppmeshVirtualNode#aws_cloud_map}
        :param dns: dns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#dns AppmeshVirtualNode#dns}
        '''
        value = AppmeshVirtualNodeSpecServiceDiscovery(
            aws_cloud_map=aws_cloud_map, dns=dns
        )

        return typing.cast(None, jsii.invoke(self, "putServiceDiscovery", [value]))

    @jsii.member(jsii_name="resetBackend")
    def reset_backend(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackend", []))

    @jsii.member(jsii_name="resetBackendDefaults")
    def reset_backend_defaults(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendDefaults", []))

    @jsii.member(jsii_name="resetListener")
    def reset_listener(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetListener", []))

    @jsii.member(jsii_name="resetLogging")
    def reset_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogging", []))

    @jsii.member(jsii_name="resetServiceDiscovery")
    def reset_service_discovery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceDiscovery", []))

    @builtins.property
    @jsii.member(jsii_name="backend")
    def backend(self) -> AppmeshVirtualNodeSpecBackendList:
        return typing.cast(AppmeshVirtualNodeSpecBackendList, jsii.get(self, "backend"))

    @builtins.property
    @jsii.member(jsii_name="backendDefaults")
    def backend_defaults(self) -> AppmeshVirtualNodeSpecBackendDefaultsOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecBackendDefaultsOutputReference, jsii.get(self, "backendDefaults"))

    @builtins.property
    @jsii.member(jsii_name="listener")
    def listener(self) -> AppmeshVirtualNodeSpecListenerList:
        return typing.cast(AppmeshVirtualNodeSpecListenerList, jsii.get(self, "listener"))

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(self) -> AppmeshVirtualNodeSpecLoggingOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecLoggingOutputReference, jsii.get(self, "logging"))

    @builtins.property
    @jsii.member(jsii_name="serviceDiscovery")
    def service_discovery(
        self,
    ) -> "AppmeshVirtualNodeSpecServiceDiscoveryOutputReference":
        return typing.cast("AppmeshVirtualNodeSpecServiceDiscoveryOutputReference", jsii.get(self, "serviceDiscovery"))

    @builtins.property
    @jsii.member(jsii_name="backendDefaultsInput")
    def backend_defaults_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecBackendDefaults]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecBackendDefaults], jsii.get(self, "backendDefaultsInput"))

    @builtins.property
    @jsii.member(jsii_name="backendInput")
    def backend_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecBackend]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecBackend]]], jsii.get(self, "backendInput"))

    @builtins.property
    @jsii.member(jsii_name="listenerInput")
    def listener_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListener]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListener]]], jsii.get(self, "listenerInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingInput")
    def logging_input(self) -> typing.Optional[AppmeshVirtualNodeSpecLogging]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecLogging], jsii.get(self, "loggingInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDiscoveryInput")
    def service_discovery_input(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecServiceDiscovery"]:
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecServiceDiscovery"], jsii.get(self, "serviceDiscoveryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshVirtualNodeSpec]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AppmeshVirtualNodeSpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dfa3b17b2346febdad63cd028ad6a6d8f7799b5e8aa705a9631f43e247ae3c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecServiceDiscovery",
    jsii_struct_bases=[],
    name_mapping={"aws_cloud_map": "awsCloudMap", "dns": "dns"},
)
class AppmeshVirtualNodeSpecServiceDiscovery:
    def __init__(
        self,
        *,
        aws_cloud_map: typing.Optional[typing.Union["AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMap", typing.Dict[builtins.str, typing.Any]]] = None,
        dns: typing.Optional[typing.Union["AppmeshVirtualNodeSpecServiceDiscoveryDns", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_cloud_map: aws_cloud_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#aws_cloud_map AppmeshVirtualNode#aws_cloud_map}
        :param dns: dns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#dns AppmeshVirtualNode#dns}
        '''
        if isinstance(aws_cloud_map, dict):
            aws_cloud_map = AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMap(**aws_cloud_map)
        if isinstance(dns, dict):
            dns = AppmeshVirtualNodeSpecServiceDiscoveryDns(**dns)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__729ff611abd7f4f62d5942c16adf00620c378fe90767f9980b7219e07fa5abaf)
            check_type(argname="argument aws_cloud_map", value=aws_cloud_map, expected_type=type_hints["aws_cloud_map"])
            check_type(argname="argument dns", value=dns, expected_type=type_hints["dns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_cloud_map is not None:
            self._values["aws_cloud_map"] = aws_cloud_map
        if dns is not None:
            self._values["dns"] = dns

    @builtins.property
    def aws_cloud_map(
        self,
    ) -> typing.Optional["AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMap"]:
        '''aws_cloud_map block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#aws_cloud_map AppmeshVirtualNode#aws_cloud_map}
        '''
        result = self._values.get("aws_cloud_map")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMap"], result)

    @builtins.property
    def dns(self) -> typing.Optional["AppmeshVirtualNodeSpecServiceDiscoveryDns"]:
        '''dns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#dns AppmeshVirtualNode#dns}
        '''
        result = self._values.get("dns")
        return typing.cast(typing.Optional["AppmeshVirtualNodeSpecServiceDiscoveryDns"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecServiceDiscovery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMap",
    jsii_struct_bases=[],
    name_mapping={
        "namespace_name": "namespaceName",
        "service_name": "serviceName",
        "attributes": "attributes",
    },
)
class AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMap:
    def __init__(
        self,
        *,
        namespace_name: builtins.str,
        service_name: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param namespace_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#namespace_name AppmeshVirtualNode#namespace_name}.
        :param service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#service_name AppmeshVirtualNode#service_name}.
        :param attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#attributes AppmeshVirtualNode#attributes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a70df3b670a0916b3a76c1641af2584a8317b66ff98cfc11276b2d9b8748e4ad)
            check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespace_name": namespace_name,
            "service_name": service_name,
        }
        if attributes is not None:
            self._values["attributes"] = attributes

    @builtins.property
    def namespace_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#namespace_name AppmeshVirtualNode#namespace_name}.'''
        result = self._values.get("namespace_name")
        assert result is not None, "Required property 'namespace_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#service_name AppmeshVirtualNode#service_name}.'''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#attributes AppmeshVirtualNode#attributes}.'''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5672fb2cc34b43d2f110e8814067296d5c05f6897bc5c51ed71227d1a2d53d6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAttributes")
    def reset_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributes", []))

    @builtins.property
    @jsii.member(jsii_name="attributesInput")
    def attributes_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "attributesInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceNameInput")
    def namespace_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "attributes"))

    @attributes.setter
    def attributes(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa59a27bbd30975e46ada881374ba2340a2ae244b6b0ee219374b16be7dba268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespaceName"))

    @namespace_name.setter
    def namespace_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ff3d333eaa3f5eb01d2011ec731ea518e9c9b2929dfa96f0178b6ee18403b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__159601c886455a1d7a0a7ae0c6115cec54272dad5f32fd8334182e51ced51ee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMap]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMap], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMap],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eee2db704a34ae93bf483fbf75e0f65fa377c382da20a219c5b82864f85895d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecServiceDiscoveryDns",
    jsii_struct_bases=[],
    name_mapping={
        "hostname": "hostname",
        "ip_preference": "ipPreference",
        "response_type": "responseType",
    },
)
class AppmeshVirtualNodeSpecServiceDiscoveryDns:
    def __init__(
        self,
        *,
        hostname: builtins.str,
        ip_preference: typing.Optional[builtins.str] = None,
        response_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#hostname AppmeshVirtualNode#hostname}.
        :param ip_preference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#ip_preference AppmeshVirtualNode#ip_preference}.
        :param response_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#response_type AppmeshVirtualNode#response_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c63dd2396854b3bd687cbf77664cf100d478bcf3c875f5c6a039b4bc45a5cbc1)
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument ip_preference", value=ip_preference, expected_type=type_hints["ip_preference"])
            check_type(argname="argument response_type", value=response_type, expected_type=type_hints["response_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hostname": hostname,
        }
        if ip_preference is not None:
            self._values["ip_preference"] = ip_preference
        if response_type is not None:
            self._values["response_type"] = response_type

    @builtins.property
    def hostname(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#hostname AppmeshVirtualNode#hostname}.'''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_preference(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#ip_preference AppmeshVirtualNode#ip_preference}.'''
        result = self._values.get("ip_preference")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#response_type AppmeshVirtualNode#response_type}.'''
        result = self._values.get("response_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshVirtualNodeSpecServiceDiscoveryDns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshVirtualNodeSpecServiceDiscoveryDnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecServiceDiscoveryDnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8537014262c7daf22ab318fbf62f966fc1410b00dea1a2f58fed5efdff8310d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIpPreference")
    def reset_ip_preference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpPreference", []))

    @jsii.member(jsii_name="resetResponseType")
    def reset_response_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseType", []))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="ipPreferenceInput")
    def ip_preference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipPreferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="responseTypeInput")
    def response_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c890ca65d9f3fcc620d437fb579dec3c5fa94e3cabb0eddb5b783766b65751dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipPreference")
    def ip_preference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipPreference"))

    @ip_preference.setter
    def ip_preference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171858d63544d9e8c9952d65a8beb7960d056966514b51fa658046f30ce5d0cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipPreference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseType")
    def response_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseType"))

    @response_type.setter
    def response_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__955cd1cbc5f274a7f8b0a58d0a53950113ec3ab64ecd3501b30e2414cd6ff586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecServiceDiscoveryDns]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecServiceDiscoveryDns], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecServiceDiscoveryDns],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3d86ee97a9f2e9590ae01d5ef74ca4d741ff4525fc0e5244fa47888b78a10c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshVirtualNodeSpecServiceDiscoveryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshVirtualNode.AppmeshVirtualNodeSpecServiceDiscoveryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d4fc67c6f2c575be16ad7a0a164f5271e830b09327670a6dd78f4b3bc77e597)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAwsCloudMap")
    def put_aws_cloud_map(
        self,
        *,
        namespace_name: builtins.str,
        service_name: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param namespace_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#namespace_name AppmeshVirtualNode#namespace_name}.
        :param service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#service_name AppmeshVirtualNode#service_name}.
        :param attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#attributes AppmeshVirtualNode#attributes}.
        '''
        value = AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMap(
            namespace_name=namespace_name,
            service_name=service_name,
            attributes=attributes,
        )

        return typing.cast(None, jsii.invoke(self, "putAwsCloudMap", [value]))

    @jsii.member(jsii_name="putDns")
    def put_dns(
        self,
        *,
        hostname: builtins.str,
        ip_preference: typing.Optional[builtins.str] = None,
        response_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#hostname AppmeshVirtualNode#hostname}.
        :param ip_preference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#ip_preference AppmeshVirtualNode#ip_preference}.
        :param response_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_virtual_node#response_type AppmeshVirtualNode#response_type}.
        '''
        value = AppmeshVirtualNodeSpecServiceDiscoveryDns(
            hostname=hostname, ip_preference=ip_preference, response_type=response_type
        )

        return typing.cast(None, jsii.invoke(self, "putDns", [value]))

    @jsii.member(jsii_name="resetAwsCloudMap")
    def reset_aws_cloud_map(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsCloudMap", []))

    @jsii.member(jsii_name="resetDns")
    def reset_dns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDns", []))

    @builtins.property
    @jsii.member(jsii_name="awsCloudMap")
    def aws_cloud_map(
        self,
    ) -> AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMapOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMapOutputReference, jsii.get(self, "awsCloudMap"))

    @builtins.property
    @jsii.member(jsii_name="dns")
    def dns(self) -> AppmeshVirtualNodeSpecServiceDiscoveryDnsOutputReference:
        return typing.cast(AppmeshVirtualNodeSpecServiceDiscoveryDnsOutputReference, jsii.get(self, "dns"))

    @builtins.property
    @jsii.member(jsii_name="awsCloudMapInput")
    def aws_cloud_map_input(
        self,
    ) -> typing.Optional[AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMap]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMap], jsii.get(self, "awsCloudMapInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsInput")
    def dns_input(self) -> typing.Optional[AppmeshVirtualNodeSpecServiceDiscoveryDns]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecServiceDiscoveryDns], jsii.get(self, "dnsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshVirtualNodeSpecServiceDiscovery]:
        return typing.cast(typing.Optional[AppmeshVirtualNodeSpecServiceDiscovery], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshVirtualNodeSpecServiceDiscovery],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__409405e88adc9645648e0a50fcc83256e83b7b8dd2e0674ad437e9b9fc008672)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppmeshVirtualNode",
    "AppmeshVirtualNodeConfig",
    "AppmeshVirtualNodeSpec",
    "AppmeshVirtualNodeSpecBackend",
    "AppmeshVirtualNodeSpecBackendDefaults",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicy",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyOutputReference",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTls",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificate",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFile",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFileOutputReference",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateOutputReference",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSds",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSdsOutputReference",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsOutputReference",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidation",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationOutputReference",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNames",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatch",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatchOutputReference",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesOutputReference",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrust",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcm",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcmOutputReference",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFile",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFileOutputReference",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustOutputReference",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSds",
    "AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSdsOutputReference",
    "AppmeshVirtualNodeSpecBackendDefaultsOutputReference",
    "AppmeshVirtualNodeSpecBackendList",
    "AppmeshVirtualNodeSpecBackendOutputReference",
    "AppmeshVirtualNodeSpecBackendVirtualService",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicy",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyOutputReference",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTls",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificate",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFile",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFileOutputReference",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateOutputReference",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSds",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSdsOutputReference",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsOutputReference",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidation",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationOutputReference",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNames",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatch",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatchOutputReference",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesOutputReference",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrust",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcm",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcmOutputReference",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFile",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFileOutputReference",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustOutputReference",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSds",
    "AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSdsOutputReference",
    "AppmeshVirtualNodeSpecBackendVirtualServiceOutputReference",
    "AppmeshVirtualNodeSpecListener",
    "AppmeshVirtualNodeSpecListenerConnectionPool",
    "AppmeshVirtualNodeSpecListenerConnectionPoolGrpc",
    "AppmeshVirtualNodeSpecListenerConnectionPoolGrpcOutputReference",
    "AppmeshVirtualNodeSpecListenerConnectionPoolHttp",
    "AppmeshVirtualNodeSpecListenerConnectionPoolHttp2",
    "AppmeshVirtualNodeSpecListenerConnectionPoolHttp2List",
    "AppmeshVirtualNodeSpecListenerConnectionPoolHttp2OutputReference",
    "AppmeshVirtualNodeSpecListenerConnectionPoolHttpList",
    "AppmeshVirtualNodeSpecListenerConnectionPoolHttpOutputReference",
    "AppmeshVirtualNodeSpecListenerConnectionPoolOutputReference",
    "AppmeshVirtualNodeSpecListenerConnectionPoolTcp",
    "AppmeshVirtualNodeSpecListenerConnectionPoolTcpList",
    "AppmeshVirtualNodeSpecListenerConnectionPoolTcpOutputReference",
    "AppmeshVirtualNodeSpecListenerHealthCheck",
    "AppmeshVirtualNodeSpecListenerHealthCheckOutputReference",
    "AppmeshVirtualNodeSpecListenerList",
    "AppmeshVirtualNodeSpecListenerOutlierDetection",
    "AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDuration",
    "AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDurationOutputReference",
    "AppmeshVirtualNodeSpecListenerOutlierDetectionInterval",
    "AppmeshVirtualNodeSpecListenerOutlierDetectionIntervalOutputReference",
    "AppmeshVirtualNodeSpecListenerOutlierDetectionOutputReference",
    "AppmeshVirtualNodeSpecListenerOutputReference",
    "AppmeshVirtualNodeSpecListenerPortMapping",
    "AppmeshVirtualNodeSpecListenerPortMappingOutputReference",
    "AppmeshVirtualNodeSpecListenerTimeout",
    "AppmeshVirtualNodeSpecListenerTimeoutGrpc",
    "AppmeshVirtualNodeSpecListenerTimeoutGrpcIdle",
    "AppmeshVirtualNodeSpecListenerTimeoutGrpcIdleOutputReference",
    "AppmeshVirtualNodeSpecListenerTimeoutGrpcOutputReference",
    "AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequest",
    "AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequestOutputReference",
    "AppmeshVirtualNodeSpecListenerTimeoutHttp",
    "AppmeshVirtualNodeSpecListenerTimeoutHttp2",
    "AppmeshVirtualNodeSpecListenerTimeoutHttp2Idle",
    "AppmeshVirtualNodeSpecListenerTimeoutHttp2IdleOutputReference",
    "AppmeshVirtualNodeSpecListenerTimeoutHttp2OutputReference",
    "AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequest",
    "AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequestOutputReference",
    "AppmeshVirtualNodeSpecListenerTimeoutHttpIdle",
    "AppmeshVirtualNodeSpecListenerTimeoutHttpIdleOutputReference",
    "AppmeshVirtualNodeSpecListenerTimeoutHttpOutputReference",
    "AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequest",
    "AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequestOutputReference",
    "AppmeshVirtualNodeSpecListenerTimeoutOutputReference",
    "AppmeshVirtualNodeSpecListenerTimeoutTcp",
    "AppmeshVirtualNodeSpecListenerTimeoutTcpIdle",
    "AppmeshVirtualNodeSpecListenerTimeoutTcpIdleOutputReference",
    "AppmeshVirtualNodeSpecListenerTimeoutTcpOutputReference",
    "AppmeshVirtualNodeSpecListenerTls",
    "AppmeshVirtualNodeSpecListenerTlsCertificate",
    "AppmeshVirtualNodeSpecListenerTlsCertificateAcm",
    "AppmeshVirtualNodeSpecListenerTlsCertificateAcmOutputReference",
    "AppmeshVirtualNodeSpecListenerTlsCertificateFile",
    "AppmeshVirtualNodeSpecListenerTlsCertificateFileOutputReference",
    "AppmeshVirtualNodeSpecListenerTlsCertificateOutputReference",
    "AppmeshVirtualNodeSpecListenerTlsCertificateSds",
    "AppmeshVirtualNodeSpecListenerTlsCertificateSdsOutputReference",
    "AppmeshVirtualNodeSpecListenerTlsOutputReference",
    "AppmeshVirtualNodeSpecListenerTlsValidation",
    "AppmeshVirtualNodeSpecListenerTlsValidationOutputReference",
    "AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNames",
    "AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatch",
    "AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatchOutputReference",
    "AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesOutputReference",
    "AppmeshVirtualNodeSpecListenerTlsValidationTrust",
    "AppmeshVirtualNodeSpecListenerTlsValidationTrustFile",
    "AppmeshVirtualNodeSpecListenerTlsValidationTrustFileOutputReference",
    "AppmeshVirtualNodeSpecListenerTlsValidationTrustOutputReference",
    "AppmeshVirtualNodeSpecListenerTlsValidationTrustSds",
    "AppmeshVirtualNodeSpecListenerTlsValidationTrustSdsOutputReference",
    "AppmeshVirtualNodeSpecLogging",
    "AppmeshVirtualNodeSpecLoggingAccessLog",
    "AppmeshVirtualNodeSpecLoggingAccessLogFile",
    "AppmeshVirtualNodeSpecLoggingAccessLogFileFormat",
    "AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson",
    "AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJsonList",
    "AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJsonOutputReference",
    "AppmeshVirtualNodeSpecLoggingAccessLogFileFormatOutputReference",
    "AppmeshVirtualNodeSpecLoggingAccessLogFileOutputReference",
    "AppmeshVirtualNodeSpecLoggingAccessLogOutputReference",
    "AppmeshVirtualNodeSpecLoggingOutputReference",
    "AppmeshVirtualNodeSpecOutputReference",
    "AppmeshVirtualNodeSpecServiceDiscovery",
    "AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMap",
    "AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMapOutputReference",
    "AppmeshVirtualNodeSpecServiceDiscoveryDns",
    "AppmeshVirtualNodeSpecServiceDiscoveryDnsOutputReference",
    "AppmeshVirtualNodeSpecServiceDiscoveryOutputReference",
]

publication.publish()

def _typecheckingstub__5172288e5618603275da7a129ce2c33bfdb6d64cdc79753460b0d75c9f09b815(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    mesh_name: builtins.str,
    name: builtins.str,
    spec: typing.Union[AppmeshVirtualNodeSpec, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    mesh_owner: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__50d95e439e0830896ed0f36b9f7d80cb70cec9f2d2b37fece1d9b1f98950a13f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce963d2efec943ec5501b4b5d04104d986cdfb13f502087789974aa8b6c37bf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e094899f10368d6842a1a923ba3a02c86107862d2bea3786c848ad33c06eeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4822a7d1c04a3f787345cf69a4b5f15476a140a7f4584e1007febee8cc309af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d843d85067b59a7b2c3a73b2872991ff2a93c31c35a6cd33a4f1ab3ba068011f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f6fc608c9b24144a8d089171900b7d4a6c89b4ab608f8cb245cd32544e6e52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91176d8b65b7d306333342e03a6958ac614635c29038edc42875fbbef46c54a6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f003ad776c786ac2d620dd9397e3e1ae1d2cecbffec457172bcfb853cfd36ed6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ab6abfc8bf5ae852b956a9a27185f830830809376fbac4fc779c0ce20e559a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mesh_name: builtins.str,
    name: builtins.str,
    spec: typing.Union[AppmeshVirtualNodeSpec, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    mesh_owner: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb3670928005760dd0de1ce79f1c2d5168518892756da39d9c5131ffe8823e84(
    *,
    backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecBackend, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backend_defaults: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendDefaults, typing.Dict[builtins.str, typing.Any]]] = None,
    listener: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecListener, typing.Dict[builtins.str, typing.Any]]]]] = None,
    logging: typing.Optional[typing.Union[AppmeshVirtualNodeSpecLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    service_discovery: typing.Optional[typing.Union[AppmeshVirtualNodeSpecServiceDiscovery, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d32520f73281c67a6cd2419ec79267a8e8c19cee0d5b66f15006f4695c779cc(
    *,
    virtual_service: typing.Union[AppmeshVirtualNodeSpecBackendVirtualService, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd33021a513758747438c149a283732e7766db464da1908774b32979cd07b3ad(
    *,
    client_policy: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendDefaultsClientPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48cd84ee72f9a9393ecb780a9bd50771dd3f615313fccf78d63991635f6df76d(
    *,
    tls: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTls, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e019bf5f23d13b34b7983b1096f72891b1e5d6c5230125ccee7b9bc4f66bbd11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__106b169ca54cf898a21e9bf0f4dd6eb6de22aecd63e38d882a91e9b4bba68dc4(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ffad650a7d594789bbe2b6cb03a444fad78409fcb16533a248c4a23c7ced97(
    *,
    validation: typing.Union[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidation, typing.Dict[builtins.str, typing.Any]],
    certificate: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a7ca3ee1dbe54b9d1bff36effb8a69e9404bf3207cd8e8fc2be9a3938e4f36(
    *,
    file: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFile, typing.Dict[builtins.str, typing.Any]]] = None,
    sds: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSds, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aaf37ec87517ea7d5b1cc5fff355189e3240d330cc1cbd0fa5bf92490533679(
    *,
    certificate_chain: builtins.str,
    private_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517309efa9fa546a6205c45172ee9381f9e668ec77a054276e84b670b24222c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318eb6bb5c288ee05af2dcedf11bdfaac94601e33b09278ced698f1150cf90a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c4491ab2f0fdcafa407522517c48aae87ea0f700e360ab1915f0c6c074a1c4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__815e74f988ad73a9e5c0e32f50b2ba667ff5fdcfe56a712aa65baecc88184361(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0442697b2f95d0f87fd75f76bfcd155313fdbe838ddd07aa570930ff0bc432e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85abbe0adcb67fc57d0ce27c04737b3c05ab072af253385631cab24be431b0e0(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635d855d0edb6ef7acaab392b973833cb5b96cb0caa05f84585136f79bd42f45(
    *,
    secret_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b925886256fdf896462d51e5b5c0d44586f67bbe3bbcb8809c4851882d827f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887ac4834ec91e3021e9f400769c5e5cadab78876b8ddabcbe22b9b467cde638(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ee46dc18be4a92668f70126a88af9e403a59bbe0ffef1ee2d9445466495137(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsCertificateSds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9534d26d71ae836081c286ac59730443d1849065da29346fa770393da8711820(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c74d46ad473e13122a53e5490509218d836a8f6b248aaeaa49d96117f7c52f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d528f9437080ca0fccdc4a2357274844de2c6e9d533e227a40b3b6b8c71023d3(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e32d8c2e96fdee87aed0d583903b2861f58db42907edc5ed38b5a221b6064c(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTls],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc22af273546981bf1a31eff9e1d787cc2534e1eafe67a7b3be66376a4e9c53e(
    *,
    trust: typing.Union[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrust, typing.Dict[builtins.str, typing.Any]],
    subject_alternative_names: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNames, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1719597d0286fe4402517fd8be212c30d2b8cf6022b816e7bb4b2c02380cb210(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73797900476fad92ec59919c3dea51ef619915a20b4ad6ce5c07b7f86e88d863(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36e57b54d9166e817f334d93cde771d07252c0b1ff8ae44a2c55f7483c901881(
    *,
    match: typing.Union[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatch, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1419ff5226d4ed1dafe5bb14ccf1d54586e40cf21bedffc8ca8fd04edb32664(
    *,
    exact: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93432844e7f980123477d73a54997639ae497f709e5b018909bc44d8e18d1fa2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64dfca17f0c8760593659a0973a47143aae737b004e0d5fb5c0452fc33a7a159(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c3bc738c5eb46220677d58539b0bcffeeac3db18d66777a402f56c88730b083(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNamesMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2435dac827fde8d8157e21eea4e2da469d27fe216eca847b944e8e8504ce03a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44252b818b779626eff76f36063e46bee38fe6882b45d1d7160ace1302c03c4f(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationSubjectAlternativeNames],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e16b470e76136ee369e35c40c934e2f12c2b510553b2bcc6fc49590b1801273(
    *,
    acm: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcm, typing.Dict[builtins.str, typing.Any]]] = None,
    file: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFile, typing.Dict[builtins.str, typing.Any]]] = None,
    sds: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSds, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b6538d1437f2ffea5c8607bef33e77816bd952990d2e45d7dcdf192f3225880(
    *,
    certificate_authority_arns: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7cd0d762e4f5edecb066da5813ed2404a88591884e870dda35473b365c93df6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f149bbe3b0d7ade15afe279ff3581d9b214abae95c62e5df295a2d6be73b516(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3844ef822d04d070a3746690e70438d7e0f4ff6c1e39d3cf723d5015aebfc4f2(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustAcm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b19fe038617776975a77d91ce46c75f93072cc4fd1a6d9f1df858f35e8e8976(
    *,
    certificate_chain: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80680ff1cefe20e72a434038ed9534051975914b25d1d90b186fe9b54bdc188b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__268c047408d1016b18d0a77063ef3cf233d73ec2b74998d0f40589f3e90e3a2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3acaba05a4dda01e34052963e169738fdeca5441bd9af5992fba926ffd6020f4(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2b790162650c87a8cee2a9a205a79876a55578df769ad0ebc226b71e215cd05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf1eb3f231ce2587c22cef2b12597bb55362e0501c9746c82539bfac9e87e141(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrust],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0c7779a137dd298d0cc0a9e2479e8ece96c29da94ba28ac2f5bcad22f7b634(
    *,
    secret_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9867bbd527aeb05631a7876e890cf24d7a92a1b4980c9beb7f67ad726dce7cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194730bcd1d931eac156bef92f4c15fed5bcca90a069ff148fd842602b9ea45c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f320eab480bf8547961df17ff8e07ee519ffe8ad2aeb06fbbd8ccb4fbedcf8a0(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaultsClientPolicyTlsValidationTrustSds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74197984ad540fbe31cb721b95f5c02bfb74c76fc371562feb3b8ed850db527(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__949b65fa643e8a33bc2a4bdc252c6eefa3e7d8fec2c49d4c0069bf9db04dda21(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendDefaults],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846d08fff3865e2782f4baf44e6b55fce3dc3cadd52c987fd8f28a56463977e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46cd71bf3ad64774d78f11df0139c65d0183b7fda436104be6cc598e8415a617(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a330114425792bb26f60faa00231f2bb58ed95351d1f63274cec575186f56a72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab4f3d55eb0fa52e1bd90ca0089775f676e5d7278620aa76e34dfd847300945(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e36970f41d5693888b62f8f53622ef16872b78ca592aa0045b263957096e72(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__295497814b9b03dfe8e569715516fb2eeae0bc0c1b1c511acacceccc95d2816b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecBackend]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5482d91ab7e70f3d4638387c96e076178a1163605ae3285204dd2b3453440e81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e6726c71bfaa2a7e65f87e7885124aca0cc746ed4c5542e50ddaa5a36279d6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecBackend]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f4d312da85b87a536a8875c6aab1c1dd89f47c6ffb19f1ae8da669c13084ef(
    *,
    virtual_service_name: builtins.str,
    client_policy: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775fc1aa60f57f5ace1c7515a4df3912fd83cb78168342e06d5668038ef82028(
    *,
    tls: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTls, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b6c6b67381d596d301f0c9abbd044218268a8a7e6d44326d36a790853aca4f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0451640a4e83ff92a38bf279ed9e69e1d58c31ac426d007e0bc281f6429a890a(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1526cec49cfb192e2f8617340468da15ee2c3afa005fb4b4d307d56f6070be62(
    *,
    validation: typing.Union[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidation, typing.Dict[builtins.str, typing.Any]],
    certificate: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d8dd0725190f46b919604a90660e9515e91ab7080f846559ed376c24bcf5d65(
    *,
    file: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFile, typing.Dict[builtins.str, typing.Any]]] = None,
    sds: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSds, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e393e077d51e815c2046f7ef4b46a3d90802d9d45a151176d2dec4419d5c42cc(
    *,
    certificate_chain: builtins.str,
    private_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18460e055ae4a6c34641122028a298bfffe32152a0ba6b98cd02719acea7d3fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5aa248349b8894e0b7e64e8eadd1840adc889436d4f0a236f8e00463ebfdaf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0927540cd8978b9c4795a649819a46a4aee6614b3f607479a3ad8671de4e4a8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95fb331bc3f44f8a99a4e4e7ec6f1fb23d14fe24214bcff5458e7c4484609c7a(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f6e8ffc8b3f9791cdd5b2de841f59e3060ef33cafbec3dae14059b8f08d64a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a2e3a7db8586b2d77652ec963c9c182641d2cce8cc7fb50cc1a6551b824d6c(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5470222945e75caa1b29e0feef2eaf2a484f96450a3d68a706abbf8cf55651a9(
    *,
    secret_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83bcffd9228f83bd1860005fd335ef4e9fb60d9d050bdd712fc1da2220919b43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebdbfb109eaa9cbab82b00d1f16e12593ad286944841aeecc13fde2290634ae0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2333cf273c824f793ea32163592dd659b11ab1c1250981904ea8a0b8a8e0d5d(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsCertificateSds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff03d13d6e5dad00a2a4722813d7a732ffc125097b7dbbf97a0596161cd6fbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b2be19d0305e24dfc1c66afbe7f114772e320eaa8635844fa2d40d8171a54c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ba02b28e4bd0d3b998b7718afb5a7e26349168780051b85bceaa87582c4b1a(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdfec02b9bad6a1aff766d51c89f0ca17a2013ba2739ad6aa5e5bf65b0e080aa(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTls],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1469043d2d41b6388729253eb5e711e779d0a8ba4af5a4ed6ecd8f6cf87e3c(
    *,
    trust: typing.Union[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrust, typing.Dict[builtins.str, typing.Any]],
    subject_alternative_names: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNames, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab5bae7e6a2f303fad030d1be235f2f9ba5e212852df3e69e5187e106977c8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c427c48774bf4db3d65c27b440f830dfc6628ffc74fd0597ba6f5df0cecc2d5a(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2faad516a91946fd71e7883add8638663e7d678cd500b42211bdbcc587ea3a(
    *,
    match: typing.Union[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatch, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5f2ee50c4681f7381af10bcaed2a169b8cb8211a46690c6c74d921ec225236(
    *,
    exact: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f21a2744a3ea44861f697c5c6cd3c98171382445e09eb6498b5409ef6c9453e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__922522833177aacd4026e2be619f6ff80712d32d2fa3affded8cc0240180b464(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d3e1d133f7d75c6d3f748956544fcb0cba9c65cf0c42723e6356af9969f47b(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNamesMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a11961755ea0808f73ec2b56f8479b95d68c696ab9e5f10b45ae401da9982d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a55257f574576600529746acae425ea36274f73581b838308b3825bc5eb9d6a(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationSubjectAlternativeNames],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__902566a25f335d452a4cb5beab0f1427ca21a2423f3744592c1262f0ce3bb150(
    *,
    acm: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcm, typing.Dict[builtins.str, typing.Any]]] = None,
    file: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFile, typing.Dict[builtins.str, typing.Any]]] = None,
    sds: typing.Optional[typing.Union[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSds, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e471341ada4d946d4bc2d08752d910916e317c294455c7d4a58f90e602dfa70(
    *,
    certificate_authority_arns: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad3ba2e86c451e14d52a36b0aecacefcc87d28871a9f9c37dc29ee9629b06118(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd4fae775a4c4e9980e95e512ad5e3edac465b9f5effd6db1d0f98c6df05f2a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0cb072c7d7088fbdf555be7efea808af6e1bbad04e22947fb5bc93b425409df(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustAcm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87020fefaaf68ce26a570fb41ec040d243ba528210743dd54d4cd0106c2ec8dc(
    *,
    certificate_chain: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10dc30d8a2c34396f37e68e618097a9bce4255c1f04d50e8cd0393c6fc7516be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__121de9584e9375fcffa55702785e73a52f0bd917be093af6fea2f573bb0e7d3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3839ccd190ed67ef0e7704d85962830e455c2eb914ed21c3740f1da2fe03dacd(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9863588a4a3947b6feb327a22e8e0ae5455d25331cc95b7e1f491b5b34f1bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a18442cab100a7dff0896835744ee34b778c6023acdaf0c57bb9da7ef1549a(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrust],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ae7a895ac0787b4fe99fe127a16e863061bf492472f0525a932372908cf2f5(
    *,
    secret_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72dab4b57c830efec642b6277d8ea4ca552afb03830c46510224051916fc4d16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956690f54bb1a7ba44f0eea89c5deb40d6ceaf3b6041a3056e6cccddf375c663(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efbeee29f6594b043d3aa7db58a8119c3d8635ab33fd5afe55de63bea7a0b058(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualServiceClientPolicyTlsValidationTrustSds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fb2e096f7eed12132d9a56c5f0112760305eef60b8b3bb7a868f0fb3856915(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8b1c6580fd4b1fa7517c289a2727bfc2c99efbf9e740f935e4f8a2b76bc427(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab96276caf119bd05f756ff982c777e222b288d50b29ef826695114819d6c178(
    value: typing.Optional[AppmeshVirtualNodeSpecBackendVirtualService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aea8038318bff130d5d658f590a0a37973ccc243c270c91faeeeeca28ce7187(
    *,
    port_mapping: typing.Union[AppmeshVirtualNodeSpecListenerPortMapping, typing.Dict[builtins.str, typing.Any]],
    connection_pool: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerConnectionPool, typing.Dict[builtins.str, typing.Any]]] = None,
    health_check: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    outlier_detection: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerOutlierDetection, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTimeout, typing.Dict[builtins.str, typing.Any]]] = None,
    tls: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTls, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ea32c907c44c415ecc019e66bdbea78de97ed87fe938818d232b515fc6fe86(
    *,
    grpc: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerConnectionPoolGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
    http: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecListenerConnectionPoolHttp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    http2: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecListenerConnectionPoolHttp2, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tcp: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecListenerConnectionPoolTcp, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2d614fa081e6102e7eb5137e1ad148c9079759d739808a7faba950beac7980(
    *,
    max_requests: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917fb3f725aff8daae81da8c6060cd31ba7b7e5403a37b8a5aec320f1ae3a910(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8919047292285f7612f634f9889fbcf9076791f3da868f401b803b9953f279a7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951eb92239a0f1d416b32d4da23f2c376dab2f8a4122cd4b48da36aef51ffa19(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerConnectionPoolGrpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f34b42558abed1bf46bd1217b972fead89b015a89e308d378cc5768b5d7d61a(
    *,
    max_connections: jsii.Number,
    max_pending_requests: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba5903882d9fe88fb0a675c700703c36880f574e54bcec0165c890116ad138a(
    *,
    max_requests: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300bc440b62ffea8b45ece5ee0fc669a38dc06fd9b42b758dbb07e64d09a0bd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87fbdf228f4f88e92c9f1ce5e1608bcd9c040e0acef0e770dfb310cef2be6d04(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb7f59a195f6c2bad6c887023247917fd136e57d5384240cf71146fde04eeca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb976d114550cb62a4adffb679197e4bfe93653c8689a006eb91f13ef89735a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__456c3f5a4cf37c85d69ab48f6622dd4e3e040d13ef325a698a67d9a096808433(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c042b5686d09d34894afd72f0e884c013ddef2fd414c822cfd43855a7e4aa2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListenerConnectionPoolHttp2]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__907092f47eecb9e084c3e66bd6371f51bf4b0c695a3d01c8c591c5c6d3a7667b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d2f740689f1d88f769758db56ef6e3bdb1dcc0b30401ca6d8e7f599d3a8023e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17331c7e129e848abde07a19f595be87c0ad39da98327d32e05563fa690babaa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecListenerConnectionPoolHttp2]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc5993d9dcd1ac329cf356b9bcae778b5fd4110a0d8d74833a7b552269a06fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a75527128704c8de14fd264e6f330b371e67af80329cb7ecef2c7bd4580f29(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eccc261fe0737d88c481274f78debf7f5759022b8ba1b40d4a7ebfeed21733f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd5748bcf2be6d42a55add58e4c8c478d273d4b502a8f63e82deced0e45b09f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e352145892ef47bd76f9fa1425f0e3691799b2a9820ec66a0240b1463c826fb0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4234c80159704a370a1d7cdfc5faf97e9267af69c28bd591512310f9fe03392(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListenerConnectionPoolHttp]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fec6dcf01169f0574ad664c7e00ccab8d8d84f0e23f87aabcbff96d7642652c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f00ecc140d05cd6ea0d38bb5953c4374578979c0197e8cf1583cd62db083fb5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d59fb070c9999a5dab86ce8ac1354bd7efb645dc181b9e4bfc72c629e1ae6dd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ebba2bb518e77fbe0e107dae5d50d8bef4ddb9d94f3d80774320050078899a9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecListenerConnectionPoolHttp]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415876b3fc51480ae1ab8f078e367af26fee31abaad771cc42a394d44d0b3547(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9927633eedf112caf459eabe82f7659c19cf64de16cac78eea000e793e2633c1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecListenerConnectionPoolHttp, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__781e759142de1e3fd2513c3b734eb97d5c3d9b5b1bb999ef18741bcbeaca6657(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecListenerConnectionPoolHttp2, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae9cac6da59f29b1bb5b6d27d5315fd2c21da6cc4ad1ef2f20a44492c1d5730(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecListenerConnectionPoolTcp, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cece5e28ee7cebe9b6afb461e8f16cf1a7cf68147f7dcd1a38bcd8a648a488b(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerConnectionPool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1daabf9db4ed7214bf52ab8d60f32b14a0cfa1f5227326a63e9ad0d425da1e3c(
    *,
    max_connections: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5835ea8c0ab745b4aa8a3fe9841cc775368ca1708afc313e981cda5e3a3ca83f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72fb8f01bee7a9b072349eb006d91f8a5358d6e9f373e167df1f23fd543345ea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1096bc9856c0f132a8e73b4cffd2d676df1b5dd77d9f2fa3fb173c02db3a3192(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc29fd206276e628423cc2918033e9c10bc62ee6bf0a6544c9e9b6b1a3d4f774(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2949ceda5d5155df47b566eaf8b1648aebbe00d9c76ac15ac5e1bb4b882fc8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dbdc90ef05ef2ad7e92b97cb1c3b296edc23847c6a01d95dab7a7cde62061e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListenerConnectionPoolTcp]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d3efd60247b2223fd09de9b6b1c3438870ea38f63afdabcba329eb79de64e3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__122a1cd444f30ab87ca4856e1f05f2dd262c574d2f6f7862656d6808ced14668(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3a2a1e21c6ebeea0400826f9f6607f41b0e2f1f0280d2b9fa5009b33e0b446(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecListenerConnectionPoolTcp]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85f643d8d3b5c4563f3fad129a21467cfb050601dfd9612f13469c81b59a91e(
    *,
    healthy_threshold: jsii.Number,
    interval_millis: jsii.Number,
    protocol: builtins.str,
    timeout_millis: jsii.Number,
    unhealthy_threshold: jsii.Number,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc83897da947fba66ca2bce770c8eee15b0b6add30ae2986463fa7d96fa8401e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7acd1c99b728928436e14cfef907f0d540effcc1e4cdb0cbb1d4c542363e7de0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c586e2ab06c2bea6be6dd245ea0395713bb7457498998c111017a4a2a0722b3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb73014deb379d3f9dcde455db8dd65b81a2be9bb3918ee32cf680df1ec2da4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9921f60d1d6266c1e1172747ebab5479807f45188ba733eade3c20c71824b6c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b548fad1b683448e07b88b401a7791af48e3d756be57efd36e8e0c8723cff1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c9742a070b0633178cb7d252a632e2f4f75a385b42b2bafceb3bdd1efb69eb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70addfdbd6c473a2e34649fc14c016211856cbf588344295d1252f804ebf4449(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90de23ec2a87403b95095ac9999ae9130d815b8264822aa3cbcf51f24dc35615(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerHealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e75df8ddb205a18005405f1e71b4637caf6845e18fecdda8ce59f5f6937986(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b765d692159cadcb49f8bcebfcada0c48dcf449c5ef8982d7055f16794a2b5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9208d189a894751a2f8743902d67c7daa577cfeb9a108db3b7006ba46c01dfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ccd5b2844e929079474dea8438fcd5b40acea6c43667bb6cc980349047db10(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7966bb181d7d7dc923e4b302ed19f0aeeb8030b157e97bf8cd6547f02de19218(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__442d2e2d5ae3ffa9b92d61c7c90f00cc074c54d26afe7ccc020a056bd4c54368(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecListener]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690e93ef7bd28ae3e60f0ab649c2ab9b2b900792bf1db31c987ca9edd2877202(
    *,
    base_ejection_duration: typing.Union[AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDuration, typing.Dict[builtins.str, typing.Any]],
    interval: typing.Union[AppmeshVirtualNodeSpecListenerOutlierDetectionInterval, typing.Dict[builtins.str, typing.Any]],
    max_ejection_percent: jsii.Number,
    max_server_errors: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f802836bc379bfd9b425ea3e35685362edf326b7b5e6131cbc91f25b294b9e28(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ead37a9a8a6a011f062ee91f60673320b3bccc38229a709d1c717b808aa041(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f89ebc62f4c60e047189e7570b28b4db96c5f738ad019c17783e93f1fa3f74e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca3f79215e97f94448e1e801b4cb5a62b56e56d1a8d2fa86fa401610da0f00c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ec5aa8b77fa3776c5028b067be6eeadacc8e7bb4e2788f8bd27c441cf8b7f1(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerOutlierDetectionBaseEjectionDuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606ec4b20c12614d7bc452e3554b3ffe7c6d3a164285beacb533e8cef9721876(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16547425888639a057f8223a558aa7a7393ee0196be9925cd03a579dee30d6f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf716140f7279c41759bf4c06032bb7ec8f1bf1f10b42cd3a404e0a73dc4af4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f624742ce97fc68f47196c74f0f745cc29002a8d8a0ca49522a53a53f6c83188(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68dbc9b097ee50f9ebdc8656243445a8798ea9381a0c5faae418ab5d7f2b7330(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerOutlierDetectionInterval],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d661e5f26d8425ae1e58b9e56ad93fdc5a9d678ab7bd128cbb35a27d89aa3f2f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e236bb669e860db01a485e7e56f8044de29939afa816167144f16a8f4a8e8a49(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4e34bc5de4297ca4d3290ea80a52ae80f4d7f715028f53bb2c9f931f4398b3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30d1428fc674f010bb81e1f81eeb13c89965878fddd4fcdfd35bc901215ddfd(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerOutlierDetection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd55217b93e40911d1ecda11d71c59dc1d70980217014e9e7994c50947d8f32c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7619ef86bb0ddb51984c6ebc9badfb2ebc8cec28727d05be496f06fd9822c0f4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecListener]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c1c21670687f0f070a441165738cd45499f4b3d09912695d30bf79ad5b0508(
    *,
    port: jsii.Number,
    protocol: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c77257dc7c528076c91f1092713d792faa9d0ae7fbab190c080cacd9db2a95a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b22de44f453447d36e295b5757a218b0ea2618d846420d7e08d3de6aaf0ce35(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be6dc8742326d85e251bab26d255b693e247596d1b8e65f508fb3e8718cfc72b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b104cf7648b7fb7a29c82a82c5d219d542981444d98db4e2a86690450bb3ff1(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerPortMapping],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__707a95db1e3acdd56aff29deb72e18760e0e36c6427ca80d3e27a07372cbd8cb(
    *,
    grpc: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTimeoutGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
    http: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTimeoutHttp, typing.Dict[builtins.str, typing.Any]]] = None,
    http2: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTimeoutHttp2, typing.Dict[builtins.str, typing.Any]]] = None,
    tcp: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTimeoutTcp, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5010307f3157802a5b1a459151324f99d4ebca3a8c54fb87e024072838047086(
    *,
    idle: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTimeoutGrpcIdle, typing.Dict[builtins.str, typing.Any]]] = None,
    per_request: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequest, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ebb1815705321677556f7bd18a92416c07efb7f4e3798c4e3864de0439bec5(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68979f9e310de626f542e4879829255d1cef3783a3e8c92d18b828fba6993970(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec0dd9a7da54ec48e9e1c103b4fc6bbccea5681745c98c34268d88270fdfd24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__992676e144eedb5e45249f40440cea4764eef22c8e3175fa9088c8bb8de306b5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__174e7e09c9477093e242cc4aaf31c4e385f33cee56a3fa15c143be65f4225664(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutGrpcIdle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47acb1cb0095eee4643fd6126194ef644e550fc79f38225c5d5f5e96e862ec31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a430edceb53a611b2495696e948a04c32d2debb54312d4139fb7f1269f51d28(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutGrpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13dc0c135eb1f47ef5a791fc98e26d4df5c28b6d80818d1c27fe24e2991ec451(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0320183d1b8cc5abe0841644492fea4cf0aa166052e0d750168b38c57ace8a5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77bbde38e2eb0bf85010e3227e482c31f1f498dff73218925ab353ce3c80ae55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d8a9840f81b9452b155ef20fbdf5bd854755faeccd6836e65867be67aa854d3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513bfbbb87665b64fb806c1ced08d93663bfcf67343ec67b1c5ea771b8780e02(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutGrpcPerRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__601839862576df9110eea01502746d98b6a9df02c4ea524d8ea00e0f50723850(
    *,
    idle: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTimeoutHttpIdle, typing.Dict[builtins.str, typing.Any]]] = None,
    per_request: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequest, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c5a575035359b65c266bcde9f1d9c0209aca73f40eef7716568d24d208a74d(
    *,
    idle: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTimeoutHttp2Idle, typing.Dict[builtins.str, typing.Any]]] = None,
    per_request: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequest, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30476edec9a9ad78f6e0746b78e07810362346ced0f10e341a118b375f61466c(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64f2d002ccf274db0f13068384f1d13957f34c48e28927c59867e6550e5f685(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fef0f31e3917dcf9bdc9d0ac08dad97da596725b797a6183cf8cfe36bfc02e9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a83c22e49d297f4d2be6f54916587f17a812b118ab2f58a804ee8e71b18f407a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac15d1c3ed0d8fd8cb22d5242a1f92776cd4f9cfeed7f6a799eaffd00c36b1e(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp2Idle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041f4efc8991afb2c8bbb7da16b2326ab7f8575f641d57ac2156b05370b6f46b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d742bd1e52273c6052834d63f1f26e076cdf09f06c2d0e708b47dbf2f70560d(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee78dffe70fbe3a5a52a6777677d1dd254ca1404adfa5ece5df14288a98bbcf1(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18bdb8561d417fd6faf74afde077d8c76acbdc5e861fd95e5932274b1095e8a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec66165dd3782a49d680edd1af4f3e97feb5e631dd7ac91567e6e3e011be3b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8798140b1c0cf9986f23ac10b953ae1b7819e1d2c28cd4a98d5e089ef78d5a57(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f814b8cad6ffdb08a9da52ed1ddcbcf54a8011a509709afa8a7d3a89e0bcf389(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp2PerRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c657ee4dde23aad2d9fd5c2e28eb505ed40e55872093e6024fdcfa69efba55f(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c13424b42a248eec2268cbfae0b0da69215f1ed551cdbdf618d08a86528a87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58cac95dfd8e29de08d5d080350e64a3b4dfd8d2d6e7b3e1f3ed925a4e30087f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b243303a170e632aadd3be8aa4827501ceff56c0ce50f7b0a043eb20a09f1b29(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6360349cec12b28e78535887b53a154ae6771dae66ceb76f93bf2d52254e13a0(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttpIdle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb6d02002fc2418b0f5c123cbdf8096519cef88f88987eed4cdc531004e26cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9d62a69e2ba32eca35d9ee3e864ed47384b6ec69153b7900a9396738ebc65b(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2c15b1b093bd7f4b0ec55b6dc6dcb42dbdfe530de4f2b2c55f856a641c02cc(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fe3c9e47e98b087efe2064c864f4f598b8018eed314bbe662cccb42d2c0943(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff714090fa8fd9e95d80003623a333ded332ccaeeb130fd106d0fad0f89b06bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b0131a2730ed9a05fb417553d1ac62ffcef6bd45e4449fc86d88162fe396b9b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6816e40befc4d7c7203a300d63c947fa070bd71d887ec70dd913f3a32230ac3(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutHttpPerRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1817705d9c341502beb77690d845d7a546b18bc5eaaa70a218be99841e5900(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405a488a3b470935e01ecf995c7e71347d02cdd28335a14f673fa28d36f2274b(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce095d021bcab6e83045da7fba962bd64b7849953aca23a6d3f0f60bfed87879(
    *,
    idle: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTimeoutTcpIdle, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eefd315f8342b82ceb436942ca903e88e49f109364d4f82c268440cb8f19c01e(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5610bcffd3483037363f6e5bf604ac4bd734854ea2881b80d0c52ae1fb99c40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637a355710d0e1125f58ced96921e002fa0e4a2cb2553b1d404b169f1b0ba856(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__558fb09fa49486272487075cf63d5c2237a14fd1ac81f3de2e3def202516805d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25eb16c6c94514c62f5d63dc8c825246031244e44a46dc51688736abba16b673(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutTcpIdle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1944e848642d3b456ace5210683395721fd838e850cf49ebf0ad986b2b3d9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc714be83374164ab58837c3280a9a005a64b83301a0e2f43a0e6a459af3354(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTimeoutTcp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf6de424d1fcd8acf772a6de338466e362120abdd55fa063ee5c3c06151bfa7(
    *,
    certificate: typing.Union[AppmeshVirtualNodeSpecListenerTlsCertificate, typing.Dict[builtins.str, typing.Any]],
    mode: builtins.str,
    validation: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTlsValidation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4b719aec6cc2a4f5d6cc7a54b2d2aa4e77e0de939cd1d7d2c58b8995fbf18d(
    *,
    acm: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTlsCertificateAcm, typing.Dict[builtins.str, typing.Any]]] = None,
    file: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTlsCertificateFile, typing.Dict[builtins.str, typing.Any]]] = None,
    sds: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTlsCertificateSds, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a671216257ea7674c0a41da6f94ce94819789a641d84c572da4af4da95ccb021(
    *,
    certificate_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__535b3fae09737d1c53671cdeab7c34934498f75e5b3ac1e51c6ef4e63a98466a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b17cc259d829f18e97365726a42dcc5f45a3fa494097198bd0789d32f8f520(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d07bb4f91c6f44006c215d58d6c236fe3e09ee247fc75299de035836f730cd4(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificateAcm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186828500702a7b2f6466b6cf824e8df0cef7828750305030d8400cdc1b3b406(
    *,
    certificate_chain: builtins.str,
    private_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ce07f769fcf43206ce2dcb4c78ebd8824c50a20342508f0d88ef49f144f380(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5154b833173ccc8231c97357021869e33ae7a35a5774cf9f587267e80a772103(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36de67039b45dcb00eb42561b2d0c3fc68e158c89e08e71f7196579f9eded353(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a53e9ab10c659e290dce972365cb02ac759d2dd9b3731dbc180859945d2798a2(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificateFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c872f656bcce6068f45ad5b2a88c7d93c7f96118d8f514d6217191a1a4aca2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6baeeb183c4089c18d0eadffd060f6d3b64a3243ad9663768ea450c248ee9ef2(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16e5887610ce342e6114abd83e3adb62e5abb9a070e8e74046767e0b990e137(
    *,
    secret_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd39c9dc24689828a9c927520ece9e0cf7fae7fecd028c530d7418f6256273e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a77f77842546bb6378b37eee62a95dcd6205e5fa176c9680ce037464127000cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2354f3cc5ff5c4049fa95cc414acc3f4ce30f99964568d58363a8a1db1710429(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsCertificateSds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0856f9064d64260e779ee36bf974472c1ac6abbfc266ab405831e7b95958799e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2f859ca82cd8fbb5aadd435ba3e4838e6bbc29872a0d7230c95ba8d3dddccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5121c8c419313027f13a74bd4ae42a54d740f1af4423442a0f00fb6485c65456(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTls],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__518bd6376c329f12f2fda55a6d16b4ed328bacaf056e13886b700f9216238a2f(
    *,
    trust: typing.Union[AppmeshVirtualNodeSpecListenerTlsValidationTrust, typing.Dict[builtins.str, typing.Any]],
    subject_alternative_names: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNames, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40f806c5d356169e137df37785163d789392e7956d45d52ecca5e008b21844d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__970effe4f426be89eb86210fd037a1c4d6e326b1be29b4715720d02189c1b63b(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe1488fe05ecfee31abe64385a366cde9884276143bcaace8ff68e0fa7ad582(
    *,
    match: typing.Union[AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatch, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b159023ca6dddf90287e68de492ddde382ae9e0761ceed04dad00cf5c788b3ab(
    *,
    exact: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__805f81d218d290c1469cafa93b806ea0f9808618feac3d7e6b3f17a2f5bab927(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31cc28bad873b3727a8155d0ec29c1d22f9a25548f3aec99af4ff51ded777b9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77021ea2c406770b80574cf789f38e9ec0987b22b294c3c22bd53ccf790b0f7f(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNamesMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e5fdab551e6ec6391171f063b509d60207509315438041a5c6c236877a6867c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6227324ffff2ab7dd34d819bf152b09e120fccd121430b46ee9bfdbbce02db4c(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationSubjectAlternativeNames],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff3c6f6c6abddc1afaba37ce4cd324d3361c9381c423d77997f0ccc758d7631(
    *,
    file: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTlsValidationTrustFile, typing.Dict[builtins.str, typing.Any]]] = None,
    sds: typing.Optional[typing.Union[AppmeshVirtualNodeSpecListenerTlsValidationTrustSds, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f1e3458672d50d85e4e02c2ad8cecaa56027bbf8b0249dddda2f5bc90941f5e(
    *,
    certificate_chain: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375aa6d60ef3496d0f1d9cb46ac483e4a35cdfa36018615ffb5e4066fc0b5b9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daae9348044505676185cc0db3b40a873e4d6a85b9a72aa6b775d1ba49a8bd47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__954717ab823ebd5475bae9638d66f4325647547979dc796643a0e59df0e6de03(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationTrustFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__133c9391b1138d9526befe10dd7012a0b14358d7a54925503d737b52bce34af6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4baeb1f3f84c8cf32c8f822209f7d60bd1f4a42f3ad9aecef0d6796e9ae8cebb(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationTrust],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5fc50a3e346769122ea48e89997f981d4ab20d622a40b554fddb6e831aa6c42(
    *,
    secret_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e34aab2bc4d844fd5fa5e6dbac8d27f7fb746a33be82144177818c85910f86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__434d82beced3be62259436409d4dc5dad232213be473a6017781a3a9e7de8ef6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c9714ac784ed88e06ef5441d4d8fd0908bb1e4bdd75c6b9021fca52623018bd(
    value: typing.Optional[AppmeshVirtualNodeSpecListenerTlsValidationTrustSds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dece958470d6700b67c466feeec007a9b81d013d132a2690516a3ca1239663c(
    *,
    access_log: typing.Optional[typing.Union[AppmeshVirtualNodeSpecLoggingAccessLog, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a77467a093cd3c6c3ae386c05d8e47d624c5ec44eee821b32c874c3b85f527(
    *,
    file: typing.Optional[typing.Union[AppmeshVirtualNodeSpecLoggingAccessLogFile, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edccd1650586ebc2d11d181dccb094d55ec80e00a46eaf6ea8a466f4379b155e(
    *,
    path: builtins.str,
    format: typing.Optional[typing.Union[AppmeshVirtualNodeSpecLoggingAccessLogFileFormat, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b5ae4168c4ae5b3d276016fb1f7c2e2a46053381881e8bb4cb9ee2a4a41c1f6(
    *,
    json: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson, typing.Dict[builtins.str, typing.Any]]]]] = None,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b00d0079832070fefa149922c999da01361faf1719e42b3e69103109a67fbbd(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05d761429eac7f7678a5ef8035d1153c4f35be6fc34e1461d617ce535b3be42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe95824c88e67d095fe52a2d808c3ee9063aa741822bd8aea70e90c0164da4f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51ba327b53147156674ada72a1614bb6a5e7a9fd682cafc8e92c3670fd753597(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4317b213509c9f4fe3090849367a2e2ffa7a0be5cc4735dcbf114c933db6038(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d1ee3429988c982c787035bd8e93a2a278da51884f5ffa1dbe5c1f7ec979fa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea4d9abbb8e28494fec38ff4cecb17e0794873f0aa044ab1590f5a8a99d92c0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d00198adc5d7fc081cb843326cb33955bc16e6129619c9591838d4ae693ab04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e59b3deb8f54570cd2a25c573b53f36e5b91788afb4a854e9e1a1443b88db26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db62a454b8490bdebe53711cdcc7f1e882927760a9edba511729000ce23beb73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f388ac2c6327db1c899089a7d388a35c47987a929a826e65ea00c369ec8fc6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a98c817e1b519d1ca526a6a84c8c943408dfb0bfbbbb4150148e22a91daa8d34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64aee2fd0143743888229b78f0328b1a38c02706daf2e866bee15c98d2971b38(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecLoggingAccessLogFileFormatJson, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7756ee7d0dba5df783d939db04370c76adcc80b3c5360b6ef8df2ad5be315d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02abf7095df8107d99faade0141f7d45dc823380ea2917183b0011c4abbe8819(
    value: typing.Optional[AppmeshVirtualNodeSpecLoggingAccessLogFileFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__371b9871810ac596a63d9aab4a376b2afa8d36b66871b9dac048fbc36f58c5d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b606d497cb473cd835ee956ae9ae04c1f0b1c803e068fd9d01816edaf4359b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__840978a44ced820f0191b0e5d9fb3f08d5a807d75b8f8a232dd0627675877dcd(
    value: typing.Optional[AppmeshVirtualNodeSpecLoggingAccessLogFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb93f28cba7dd0f2ef37b0105630822ad53722fc6181676c73ec359f495d2c96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b749db6f87d6f17920ac30aa152f2cffb106b2f572dfcc9be4dfcca47b011b(
    value: typing.Optional[AppmeshVirtualNodeSpecLoggingAccessLog],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97db36f59a7d52f1f4db51fa90e2459df4881fa16a5f7dac9bc112c3f3cd3f87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f24dadc95f3f8cd551acc4276bcf04a7d8175f46299d3e2ae8b93599bc2df1(
    value: typing.Optional[AppmeshVirtualNodeSpecLogging],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa09647374b70aa19e94530936edc89bae8ea5136b236910363c9b0dbd9360ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72eff2cc5ba6da8554708c813252bea14ef79fd9d84b5f4e0a56c82e72be720f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecBackend, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d404752c5f6889f8bf94616b3c17fa76f1961b08b39d2830de3529c5e9ad52(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshVirtualNodeSpecListener, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dfa3b17b2346febdad63cd028ad6a6d8f7799b5e8aa705a9631f43e247ae3c6(
    value: typing.Optional[AppmeshVirtualNodeSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__729ff611abd7f4f62d5942c16adf00620c378fe90767f9980b7219e07fa5abaf(
    *,
    aws_cloud_map: typing.Optional[typing.Union[AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMap, typing.Dict[builtins.str, typing.Any]]] = None,
    dns: typing.Optional[typing.Union[AppmeshVirtualNodeSpecServiceDiscoveryDns, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a70df3b670a0916b3a76c1641af2584a8317b66ff98cfc11276b2d9b8748e4ad(
    *,
    namespace_name: builtins.str,
    service_name: builtins.str,
    attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5672fb2cc34b43d2f110e8814067296d5c05f6897bc5c51ed71227d1a2d53d6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa59a27bbd30975e46ada881374ba2340a2ae244b6b0ee219374b16be7dba268(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ff3d333eaa3f5eb01d2011ec731ea518e9c9b2929dfa96f0178b6ee18403b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159601c886455a1d7a0a7ae0c6115cec54272dad5f32fd8334182e51ced51ee4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eee2db704a34ae93bf483fbf75e0f65fa377c382da20a219c5b82864f85895d(
    value: typing.Optional[AppmeshVirtualNodeSpecServiceDiscoveryAwsCloudMap],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c63dd2396854b3bd687cbf77664cf100d478bcf3c875f5c6a039b4bc45a5cbc1(
    *,
    hostname: builtins.str,
    ip_preference: typing.Optional[builtins.str] = None,
    response_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8537014262c7daf22ab318fbf62f966fc1410b00dea1a2f58fed5efdff8310d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c890ca65d9f3fcc620d437fb579dec3c5fa94e3cabb0eddb5b783766b65751dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171858d63544d9e8c9952d65a8beb7960d056966514b51fa658046f30ce5d0cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__955cd1cbc5f274a7f8b0a58d0a53950113ec3ab64ecd3501b30e2414cd6ff586(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3d86ee97a9f2e9590ae01d5ef74ca4d741ff4525fc0e5244fa47888b78a10c(
    value: typing.Optional[AppmeshVirtualNodeSpecServiceDiscoveryDns],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4fc67c6f2c575be16ad7a0a164f5271e830b09327670a6dd78f4b3bc77e597(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409405e88adc9645648e0a50fcc83256e83b7b8dd2e0674ad437e9b9fc008672(
    value: typing.Optional[AppmeshVirtualNodeSpecServiceDiscovery],
) -> None:
    """Type checking stubs"""
    pass
