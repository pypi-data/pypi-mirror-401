r'''
# `aws_appmesh_route`

Refer to the Terraform Registry for docs: [`aws_appmesh_route`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route).
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


class AppmeshRoute(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRoute",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route aws_appmesh_route}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        mesh_name: builtins.str,
        name: builtins.str,
        spec: typing.Union["AppmeshRouteSpec", typing.Dict[builtins.str, typing.Any]],
        virtual_router_name: builtins.str,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route aws_appmesh_route} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param mesh_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#mesh_name AppmeshRoute#mesh_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#name AppmeshRoute#name}.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#spec AppmeshRoute#spec}
        :param virtual_router_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#virtual_router_name AppmeshRoute#virtual_router_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#id AppmeshRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mesh_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#mesh_owner AppmeshRoute#mesh_owner}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#region AppmeshRoute#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#tags AppmeshRoute#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#tags_all AppmeshRoute#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a3d1e8f00e7393411b9d39f2b5a5cae13649e67c30f4bd45f2ae0cab466e731)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppmeshRouteConfig(
            mesh_name=mesh_name,
            name=name,
            spec=spec,
            virtual_router_name=virtual_router_name,
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
        '''Generates CDKTF code for importing a AppmeshRoute resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppmeshRoute to import.
        :param import_from_id: The id of the existing AppmeshRoute that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppmeshRoute to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd4c812dab29251147c0e210e3992ed465b70982ef907190ff0b1f7b1f49d098)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        grpc_route: typing.Optional[typing.Union["AppmeshRouteSpecGrpcRoute", typing.Dict[builtins.str, typing.Any]]] = None,
        http2_route: typing.Optional[typing.Union["AppmeshRouteSpecHttp2Route", typing.Dict[builtins.str, typing.Any]]] = None,
        http_route: typing.Optional[typing.Union["AppmeshRouteSpecHttpRoute", typing.Dict[builtins.str, typing.Any]]] = None,
        priority: typing.Optional[jsii.Number] = None,
        tcp_route: typing.Optional[typing.Union["AppmeshRouteSpecTcpRoute", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param grpc_route: grpc_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#grpc_route AppmeshRoute#grpc_route}
        :param http2_route: http2_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#http2_route AppmeshRoute#http2_route}
        :param http_route: http_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#http_route AppmeshRoute#http_route}
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#priority AppmeshRoute#priority}.
        :param tcp_route: tcp_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#tcp_route AppmeshRoute#tcp_route}
        '''
        value = AppmeshRouteSpec(
            grpc_route=grpc_route,
            http2_route=http2_route,
            http_route=http_route,
            priority=priority,
            tcp_route=tcp_route,
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
    def spec(self) -> "AppmeshRouteSpecOutputReference":
        return typing.cast("AppmeshRouteSpecOutputReference", jsii.get(self, "spec"))

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
    def spec_input(self) -> typing.Optional["AppmeshRouteSpec"]:
        return typing.cast(typing.Optional["AppmeshRouteSpec"], jsii.get(self, "specInput"))

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
    @jsii.member(jsii_name="virtualRouterNameInput")
    def virtual_router_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualRouterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bbb86ef48f5e66a8f9e96bfda342822896d8f89473aebd47bae203d647f649e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "meshName"))

    @mesh_name.setter
    def mesh_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38d7920f7b0e09f8a9fb3068b8ef2ca1b2af99f5836896ac875bcc4c189e0064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "meshName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="meshOwner")
    def mesh_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "meshOwner"))

    @mesh_owner.setter
    def mesh_owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8376b6eda9798ea8c8004001a86b19e8477c2f36eb79ab18f97afa72e4fc4e15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "meshOwner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8ac8aeede9bc80adf88bf720d9fc9b9aa54d16aa1b85fcb7fb33de2d1c8d21c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__901ff726f6a5ac0a43c6bb05381528ab4c76a9d541d8b199454dcb65123a5e9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec08557560c171f930b6ed653d656e953bd699422f8d8115589d4d05ed89c93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1a9d6e6ba102d7306d444664b0d60be0ef5f225adf2995d6c4e1776a490a1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualRouterName")
    def virtual_router_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualRouterName"))

    @virtual_router_name.setter
    def virtual_router_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25dfb3c4ac950ac1c2e0fa910890189a4ab244c65085ae3c95b39fa596b98782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualRouterName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteConfig",
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
        "virtual_router_name": "virtualRouterName",
        "id": "id",
        "mesh_owner": "meshOwner",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class AppmeshRouteConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        spec: typing.Union["AppmeshRouteSpec", typing.Dict[builtins.str, typing.Any]],
        virtual_router_name: builtins.str,
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
        :param mesh_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#mesh_name AppmeshRoute#mesh_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#name AppmeshRoute#name}.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#spec AppmeshRoute#spec}
        :param virtual_router_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#virtual_router_name AppmeshRoute#virtual_router_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#id AppmeshRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mesh_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#mesh_owner AppmeshRoute#mesh_owner}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#region AppmeshRoute#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#tags AppmeshRoute#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#tags_all AppmeshRoute#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(spec, dict):
            spec = AppmeshRouteSpec(**spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aacd234c84e88200dcb33f0b26ea493962eec03fd601fad4fe6745b80aef5d49)
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
            check_type(argname="argument virtual_router_name", value=virtual_router_name, expected_type=type_hints["virtual_router_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument mesh_owner", value=mesh_owner, expected_type=type_hints["mesh_owner"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mesh_name": mesh_name,
            "name": name,
            "spec": spec,
            "virtual_router_name": virtual_router_name,
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#mesh_name AppmeshRoute#mesh_name}.'''
        result = self._values.get("mesh_name")
        assert result is not None, "Required property 'mesh_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#name AppmeshRoute#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spec(self) -> "AppmeshRouteSpec":
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#spec AppmeshRoute#spec}
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast("AppmeshRouteSpec", result)

    @builtins.property
    def virtual_router_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#virtual_router_name AppmeshRoute#virtual_router_name}.'''
        result = self._values.get("virtual_router_name")
        assert result is not None, "Required property 'virtual_router_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#id AppmeshRoute#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#mesh_owner AppmeshRoute#mesh_owner}.'''
        result = self._values.get("mesh_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#region AppmeshRoute#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#tags AppmeshRoute#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#tags_all AppmeshRoute#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpec",
    jsii_struct_bases=[],
    name_mapping={
        "grpc_route": "grpcRoute",
        "http2_route": "http2Route",
        "http_route": "httpRoute",
        "priority": "priority",
        "tcp_route": "tcpRoute",
    },
)
class AppmeshRouteSpec:
    def __init__(
        self,
        *,
        grpc_route: typing.Optional[typing.Union["AppmeshRouteSpecGrpcRoute", typing.Dict[builtins.str, typing.Any]]] = None,
        http2_route: typing.Optional[typing.Union["AppmeshRouteSpecHttp2Route", typing.Dict[builtins.str, typing.Any]]] = None,
        http_route: typing.Optional[typing.Union["AppmeshRouteSpecHttpRoute", typing.Dict[builtins.str, typing.Any]]] = None,
        priority: typing.Optional[jsii.Number] = None,
        tcp_route: typing.Optional[typing.Union["AppmeshRouteSpecTcpRoute", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param grpc_route: grpc_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#grpc_route AppmeshRoute#grpc_route}
        :param http2_route: http2_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#http2_route AppmeshRoute#http2_route}
        :param http_route: http_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#http_route AppmeshRoute#http_route}
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#priority AppmeshRoute#priority}.
        :param tcp_route: tcp_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#tcp_route AppmeshRoute#tcp_route}
        '''
        if isinstance(grpc_route, dict):
            grpc_route = AppmeshRouteSpecGrpcRoute(**grpc_route)
        if isinstance(http2_route, dict):
            http2_route = AppmeshRouteSpecHttp2Route(**http2_route)
        if isinstance(http_route, dict):
            http_route = AppmeshRouteSpecHttpRoute(**http_route)
        if isinstance(tcp_route, dict):
            tcp_route = AppmeshRouteSpecTcpRoute(**tcp_route)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a23f8a7f95fddce21fb15c452d84d6e5f0c4fd98291a7d2d51f5dbfb1987b66d)
            check_type(argname="argument grpc_route", value=grpc_route, expected_type=type_hints["grpc_route"])
            check_type(argname="argument http2_route", value=http2_route, expected_type=type_hints["http2_route"])
            check_type(argname="argument http_route", value=http_route, expected_type=type_hints["http_route"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument tcp_route", value=tcp_route, expected_type=type_hints["tcp_route"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if grpc_route is not None:
            self._values["grpc_route"] = grpc_route
        if http2_route is not None:
            self._values["http2_route"] = http2_route
        if http_route is not None:
            self._values["http_route"] = http_route
        if priority is not None:
            self._values["priority"] = priority
        if tcp_route is not None:
            self._values["tcp_route"] = tcp_route

    @builtins.property
    def grpc_route(self) -> typing.Optional["AppmeshRouteSpecGrpcRoute"]:
        '''grpc_route block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#grpc_route AppmeshRoute#grpc_route}
        '''
        result = self._values.get("grpc_route")
        return typing.cast(typing.Optional["AppmeshRouteSpecGrpcRoute"], result)

    @builtins.property
    def http2_route(self) -> typing.Optional["AppmeshRouteSpecHttp2Route"]:
        '''http2_route block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#http2_route AppmeshRoute#http2_route}
        '''
        result = self._values.get("http2_route")
        return typing.cast(typing.Optional["AppmeshRouteSpecHttp2Route"], result)

    @builtins.property
    def http_route(self) -> typing.Optional["AppmeshRouteSpecHttpRoute"]:
        '''http_route block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#http_route AppmeshRoute#http_route}
        '''
        result = self._values.get("http_route")
        return typing.cast(typing.Optional["AppmeshRouteSpecHttpRoute"], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#priority AppmeshRoute#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_route(self) -> typing.Optional["AppmeshRouteSpecTcpRoute"]:
        '''tcp_route block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#tcp_route AppmeshRoute#tcp_route}
        '''
        result = self._values.get("tcp_route")
        return typing.cast(typing.Optional["AppmeshRouteSpecTcpRoute"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRoute",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "match": "match",
        "retry_policy": "retryPolicy",
        "timeout": "timeout",
    },
)
class AppmeshRouteSpecGrpcRoute:
    def __init__(
        self,
        *,
        action: typing.Union["AppmeshRouteSpecGrpcRouteAction", typing.Dict[builtins.str, typing.Any]],
        match: typing.Optional[typing.Union["AppmeshRouteSpecGrpcRouteMatch", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_policy: typing.Optional[typing.Union["AppmeshRouteSpecGrpcRouteRetryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[typing.Union["AppmeshRouteSpecGrpcRouteTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#action AppmeshRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#retry_policy AppmeshRoute#retry_policy}
        :param timeout: timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#timeout AppmeshRoute#timeout}
        '''
        if isinstance(action, dict):
            action = AppmeshRouteSpecGrpcRouteAction(**action)
        if isinstance(match, dict):
            match = AppmeshRouteSpecGrpcRouteMatch(**match)
        if isinstance(retry_policy, dict):
            retry_policy = AppmeshRouteSpecGrpcRouteRetryPolicy(**retry_policy)
        if isinstance(timeout, dict):
            timeout = AppmeshRouteSpecGrpcRouteTimeout(**timeout)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__416ab6b26121fac56a5841b675bf17558b9a0ef2e6cf723cd684f4a35909866d)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument retry_policy", value=retry_policy, expected_type=type_hints["retry_policy"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
        }
        if match is not None:
            self._values["match"] = match
        if retry_policy is not None:
            self._values["retry_policy"] = retry_policy
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def action(self) -> "AppmeshRouteSpecGrpcRouteAction":
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#action AppmeshRoute#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("AppmeshRouteSpecGrpcRouteAction", result)

    @builtins.property
    def match(self) -> typing.Optional["AppmeshRouteSpecGrpcRouteMatch"]:
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional["AppmeshRouteSpecGrpcRouteMatch"], result)

    @builtins.property
    def retry_policy(self) -> typing.Optional["AppmeshRouteSpecGrpcRouteRetryPolicy"]:
        '''retry_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#retry_policy AppmeshRoute#retry_policy}
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional["AppmeshRouteSpecGrpcRouteRetryPolicy"], result)

    @builtins.property
    def timeout(self) -> typing.Optional["AppmeshRouteSpecGrpcRouteTimeout"]:
        '''timeout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#timeout AppmeshRoute#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional["AppmeshRouteSpecGrpcRouteTimeout"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecGrpcRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteAction",
    jsii_struct_bases=[],
    name_mapping={"weighted_target": "weightedTarget"},
)
class AppmeshRouteSpecGrpcRouteAction:
    def __init__(
        self,
        *,
        weighted_target: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshRouteSpecGrpcRouteActionWeightedTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param weighted_target: weighted_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weighted_target AppmeshRoute#weighted_target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa16bd6f237b42ac82923061e008316f759e460bcd9f5c6478a9464de2996374)
            check_type(argname="argument weighted_target", value=weighted_target, expected_type=type_hints["weighted_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "weighted_target": weighted_target,
        }

    @builtins.property
    def weighted_target(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecGrpcRouteActionWeightedTarget"]]:
        '''weighted_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weighted_target AppmeshRoute#weighted_target}
        '''
        result = self._values.get("weighted_target")
        assert result is not None, "Required property 'weighted_target' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecGrpcRouteActionWeightedTarget"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecGrpcRouteAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecGrpcRouteActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c16ad4b289be210eacef1d8cd4feeca2f3f6ca1718b337bfa71d2107de3639d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putWeightedTarget")
    def put_weighted_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshRouteSpecGrpcRouteActionWeightedTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a042d94a351ff117f86dbd4e030edd48cff9841ba494323f53d380a4a3038e52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWeightedTarget", [value]))

    @builtins.property
    @jsii.member(jsii_name="weightedTarget")
    def weighted_target(self) -> "AppmeshRouteSpecGrpcRouteActionWeightedTargetList":
        return typing.cast("AppmeshRouteSpecGrpcRouteActionWeightedTargetList", jsii.get(self, "weightedTarget"))

    @builtins.property
    @jsii.member(jsii_name="weightedTargetInput")
    def weighted_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecGrpcRouteActionWeightedTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecGrpcRouteActionWeightedTarget"]]], jsii.get(self, "weightedTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecGrpcRouteAction]:
        return typing.cast(typing.Optional[AppmeshRouteSpecGrpcRouteAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecGrpcRouteAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2476ec4ebaec04d18402d7d67f629ef03e28e33f5ada3f1844d3447488fa0582)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteActionWeightedTarget",
    jsii_struct_bases=[],
    name_mapping={"virtual_node": "virtualNode", "weight": "weight", "port": "port"},
)
class AppmeshRouteSpecGrpcRouteActionWeightedTarget:
    def __init__(
        self,
        *,
        virtual_node: builtins.str,
        weight: jsii.Number,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param virtual_node: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#virtual_node AppmeshRoute#virtual_node}.
        :param weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weight AppmeshRoute#weight}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee4b2e07e641d56f267a75d27d99382e3c035a0976a0746688b0737cb322a3fc)
            check_type(argname="argument virtual_node", value=virtual_node, expected_type=type_hints["virtual_node"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_node": virtual_node,
            "weight": weight,
        }
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def virtual_node(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#virtual_node AppmeshRoute#virtual_node}.'''
        result = self._values.get("virtual_node")
        assert result is not None, "Required property 'virtual_node' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def weight(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weight AppmeshRoute#weight}.'''
        result = self._values.get("weight")
        assert result is not None, "Required property 'weight' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecGrpcRouteActionWeightedTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecGrpcRouteActionWeightedTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteActionWeightedTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ab97bf7e32f67dfb81acc05186eddbe05696e4616b305441beaac6beedd35e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppmeshRouteSpecGrpcRouteActionWeightedTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__129bc1b89ad93b81fd640f74bc0a569aebd115080984b42440462370826cd674)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshRouteSpecGrpcRouteActionWeightedTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3c232d4e0d82fbebcb4ccabad4994dd27b7b576485f14627f2ce9f03543644)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e54122e8c4f18026a3a41f10dddc541bb0014f21c438961c4205bc7fc0ff16f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d0d047f0f98e5bcb9cbb8fc00a391480b9cd8c1d952f08e0a47718bc7eb9b1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecGrpcRouteActionWeightedTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecGrpcRouteActionWeightedTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecGrpcRouteActionWeightedTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aa4fd4fa74bd45fe7403ccd9a50952ebd6e510918aa8c7df518c50feca9ad46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecGrpcRouteActionWeightedTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteActionWeightedTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cec7837978ef66f9d8703ab0f611e559914c2413c84b8f02d79a3ebf6640b7f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNodeInput")
    def virtual_node_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7518a71a47b1a8e722dfabb0fa256f64536c5d2a257337cce7470461c9e4ffe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNode")
    def virtual_node(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNode"))

    @virtual_node.setter
    def virtual_node(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a2df39475addc715646a369d33668a464ed17a3c3e73004991ccb7392e26450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb6771292d43f7b268a19f36e303e167e8c62809479b91d4daa958a93a780ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecGrpcRouteActionWeightedTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecGrpcRouteActionWeightedTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecGrpcRouteActionWeightedTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbacae1069530782a6fd186c77fd0f4302ea7eb62ec3f2f4b889ddaec375a4ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteMatch",
    jsii_struct_bases=[],
    name_mapping={
        "metadata": "metadata",
        "method_name": "methodName",
        "port": "port",
        "prefix": "prefix",
        "service_name": "serviceName",
    },
)
class AppmeshRouteSpecGrpcRouteMatch:
    def __init__(
        self,
        *,
        metadata: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshRouteSpecGrpcRouteMatchMetadata", typing.Dict[builtins.str, typing.Any]]]]] = None,
        method_name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        prefix: typing.Optional[builtins.str] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#metadata AppmeshRoute#metadata}
        :param method_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#method_name AppmeshRoute#method_name}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#prefix AppmeshRoute#prefix}.
        :param service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#service_name AppmeshRoute#service_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5e53d2f4f0cc057be5ce75e6758e2e69f237c790c20d5bd4dc221679759d79)
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument method_name", value=method_name, expected_type=type_hints["method_name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metadata is not None:
            self._values["metadata"] = metadata
        if method_name is not None:
            self._values["method_name"] = method_name
        if port is not None:
            self._values["port"] = port
        if prefix is not None:
            self._values["prefix"] = prefix
        if service_name is not None:
            self._values["service_name"] = service_name

    @builtins.property
    def metadata(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecGrpcRouteMatchMetadata"]]]:
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#metadata AppmeshRoute#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecGrpcRouteMatchMetadata"]]], result)

    @builtins.property
    def method_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#method_name AppmeshRoute#method_name}.'''
        result = self._values.get("method_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#prefix AppmeshRoute#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#service_name AppmeshRoute#service_name}.'''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecGrpcRouteMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteMatchMetadata",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "invert": "invert", "match": "match"},
)
class AppmeshRouteSpecGrpcRouteMatchMetadata:
    def __init__(
        self,
        *,
        name: builtins.str,
        invert: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        match: typing.Optional[typing.Union["AppmeshRouteSpecGrpcRouteMatchMetadataMatch", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#name AppmeshRoute#name}.
        :param invert: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#invert AppmeshRoute#invert}.
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        '''
        if isinstance(match, dict):
            match = AppmeshRouteSpecGrpcRouteMatchMetadataMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb5a3a43fbca2f34120501278e299e1351568a09679a0408140d8fbbca2809f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument invert", value=invert, expected_type=type_hints["invert"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if invert is not None:
            self._values["invert"] = invert
        if match is not None:
            self._values["match"] = match

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#name AppmeshRoute#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def invert(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#invert AppmeshRoute#invert}.'''
        result = self._values.get("invert")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def match(self) -> typing.Optional["AppmeshRouteSpecGrpcRouteMatchMetadataMatch"]:
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional["AppmeshRouteSpecGrpcRouteMatchMetadataMatch"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecGrpcRouteMatchMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecGrpcRouteMatchMetadataList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteMatchMetadataList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__821848d703ad5c8c30aace203ec5c8ba97a14ed30807f54c5420e9130c3f5f2c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppmeshRouteSpecGrpcRouteMatchMetadataOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ffd1d244346d31940f77946d701fbd1740ebb538e6fd91201f1272e360204a8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshRouteSpecGrpcRouteMatchMetadataOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02711fe0e9aacc7cc436604e633b75078d885f4d0f6ebb22be58abb1fd9294fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cf08ffefb19d9b279f5b5d65b0bc7294acbdf6c3c4208149ce5320facd9b514)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8e19f67b41d0dd51ed249a2355ed43b8a80dfff4c130b42c2d489a5716ab77b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecGrpcRouteMatchMetadata]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecGrpcRouteMatchMetadata]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecGrpcRouteMatchMetadata]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a993d3cc071522faf2b8100bc5a083c1f1ae994e5058d2489bfacfb2792f40f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteMatchMetadataMatch",
    jsii_struct_bases=[],
    name_mapping={
        "exact": "exact",
        "prefix": "prefix",
        "range": "range",
        "regex": "regex",
        "suffix": "suffix",
    },
)
class AppmeshRouteSpecGrpcRouteMatchMetadataMatch:
    def __init__(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        range: typing.Optional[typing.Union["AppmeshRouteSpecGrpcRouteMatchMetadataMatchRange", typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#prefix AppmeshRoute#prefix}.
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#range AppmeshRoute#range}
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#regex AppmeshRoute#regex}.
        :param suffix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#suffix AppmeshRoute#suffix}.
        '''
        if isinstance(range, dict):
            range = AppmeshRouteSpecGrpcRouteMatchMetadataMatchRange(**range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ccaa662486807dc3d3cc1286b54fabbd3e426bfb036a0ca92608bcdc6f50b8)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exact is not None:
            self._values["exact"] = exact
        if prefix is not None:
            self._values["prefix"] = prefix
        if range is not None:
            self._values["range"] = range
        if regex is not None:
            self._values["regex"] = regex
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.'''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#prefix AppmeshRoute#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range(
        self,
    ) -> typing.Optional["AppmeshRouteSpecGrpcRouteMatchMetadataMatchRange"]:
        '''range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#range AppmeshRoute#range}
        '''
        result = self._values.get("range")
        return typing.cast(typing.Optional["AppmeshRouteSpecGrpcRouteMatchMetadataMatchRange"], result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#regex AppmeshRoute#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#suffix AppmeshRoute#suffix}.'''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecGrpcRouteMatchMetadataMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecGrpcRouteMatchMetadataMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteMatchMetadataMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5436a17a8f2ed8b0c5c7f4448a97d532a519691d1f9577db674776853844697)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRange")
    def put_range(self, *, end: jsii.Number, start: jsii.Number) -> None:
        '''
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#end AppmeshRoute#end}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#start AppmeshRoute#start}.
        '''
        value = AppmeshRouteSpecGrpcRouteMatchMetadataMatchRange(end=end, start=start)

        return typing.cast(None, jsii.invoke(self, "putRange", [value]))

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetRange")
    def reset_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRange", []))

    @jsii.member(jsii_name="resetRegex")
    def reset_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegex", []))

    @jsii.member(jsii_name="resetSuffix")
    def reset_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(
        self,
    ) -> "AppmeshRouteSpecGrpcRouteMatchMetadataMatchRangeOutputReference":
        return typing.cast("AppmeshRouteSpecGrpcRouteMatchMetadataMatchRangeOutputReference", jsii.get(self, "range"))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(
        self,
    ) -> typing.Optional["AppmeshRouteSpecGrpcRouteMatchMetadataMatchRange"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecGrpcRouteMatchMetadataMatchRange"], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="suffixInput")
    def suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suffixInput"))

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__076dfab0fe5ed583c8ff3df7e04b0f2ec1b20c8cbcfbe9facd3e97a7cbea19dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f60a88939bfe0f76d6208de0085bb5ffbb27650b8b6af31a91e4606529dfcf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51b997205ef710953fbe5998f28a0c15ae0196d23b4809b705ecd2088b827631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e99c7a0ca095d684c0598a8671b818ec3ecc472b88689c7a1db17c4664b82ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshRouteSpecGrpcRouteMatchMetadataMatch]:
        return typing.cast(typing.Optional[AppmeshRouteSpecGrpcRouteMatchMetadataMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecGrpcRouteMatchMetadataMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce4da8bbc75427b47ea3e69851eff4c4567fe6473076c3fb8f457c9c14d10d7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteMatchMetadataMatchRange",
    jsii_struct_bases=[],
    name_mapping={"end": "end", "start": "start"},
)
class AppmeshRouteSpecGrpcRouteMatchMetadataMatchRange:
    def __init__(self, *, end: jsii.Number, start: jsii.Number) -> None:
        '''
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#end AppmeshRoute#end}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#start AppmeshRoute#start}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0afc9bf99631ae435b63555729c9537664ff68511dae32039f7cf65602346810)
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end": end,
            "start": start,
        }

    @builtins.property
    def end(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#end AppmeshRoute#end}.'''
        result = self._values.get("end")
        assert result is not None, "Required property 'end' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#start AppmeshRoute#start}.'''
        result = self._values.get("start")
        assert result is not None, "Required property 'start' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecGrpcRouteMatchMetadataMatchRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecGrpcRouteMatchMetadataMatchRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteMatchMetadataMatchRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b927e72155afbff00900149665f192e3025c856f9de21a473e995aa1ce552f83)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "end"))

    @end.setter
    def end(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__176a41e5f7f96cf10a88d7cce1d26a8d3e7251e817c6af8a08b2d00941c6d2ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "start"))

    @start.setter
    def start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baa813ff4c66187af0957a5b5177b33b46e759341e7b0a27c74c1960314e98da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshRouteSpecGrpcRouteMatchMetadataMatchRange]:
        return typing.cast(typing.Optional[AppmeshRouteSpecGrpcRouteMatchMetadataMatchRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecGrpcRouteMatchMetadataMatchRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff81a6a7b5b3ca08ce0d096ae4a8095dedc54f6bbdd4fd4580b403e5560a22a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecGrpcRouteMatchMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteMatchMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a96c6d1d7d98f50a67e0c915737628648c622ffb3cfefbff1e7634fee48a30bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        range: typing.Optional[typing.Union[AppmeshRouteSpecGrpcRouteMatchMetadataMatchRange, typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#prefix AppmeshRoute#prefix}.
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#range AppmeshRoute#range}
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#regex AppmeshRoute#regex}.
        :param suffix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#suffix AppmeshRoute#suffix}.
        '''
        value = AppmeshRouteSpecGrpcRouteMatchMetadataMatch(
            exact=exact, prefix=prefix, range=range, regex=regex, suffix=suffix
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="resetInvert")
    def reset_invert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvert", []))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> AppmeshRouteSpecGrpcRouteMatchMetadataMatchOutputReference:
        return typing.cast(AppmeshRouteSpecGrpcRouteMatchMetadataMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="invertInput")
    def invert_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invertInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(
        self,
    ) -> typing.Optional[AppmeshRouteSpecGrpcRouteMatchMetadataMatch]:
        return typing.cast(typing.Optional[AppmeshRouteSpecGrpcRouteMatchMetadataMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="invert")
    def invert(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invert"))

    @invert.setter
    def invert(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd65ecda8bfb888114eebed6f54ba7d55dca8d4e9f7dce5924a255caf2b9d01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f68e3f55e451503587a7a02d1239dc0733e5a0a679a801d07589d690563d4391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecGrpcRouteMatchMetadata]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecGrpcRouteMatchMetadata]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecGrpcRouteMatchMetadata]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4885a1e6bf19eb126e3dea53f7968a053102b2f8c435a543a4a9f23982016f32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecGrpcRouteMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0c93808ac81c6d8a0a147e6f123969c2c83810dcf16e6c61e6dbbc31099382f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetadata")
    def put_metadata(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecGrpcRouteMatchMetadata, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb682750ec8f5325c77bd1fae818fe8b4b96ac08d52a8841971dc7a53c5f3aa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetadata", [value]))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetMethodName")
    def reset_method_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethodName", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetServiceName")
    def reset_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceName", []))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> AppmeshRouteSpecGrpcRouteMatchMetadataList:
        return typing.cast(AppmeshRouteSpecGrpcRouteMatchMetadataList, jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecGrpcRouteMatchMetadata]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecGrpcRouteMatchMetadata]]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="methodNameInput")
    def method_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodNameInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="methodName")
    def method_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "methodName"))

    @method_name.setter
    def method_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3d0d1155d384ce658672d4aeeda93ca40ab3aa2f58f390afd3b6981840f9fea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "methodName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36260ab3804278d6a85014446cefdc16ed82a3bfb7efbe1f9d3bb07b1533ac30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1f12263cd2fa6fe7293641a4af91eaf1eec2924518f83b187291ee452ec5752)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e628707ea5bda1bd3c44e121c7475d450aebad6b175388a753f6dd1a94339d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecGrpcRouteMatch]:
        return typing.cast(typing.Optional[AppmeshRouteSpecGrpcRouteMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecGrpcRouteMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__564fb493defb927787b1aa151425ee094c12c4ffb9bd6031eaec2c0c2f141d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecGrpcRouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b35d4980808fa13346415b4625ea4ab779b882299a7f163eb152629201a92113)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        weighted_target: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecGrpcRouteActionWeightedTarget, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param weighted_target: weighted_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weighted_target AppmeshRoute#weighted_target}
        '''
        value = AppmeshRouteSpecGrpcRouteAction(weighted_target=weighted_target)

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        metadata: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecGrpcRouteMatchMetadata, typing.Dict[builtins.str, typing.Any]]]]] = None,
        method_name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        prefix: typing.Optional[builtins.str] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#metadata AppmeshRoute#metadata}
        :param method_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#method_name AppmeshRoute#method_name}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#prefix AppmeshRoute#prefix}.
        :param service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#service_name AppmeshRoute#service_name}.
        '''
        value = AppmeshRouteSpecGrpcRouteMatch(
            metadata=metadata,
            method_name=method_name,
            port=port,
            prefix=prefix,
            service_name=service_name,
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="putRetryPolicy")
    def put_retry_policy(
        self,
        *,
        max_retries: jsii.Number,
        per_retry_timeout: typing.Union["AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeout", typing.Dict[builtins.str, typing.Any]],
        grpc_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
        http_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
        tcp_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param max_retries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#max_retries AppmeshRoute#max_retries}.
        :param per_retry_timeout: per_retry_timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#per_retry_timeout AppmeshRoute#per_retry_timeout}
        :param grpc_retry_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#grpc_retry_events AppmeshRoute#grpc_retry_events}.
        :param http_retry_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#http_retry_events AppmeshRoute#http_retry_events}.
        :param tcp_retry_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#tcp_retry_events AppmeshRoute#tcp_retry_events}.
        '''
        value = AppmeshRouteSpecGrpcRouteRetryPolicy(
            max_retries=max_retries,
            per_retry_timeout=per_retry_timeout,
            grpc_retry_events=grpc_retry_events,
            http_retry_events=http_retry_events,
            tcp_retry_events=tcp_retry_events,
        )

        return typing.cast(None, jsii.invoke(self, "putRetryPolicy", [value]))

    @jsii.member(jsii_name="putTimeout")
    def put_timeout(
        self,
        *,
        idle: typing.Optional[typing.Union["AppmeshRouteSpecGrpcRouteTimeoutIdle", typing.Dict[builtins.str, typing.Any]]] = None,
        per_request: typing.Optional[typing.Union["AppmeshRouteSpecGrpcRouteTimeoutPerRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param idle: idle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#idle AppmeshRoute#idle}
        :param per_request: per_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#per_request AppmeshRoute#per_request}
        '''
        value = AppmeshRouteSpecGrpcRouteTimeout(idle=idle, per_request=per_request)

        return typing.cast(None, jsii.invoke(self, "putTimeout", [value]))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

    @jsii.member(jsii_name="resetRetryPolicy")
    def reset_retry_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryPolicy", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> AppmeshRouteSpecGrpcRouteActionOutputReference:
        return typing.cast(AppmeshRouteSpecGrpcRouteActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> AppmeshRouteSpecGrpcRouteMatchOutputReference:
        return typing.cast(AppmeshRouteSpecGrpcRouteMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicy")
    def retry_policy(self) -> "AppmeshRouteSpecGrpcRouteRetryPolicyOutputReference":
        return typing.cast("AppmeshRouteSpecGrpcRouteRetryPolicyOutputReference", jsii.get(self, "retryPolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> "AppmeshRouteSpecGrpcRouteTimeoutOutputReference":
        return typing.cast("AppmeshRouteSpecGrpcRouteTimeoutOutputReference", jsii.get(self, "timeout"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[AppmeshRouteSpecGrpcRouteAction]:
        return typing.cast(typing.Optional[AppmeshRouteSpecGrpcRouteAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[AppmeshRouteSpecGrpcRouteMatch]:
        return typing.cast(typing.Optional[AppmeshRouteSpecGrpcRouteMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicyInput")
    def retry_policy_input(
        self,
    ) -> typing.Optional["AppmeshRouteSpecGrpcRouteRetryPolicy"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecGrpcRouteRetryPolicy"], jsii.get(self, "retryPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional["AppmeshRouteSpecGrpcRouteTimeout"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecGrpcRouteTimeout"], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecGrpcRoute]:
        return typing.cast(typing.Optional[AppmeshRouteSpecGrpcRoute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AppmeshRouteSpecGrpcRoute]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3a4e65229082dd588d61cbbf6b97debb811e1466a642e2fbeb1b038071d88c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteRetryPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "max_retries": "maxRetries",
        "per_retry_timeout": "perRetryTimeout",
        "grpc_retry_events": "grpcRetryEvents",
        "http_retry_events": "httpRetryEvents",
        "tcp_retry_events": "tcpRetryEvents",
    },
)
class AppmeshRouteSpecGrpcRouteRetryPolicy:
    def __init__(
        self,
        *,
        max_retries: jsii.Number,
        per_retry_timeout: typing.Union["AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeout", typing.Dict[builtins.str, typing.Any]],
        grpc_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
        http_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
        tcp_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param max_retries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#max_retries AppmeshRoute#max_retries}.
        :param per_retry_timeout: per_retry_timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#per_retry_timeout AppmeshRoute#per_retry_timeout}
        :param grpc_retry_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#grpc_retry_events AppmeshRoute#grpc_retry_events}.
        :param http_retry_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#http_retry_events AppmeshRoute#http_retry_events}.
        :param tcp_retry_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#tcp_retry_events AppmeshRoute#tcp_retry_events}.
        '''
        if isinstance(per_retry_timeout, dict):
            per_retry_timeout = AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeout(**per_retry_timeout)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1413e14fc93eee39effb0388fc7806e69c59c54e7c8dc92ee6744441b59511d0)
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument per_retry_timeout", value=per_retry_timeout, expected_type=type_hints["per_retry_timeout"])
            check_type(argname="argument grpc_retry_events", value=grpc_retry_events, expected_type=type_hints["grpc_retry_events"])
            check_type(argname="argument http_retry_events", value=http_retry_events, expected_type=type_hints["http_retry_events"])
            check_type(argname="argument tcp_retry_events", value=tcp_retry_events, expected_type=type_hints["tcp_retry_events"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_retries": max_retries,
            "per_retry_timeout": per_retry_timeout,
        }
        if grpc_retry_events is not None:
            self._values["grpc_retry_events"] = grpc_retry_events
        if http_retry_events is not None:
            self._values["http_retry_events"] = http_retry_events
        if tcp_retry_events is not None:
            self._values["tcp_retry_events"] = tcp_retry_events

    @builtins.property
    def max_retries(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#max_retries AppmeshRoute#max_retries}.'''
        result = self._values.get("max_retries")
        assert result is not None, "Required property 'max_retries' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def per_retry_timeout(
        self,
    ) -> "AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeout":
        '''per_retry_timeout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#per_retry_timeout AppmeshRoute#per_retry_timeout}
        '''
        result = self._values.get("per_retry_timeout")
        assert result is not None, "Required property 'per_retry_timeout' is missing"
        return typing.cast("AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeout", result)

    @builtins.property
    def grpc_retry_events(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#grpc_retry_events AppmeshRoute#grpc_retry_events}.'''
        result = self._values.get("grpc_retry_events")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def http_retry_events(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#http_retry_events AppmeshRoute#http_retry_events}.'''
        result = self._values.get("http_retry_events")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tcp_retry_events(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#tcp_retry_events AppmeshRoute#tcp_retry_events}.'''
        result = self._values.get("tcp_retry_events")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecGrpcRouteRetryPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecGrpcRouteRetryPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteRetryPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12633761a61cd1b9bd3f50e5c72239c1785914487615c95a738695991998c196)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPerRetryTimeout")
    def put_per_retry_timeout(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        value_ = AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeout(
            unit=unit, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putPerRetryTimeout", [value_]))

    @jsii.member(jsii_name="resetGrpcRetryEvents")
    def reset_grpc_retry_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpcRetryEvents", []))

    @jsii.member(jsii_name="resetHttpRetryEvents")
    def reset_http_retry_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpRetryEvents", []))

    @jsii.member(jsii_name="resetTcpRetryEvents")
    def reset_tcp_retry_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpRetryEvents", []))

    @builtins.property
    @jsii.member(jsii_name="perRetryTimeout")
    def per_retry_timeout(
        self,
    ) -> "AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeoutOutputReference":
        return typing.cast("AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeoutOutputReference", jsii.get(self, "perRetryTimeout"))

    @builtins.property
    @jsii.member(jsii_name="grpcRetryEventsInput")
    def grpc_retry_events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "grpcRetryEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="httpRetryEventsInput")
    def http_retry_events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "httpRetryEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetriesInput")
    def max_retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetriesInput"))

    @builtins.property
    @jsii.member(jsii_name="perRetryTimeoutInput")
    def per_retry_timeout_input(
        self,
    ) -> typing.Optional["AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeout"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeout"], jsii.get(self, "perRetryTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpRetryEventsInput")
    def tcp_retry_events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tcpRetryEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcRetryEvents")
    def grpc_retry_events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "grpcRetryEvents"))

    @grpc_retry_events.setter
    def grpc_retry_events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b53bc0789436d1d403e3df3e4330c8812a5d816b6d2e49139c443ca339c586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grpcRetryEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpRetryEvents")
    def http_retry_events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "httpRetryEvents"))

    @http_retry_events.setter
    def http_retry_events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49a46f530cb45dc6d27f3d8695bbd59dcee6b3d3ed6f0d224e28640a095d703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpRetryEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a68afb5c0fba10bc486f6bf464340d98ebbca868482eb677e2665bc1d88345e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tcpRetryEvents")
    def tcp_retry_events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tcpRetryEvents"))

    @tcp_retry_events.setter
    def tcp_retry_events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a41e1e8602d39cf4cc4fff814300c8d62dd8c6612edeaa3dbd83f59caf89b29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tcpRetryEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecGrpcRouteRetryPolicy]:
        return typing.cast(typing.Optional[AppmeshRouteSpecGrpcRouteRetryPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecGrpcRouteRetryPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dbc37cdaef7efbd19bcce2c5913e4a165d6cddefc3bd2090a1c6eb11e327ce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeout",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeout:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29069b88535700ed2c40fccfea8a93b670dddd37990b9d5d93315adc0a05c984)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c9409b046efa07342acfb09ce20d326b100976a1d28d3f83f1648ad43ce6b5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14e894b042718ea1a964677555cfda28823d8e0ccd619c52a5bd04e6c38d2af5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e739b5f8c223c828c9bcf6de124db52980d98c4ccf01d8b76285f79c6f755f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeout]:
        return typing.cast(typing.Optional[AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de61cbadbb11247d6c15ab3a62daf7627d8713c96898b736c85c918c00970073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteTimeout",
    jsii_struct_bases=[],
    name_mapping={"idle": "idle", "per_request": "perRequest"},
)
class AppmeshRouteSpecGrpcRouteTimeout:
    def __init__(
        self,
        *,
        idle: typing.Optional[typing.Union["AppmeshRouteSpecGrpcRouteTimeoutIdle", typing.Dict[builtins.str, typing.Any]]] = None,
        per_request: typing.Optional[typing.Union["AppmeshRouteSpecGrpcRouteTimeoutPerRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param idle: idle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#idle AppmeshRoute#idle}
        :param per_request: per_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#per_request AppmeshRoute#per_request}
        '''
        if isinstance(idle, dict):
            idle = AppmeshRouteSpecGrpcRouteTimeoutIdle(**idle)
        if isinstance(per_request, dict):
            per_request = AppmeshRouteSpecGrpcRouteTimeoutPerRequest(**per_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c41f32f021e11d212657a0631f8f42b4958347cb0a710d7d1c7916de02e5226a)
            check_type(argname="argument idle", value=idle, expected_type=type_hints["idle"])
            check_type(argname="argument per_request", value=per_request, expected_type=type_hints["per_request"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if idle is not None:
            self._values["idle"] = idle
        if per_request is not None:
            self._values["per_request"] = per_request

    @builtins.property
    def idle(self) -> typing.Optional["AppmeshRouteSpecGrpcRouteTimeoutIdle"]:
        '''idle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#idle AppmeshRoute#idle}
        '''
        result = self._values.get("idle")
        return typing.cast(typing.Optional["AppmeshRouteSpecGrpcRouteTimeoutIdle"], result)

    @builtins.property
    def per_request(
        self,
    ) -> typing.Optional["AppmeshRouteSpecGrpcRouteTimeoutPerRequest"]:
        '''per_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#per_request AppmeshRoute#per_request}
        '''
        result = self._values.get("per_request")
        return typing.cast(typing.Optional["AppmeshRouteSpecGrpcRouteTimeoutPerRequest"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecGrpcRouteTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteTimeoutIdle",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshRouteSpecGrpcRouteTimeoutIdle:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d978bfd027c4091fc971fd1866f671e266e844391cfb00b87fcc45cf56ea0817)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecGrpcRouteTimeoutIdle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecGrpcRouteTimeoutIdleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteTimeoutIdleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3021067b06938b60431fe973a7ef6ead090e9833569b75200fb75c4bdcb06ecd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6d15d8771b3d2e9d104827cc6f6a8de69b76c0f93e0e94b9378e96378bde89b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b1dab5d6b710f98f1feb16793a9c8f0e908e831613875bbef6af3c74b0c1be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecGrpcRouteTimeoutIdle]:
        return typing.cast(typing.Optional[AppmeshRouteSpecGrpcRouteTimeoutIdle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecGrpcRouteTimeoutIdle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2374f7b9bba56b2eb62b4acc3bdfa01fa2e0894e75587683a6bff6b94750f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecGrpcRouteTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01d33039640ecda9b3b76d7f69fc66195da2824dd28267c0fc55a6db1b65da2d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIdle")
    def put_idle(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        value_ = AppmeshRouteSpecGrpcRouteTimeoutIdle(unit=unit, value=value)

        return typing.cast(None, jsii.invoke(self, "putIdle", [value_]))

    @jsii.member(jsii_name="putPerRequest")
    def put_per_request(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        value_ = AppmeshRouteSpecGrpcRouteTimeoutPerRequest(unit=unit, value=value)

        return typing.cast(None, jsii.invoke(self, "putPerRequest", [value_]))

    @jsii.member(jsii_name="resetIdle")
    def reset_idle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdle", []))

    @jsii.member(jsii_name="resetPerRequest")
    def reset_per_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerRequest", []))

    @builtins.property
    @jsii.member(jsii_name="idle")
    def idle(self) -> AppmeshRouteSpecGrpcRouteTimeoutIdleOutputReference:
        return typing.cast(AppmeshRouteSpecGrpcRouteTimeoutIdleOutputReference, jsii.get(self, "idle"))

    @builtins.property
    @jsii.member(jsii_name="perRequest")
    def per_request(
        self,
    ) -> "AppmeshRouteSpecGrpcRouteTimeoutPerRequestOutputReference":
        return typing.cast("AppmeshRouteSpecGrpcRouteTimeoutPerRequestOutputReference", jsii.get(self, "perRequest"))

    @builtins.property
    @jsii.member(jsii_name="idleInput")
    def idle_input(self) -> typing.Optional[AppmeshRouteSpecGrpcRouteTimeoutIdle]:
        return typing.cast(typing.Optional[AppmeshRouteSpecGrpcRouteTimeoutIdle], jsii.get(self, "idleInput"))

    @builtins.property
    @jsii.member(jsii_name="perRequestInput")
    def per_request_input(
        self,
    ) -> typing.Optional["AppmeshRouteSpecGrpcRouteTimeoutPerRequest"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecGrpcRouteTimeoutPerRequest"], jsii.get(self, "perRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecGrpcRouteTimeout]:
        return typing.cast(typing.Optional[AppmeshRouteSpecGrpcRouteTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecGrpcRouteTimeout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e091e7c58a9991f89fcd4eb2b98c88ba17c0110ed897a66f6e1db1b7bf2cf517)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteTimeoutPerRequest",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshRouteSpecGrpcRouteTimeoutPerRequest:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a4f0282d54764fcd61590a1475f483dc86ccda93340f602acf64ef95f7ac8c)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecGrpcRouteTimeoutPerRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecGrpcRouteTimeoutPerRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecGrpcRouteTimeoutPerRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e41352030233c811872c72c477068ad76d334e80460b07fdfa0cb6123e6e840c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72d833788d3c3c2fd1a3d5cee31f8c20dab691bfce9bca1e66676c14c7e166d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a3281a7f9b8f320e3db729460a6c7d702d6cd1ebdaec6db6f9a16350ac0e7f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshRouteSpecGrpcRouteTimeoutPerRequest]:
        return typing.cast(typing.Optional[AppmeshRouteSpecGrpcRouteTimeoutPerRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecGrpcRouteTimeoutPerRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65a389f957c16b81a207d2337f22c526b6bab0455fb3847227423e191454b2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2Route",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "match": "match",
        "retry_policy": "retryPolicy",
        "timeout": "timeout",
    },
)
class AppmeshRouteSpecHttp2Route:
    def __init__(
        self,
        *,
        action: typing.Union["AppmeshRouteSpecHttp2RouteAction", typing.Dict[builtins.str, typing.Any]],
        match: typing.Union["AppmeshRouteSpecHttp2RouteMatch", typing.Dict[builtins.str, typing.Any]],
        retry_policy: typing.Optional[typing.Union["AppmeshRouteSpecHttp2RouteRetryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[typing.Union["AppmeshRouteSpecHttp2RouteTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#action AppmeshRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#retry_policy AppmeshRoute#retry_policy}
        :param timeout: timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#timeout AppmeshRoute#timeout}
        '''
        if isinstance(action, dict):
            action = AppmeshRouteSpecHttp2RouteAction(**action)
        if isinstance(match, dict):
            match = AppmeshRouteSpecHttp2RouteMatch(**match)
        if isinstance(retry_policy, dict):
            retry_policy = AppmeshRouteSpecHttp2RouteRetryPolicy(**retry_policy)
        if isinstance(timeout, dict):
            timeout = AppmeshRouteSpecHttp2RouteTimeout(**timeout)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b55473d58b24eb99f14e4767c2ecb182cedb5421369433c9d494f01a48fa6af3)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument retry_policy", value=retry_policy, expected_type=type_hints["retry_policy"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "match": match,
        }
        if retry_policy is not None:
            self._values["retry_policy"] = retry_policy
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def action(self) -> "AppmeshRouteSpecHttp2RouteAction":
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#action AppmeshRoute#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("AppmeshRouteSpecHttp2RouteAction", result)

    @builtins.property
    def match(self) -> "AppmeshRouteSpecHttp2RouteMatch":
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("AppmeshRouteSpecHttp2RouteMatch", result)

    @builtins.property
    def retry_policy(self) -> typing.Optional["AppmeshRouteSpecHttp2RouteRetryPolicy"]:
        '''retry_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#retry_policy AppmeshRoute#retry_policy}
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional["AppmeshRouteSpecHttp2RouteRetryPolicy"], result)

    @builtins.property
    def timeout(self) -> typing.Optional["AppmeshRouteSpecHttp2RouteTimeout"]:
        '''timeout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#timeout AppmeshRoute#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional["AppmeshRouteSpecHttp2RouteTimeout"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttp2Route(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteAction",
    jsii_struct_bases=[],
    name_mapping={"weighted_target": "weightedTarget"},
)
class AppmeshRouteSpecHttp2RouteAction:
    def __init__(
        self,
        *,
        weighted_target: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshRouteSpecHttp2RouteActionWeightedTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param weighted_target: weighted_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weighted_target AppmeshRoute#weighted_target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee933731b1f1c9d5181adbbd7974dffdbf4c1098b0e757a4e079473541bdda4c)
            check_type(argname="argument weighted_target", value=weighted_target, expected_type=type_hints["weighted_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "weighted_target": weighted_target,
        }

    @builtins.property
    def weighted_target(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttp2RouteActionWeightedTarget"]]:
        '''weighted_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weighted_target AppmeshRoute#weighted_target}
        '''
        result = self._values.get("weighted_target")
        assert result is not None, "Required property 'weighted_target' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttp2RouteActionWeightedTarget"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttp2RouteAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttp2RouteActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__472759fedc8cfed1768db3b72f072cc2d021e46d60aa192bf2bb54846d426f29)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putWeightedTarget")
    def put_weighted_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshRouteSpecHttp2RouteActionWeightedTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8832c4bcb2f0755791fa169c2762e33900e467b01e36a34eb755f0cbcf465111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWeightedTarget", [value]))

    @builtins.property
    @jsii.member(jsii_name="weightedTarget")
    def weighted_target(self) -> "AppmeshRouteSpecHttp2RouteActionWeightedTargetList":
        return typing.cast("AppmeshRouteSpecHttp2RouteActionWeightedTargetList", jsii.get(self, "weightedTarget"))

    @builtins.property
    @jsii.member(jsii_name="weightedTargetInput")
    def weighted_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttp2RouteActionWeightedTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttp2RouteActionWeightedTarget"]]], jsii.get(self, "weightedTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecHttp2RouteAction]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttp2RouteAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttp2RouteAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71d602da6abb850b8ed8f9c96d2af4d544e11dfb386c2985ebc5345a123524ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteActionWeightedTarget",
    jsii_struct_bases=[],
    name_mapping={"virtual_node": "virtualNode", "weight": "weight", "port": "port"},
)
class AppmeshRouteSpecHttp2RouteActionWeightedTarget:
    def __init__(
        self,
        *,
        virtual_node: builtins.str,
        weight: jsii.Number,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param virtual_node: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#virtual_node AppmeshRoute#virtual_node}.
        :param weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weight AppmeshRoute#weight}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11e8a70d302cd479cfef42fb68244d48ba18d2a9c2ff219cf827863825018356)
            check_type(argname="argument virtual_node", value=virtual_node, expected_type=type_hints["virtual_node"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_node": virtual_node,
            "weight": weight,
        }
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def virtual_node(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#virtual_node AppmeshRoute#virtual_node}.'''
        result = self._values.get("virtual_node")
        assert result is not None, "Required property 'virtual_node' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def weight(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weight AppmeshRoute#weight}.'''
        result = self._values.get("weight")
        assert result is not None, "Required property 'weight' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttp2RouteActionWeightedTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttp2RouteActionWeightedTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteActionWeightedTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d14a096d9af81255e02d51030e03510a9ebbed88045e1cd7c39d14d4061ec525)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppmeshRouteSpecHttp2RouteActionWeightedTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc27cf9de415893f678ede7a69207fe17b9bc24a1ba610d4fcc7b5b47050fc23)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshRouteSpecHttp2RouteActionWeightedTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31ca5385e4baa90a0debf168d4a55d79f8e276099036aec2fec5c24a83779857)
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
            type_hints = typing.get_type_hints(_typecheckingstub__917dfb2604b07ca24209b59c5209759a05cc5008d076ba3803da125b08ce6ad2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91b0e1ef154e3d64507b9c1b95c2b68157535666f243019b293ad578269841a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttp2RouteActionWeightedTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttp2RouteActionWeightedTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttp2RouteActionWeightedTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9692d7275530748b2983052ce6d1511384310760481804bd596a0c82fde47e07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecHttp2RouteActionWeightedTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteActionWeightedTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29a3b3881e7e158b22d676a0388fcefe4498fafe7b3be1f2ddf4c2f3b899de41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNodeInput")
    def virtual_node_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__645173082439041f2b981f02b0e150a242d179acd78474da81000158e276ebae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNode")
    def virtual_node(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNode"))

    @virtual_node.setter
    def virtual_node(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70db9bf493b0eeaeb2dd9d67692446514b2959473f03442cdb3b4ef2c0e2faf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d51aa1d05b02e1b0e214d85c98e8c29c90697e41513e2e7ea7efc1f434fa1ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttp2RouteActionWeightedTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttp2RouteActionWeightedTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttp2RouteActionWeightedTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e027421aded2ad8ee90b7b6d1b809aebeea89cc4da25d03b5a2d959daebf665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteMatch",
    jsii_struct_bases=[],
    name_mapping={
        "header": "header",
        "method": "method",
        "path": "path",
        "port": "port",
        "prefix": "prefix",
        "query_parameter": "queryParameter",
        "scheme": "scheme",
    },
)
class AppmeshRouteSpecHttp2RouteMatch:
    def __init__(
        self,
        *,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshRouteSpecHttp2RouteMatchHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        method: typing.Optional[builtins.str] = None,
        path: typing.Optional[typing.Union["AppmeshRouteSpecHttp2RouteMatchPath", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        prefix: typing.Optional[builtins.str] = None,
        query_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshRouteSpecHttp2RouteMatchQueryParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#header AppmeshRoute#header}
        :param method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#method AppmeshRoute#method}.
        :param path: path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#path AppmeshRoute#path}
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#prefix AppmeshRoute#prefix}.
        :param query_parameter: query_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#query_parameter AppmeshRoute#query_parameter}
        :param scheme: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#scheme AppmeshRoute#scheme}.
        '''
        if isinstance(path, dict):
            path = AppmeshRouteSpecHttp2RouteMatchPath(**path)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc12609ffd8b048bbe0f2ed51abf848d9e1f9eb551f602b1b0c708a734c083ef)
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument query_parameter", value=query_parameter, expected_type=type_hints["query_parameter"])
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header is not None:
            self._values["header"] = header
        if method is not None:
            self._values["method"] = method
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if prefix is not None:
            self._values["prefix"] = prefix
        if query_parameter is not None:
            self._values["query_parameter"] = query_parameter
        if scheme is not None:
            self._values["scheme"] = scheme

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttp2RouteMatchHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#header AppmeshRoute#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttp2RouteMatchHeader"]]], result)

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#method AppmeshRoute#method}.'''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional["AppmeshRouteSpecHttp2RouteMatchPath"]:
        '''path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#path AppmeshRoute#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional["AppmeshRouteSpecHttp2RouteMatchPath"], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#prefix AppmeshRoute#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttp2RouteMatchQueryParameter"]]]:
        '''query_parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#query_parameter AppmeshRoute#query_parameter}
        '''
        result = self._values.get("query_parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttp2RouteMatchQueryParameter"]]], result)

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#scheme AppmeshRoute#scheme}.'''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttp2RouteMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteMatchHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "invert": "invert", "match": "match"},
)
class AppmeshRouteSpecHttp2RouteMatchHeader:
    def __init__(
        self,
        *,
        name: builtins.str,
        invert: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        match: typing.Optional[typing.Union["AppmeshRouteSpecHttp2RouteMatchHeaderMatch", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#name AppmeshRoute#name}.
        :param invert: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#invert AppmeshRoute#invert}.
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        '''
        if isinstance(match, dict):
            match = AppmeshRouteSpecHttp2RouteMatchHeaderMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__031e0801333c9ab9e4f6abd1a89222fbe64d9c4d9cfa7241db26dc3b3790b402)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument invert", value=invert, expected_type=type_hints["invert"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if invert is not None:
            self._values["invert"] = invert
        if match is not None:
            self._values["match"] = match

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#name AppmeshRoute#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def invert(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#invert AppmeshRoute#invert}.'''
        result = self._values.get("invert")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def match(self) -> typing.Optional["AppmeshRouteSpecHttp2RouteMatchHeaderMatch"]:
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional["AppmeshRouteSpecHttp2RouteMatchHeaderMatch"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttp2RouteMatchHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttp2RouteMatchHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteMatchHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df2beaccb0552b637a178cab9bd23969f32aaf8dd6a4124a1cd2df1b2f923762)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppmeshRouteSpecHttp2RouteMatchHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc3447db7abe177279ff32397bcd35318ca3635633d30c5449c937de8bb17bc1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshRouteSpecHttp2RouteMatchHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da385d5b84908dc6b204e29b350fae231a430cc07fd19bedc6961c7412636c74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bec786c788b414c4b9ff1069c0b48970e70eddc47a31109586770e8b11519147)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c41bfa1737a6ac02941ea2191c76c7f0ced764a93596fa4dbe00d333b647575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttp2RouteMatchHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttp2RouteMatchHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttp2RouteMatchHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7234348140d715ec2d4a451243f4fd83048a6c2203dad838574ed46abafa3c22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteMatchHeaderMatch",
    jsii_struct_bases=[],
    name_mapping={
        "exact": "exact",
        "prefix": "prefix",
        "range": "range",
        "regex": "regex",
        "suffix": "suffix",
    },
)
class AppmeshRouteSpecHttp2RouteMatchHeaderMatch:
    def __init__(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        range: typing.Optional[typing.Union["AppmeshRouteSpecHttp2RouteMatchHeaderMatchRange", typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#prefix AppmeshRoute#prefix}.
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#range AppmeshRoute#range}
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#regex AppmeshRoute#regex}.
        :param suffix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#suffix AppmeshRoute#suffix}.
        '''
        if isinstance(range, dict):
            range = AppmeshRouteSpecHttp2RouteMatchHeaderMatchRange(**range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad9e7fd0b4dc814fe78cc27cd28fe0ecac9f9bc0f9ffb0ad2e1afb9439ba706c)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exact is not None:
            self._values["exact"] = exact
        if prefix is not None:
            self._values["prefix"] = prefix
        if range is not None:
            self._values["range"] = range
        if regex is not None:
            self._values["regex"] = regex
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.'''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#prefix AppmeshRoute#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range(
        self,
    ) -> typing.Optional["AppmeshRouteSpecHttp2RouteMatchHeaderMatchRange"]:
        '''range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#range AppmeshRoute#range}
        '''
        result = self._values.get("range")
        return typing.cast(typing.Optional["AppmeshRouteSpecHttp2RouteMatchHeaderMatchRange"], result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#regex AppmeshRoute#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#suffix AppmeshRoute#suffix}.'''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttp2RouteMatchHeaderMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttp2RouteMatchHeaderMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteMatchHeaderMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82ee4e09122f9143698676a7b184b54d20f933d73070b38b7555e5b8c551e8d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRange")
    def put_range(self, *, end: jsii.Number, start: jsii.Number) -> None:
        '''
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#end AppmeshRoute#end}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#start AppmeshRoute#start}.
        '''
        value = AppmeshRouteSpecHttp2RouteMatchHeaderMatchRange(end=end, start=start)

        return typing.cast(None, jsii.invoke(self, "putRange", [value]))

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetRange")
    def reset_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRange", []))

    @jsii.member(jsii_name="resetRegex")
    def reset_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegex", []))

    @jsii.member(jsii_name="resetSuffix")
    def reset_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(self) -> "AppmeshRouteSpecHttp2RouteMatchHeaderMatchRangeOutputReference":
        return typing.cast("AppmeshRouteSpecHttp2RouteMatchHeaderMatchRangeOutputReference", jsii.get(self, "range"))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(
        self,
    ) -> typing.Optional["AppmeshRouteSpecHttp2RouteMatchHeaderMatchRange"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecHttp2RouteMatchHeaderMatchRange"], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="suffixInput")
    def suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suffixInput"))

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2439f994bedda0e589fafbc1170b8c1ab52411d5f2ffc5f274b424d6dac6e054)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e972cd9e5c05b16e57e5cca53eae075f4290e621b59f22dac2d5c96be7c15e1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ef77c116e38dcf36e873eda242ea9485c5886736c2d9a77a1311476389e68f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4668bb1c7260f11280e11751d681f1b440f8a8cee515eb555968c0f95d844397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshRouteSpecHttp2RouteMatchHeaderMatch]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttp2RouteMatchHeaderMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttp2RouteMatchHeaderMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3f4cb1e49dfc248926045706d736637be6be2d129c268f22f135bef9240efd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteMatchHeaderMatchRange",
    jsii_struct_bases=[],
    name_mapping={"end": "end", "start": "start"},
)
class AppmeshRouteSpecHttp2RouteMatchHeaderMatchRange:
    def __init__(self, *, end: jsii.Number, start: jsii.Number) -> None:
        '''
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#end AppmeshRoute#end}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#start AppmeshRoute#start}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6669eacf273560fbc62e70a5a73ead3467504890c5279260563af593c2ed63a7)
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end": end,
            "start": start,
        }

    @builtins.property
    def end(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#end AppmeshRoute#end}.'''
        result = self._values.get("end")
        assert result is not None, "Required property 'end' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#start AppmeshRoute#start}.'''
        result = self._values.get("start")
        assert result is not None, "Required property 'start' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttp2RouteMatchHeaderMatchRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttp2RouteMatchHeaderMatchRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteMatchHeaderMatchRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10ec4ad9cac2f951d9203410e2e3ba065ce44d801ce7ec33c9b984ead9172b50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "end"))

    @end.setter
    def end(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5a870752783485f225d0a8eeadc397d24b2938462f40a23e644be8f8febd17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "start"))

    @start.setter
    def start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65e3af8905d8013299291de419526b302d19c4658ebd58efc3da026ca52832af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshRouteSpecHttp2RouteMatchHeaderMatchRange]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttp2RouteMatchHeaderMatchRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttp2RouteMatchHeaderMatchRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f837abf20a511cf3a7a1e66f2f034919550d5c13998ca8b9f5210cb881eacfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecHttp2RouteMatchHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteMatchHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6f29845cc7b8245ad3dcfbbc9b8852656c4d8b420e4c26c8efa4f263bdb333b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        range: typing.Optional[typing.Union[AppmeshRouteSpecHttp2RouteMatchHeaderMatchRange, typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#prefix AppmeshRoute#prefix}.
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#range AppmeshRoute#range}
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#regex AppmeshRoute#regex}.
        :param suffix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#suffix AppmeshRoute#suffix}.
        '''
        value = AppmeshRouteSpecHttp2RouteMatchHeaderMatch(
            exact=exact, prefix=prefix, range=range, regex=regex, suffix=suffix
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="resetInvert")
    def reset_invert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvert", []))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> AppmeshRouteSpecHttp2RouteMatchHeaderMatchOutputReference:
        return typing.cast(AppmeshRouteSpecHttp2RouteMatchHeaderMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="invertInput")
    def invert_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invertInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(
        self,
    ) -> typing.Optional[AppmeshRouteSpecHttp2RouteMatchHeaderMatch]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttp2RouteMatchHeaderMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="invert")
    def invert(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invert"))

    @invert.setter
    def invert(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e81867a18cce568e1c95df44f8f30d5e5265e62b3d8df53a520d8d71e83245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f14b2b02027a355eebc7b40b17eae2a87ee8eb70952150a336152bf4b826beb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttp2RouteMatchHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttp2RouteMatchHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttp2RouteMatchHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abd5f1a556ab1af8704508935cf82c244b7d93f4bf7eeccc0f072665740c6b9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecHttp2RouteMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f608bc2a25d3733ffe02c05799b4a512bed0800987a629f4b0861ea7e518450)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttp2RouteMatchHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e7e1ccd2d7f402760325ae8c221bc0a07acc1caa32fbdf3ee993d2572e364f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="putPath")
    def put_path(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#regex AppmeshRoute#regex}.
        '''
        value = AppmeshRouteSpecHttp2RouteMatchPath(exact=exact, regex=regex)

        return typing.cast(None, jsii.invoke(self, "putPath", [value]))

    @jsii.member(jsii_name="putQueryParameter")
    def put_query_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshRouteSpecHttp2RouteMatchQueryParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d95db041f2718d04864fbcdca9c1f9cc1cd24e458f743ab87786820722eda9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQueryParameter", [value]))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetQueryParameter")
    def reset_query_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryParameter", []))

    @jsii.member(jsii_name="resetScheme")
    def reset_scheme(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheme", []))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> AppmeshRouteSpecHttp2RouteMatchHeaderList:
        return typing.cast(AppmeshRouteSpecHttp2RouteMatchHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> "AppmeshRouteSpecHttp2RouteMatchPathOutputReference":
        return typing.cast("AppmeshRouteSpecHttp2RouteMatchPathOutputReference", jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="queryParameter")
    def query_parameter(self) -> "AppmeshRouteSpecHttp2RouteMatchQueryParameterList":
        return typing.cast("AppmeshRouteSpecHttp2RouteMatchQueryParameterList", jsii.get(self, "queryParameter"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttp2RouteMatchHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttp2RouteMatchHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional["AppmeshRouteSpecHttp2RouteMatchPath"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecHttp2RouteMatchPath"], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="queryParameterInput")
    def query_parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttp2RouteMatchQueryParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttp2RouteMatchQueryParameter"]]], jsii.get(self, "queryParameterInput"))

    @builtins.property
    @jsii.member(jsii_name="schemeInput")
    def scheme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemeInput"))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24714c82e2dd390f5c66a0243193419db81241d0e9848c1f8d4e32927c89f8b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7029381d454584e5b347857c8e3449fbf87ddcb36683e02d39ed16c9cc3b3284)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17069898db90cf2d541c809e43d39b59a15aa68e854854835f5e413df12a9de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheme"))

    @scheme.setter
    def scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0448ace646e446805908877f5f16d1acd03ee380d09146e2c1155e4aec43b86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecHttp2RouteMatch]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttp2RouteMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttp2RouteMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c03bf2eba240dc2dd683446a542049ae66764978c65536f64d18e47feb2387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteMatchPath",
    jsii_struct_bases=[],
    name_mapping={"exact": "exact", "regex": "regex"},
)
class AppmeshRouteSpecHttp2RouteMatchPath:
    def __init__(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#regex AppmeshRoute#regex}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2034d172255f6a6ad1dd4802d1141f0b25707c417a6587c2fe5508cfe4292d8d)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exact is not None:
            self._values["exact"] = exact
        if regex is not None:
            self._values["regex"] = regex

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.'''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#regex AppmeshRoute#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttp2RouteMatchPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttp2RouteMatchPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteMatchPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ac777135aeb245dd7e477f79cbf034335e9d89c63e787e2d403fa9ac8f1e004)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetRegex")
    def reset_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegex", []))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f281521f7071b05bce0e0c48f21b7d2188e5e4ade06c9812db508d24850c13a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__974975e54c0bab42a3c327755573ec2838dc45cf63431d12efa91e48b9f1dae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecHttp2RouteMatchPath]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttp2RouteMatchPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttp2RouteMatchPath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e04aea31e5992318a2e7f9f851af7e34b36864bcf3ae285189a22ce79ff707a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteMatchQueryParameter",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "match": "match"},
)
class AppmeshRouteSpecHttp2RouteMatchQueryParameter:
    def __init__(
        self,
        *,
        name: builtins.str,
        match: typing.Optional[typing.Union["AppmeshRouteSpecHttp2RouteMatchQueryParameterMatch", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#name AppmeshRoute#name}.
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        '''
        if isinstance(match, dict):
            match = AppmeshRouteSpecHttp2RouteMatchQueryParameterMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41a7964da47fa649d7d27de019a8282ec7afb82edeb3ee44364431ab64185c99)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if match is not None:
            self._values["match"] = match

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#name AppmeshRoute#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match(
        self,
    ) -> typing.Optional["AppmeshRouteSpecHttp2RouteMatchQueryParameterMatch"]:
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional["AppmeshRouteSpecHttp2RouteMatchQueryParameterMatch"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttp2RouteMatchQueryParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttp2RouteMatchQueryParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteMatchQueryParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4966074ce864e7f11915a9fd74d4ab3b02090829bd5de8f15b0f65260bf0b4c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppmeshRouteSpecHttp2RouteMatchQueryParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__475ac4e9de7acb4d025f1092af7e047f4ed1c7419819a8df667f1d2855a153e5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshRouteSpecHttp2RouteMatchQueryParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4700d2be3f51357d0dbbb19dc407e3765aeb93205a508d3f52ab09fc1ceaa90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb4f3caaf3faab5d87a7a132ecfc4ce46e5828b19e48f2a32db6d4c6289abbee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__644c72048e79eec062854f516d2f179237a586db108b2cb28bdbed3206e92fce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttp2RouteMatchQueryParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttp2RouteMatchQueryParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttp2RouteMatchQueryParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aac4705e8751dc879a602b31d60cc40d717782bb784a3bc1c1ef466e8e5a81ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteMatchQueryParameterMatch",
    jsii_struct_bases=[],
    name_mapping={"exact": "exact"},
)
class AppmeshRouteSpecHttp2RouteMatchQueryParameterMatch:
    def __init__(self, *, exact: typing.Optional[builtins.str] = None) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caf734ac2f04e5ddb5b1823e7e9ba0a6460fcfeb35c604ac07163319c5a15a1b)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exact is not None:
            self._values["exact"] = exact

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.'''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttp2RouteMatchQueryParameterMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttp2RouteMatchQueryParameterMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteMatchQueryParameterMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87799587782a5506e64bbe1b94800a489031d0d540b5ab3fd540c7ea24281af1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20dcc629254c49ba98be81294bc088954650bfba614abc1d28a8e723b88156a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshRouteSpecHttp2RouteMatchQueryParameterMatch]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttp2RouteMatchQueryParameterMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttp2RouteMatchQueryParameterMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f34dee27fbb937b65c4c614b9ca03bf074dd4f017483ad08c3197398908d28b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecHttp2RouteMatchQueryParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteMatchQueryParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__673ed2c0d5e42d2b225824c1e1fe32f4494329a7ca886517b98e3b2789b6987b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatch")
    def put_match(self, *, exact: typing.Optional[builtins.str] = None) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.
        '''
        value = AppmeshRouteSpecHttp2RouteMatchQueryParameterMatch(exact=exact)

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(
        self,
    ) -> AppmeshRouteSpecHttp2RouteMatchQueryParameterMatchOutputReference:
        return typing.cast(AppmeshRouteSpecHttp2RouteMatchQueryParameterMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(
        self,
    ) -> typing.Optional[AppmeshRouteSpecHttp2RouteMatchQueryParameterMatch]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttp2RouteMatchQueryParameterMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8578f8fdd0d1df8cf5ac04440807f08e0d36b7e78a6ee333c08ccdb0effccb88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttp2RouteMatchQueryParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttp2RouteMatchQueryParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttp2RouteMatchQueryParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__885847ae6d8157267114372a428307738bd3a8e904610b44b1a0ff472c8f446f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecHttp2RouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b8309f6847ec7b0d02d47517e09b26a6bbc9d092a33d95b51c961cb7b7bec25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        weighted_target: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttp2RouteActionWeightedTarget, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param weighted_target: weighted_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weighted_target AppmeshRoute#weighted_target}
        '''
        value = AppmeshRouteSpecHttp2RouteAction(weighted_target=weighted_target)

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttp2RouteMatchHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
        method: typing.Optional[builtins.str] = None,
        path: typing.Optional[typing.Union[AppmeshRouteSpecHttp2RouteMatchPath, typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        prefix: typing.Optional[builtins.str] = None,
        query_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttp2RouteMatchQueryParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#header AppmeshRoute#header}
        :param method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#method AppmeshRoute#method}.
        :param path: path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#path AppmeshRoute#path}
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#prefix AppmeshRoute#prefix}.
        :param query_parameter: query_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#query_parameter AppmeshRoute#query_parameter}
        :param scheme: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#scheme AppmeshRoute#scheme}.
        '''
        value = AppmeshRouteSpecHttp2RouteMatch(
            header=header,
            method=method,
            path=path,
            port=port,
            prefix=prefix,
            query_parameter=query_parameter,
            scheme=scheme,
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="putRetryPolicy")
    def put_retry_policy(
        self,
        *,
        max_retries: jsii.Number,
        per_retry_timeout: typing.Union["AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeout", typing.Dict[builtins.str, typing.Any]],
        http_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
        tcp_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param max_retries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#max_retries AppmeshRoute#max_retries}.
        :param per_retry_timeout: per_retry_timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#per_retry_timeout AppmeshRoute#per_retry_timeout}
        :param http_retry_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#http_retry_events AppmeshRoute#http_retry_events}.
        :param tcp_retry_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#tcp_retry_events AppmeshRoute#tcp_retry_events}.
        '''
        value = AppmeshRouteSpecHttp2RouteRetryPolicy(
            max_retries=max_retries,
            per_retry_timeout=per_retry_timeout,
            http_retry_events=http_retry_events,
            tcp_retry_events=tcp_retry_events,
        )

        return typing.cast(None, jsii.invoke(self, "putRetryPolicy", [value]))

    @jsii.member(jsii_name="putTimeout")
    def put_timeout(
        self,
        *,
        idle: typing.Optional[typing.Union["AppmeshRouteSpecHttp2RouteTimeoutIdle", typing.Dict[builtins.str, typing.Any]]] = None,
        per_request: typing.Optional[typing.Union["AppmeshRouteSpecHttp2RouteTimeoutPerRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param idle: idle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#idle AppmeshRoute#idle}
        :param per_request: per_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#per_request AppmeshRoute#per_request}
        '''
        value = AppmeshRouteSpecHttp2RouteTimeout(idle=idle, per_request=per_request)

        return typing.cast(None, jsii.invoke(self, "putTimeout", [value]))

    @jsii.member(jsii_name="resetRetryPolicy")
    def reset_retry_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryPolicy", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> AppmeshRouteSpecHttp2RouteActionOutputReference:
        return typing.cast(AppmeshRouteSpecHttp2RouteActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> AppmeshRouteSpecHttp2RouteMatchOutputReference:
        return typing.cast(AppmeshRouteSpecHttp2RouteMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicy")
    def retry_policy(self) -> "AppmeshRouteSpecHttp2RouteRetryPolicyOutputReference":
        return typing.cast("AppmeshRouteSpecHttp2RouteRetryPolicyOutputReference", jsii.get(self, "retryPolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> "AppmeshRouteSpecHttp2RouteTimeoutOutputReference":
        return typing.cast("AppmeshRouteSpecHttp2RouteTimeoutOutputReference", jsii.get(self, "timeout"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[AppmeshRouteSpecHttp2RouteAction]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttp2RouteAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[AppmeshRouteSpecHttp2RouteMatch]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttp2RouteMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicyInput")
    def retry_policy_input(
        self,
    ) -> typing.Optional["AppmeshRouteSpecHttp2RouteRetryPolicy"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecHttp2RouteRetryPolicy"], jsii.get(self, "retryPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional["AppmeshRouteSpecHttp2RouteTimeout"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecHttp2RouteTimeout"], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecHttp2Route]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttp2Route], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttp2Route],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5197336aaad2f09bbe1770c9efdb3dd136f8bf32aa873f570c1e80c1600268b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteRetryPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "max_retries": "maxRetries",
        "per_retry_timeout": "perRetryTimeout",
        "http_retry_events": "httpRetryEvents",
        "tcp_retry_events": "tcpRetryEvents",
    },
)
class AppmeshRouteSpecHttp2RouteRetryPolicy:
    def __init__(
        self,
        *,
        max_retries: jsii.Number,
        per_retry_timeout: typing.Union["AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeout", typing.Dict[builtins.str, typing.Any]],
        http_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
        tcp_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param max_retries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#max_retries AppmeshRoute#max_retries}.
        :param per_retry_timeout: per_retry_timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#per_retry_timeout AppmeshRoute#per_retry_timeout}
        :param http_retry_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#http_retry_events AppmeshRoute#http_retry_events}.
        :param tcp_retry_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#tcp_retry_events AppmeshRoute#tcp_retry_events}.
        '''
        if isinstance(per_retry_timeout, dict):
            per_retry_timeout = AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeout(**per_retry_timeout)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b28cbc45eed18fea697098861e1b58ca77a0744d0222e846f112f26ef982fc5)
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument per_retry_timeout", value=per_retry_timeout, expected_type=type_hints["per_retry_timeout"])
            check_type(argname="argument http_retry_events", value=http_retry_events, expected_type=type_hints["http_retry_events"])
            check_type(argname="argument tcp_retry_events", value=tcp_retry_events, expected_type=type_hints["tcp_retry_events"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_retries": max_retries,
            "per_retry_timeout": per_retry_timeout,
        }
        if http_retry_events is not None:
            self._values["http_retry_events"] = http_retry_events
        if tcp_retry_events is not None:
            self._values["tcp_retry_events"] = tcp_retry_events

    @builtins.property
    def max_retries(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#max_retries AppmeshRoute#max_retries}.'''
        result = self._values.get("max_retries")
        assert result is not None, "Required property 'max_retries' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def per_retry_timeout(
        self,
    ) -> "AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeout":
        '''per_retry_timeout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#per_retry_timeout AppmeshRoute#per_retry_timeout}
        '''
        result = self._values.get("per_retry_timeout")
        assert result is not None, "Required property 'per_retry_timeout' is missing"
        return typing.cast("AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeout", result)

    @builtins.property
    def http_retry_events(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#http_retry_events AppmeshRoute#http_retry_events}.'''
        result = self._values.get("http_retry_events")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tcp_retry_events(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#tcp_retry_events AppmeshRoute#tcp_retry_events}.'''
        result = self._values.get("tcp_retry_events")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttp2RouteRetryPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttp2RouteRetryPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteRetryPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b47a405eb13bcfb096e04f299d88244757b36b77bddfcb249d140fe3d2e8257a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPerRetryTimeout")
    def put_per_retry_timeout(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        value_ = AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeout(
            unit=unit, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putPerRetryTimeout", [value_]))

    @jsii.member(jsii_name="resetHttpRetryEvents")
    def reset_http_retry_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpRetryEvents", []))

    @jsii.member(jsii_name="resetTcpRetryEvents")
    def reset_tcp_retry_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpRetryEvents", []))

    @builtins.property
    @jsii.member(jsii_name="perRetryTimeout")
    def per_retry_timeout(
        self,
    ) -> "AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeoutOutputReference":
        return typing.cast("AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeoutOutputReference", jsii.get(self, "perRetryTimeout"))

    @builtins.property
    @jsii.member(jsii_name="httpRetryEventsInput")
    def http_retry_events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "httpRetryEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetriesInput")
    def max_retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetriesInput"))

    @builtins.property
    @jsii.member(jsii_name="perRetryTimeoutInput")
    def per_retry_timeout_input(
        self,
    ) -> typing.Optional["AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeout"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeout"], jsii.get(self, "perRetryTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpRetryEventsInput")
    def tcp_retry_events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tcpRetryEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="httpRetryEvents")
    def http_retry_events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "httpRetryEvents"))

    @http_retry_events.setter
    def http_retry_events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4092a8975d9c3089886373e47f3e1ef7a45be63a9ab0d6f1f1171b88614d798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpRetryEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d6e6e469c0bf256e7fd8c6ccc5741d6bc0513baed4b605f4d8a358b25ca1f2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tcpRetryEvents")
    def tcp_retry_events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tcpRetryEvents"))

    @tcp_retry_events.setter
    def tcp_retry_events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c71a4cf6b846278c9cccc418af3411331f486ed885423ec258ecc26c5162d28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tcpRetryEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecHttp2RouteRetryPolicy]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttp2RouteRetryPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttp2RouteRetryPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb639ea1b797ba9d53b454336e9d153d1717d4faabb123104d27d55a0d22869d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeout",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeout:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93d208ab9afa282e201344e3a9091c40a6915548d7dec71f75ded404cdf7c9c)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fd16df750740a8312f27750ff370bb070afbe7f094088932796de8818e0d10d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e0a92b2e11a60d8a9b2b936926e82e3dec2b1403c57a4225437c18dd6666372)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b2dae1977eac86ea18d75b282b90a9db9f4347592bd8e80e5151df0c9acadac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeout]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51137cc26698cc683bdf74d67cbd8ca5350ca075f2a18d11d94a7b1951c23c68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteTimeout",
    jsii_struct_bases=[],
    name_mapping={"idle": "idle", "per_request": "perRequest"},
)
class AppmeshRouteSpecHttp2RouteTimeout:
    def __init__(
        self,
        *,
        idle: typing.Optional[typing.Union["AppmeshRouteSpecHttp2RouteTimeoutIdle", typing.Dict[builtins.str, typing.Any]]] = None,
        per_request: typing.Optional[typing.Union["AppmeshRouteSpecHttp2RouteTimeoutPerRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param idle: idle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#idle AppmeshRoute#idle}
        :param per_request: per_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#per_request AppmeshRoute#per_request}
        '''
        if isinstance(idle, dict):
            idle = AppmeshRouteSpecHttp2RouteTimeoutIdle(**idle)
        if isinstance(per_request, dict):
            per_request = AppmeshRouteSpecHttp2RouteTimeoutPerRequest(**per_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c4e4580ffce5a359985ad1c622877b5b5dea44afb003f629117153ee78f6e0f)
            check_type(argname="argument idle", value=idle, expected_type=type_hints["idle"])
            check_type(argname="argument per_request", value=per_request, expected_type=type_hints["per_request"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if idle is not None:
            self._values["idle"] = idle
        if per_request is not None:
            self._values["per_request"] = per_request

    @builtins.property
    def idle(self) -> typing.Optional["AppmeshRouteSpecHttp2RouteTimeoutIdle"]:
        '''idle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#idle AppmeshRoute#idle}
        '''
        result = self._values.get("idle")
        return typing.cast(typing.Optional["AppmeshRouteSpecHttp2RouteTimeoutIdle"], result)

    @builtins.property
    def per_request(
        self,
    ) -> typing.Optional["AppmeshRouteSpecHttp2RouteTimeoutPerRequest"]:
        '''per_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#per_request AppmeshRoute#per_request}
        '''
        result = self._values.get("per_request")
        return typing.cast(typing.Optional["AppmeshRouteSpecHttp2RouteTimeoutPerRequest"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttp2RouteTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteTimeoutIdle",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshRouteSpecHttp2RouteTimeoutIdle:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f054045eb3f2f888eeac53d5da8a08011b72e4c4189fa08da256417dd90f1269)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttp2RouteTimeoutIdle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttp2RouteTimeoutIdleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteTimeoutIdleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c89a1262682abadee4a1ab5ebdcba062685671e6bc677766b59909e3db08de04)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4192c3f3efd34974f8bef6932b264ab617e564f3655c2ecef2757afed234f8d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783189080c91d0d33f0f12822880d6aea831b63fa9def6adf70bb19203249568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecHttp2RouteTimeoutIdle]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttp2RouteTimeoutIdle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttp2RouteTimeoutIdle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d4f749db2bf258291c735b21603c87d80197492de3b26727cde709afca67fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecHttp2RouteTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e585f731b1c5cfa5d41c15e5cd3176b5f49680613b40183d690e9d1ed41cf975)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIdle")
    def put_idle(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        value_ = AppmeshRouteSpecHttp2RouteTimeoutIdle(unit=unit, value=value)

        return typing.cast(None, jsii.invoke(self, "putIdle", [value_]))

    @jsii.member(jsii_name="putPerRequest")
    def put_per_request(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        value_ = AppmeshRouteSpecHttp2RouteTimeoutPerRequest(unit=unit, value=value)

        return typing.cast(None, jsii.invoke(self, "putPerRequest", [value_]))

    @jsii.member(jsii_name="resetIdle")
    def reset_idle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdle", []))

    @jsii.member(jsii_name="resetPerRequest")
    def reset_per_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerRequest", []))

    @builtins.property
    @jsii.member(jsii_name="idle")
    def idle(self) -> AppmeshRouteSpecHttp2RouteTimeoutIdleOutputReference:
        return typing.cast(AppmeshRouteSpecHttp2RouteTimeoutIdleOutputReference, jsii.get(self, "idle"))

    @builtins.property
    @jsii.member(jsii_name="perRequest")
    def per_request(
        self,
    ) -> "AppmeshRouteSpecHttp2RouteTimeoutPerRequestOutputReference":
        return typing.cast("AppmeshRouteSpecHttp2RouteTimeoutPerRequestOutputReference", jsii.get(self, "perRequest"))

    @builtins.property
    @jsii.member(jsii_name="idleInput")
    def idle_input(self) -> typing.Optional[AppmeshRouteSpecHttp2RouteTimeoutIdle]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttp2RouteTimeoutIdle], jsii.get(self, "idleInput"))

    @builtins.property
    @jsii.member(jsii_name="perRequestInput")
    def per_request_input(
        self,
    ) -> typing.Optional["AppmeshRouteSpecHttp2RouteTimeoutPerRequest"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecHttp2RouteTimeoutPerRequest"], jsii.get(self, "perRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecHttp2RouteTimeout]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttp2RouteTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttp2RouteTimeout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85afec4678c8c274dd949d30a97872d2a23b8f105cae162a4165ccf5de7176b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteTimeoutPerRequest",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshRouteSpecHttp2RouteTimeoutPerRequest:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87958a800ce8ace76d2e22933b50ade55632674b126bcf471a478e9b75281e01)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttp2RouteTimeoutPerRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttp2RouteTimeoutPerRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttp2RouteTimeoutPerRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f8a45b35bfa0d0bb55f67339705be710eb69506430f33093e355948620ce727)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2ca74766c75908c5591ae627bdc65d55b1ac46f94a329ef83244df6e645f871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c953f1727ff2eb5339645fcb376f3be3f25352040e3739568f0c7131395e6220)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshRouteSpecHttp2RouteTimeoutPerRequest]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttp2RouteTimeoutPerRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttp2RouteTimeoutPerRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c19d79cbbc5d7e923154c5b277977a80e973a19a3ab5ed4b98faa8926181cc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRoute",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "match": "match",
        "retry_policy": "retryPolicy",
        "timeout": "timeout",
    },
)
class AppmeshRouteSpecHttpRoute:
    def __init__(
        self,
        *,
        action: typing.Union["AppmeshRouteSpecHttpRouteAction", typing.Dict[builtins.str, typing.Any]],
        match: typing.Union["AppmeshRouteSpecHttpRouteMatch", typing.Dict[builtins.str, typing.Any]],
        retry_policy: typing.Optional[typing.Union["AppmeshRouteSpecHttpRouteRetryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[typing.Union["AppmeshRouteSpecHttpRouteTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#action AppmeshRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#retry_policy AppmeshRoute#retry_policy}
        :param timeout: timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#timeout AppmeshRoute#timeout}
        '''
        if isinstance(action, dict):
            action = AppmeshRouteSpecHttpRouteAction(**action)
        if isinstance(match, dict):
            match = AppmeshRouteSpecHttpRouteMatch(**match)
        if isinstance(retry_policy, dict):
            retry_policy = AppmeshRouteSpecHttpRouteRetryPolicy(**retry_policy)
        if isinstance(timeout, dict):
            timeout = AppmeshRouteSpecHttpRouteTimeout(**timeout)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7930fa2166cd452f4e1aa39651007958ef8bd300329cabc184222c59544395)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument retry_policy", value=retry_policy, expected_type=type_hints["retry_policy"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "match": match,
        }
        if retry_policy is not None:
            self._values["retry_policy"] = retry_policy
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def action(self) -> "AppmeshRouteSpecHttpRouteAction":
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#action AppmeshRoute#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("AppmeshRouteSpecHttpRouteAction", result)

    @builtins.property
    def match(self) -> "AppmeshRouteSpecHttpRouteMatch":
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("AppmeshRouteSpecHttpRouteMatch", result)

    @builtins.property
    def retry_policy(self) -> typing.Optional["AppmeshRouteSpecHttpRouteRetryPolicy"]:
        '''retry_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#retry_policy AppmeshRoute#retry_policy}
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional["AppmeshRouteSpecHttpRouteRetryPolicy"], result)

    @builtins.property
    def timeout(self) -> typing.Optional["AppmeshRouteSpecHttpRouteTimeout"]:
        '''timeout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#timeout AppmeshRoute#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional["AppmeshRouteSpecHttpRouteTimeout"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttpRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteAction",
    jsii_struct_bases=[],
    name_mapping={"weighted_target": "weightedTarget"},
)
class AppmeshRouteSpecHttpRouteAction:
    def __init__(
        self,
        *,
        weighted_target: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshRouteSpecHttpRouteActionWeightedTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param weighted_target: weighted_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weighted_target AppmeshRoute#weighted_target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d31e4597376e085d0af5420c1198bede0d33ffa0a267d1f045eaee405e9ccbe)
            check_type(argname="argument weighted_target", value=weighted_target, expected_type=type_hints["weighted_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "weighted_target": weighted_target,
        }

    @builtins.property
    def weighted_target(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttpRouteActionWeightedTarget"]]:
        '''weighted_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weighted_target AppmeshRoute#weighted_target}
        '''
        result = self._values.get("weighted_target")
        assert result is not None, "Required property 'weighted_target' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttpRouteActionWeightedTarget"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttpRouteAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttpRouteActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4be419beef886e9c00417f10990b2371c03e7fce3645769fe2aa5408370ed365)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putWeightedTarget")
    def put_weighted_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshRouteSpecHttpRouteActionWeightedTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26770e486a9ea18ecf303d9fa21efcaa600a0ed8f6eebb73362b8d20c05ef374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWeightedTarget", [value]))

    @builtins.property
    @jsii.member(jsii_name="weightedTarget")
    def weighted_target(self) -> "AppmeshRouteSpecHttpRouteActionWeightedTargetList":
        return typing.cast("AppmeshRouteSpecHttpRouteActionWeightedTargetList", jsii.get(self, "weightedTarget"))

    @builtins.property
    @jsii.member(jsii_name="weightedTargetInput")
    def weighted_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttpRouteActionWeightedTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttpRouteActionWeightedTarget"]]], jsii.get(self, "weightedTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecHttpRouteAction]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttpRouteAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttpRouteAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__954071da1ac8490efcf5e341d99a94f5be52f702363f4533d0ea11ce50cf378a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteActionWeightedTarget",
    jsii_struct_bases=[],
    name_mapping={"virtual_node": "virtualNode", "weight": "weight", "port": "port"},
)
class AppmeshRouteSpecHttpRouteActionWeightedTarget:
    def __init__(
        self,
        *,
        virtual_node: builtins.str,
        weight: jsii.Number,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param virtual_node: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#virtual_node AppmeshRoute#virtual_node}.
        :param weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weight AppmeshRoute#weight}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac67c263c605cfb4c48f02f6f4d87ec6cdbfb55eac4a32958ac48c469ebc8e04)
            check_type(argname="argument virtual_node", value=virtual_node, expected_type=type_hints["virtual_node"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_node": virtual_node,
            "weight": weight,
        }
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def virtual_node(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#virtual_node AppmeshRoute#virtual_node}.'''
        result = self._values.get("virtual_node")
        assert result is not None, "Required property 'virtual_node' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def weight(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weight AppmeshRoute#weight}.'''
        result = self._values.get("weight")
        assert result is not None, "Required property 'weight' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttpRouteActionWeightedTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttpRouteActionWeightedTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteActionWeightedTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5de54ccd7ce2a19db9888887668b198e615e1d1ab6a673aaa366ec89e3e46c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppmeshRouteSpecHttpRouteActionWeightedTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af0af28306e1ab624cae0fcaf9e0be94ba165022e4035ec19abca8f845f8e282)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshRouteSpecHttpRouteActionWeightedTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd76d9d4bfba2b0c7f00909ba8380a103f71181dd95481767cd980ce75b7b22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__651c563955443401cc93dee361623695edd87c944ab501c9abda685ec3f94272)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66e8feab02d526a06a30e22c5c569f6e4b459323e00e22766912e2141d747c93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttpRouteActionWeightedTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttpRouteActionWeightedTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttpRouteActionWeightedTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbda95e2ea447b212550d7352140e041b3778ebd35b61a447ad2de40dd40c94c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecHttpRouteActionWeightedTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteActionWeightedTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9af8863ebce1975149ef25b440ee2b15c9881cead2778465233ddc68264a83a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNodeInput")
    def virtual_node_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb83b7ed6c376f2988db4e3f889d43e8f4e426f147ae19ab377eb400c7605ea3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNode")
    def virtual_node(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNode"))

    @virtual_node.setter
    def virtual_node(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad96cf5c78c1ffba755ab024ebefe37c625a19166b0ece097b0db206cea7d745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__729b3db763c92807b6e1a6d963caa0412dd79f98cdbac4af522fd47a05b37646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttpRouteActionWeightedTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttpRouteActionWeightedTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttpRouteActionWeightedTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b4ac75dc73343b79e72d689d64e776954b2b1e8ef9a91a5885aa328e17cfc37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteMatch",
    jsii_struct_bases=[],
    name_mapping={
        "header": "header",
        "method": "method",
        "path": "path",
        "port": "port",
        "prefix": "prefix",
        "query_parameter": "queryParameter",
        "scheme": "scheme",
    },
)
class AppmeshRouteSpecHttpRouteMatch:
    def __init__(
        self,
        *,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshRouteSpecHttpRouteMatchHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        method: typing.Optional[builtins.str] = None,
        path: typing.Optional[typing.Union["AppmeshRouteSpecHttpRouteMatchPath", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        prefix: typing.Optional[builtins.str] = None,
        query_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshRouteSpecHttpRouteMatchQueryParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#header AppmeshRoute#header}
        :param method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#method AppmeshRoute#method}.
        :param path: path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#path AppmeshRoute#path}
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#prefix AppmeshRoute#prefix}.
        :param query_parameter: query_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#query_parameter AppmeshRoute#query_parameter}
        :param scheme: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#scheme AppmeshRoute#scheme}.
        '''
        if isinstance(path, dict):
            path = AppmeshRouteSpecHttpRouteMatchPath(**path)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0ee0c10eb43c2d0dc559e3903c8fbb7c5b315ac9d5dce74930ad334a2894c2e)
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument query_parameter", value=query_parameter, expected_type=type_hints["query_parameter"])
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header is not None:
            self._values["header"] = header
        if method is not None:
            self._values["method"] = method
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if prefix is not None:
            self._values["prefix"] = prefix
        if query_parameter is not None:
            self._values["query_parameter"] = query_parameter
        if scheme is not None:
            self._values["scheme"] = scheme

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttpRouteMatchHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#header AppmeshRoute#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttpRouteMatchHeader"]]], result)

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#method AppmeshRoute#method}.'''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional["AppmeshRouteSpecHttpRouteMatchPath"]:
        '''path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#path AppmeshRoute#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional["AppmeshRouteSpecHttpRouteMatchPath"], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#prefix AppmeshRoute#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttpRouteMatchQueryParameter"]]]:
        '''query_parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#query_parameter AppmeshRoute#query_parameter}
        '''
        result = self._values.get("query_parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttpRouteMatchQueryParameter"]]], result)

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#scheme AppmeshRoute#scheme}.'''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttpRouteMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteMatchHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "invert": "invert", "match": "match"},
)
class AppmeshRouteSpecHttpRouteMatchHeader:
    def __init__(
        self,
        *,
        name: builtins.str,
        invert: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        match: typing.Optional[typing.Union["AppmeshRouteSpecHttpRouteMatchHeaderMatch", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#name AppmeshRoute#name}.
        :param invert: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#invert AppmeshRoute#invert}.
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        '''
        if isinstance(match, dict):
            match = AppmeshRouteSpecHttpRouteMatchHeaderMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f6f3ea747c177546e59f7c0d28309d9df9e6c5fd405bccda45a6839c7b21966)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument invert", value=invert, expected_type=type_hints["invert"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if invert is not None:
            self._values["invert"] = invert
        if match is not None:
            self._values["match"] = match

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#name AppmeshRoute#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def invert(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#invert AppmeshRoute#invert}.'''
        result = self._values.get("invert")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def match(self) -> typing.Optional["AppmeshRouteSpecHttpRouteMatchHeaderMatch"]:
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional["AppmeshRouteSpecHttpRouteMatchHeaderMatch"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttpRouteMatchHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttpRouteMatchHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteMatchHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27a4cfb36a0302e6b23ff644c93c48e8de5156a4d2148ad406b3354d2ad0a6b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppmeshRouteSpecHttpRouteMatchHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a8a34ed551fe42adb96c4e94502e24453468a9a347c1294acee1ea5f654c7ef)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshRouteSpecHttpRouteMatchHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__597245a7aeb72e1c4db15570871f4734db394bc7e2c1a2c17d4fda884af0c93a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d57bf7800a4f44f50c43363a69715d9779316d777c63d0479a8d54930c3bc7d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__900ea21a9901850dab17bf7854bc33c58cbd2b5f440081d7ed0f0280522dbf02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttpRouteMatchHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttpRouteMatchHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttpRouteMatchHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9427242acc76105159ca812aacaae6103cee776dbcf5bccaa9ae234a59edc58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteMatchHeaderMatch",
    jsii_struct_bases=[],
    name_mapping={
        "exact": "exact",
        "prefix": "prefix",
        "range": "range",
        "regex": "regex",
        "suffix": "suffix",
    },
)
class AppmeshRouteSpecHttpRouteMatchHeaderMatch:
    def __init__(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        range: typing.Optional[typing.Union["AppmeshRouteSpecHttpRouteMatchHeaderMatchRange", typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#prefix AppmeshRoute#prefix}.
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#range AppmeshRoute#range}
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#regex AppmeshRoute#regex}.
        :param suffix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#suffix AppmeshRoute#suffix}.
        '''
        if isinstance(range, dict):
            range = AppmeshRouteSpecHttpRouteMatchHeaderMatchRange(**range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4ca6d960d48974787c055af36a19eb553340dce11f0bc7e81ddeab59d1e83a9)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exact is not None:
            self._values["exact"] = exact
        if prefix is not None:
            self._values["prefix"] = prefix
        if range is not None:
            self._values["range"] = range
        if regex is not None:
            self._values["regex"] = regex
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.'''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#prefix AppmeshRoute#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range(
        self,
    ) -> typing.Optional["AppmeshRouteSpecHttpRouteMatchHeaderMatchRange"]:
        '''range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#range AppmeshRoute#range}
        '''
        result = self._values.get("range")
        return typing.cast(typing.Optional["AppmeshRouteSpecHttpRouteMatchHeaderMatchRange"], result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#regex AppmeshRoute#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#suffix AppmeshRoute#suffix}.'''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttpRouteMatchHeaderMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttpRouteMatchHeaderMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteMatchHeaderMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f850dab62d4feb700eddec38170b64f884d1e30e3188ad3183e8470b71203a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRange")
    def put_range(self, *, end: jsii.Number, start: jsii.Number) -> None:
        '''
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#end AppmeshRoute#end}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#start AppmeshRoute#start}.
        '''
        value = AppmeshRouteSpecHttpRouteMatchHeaderMatchRange(end=end, start=start)

        return typing.cast(None, jsii.invoke(self, "putRange", [value]))

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetRange")
    def reset_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRange", []))

    @jsii.member(jsii_name="resetRegex")
    def reset_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegex", []))

    @jsii.member(jsii_name="resetSuffix")
    def reset_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(self) -> "AppmeshRouteSpecHttpRouteMatchHeaderMatchRangeOutputReference":
        return typing.cast("AppmeshRouteSpecHttpRouteMatchHeaderMatchRangeOutputReference", jsii.get(self, "range"))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(
        self,
    ) -> typing.Optional["AppmeshRouteSpecHttpRouteMatchHeaderMatchRange"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecHttpRouteMatchHeaderMatchRange"], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="suffixInput")
    def suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suffixInput"))

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d3e068182fb545b1c6fe6762476c3b188b0a7107a3892c898ddbd69e2d2b5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff1ed940296510df7e3b5f948d160c6f090af7f12717b4658c171e19c262548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b52d5960dacea8e13afff6fc543ed7968cda227d47e15b9724ec4d409d0d3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783ae0df655142df3571a0f6fcc55217a54ac75a154851a9fa96e26511b0b874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshRouteSpecHttpRouteMatchHeaderMatch]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttpRouteMatchHeaderMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttpRouteMatchHeaderMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3548cc817f92838c1161438e2ccdabee9441f78713844091f3de5e9327a7d7ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteMatchHeaderMatchRange",
    jsii_struct_bases=[],
    name_mapping={"end": "end", "start": "start"},
)
class AppmeshRouteSpecHttpRouteMatchHeaderMatchRange:
    def __init__(self, *, end: jsii.Number, start: jsii.Number) -> None:
        '''
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#end AppmeshRoute#end}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#start AppmeshRoute#start}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c0db3c1f2d51e8289724914d1d00e6adb1ea27366f62bb524a720fe89ea173)
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end": end,
            "start": start,
        }

    @builtins.property
    def end(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#end AppmeshRoute#end}.'''
        result = self._values.get("end")
        assert result is not None, "Required property 'end' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#start AppmeshRoute#start}.'''
        result = self._values.get("start")
        assert result is not None, "Required property 'start' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttpRouteMatchHeaderMatchRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttpRouteMatchHeaderMatchRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteMatchHeaderMatchRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cda08f5abe5cc919e61200bb84b2b72825d68c9f9634b8f4ff0f6a4df53936e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "end"))

    @end.setter
    def end(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077e8a9887bd5d093f9b63473086f74f4d9753122850e20f71a4a548c7288c65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "start"))

    @start.setter
    def start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bd5c4d8477614fd8f68612feaf970ba76ec5d7fb5acb2741ae282790153b5a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshRouteSpecHttpRouteMatchHeaderMatchRange]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttpRouteMatchHeaderMatchRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttpRouteMatchHeaderMatchRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16dec92c602dedc4a4113da19cbe88cee8f562b2c2f851f5db3c4a9ddc83a7af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecHttpRouteMatchHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteMatchHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a1d86bf3613f908ed6e7f4619e83c1492bf7d03cd2d4a324bfb28170dc40a8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        range: typing.Optional[typing.Union[AppmeshRouteSpecHttpRouteMatchHeaderMatchRange, typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#prefix AppmeshRoute#prefix}.
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#range AppmeshRoute#range}
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#regex AppmeshRoute#regex}.
        :param suffix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#suffix AppmeshRoute#suffix}.
        '''
        value = AppmeshRouteSpecHttpRouteMatchHeaderMatch(
            exact=exact, prefix=prefix, range=range, regex=regex, suffix=suffix
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="resetInvert")
    def reset_invert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvert", []))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> AppmeshRouteSpecHttpRouteMatchHeaderMatchOutputReference:
        return typing.cast(AppmeshRouteSpecHttpRouteMatchHeaderMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="invertInput")
    def invert_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invertInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[AppmeshRouteSpecHttpRouteMatchHeaderMatch]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttpRouteMatchHeaderMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="invert")
    def invert(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invert"))

    @invert.setter
    def invert(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26945025bc90487e65d93f17d1eb9c5ed447e57c0e130db2c4567b4db22b7ded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f2c4c65d4bf3eb0c04acf7f626a4d79f7bda00e9a3236244bb86f3140b39e9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttpRouteMatchHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttpRouteMatchHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttpRouteMatchHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df3d0a8aebf16bf3c7a297ef7ed7975db37838c3c8133b8159d3ce0827607bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecHttpRouteMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c504916fcf15926e346acc6546b507cec460813af926b1acd71c567c865e768a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttpRouteMatchHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40386425c5522c187bf7ea6682f55a905a268018d95d1ceb0a1078acc499262d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="putPath")
    def put_path(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#regex AppmeshRoute#regex}.
        '''
        value = AppmeshRouteSpecHttpRouteMatchPath(exact=exact, regex=regex)

        return typing.cast(None, jsii.invoke(self, "putPath", [value]))

    @jsii.member(jsii_name="putQueryParameter")
    def put_query_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshRouteSpecHttpRouteMatchQueryParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c6df5cc4ad3ac88f4890c4ce6c4af5b1da22f79188edeaae8a84d2a002a3bf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQueryParameter", [value]))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetQueryParameter")
    def reset_query_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryParameter", []))

    @jsii.member(jsii_name="resetScheme")
    def reset_scheme(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheme", []))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> AppmeshRouteSpecHttpRouteMatchHeaderList:
        return typing.cast(AppmeshRouteSpecHttpRouteMatchHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> "AppmeshRouteSpecHttpRouteMatchPathOutputReference":
        return typing.cast("AppmeshRouteSpecHttpRouteMatchPathOutputReference", jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="queryParameter")
    def query_parameter(self) -> "AppmeshRouteSpecHttpRouteMatchQueryParameterList":
        return typing.cast("AppmeshRouteSpecHttpRouteMatchQueryParameterList", jsii.get(self, "queryParameter"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttpRouteMatchHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttpRouteMatchHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional["AppmeshRouteSpecHttpRouteMatchPath"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecHttpRouteMatchPath"], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="queryParameterInput")
    def query_parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttpRouteMatchQueryParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecHttpRouteMatchQueryParameter"]]], jsii.get(self, "queryParameterInput"))

    @builtins.property
    @jsii.member(jsii_name="schemeInput")
    def scheme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemeInput"))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3d0cd483b88fbb27cafb9c91d0afd3f712a6b2610793b529ed03f96264b89c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa855eb0a3e2af2f78aa9a5b946e8c97bcca8f41e76df67990ffd9300b18c432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35aa0a2f05868c454f348a3aecc34da3f9c04d2c5dec41360c32c70233820cf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheme"))

    @scheme.setter
    def scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d693a9fff8210cfdde70f7421b2b80a308f408078dde9c69bba5f3a6a518f029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecHttpRouteMatch]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttpRouteMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttpRouteMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7945c47d176ebcc630436809f77263f70113eee019e48c30a5b27ba13e036be9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteMatchPath",
    jsii_struct_bases=[],
    name_mapping={"exact": "exact", "regex": "regex"},
)
class AppmeshRouteSpecHttpRouteMatchPath:
    def __init__(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#regex AppmeshRoute#regex}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__386dd3f1d54d7764c2fb79c578434a4fca96312d19825df959beb9dba7f878e8)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exact is not None:
            self._values["exact"] = exact
        if regex is not None:
            self._values["regex"] = regex

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.'''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#regex AppmeshRoute#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttpRouteMatchPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttpRouteMatchPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteMatchPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bba140aaeafceb32af1ea290e424e0b1cbfda3ce006919f3f1c0c344e07b0ceb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetRegex")
    def reset_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegex", []))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44646f2d3ca9884fe989a5deff426eb129f52b7c1adb815b57a23c2f947af43f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c742ed9bd82e0e5a0d69ee23fac8a2178711c5ca6b88e9bbe7368713c9cb32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecHttpRouteMatchPath]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttpRouteMatchPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttpRouteMatchPath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2edf4c5edfdd8e8e4de245dbdfd38a1efd3bf07bff81a3532b343980204b7836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteMatchQueryParameter",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "match": "match"},
)
class AppmeshRouteSpecHttpRouteMatchQueryParameter:
    def __init__(
        self,
        *,
        name: builtins.str,
        match: typing.Optional[typing.Union["AppmeshRouteSpecHttpRouteMatchQueryParameterMatch", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#name AppmeshRoute#name}.
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        '''
        if isinstance(match, dict):
            match = AppmeshRouteSpecHttpRouteMatchQueryParameterMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7949aeba96ac899e2debadeee3437126266e92f22169f9e7ae10d22612623220)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if match is not None:
            self._values["match"] = match

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#name AppmeshRoute#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match(
        self,
    ) -> typing.Optional["AppmeshRouteSpecHttpRouteMatchQueryParameterMatch"]:
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional["AppmeshRouteSpecHttpRouteMatchQueryParameterMatch"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttpRouteMatchQueryParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttpRouteMatchQueryParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteMatchQueryParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e76cebed0c233224593b657e28433d1a8873e586fd0f66db486357d6aceba39e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppmeshRouteSpecHttpRouteMatchQueryParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a470337e261208eadaced7c1f8ff22b43fe386be850d4d5abc74d49f54b608e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshRouteSpecHttpRouteMatchQueryParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b32577bbb81a1ab4d3fb511bca36bf2e25eb224a6e25a26f41244832eba5cdd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24e055b05fc62fdaca497fb6dd8e7ae15711e99901dd040a9f13a62f79fbceee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfd54993b0b66e5daf85f7f03f2a8579143422a8bacdf5f2e831db8110935fa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttpRouteMatchQueryParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttpRouteMatchQueryParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttpRouteMatchQueryParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__967945011fb08aeee5ce6d847c8581fd4f841210866c27ea2cd0762c3e7695a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteMatchQueryParameterMatch",
    jsii_struct_bases=[],
    name_mapping={"exact": "exact"},
)
class AppmeshRouteSpecHttpRouteMatchQueryParameterMatch:
    def __init__(self, *, exact: typing.Optional[builtins.str] = None) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__154dc2045978c0c8d3fe01fbe00bf23e313ce3fdb85f0929780cf68f9285ac24)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exact is not None:
            self._values["exact"] = exact

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.'''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttpRouteMatchQueryParameterMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttpRouteMatchQueryParameterMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteMatchQueryParameterMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf059865295e413c8d73f8a3c5eaf8213c3b618684fec32abd4428dc344373bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4f2a42b8c530d6c7ef18201b355a93069cfd2e5840bc76ae7b23c30d865337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshRouteSpecHttpRouteMatchQueryParameterMatch]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttpRouteMatchQueryParameterMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttpRouteMatchQueryParameterMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c0c5309ef6c1dd744ce4ad70250643b08e4e5a77a1b4f6b1c1534a8da92f64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecHttpRouteMatchQueryParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteMatchQueryParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b34c20a2239aa5ec31f350676011fc78c9d96af8ea33002b41d8b5fd55135419)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatch")
    def put_match(self, *, exact: typing.Optional[builtins.str] = None) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#exact AppmeshRoute#exact}.
        '''
        value = AppmeshRouteSpecHttpRouteMatchQueryParameterMatch(exact=exact)

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> AppmeshRouteSpecHttpRouteMatchQueryParameterMatchOutputReference:
        return typing.cast(AppmeshRouteSpecHttpRouteMatchQueryParameterMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(
        self,
    ) -> typing.Optional[AppmeshRouteSpecHttpRouteMatchQueryParameterMatch]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttpRouteMatchQueryParameterMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a9d96837d98017f39391bc4b57bc6412f47ed18202da2383260e0c330098a97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttpRouteMatchQueryParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttpRouteMatchQueryParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttpRouteMatchQueryParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8fe7db8681acd798e9981c43bf17335e3fd16932393de6577a1ad69141d9590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecHttpRouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ab561648cce4fe32654e0e8fc05cbb3653932bccea5241f1e213302a2e27b08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        weighted_target: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttpRouteActionWeightedTarget, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param weighted_target: weighted_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weighted_target AppmeshRoute#weighted_target}
        '''
        value = AppmeshRouteSpecHttpRouteAction(weighted_target=weighted_target)

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttpRouteMatchHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
        method: typing.Optional[builtins.str] = None,
        path: typing.Optional[typing.Union[AppmeshRouteSpecHttpRouteMatchPath, typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        prefix: typing.Optional[builtins.str] = None,
        query_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttpRouteMatchQueryParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#header AppmeshRoute#header}
        :param method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#method AppmeshRoute#method}.
        :param path: path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#path AppmeshRoute#path}
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#prefix AppmeshRoute#prefix}.
        :param query_parameter: query_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#query_parameter AppmeshRoute#query_parameter}
        :param scheme: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#scheme AppmeshRoute#scheme}.
        '''
        value = AppmeshRouteSpecHttpRouteMatch(
            header=header,
            method=method,
            path=path,
            port=port,
            prefix=prefix,
            query_parameter=query_parameter,
            scheme=scheme,
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="putRetryPolicy")
    def put_retry_policy(
        self,
        *,
        max_retries: jsii.Number,
        per_retry_timeout: typing.Union["AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeout", typing.Dict[builtins.str, typing.Any]],
        http_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
        tcp_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param max_retries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#max_retries AppmeshRoute#max_retries}.
        :param per_retry_timeout: per_retry_timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#per_retry_timeout AppmeshRoute#per_retry_timeout}
        :param http_retry_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#http_retry_events AppmeshRoute#http_retry_events}.
        :param tcp_retry_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#tcp_retry_events AppmeshRoute#tcp_retry_events}.
        '''
        value = AppmeshRouteSpecHttpRouteRetryPolicy(
            max_retries=max_retries,
            per_retry_timeout=per_retry_timeout,
            http_retry_events=http_retry_events,
            tcp_retry_events=tcp_retry_events,
        )

        return typing.cast(None, jsii.invoke(self, "putRetryPolicy", [value]))

    @jsii.member(jsii_name="putTimeout")
    def put_timeout(
        self,
        *,
        idle: typing.Optional[typing.Union["AppmeshRouteSpecHttpRouteTimeoutIdle", typing.Dict[builtins.str, typing.Any]]] = None,
        per_request: typing.Optional[typing.Union["AppmeshRouteSpecHttpRouteTimeoutPerRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param idle: idle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#idle AppmeshRoute#idle}
        :param per_request: per_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#per_request AppmeshRoute#per_request}
        '''
        value = AppmeshRouteSpecHttpRouteTimeout(idle=idle, per_request=per_request)

        return typing.cast(None, jsii.invoke(self, "putTimeout", [value]))

    @jsii.member(jsii_name="resetRetryPolicy")
    def reset_retry_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryPolicy", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> AppmeshRouteSpecHttpRouteActionOutputReference:
        return typing.cast(AppmeshRouteSpecHttpRouteActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> AppmeshRouteSpecHttpRouteMatchOutputReference:
        return typing.cast(AppmeshRouteSpecHttpRouteMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicy")
    def retry_policy(self) -> "AppmeshRouteSpecHttpRouteRetryPolicyOutputReference":
        return typing.cast("AppmeshRouteSpecHttpRouteRetryPolicyOutputReference", jsii.get(self, "retryPolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> "AppmeshRouteSpecHttpRouteTimeoutOutputReference":
        return typing.cast("AppmeshRouteSpecHttpRouteTimeoutOutputReference", jsii.get(self, "timeout"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[AppmeshRouteSpecHttpRouteAction]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttpRouteAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[AppmeshRouteSpecHttpRouteMatch]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttpRouteMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicyInput")
    def retry_policy_input(
        self,
    ) -> typing.Optional["AppmeshRouteSpecHttpRouteRetryPolicy"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecHttpRouteRetryPolicy"], jsii.get(self, "retryPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional["AppmeshRouteSpecHttpRouteTimeout"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecHttpRouteTimeout"], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecHttpRoute]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttpRoute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AppmeshRouteSpecHttpRoute]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c15e14160ac590d64c4f74d06768eee7b1636adbcb95499729aa60e8b09192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteRetryPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "max_retries": "maxRetries",
        "per_retry_timeout": "perRetryTimeout",
        "http_retry_events": "httpRetryEvents",
        "tcp_retry_events": "tcpRetryEvents",
    },
)
class AppmeshRouteSpecHttpRouteRetryPolicy:
    def __init__(
        self,
        *,
        max_retries: jsii.Number,
        per_retry_timeout: typing.Union["AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeout", typing.Dict[builtins.str, typing.Any]],
        http_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
        tcp_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param max_retries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#max_retries AppmeshRoute#max_retries}.
        :param per_retry_timeout: per_retry_timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#per_retry_timeout AppmeshRoute#per_retry_timeout}
        :param http_retry_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#http_retry_events AppmeshRoute#http_retry_events}.
        :param tcp_retry_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#tcp_retry_events AppmeshRoute#tcp_retry_events}.
        '''
        if isinstance(per_retry_timeout, dict):
            per_retry_timeout = AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeout(**per_retry_timeout)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ec91a888af4f04e7277e29ed4ece2f49b0333e7f215e07cc6d3b65227fa7a0)
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument per_retry_timeout", value=per_retry_timeout, expected_type=type_hints["per_retry_timeout"])
            check_type(argname="argument http_retry_events", value=http_retry_events, expected_type=type_hints["http_retry_events"])
            check_type(argname="argument tcp_retry_events", value=tcp_retry_events, expected_type=type_hints["tcp_retry_events"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_retries": max_retries,
            "per_retry_timeout": per_retry_timeout,
        }
        if http_retry_events is not None:
            self._values["http_retry_events"] = http_retry_events
        if tcp_retry_events is not None:
            self._values["tcp_retry_events"] = tcp_retry_events

    @builtins.property
    def max_retries(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#max_retries AppmeshRoute#max_retries}.'''
        result = self._values.get("max_retries")
        assert result is not None, "Required property 'max_retries' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def per_retry_timeout(
        self,
    ) -> "AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeout":
        '''per_retry_timeout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#per_retry_timeout AppmeshRoute#per_retry_timeout}
        '''
        result = self._values.get("per_retry_timeout")
        assert result is not None, "Required property 'per_retry_timeout' is missing"
        return typing.cast("AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeout", result)

    @builtins.property
    def http_retry_events(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#http_retry_events AppmeshRoute#http_retry_events}.'''
        result = self._values.get("http_retry_events")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tcp_retry_events(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#tcp_retry_events AppmeshRoute#tcp_retry_events}.'''
        result = self._values.get("tcp_retry_events")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttpRouteRetryPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttpRouteRetryPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteRetryPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9736df1f0db389a407d000cd5caed1ace56f465a010bda96e3adbe7ef7131320)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPerRetryTimeout")
    def put_per_retry_timeout(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        value_ = AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeout(
            unit=unit, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putPerRetryTimeout", [value_]))

    @jsii.member(jsii_name="resetHttpRetryEvents")
    def reset_http_retry_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpRetryEvents", []))

    @jsii.member(jsii_name="resetTcpRetryEvents")
    def reset_tcp_retry_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpRetryEvents", []))

    @builtins.property
    @jsii.member(jsii_name="perRetryTimeout")
    def per_retry_timeout(
        self,
    ) -> "AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeoutOutputReference":
        return typing.cast("AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeoutOutputReference", jsii.get(self, "perRetryTimeout"))

    @builtins.property
    @jsii.member(jsii_name="httpRetryEventsInput")
    def http_retry_events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "httpRetryEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetriesInput")
    def max_retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetriesInput"))

    @builtins.property
    @jsii.member(jsii_name="perRetryTimeoutInput")
    def per_retry_timeout_input(
        self,
    ) -> typing.Optional["AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeout"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeout"], jsii.get(self, "perRetryTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpRetryEventsInput")
    def tcp_retry_events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tcpRetryEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="httpRetryEvents")
    def http_retry_events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "httpRetryEvents"))

    @http_retry_events.setter
    def http_retry_events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f63f390b268f7b2d6b4b5dee1842380d3b4e7730081ef66949f55c36e2045a3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpRetryEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e5148dd78ddb0e80665adda7b5da76cb634862e767dbdf55e923442f45fadfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tcpRetryEvents")
    def tcp_retry_events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tcpRetryEvents"))

    @tcp_retry_events.setter
    def tcp_retry_events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffb7016021ad9d37b73740289fc23ff7086b38cfbba001ffbafcd55b1db4ccb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tcpRetryEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecHttpRouteRetryPolicy]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttpRouteRetryPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttpRouteRetryPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c4f7e342b138d5d75891c536b27ef74e5d3fccc3dd5e1b067f76b6bc2ce1e77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeout",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeout:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__682362f24be54d0e19972a101d7f9dde431bf5e95dbbbdf9c0f60cce4661c544)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c508f07ec94f4cde89d5f3e05cbf556465bc8bedd65c026be34ba7f3147353f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__562fad77fcfd4d8820456c317b8dbcb8842ec0bf373923769f64d4d370c61d98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f26303511dae6582fc42421a714b256001b74e7ef97dd584a3faf4e4b35041b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeout]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85bba9e6ec2e9bc2b1ec3bd8c1df3a0ffbcd02da5e684f3b0f92206029c6dbcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteTimeout",
    jsii_struct_bases=[],
    name_mapping={"idle": "idle", "per_request": "perRequest"},
)
class AppmeshRouteSpecHttpRouteTimeout:
    def __init__(
        self,
        *,
        idle: typing.Optional[typing.Union["AppmeshRouteSpecHttpRouteTimeoutIdle", typing.Dict[builtins.str, typing.Any]]] = None,
        per_request: typing.Optional[typing.Union["AppmeshRouteSpecHttpRouteTimeoutPerRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param idle: idle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#idle AppmeshRoute#idle}
        :param per_request: per_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#per_request AppmeshRoute#per_request}
        '''
        if isinstance(idle, dict):
            idle = AppmeshRouteSpecHttpRouteTimeoutIdle(**idle)
        if isinstance(per_request, dict):
            per_request = AppmeshRouteSpecHttpRouteTimeoutPerRequest(**per_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8dd91686009ccb38892245af94aaf9be74a12709d89911c13229e13370b1cf5)
            check_type(argname="argument idle", value=idle, expected_type=type_hints["idle"])
            check_type(argname="argument per_request", value=per_request, expected_type=type_hints["per_request"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if idle is not None:
            self._values["idle"] = idle
        if per_request is not None:
            self._values["per_request"] = per_request

    @builtins.property
    def idle(self) -> typing.Optional["AppmeshRouteSpecHttpRouteTimeoutIdle"]:
        '''idle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#idle AppmeshRoute#idle}
        '''
        result = self._values.get("idle")
        return typing.cast(typing.Optional["AppmeshRouteSpecHttpRouteTimeoutIdle"], result)

    @builtins.property
    def per_request(
        self,
    ) -> typing.Optional["AppmeshRouteSpecHttpRouteTimeoutPerRequest"]:
        '''per_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#per_request AppmeshRoute#per_request}
        '''
        result = self._values.get("per_request")
        return typing.cast(typing.Optional["AppmeshRouteSpecHttpRouteTimeoutPerRequest"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttpRouteTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteTimeoutIdle",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshRouteSpecHttpRouteTimeoutIdle:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7502a4614c8554b87e268f5b08b030712f75f9a2ddf043458ebb0e8741a464f)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttpRouteTimeoutIdle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttpRouteTimeoutIdleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteTimeoutIdleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b79bf1fcc9775f2f3c8c4075922d4e0a00fd4c65d85cbc2125e91d74367bb30)
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
            type_hints = typing.get_type_hints(_typecheckingstub__157398d66a69b9a72d4bbc2cb4573f46965089d9b34d09428ec8eaf748ccc7fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64361ac2032e80b56a8daa333008ed74833458741a7c392ec6869216b9444dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecHttpRouteTimeoutIdle]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttpRouteTimeoutIdle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttpRouteTimeoutIdle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__301f18cfd6de60f067d17936dcc2f59ce4d513efb4258211e625c70602d7a502)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecHttpRouteTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bead220bbdfc7db744cd5d0b1a3589aa67308d757a0f9d53f9bd942600e8463)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIdle")
    def put_idle(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        value_ = AppmeshRouteSpecHttpRouteTimeoutIdle(unit=unit, value=value)

        return typing.cast(None, jsii.invoke(self, "putIdle", [value_]))

    @jsii.member(jsii_name="putPerRequest")
    def put_per_request(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        value_ = AppmeshRouteSpecHttpRouteTimeoutPerRequest(unit=unit, value=value)

        return typing.cast(None, jsii.invoke(self, "putPerRequest", [value_]))

    @jsii.member(jsii_name="resetIdle")
    def reset_idle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdle", []))

    @jsii.member(jsii_name="resetPerRequest")
    def reset_per_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerRequest", []))

    @builtins.property
    @jsii.member(jsii_name="idle")
    def idle(self) -> AppmeshRouteSpecHttpRouteTimeoutIdleOutputReference:
        return typing.cast(AppmeshRouteSpecHttpRouteTimeoutIdleOutputReference, jsii.get(self, "idle"))

    @builtins.property
    @jsii.member(jsii_name="perRequest")
    def per_request(
        self,
    ) -> "AppmeshRouteSpecHttpRouteTimeoutPerRequestOutputReference":
        return typing.cast("AppmeshRouteSpecHttpRouteTimeoutPerRequestOutputReference", jsii.get(self, "perRequest"))

    @builtins.property
    @jsii.member(jsii_name="idleInput")
    def idle_input(self) -> typing.Optional[AppmeshRouteSpecHttpRouteTimeoutIdle]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttpRouteTimeoutIdle], jsii.get(self, "idleInput"))

    @builtins.property
    @jsii.member(jsii_name="perRequestInput")
    def per_request_input(
        self,
    ) -> typing.Optional["AppmeshRouteSpecHttpRouteTimeoutPerRequest"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecHttpRouteTimeoutPerRequest"], jsii.get(self, "perRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecHttpRouteTimeout]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttpRouteTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttpRouteTimeout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d86a8e60dc03608ddc154a25643bee8afb5b86a6a6b000a22b38f8e8b7023803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteTimeoutPerRequest",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshRouteSpecHttpRouteTimeoutPerRequest:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__809efb7371f5eddea62355e228e3cdec882d12f27c0c66100c64f6cc61ac9690)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecHttpRouteTimeoutPerRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecHttpRouteTimeoutPerRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecHttpRouteTimeoutPerRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea9924362ab990ae2142fa0f858ddd6b654595b546a6e8b6445163831120ee79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55856b39ae0c949646ad9f2586b1fbef11f30072be7608c6ebed0e76f435f51c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fab3b778b284ecb74403213c2a7cb2376e81dada5b60403c6696175e2ff04305)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshRouteSpecHttpRouteTimeoutPerRequest]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttpRouteTimeoutPerRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecHttpRouteTimeoutPerRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95902367a2f4739cff73bd0c59581d7c99fb2c8beb267e468e2c93be25146f60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be05e114dfc82871af07555aa0ef90ead01713dddf262b61c539cae3ab7563db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGrpcRoute")
    def put_grpc_route(
        self,
        *,
        action: typing.Union[AppmeshRouteSpecGrpcRouteAction, typing.Dict[builtins.str, typing.Any]],
        match: typing.Optional[typing.Union[AppmeshRouteSpecGrpcRouteMatch, typing.Dict[builtins.str, typing.Any]]] = None,
        retry_policy: typing.Optional[typing.Union[AppmeshRouteSpecGrpcRouteRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[typing.Union[AppmeshRouteSpecGrpcRouteTimeout, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#action AppmeshRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#retry_policy AppmeshRoute#retry_policy}
        :param timeout: timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#timeout AppmeshRoute#timeout}
        '''
        value = AppmeshRouteSpecGrpcRoute(
            action=action, match=match, retry_policy=retry_policy, timeout=timeout
        )

        return typing.cast(None, jsii.invoke(self, "putGrpcRoute", [value]))

    @jsii.member(jsii_name="putHttp2Route")
    def put_http2_route(
        self,
        *,
        action: typing.Union[AppmeshRouteSpecHttp2RouteAction, typing.Dict[builtins.str, typing.Any]],
        match: typing.Union[AppmeshRouteSpecHttp2RouteMatch, typing.Dict[builtins.str, typing.Any]],
        retry_policy: typing.Optional[typing.Union[AppmeshRouteSpecHttp2RouteRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[typing.Union[AppmeshRouteSpecHttp2RouteTimeout, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#action AppmeshRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#retry_policy AppmeshRoute#retry_policy}
        :param timeout: timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#timeout AppmeshRoute#timeout}
        '''
        value = AppmeshRouteSpecHttp2Route(
            action=action, match=match, retry_policy=retry_policy, timeout=timeout
        )

        return typing.cast(None, jsii.invoke(self, "putHttp2Route", [value]))

    @jsii.member(jsii_name="putHttpRoute")
    def put_http_route(
        self,
        *,
        action: typing.Union[AppmeshRouteSpecHttpRouteAction, typing.Dict[builtins.str, typing.Any]],
        match: typing.Union[AppmeshRouteSpecHttpRouteMatch, typing.Dict[builtins.str, typing.Any]],
        retry_policy: typing.Optional[typing.Union[AppmeshRouteSpecHttpRouteRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[typing.Union[AppmeshRouteSpecHttpRouteTimeout, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#action AppmeshRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#retry_policy AppmeshRoute#retry_policy}
        :param timeout: timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#timeout AppmeshRoute#timeout}
        '''
        value = AppmeshRouteSpecHttpRoute(
            action=action, match=match, retry_policy=retry_policy, timeout=timeout
        )

        return typing.cast(None, jsii.invoke(self, "putHttpRoute", [value]))

    @jsii.member(jsii_name="putTcpRoute")
    def put_tcp_route(
        self,
        *,
        action: typing.Union["AppmeshRouteSpecTcpRouteAction", typing.Dict[builtins.str, typing.Any]],
        match: typing.Optional[typing.Union["AppmeshRouteSpecTcpRouteMatch", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[typing.Union["AppmeshRouteSpecTcpRouteTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#action AppmeshRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        :param timeout: timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#timeout AppmeshRoute#timeout}
        '''
        value = AppmeshRouteSpecTcpRoute(action=action, match=match, timeout=timeout)

        return typing.cast(None, jsii.invoke(self, "putTcpRoute", [value]))

    @jsii.member(jsii_name="resetGrpcRoute")
    def reset_grpc_route(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpcRoute", []))

    @jsii.member(jsii_name="resetHttp2Route")
    def reset_http2_route(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp2Route", []))

    @jsii.member(jsii_name="resetHttpRoute")
    def reset_http_route(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpRoute", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetTcpRoute")
    def reset_tcp_route(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpRoute", []))

    @builtins.property
    @jsii.member(jsii_name="grpcRoute")
    def grpc_route(self) -> AppmeshRouteSpecGrpcRouteOutputReference:
        return typing.cast(AppmeshRouteSpecGrpcRouteOutputReference, jsii.get(self, "grpcRoute"))

    @builtins.property
    @jsii.member(jsii_name="http2Route")
    def http2_route(self) -> AppmeshRouteSpecHttp2RouteOutputReference:
        return typing.cast(AppmeshRouteSpecHttp2RouteOutputReference, jsii.get(self, "http2Route"))

    @builtins.property
    @jsii.member(jsii_name="httpRoute")
    def http_route(self) -> AppmeshRouteSpecHttpRouteOutputReference:
        return typing.cast(AppmeshRouteSpecHttpRouteOutputReference, jsii.get(self, "httpRoute"))

    @builtins.property
    @jsii.member(jsii_name="tcpRoute")
    def tcp_route(self) -> "AppmeshRouteSpecTcpRouteOutputReference":
        return typing.cast("AppmeshRouteSpecTcpRouteOutputReference", jsii.get(self, "tcpRoute"))

    @builtins.property
    @jsii.member(jsii_name="grpcRouteInput")
    def grpc_route_input(self) -> typing.Optional[AppmeshRouteSpecGrpcRoute]:
        return typing.cast(typing.Optional[AppmeshRouteSpecGrpcRoute], jsii.get(self, "grpcRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="http2RouteInput")
    def http2_route_input(self) -> typing.Optional[AppmeshRouteSpecHttp2Route]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttp2Route], jsii.get(self, "http2RouteInput"))

    @builtins.property
    @jsii.member(jsii_name="httpRouteInput")
    def http_route_input(self) -> typing.Optional[AppmeshRouteSpecHttpRoute]:
        return typing.cast(typing.Optional[AppmeshRouteSpecHttpRoute], jsii.get(self, "httpRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpRouteInput")
    def tcp_route_input(self) -> typing.Optional["AppmeshRouteSpecTcpRoute"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecTcpRoute"], jsii.get(self, "tcpRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9f3a7f497b8cfd3864376dea93dd4b81210340fe9e84a485a97914b6b0e3c1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpec]:
        return typing.cast(typing.Optional[AppmeshRouteSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AppmeshRouteSpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbd98829ca5e7873ce33af4d201f9b76a8f3391578ae8ad1c5418cbde2be47af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecTcpRoute",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "match": "match", "timeout": "timeout"},
)
class AppmeshRouteSpecTcpRoute:
    def __init__(
        self,
        *,
        action: typing.Union["AppmeshRouteSpecTcpRouteAction", typing.Dict[builtins.str, typing.Any]],
        match: typing.Optional[typing.Union["AppmeshRouteSpecTcpRouteMatch", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[typing.Union["AppmeshRouteSpecTcpRouteTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#action AppmeshRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        :param timeout: timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#timeout AppmeshRoute#timeout}
        '''
        if isinstance(action, dict):
            action = AppmeshRouteSpecTcpRouteAction(**action)
        if isinstance(match, dict):
            match = AppmeshRouteSpecTcpRouteMatch(**match)
        if isinstance(timeout, dict):
            timeout = AppmeshRouteSpecTcpRouteTimeout(**timeout)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e6e1ef12dcb7151a933e653626162ac46b6f229570ca1c73fa645e3f011838)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
        }
        if match is not None:
            self._values["match"] = match
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def action(self) -> "AppmeshRouteSpecTcpRouteAction":
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#action AppmeshRoute#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("AppmeshRouteSpecTcpRouteAction", result)

    @builtins.property
    def match(self) -> typing.Optional["AppmeshRouteSpecTcpRouteMatch"]:
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#match AppmeshRoute#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional["AppmeshRouteSpecTcpRouteMatch"], result)

    @builtins.property
    def timeout(self) -> typing.Optional["AppmeshRouteSpecTcpRouteTimeout"]:
        '''timeout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#timeout AppmeshRoute#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional["AppmeshRouteSpecTcpRouteTimeout"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecTcpRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecTcpRouteAction",
    jsii_struct_bases=[],
    name_mapping={"weighted_target": "weightedTarget"},
)
class AppmeshRouteSpecTcpRouteAction:
    def __init__(
        self,
        *,
        weighted_target: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshRouteSpecTcpRouteActionWeightedTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param weighted_target: weighted_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weighted_target AppmeshRoute#weighted_target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0148b4b88e44780d90bb44cafddd150bef658d239f9e140db3ac2dc2d9a4229f)
            check_type(argname="argument weighted_target", value=weighted_target, expected_type=type_hints["weighted_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "weighted_target": weighted_target,
        }

    @builtins.property
    def weighted_target(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecTcpRouteActionWeightedTarget"]]:
        '''weighted_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weighted_target AppmeshRoute#weighted_target}
        '''
        result = self._values.get("weighted_target")
        assert result is not None, "Required property 'weighted_target' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecTcpRouteActionWeightedTarget"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecTcpRouteAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecTcpRouteActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecTcpRouteActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bb7c5a6158eedd5ea1c025d8b291d35f8aef6090e6079252ccd4a46396ade24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putWeightedTarget")
    def put_weighted_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshRouteSpecTcpRouteActionWeightedTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b001c3796bcb77ed55e3b6d996f2cd4939b5b739583d9445798669e10bdb0a2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWeightedTarget", [value]))

    @builtins.property
    @jsii.member(jsii_name="weightedTarget")
    def weighted_target(self) -> "AppmeshRouteSpecTcpRouteActionWeightedTargetList":
        return typing.cast("AppmeshRouteSpecTcpRouteActionWeightedTargetList", jsii.get(self, "weightedTarget"))

    @builtins.property
    @jsii.member(jsii_name="weightedTargetInput")
    def weighted_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecTcpRouteActionWeightedTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshRouteSpecTcpRouteActionWeightedTarget"]]], jsii.get(self, "weightedTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecTcpRouteAction]:
        return typing.cast(typing.Optional[AppmeshRouteSpecTcpRouteAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecTcpRouteAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d629a54c124fe59e0bb5d902a9be240fb41039f7f7bb69607af97b12e91ab7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecTcpRouteActionWeightedTarget",
    jsii_struct_bases=[],
    name_mapping={"virtual_node": "virtualNode", "weight": "weight", "port": "port"},
)
class AppmeshRouteSpecTcpRouteActionWeightedTarget:
    def __init__(
        self,
        *,
        virtual_node: builtins.str,
        weight: jsii.Number,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param virtual_node: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#virtual_node AppmeshRoute#virtual_node}.
        :param weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weight AppmeshRoute#weight}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a2af743b94d37fd770aa8894d2467781f44c6a9af68223bf1b732dfab474d7d)
            check_type(argname="argument virtual_node", value=virtual_node, expected_type=type_hints["virtual_node"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_node": virtual_node,
            "weight": weight,
        }
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def virtual_node(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#virtual_node AppmeshRoute#virtual_node}.'''
        result = self._values.get("virtual_node")
        assert result is not None, "Required property 'virtual_node' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def weight(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weight AppmeshRoute#weight}.'''
        result = self._values.get("weight")
        assert result is not None, "Required property 'weight' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecTcpRouteActionWeightedTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecTcpRouteActionWeightedTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecTcpRouteActionWeightedTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8402c3953905b127ebc8d5b70fdb06e859ab86047ba0ea0ee29cee8e942b715)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppmeshRouteSpecTcpRouteActionWeightedTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a917af99700ef5aa1b221f0d4405dcd442f18c2be2dbe4cbcb7acfd1e183c0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshRouteSpecTcpRouteActionWeightedTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba5416320c8999a769905c2adc0bd9c2cea95bba70d7e28d78c8c4fcfb5a2d3f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4441966f095aaf79acfe6d73ff473dc9547920519b78734e4a90d19d60835da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__343e1e1951c6313afbbabc6d07533378c2d8bb5d85c1bdf78e4479416c8de58b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecTcpRouteActionWeightedTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecTcpRouteActionWeightedTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecTcpRouteActionWeightedTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d865bc09beb2ac1e904e0e0c3fe66a8bb62bade042f8887b9a0b4c78f4b6d35c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecTcpRouteActionWeightedTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecTcpRouteActionWeightedTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff0a024cefb45407f34dd29ddca430203b21aa26b24ae75cefc868e32fd62572)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNodeInput")
    def virtual_node_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8c0b85be3e76bf2655c9f887382a2a546486ce76e58e1e110bdf780fa38e2ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNode")
    def virtual_node(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNode"))

    @virtual_node.setter
    def virtual_node(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d083c0ccf00532371eb0b5e33aa5b644d78cfbc47b3cf864a18b82d4ecff4fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37f53e68e565616eae40b4b04e12f53944972459271277d88ddfbd72bc1d5f0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecTcpRouteActionWeightedTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecTcpRouteActionWeightedTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecTcpRouteActionWeightedTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20b671069293e879312213439ad0744d01ddc1bcc6eb85126bea8608311c933e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecTcpRouteMatch",
    jsii_struct_bases=[],
    name_mapping={"port": "port"},
)
class AppmeshRouteSpecTcpRouteMatch:
    def __init__(self, *, port: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d2cb0e764df058f7fe25455c4595f84a79211cce613a13777100c6d1e55cb5)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecTcpRouteMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecTcpRouteMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecTcpRouteMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75ed49715f320a0c9aac2143bff63b7204eb734eb7d77853f312321aa59cb6cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70bf56afeb23875c5dbd8871d31d2054d729b2d46ecb79475f1e9c434f69ce13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecTcpRouteMatch]:
        return typing.cast(typing.Optional[AppmeshRouteSpecTcpRouteMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecTcpRouteMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7999fbf1e92a49043135338006cc436096ce8f553bdb1a83d2f74e66a9f6f2ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecTcpRouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecTcpRouteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc02c41c21bbfc4ed37b2ebbb5f6ba182a9063c1576b54d66efe46ce93298449)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        weighted_target: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecTcpRouteActionWeightedTarget, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param weighted_target: weighted_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#weighted_target AppmeshRoute#weighted_target}
        '''
        value = AppmeshRouteSpecTcpRouteAction(weighted_target=weighted_target)

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putMatch")
    def put_match(self, *, port: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#port AppmeshRoute#port}.
        '''
        value = AppmeshRouteSpecTcpRouteMatch(port=port)

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="putTimeout")
    def put_timeout(
        self,
        *,
        idle: typing.Optional[typing.Union["AppmeshRouteSpecTcpRouteTimeoutIdle", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param idle: idle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#idle AppmeshRoute#idle}
        '''
        value = AppmeshRouteSpecTcpRouteTimeout(idle=idle)

        return typing.cast(None, jsii.invoke(self, "putTimeout", [value]))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> AppmeshRouteSpecTcpRouteActionOutputReference:
        return typing.cast(AppmeshRouteSpecTcpRouteActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> AppmeshRouteSpecTcpRouteMatchOutputReference:
        return typing.cast(AppmeshRouteSpecTcpRouteMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> "AppmeshRouteSpecTcpRouteTimeoutOutputReference":
        return typing.cast("AppmeshRouteSpecTcpRouteTimeoutOutputReference", jsii.get(self, "timeout"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[AppmeshRouteSpecTcpRouteAction]:
        return typing.cast(typing.Optional[AppmeshRouteSpecTcpRouteAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[AppmeshRouteSpecTcpRouteMatch]:
        return typing.cast(typing.Optional[AppmeshRouteSpecTcpRouteMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional["AppmeshRouteSpecTcpRouteTimeout"]:
        return typing.cast(typing.Optional["AppmeshRouteSpecTcpRouteTimeout"], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecTcpRoute]:
        return typing.cast(typing.Optional[AppmeshRouteSpecTcpRoute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AppmeshRouteSpecTcpRoute]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd5ddab1fa8ad066ddd6c2cbd958859eeef58f6e5417a9aea5d1edb2a272f11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecTcpRouteTimeout",
    jsii_struct_bases=[],
    name_mapping={"idle": "idle"},
)
class AppmeshRouteSpecTcpRouteTimeout:
    def __init__(
        self,
        *,
        idle: typing.Optional[typing.Union["AppmeshRouteSpecTcpRouteTimeoutIdle", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param idle: idle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#idle AppmeshRoute#idle}
        '''
        if isinstance(idle, dict):
            idle = AppmeshRouteSpecTcpRouteTimeoutIdle(**idle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7bd10a1662109307e887da024a981109aed11bccea9901f0246e97c6054a50a)
            check_type(argname="argument idle", value=idle, expected_type=type_hints["idle"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if idle is not None:
            self._values["idle"] = idle

    @builtins.property
    def idle(self) -> typing.Optional["AppmeshRouteSpecTcpRouteTimeoutIdle"]:
        '''idle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#idle AppmeshRoute#idle}
        '''
        result = self._values.get("idle")
        return typing.cast(typing.Optional["AppmeshRouteSpecTcpRouteTimeoutIdle"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecTcpRouteTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecTcpRouteTimeoutIdle",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class AppmeshRouteSpecTcpRouteTimeoutIdle:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9167ae58021d3e1b85d428bfb9e78d6c8a92dd5dbfda42f099912bb930623290)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshRouteSpecTcpRouteTimeoutIdle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshRouteSpecTcpRouteTimeoutIdleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecTcpRouteTimeoutIdleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8624033283cd9364a296af242dcfe745f8c9b9cdd3ea96af22971a73bfcc51b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc970a10e3d759cd76b32a786f4d4715b43d0c1def170ebacd7a174321d9355a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f42abcfd2a263ab56341506033786caa4dded4c98e8cd9ed3480a6332e8aec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecTcpRouteTimeoutIdle]:
        return typing.cast(typing.Optional[AppmeshRouteSpecTcpRouteTimeoutIdle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecTcpRouteTimeoutIdle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ca1437abf1a5b56ddef87993e6f01e2acf3fa7e1a5731ac263e7042ce09c05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshRouteSpecTcpRouteTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshRoute.AppmeshRouteSpecTcpRouteTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36547f33a3e60c74040d1d92a8e4a244a754497c8116ce63af66a56218eda97b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIdle")
    def put_idle(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#unit AppmeshRoute#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_route#value AppmeshRoute#value}.
        '''
        value_ = AppmeshRouteSpecTcpRouteTimeoutIdle(unit=unit, value=value)

        return typing.cast(None, jsii.invoke(self, "putIdle", [value_]))

    @jsii.member(jsii_name="resetIdle")
    def reset_idle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdle", []))

    @builtins.property
    @jsii.member(jsii_name="idle")
    def idle(self) -> AppmeshRouteSpecTcpRouteTimeoutIdleOutputReference:
        return typing.cast(AppmeshRouteSpecTcpRouteTimeoutIdleOutputReference, jsii.get(self, "idle"))

    @builtins.property
    @jsii.member(jsii_name="idleInput")
    def idle_input(self) -> typing.Optional[AppmeshRouteSpecTcpRouteTimeoutIdle]:
        return typing.cast(typing.Optional[AppmeshRouteSpecTcpRouteTimeoutIdle], jsii.get(self, "idleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshRouteSpecTcpRouteTimeout]:
        return typing.cast(typing.Optional[AppmeshRouteSpecTcpRouteTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshRouteSpecTcpRouteTimeout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1089d4502013843e91c177fb51c26e1dd9f9c563ea8fb0f53ad45b6271af3418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppmeshRoute",
    "AppmeshRouteConfig",
    "AppmeshRouteSpec",
    "AppmeshRouteSpecGrpcRoute",
    "AppmeshRouteSpecGrpcRouteAction",
    "AppmeshRouteSpecGrpcRouteActionOutputReference",
    "AppmeshRouteSpecGrpcRouteActionWeightedTarget",
    "AppmeshRouteSpecGrpcRouteActionWeightedTargetList",
    "AppmeshRouteSpecGrpcRouteActionWeightedTargetOutputReference",
    "AppmeshRouteSpecGrpcRouteMatch",
    "AppmeshRouteSpecGrpcRouteMatchMetadata",
    "AppmeshRouteSpecGrpcRouteMatchMetadataList",
    "AppmeshRouteSpecGrpcRouteMatchMetadataMatch",
    "AppmeshRouteSpecGrpcRouteMatchMetadataMatchOutputReference",
    "AppmeshRouteSpecGrpcRouteMatchMetadataMatchRange",
    "AppmeshRouteSpecGrpcRouteMatchMetadataMatchRangeOutputReference",
    "AppmeshRouteSpecGrpcRouteMatchMetadataOutputReference",
    "AppmeshRouteSpecGrpcRouteMatchOutputReference",
    "AppmeshRouteSpecGrpcRouteOutputReference",
    "AppmeshRouteSpecGrpcRouteRetryPolicy",
    "AppmeshRouteSpecGrpcRouteRetryPolicyOutputReference",
    "AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeout",
    "AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeoutOutputReference",
    "AppmeshRouteSpecGrpcRouteTimeout",
    "AppmeshRouteSpecGrpcRouteTimeoutIdle",
    "AppmeshRouteSpecGrpcRouteTimeoutIdleOutputReference",
    "AppmeshRouteSpecGrpcRouteTimeoutOutputReference",
    "AppmeshRouteSpecGrpcRouteTimeoutPerRequest",
    "AppmeshRouteSpecGrpcRouteTimeoutPerRequestOutputReference",
    "AppmeshRouteSpecHttp2Route",
    "AppmeshRouteSpecHttp2RouteAction",
    "AppmeshRouteSpecHttp2RouteActionOutputReference",
    "AppmeshRouteSpecHttp2RouteActionWeightedTarget",
    "AppmeshRouteSpecHttp2RouteActionWeightedTargetList",
    "AppmeshRouteSpecHttp2RouteActionWeightedTargetOutputReference",
    "AppmeshRouteSpecHttp2RouteMatch",
    "AppmeshRouteSpecHttp2RouteMatchHeader",
    "AppmeshRouteSpecHttp2RouteMatchHeaderList",
    "AppmeshRouteSpecHttp2RouteMatchHeaderMatch",
    "AppmeshRouteSpecHttp2RouteMatchHeaderMatchOutputReference",
    "AppmeshRouteSpecHttp2RouteMatchHeaderMatchRange",
    "AppmeshRouteSpecHttp2RouteMatchHeaderMatchRangeOutputReference",
    "AppmeshRouteSpecHttp2RouteMatchHeaderOutputReference",
    "AppmeshRouteSpecHttp2RouteMatchOutputReference",
    "AppmeshRouteSpecHttp2RouteMatchPath",
    "AppmeshRouteSpecHttp2RouteMatchPathOutputReference",
    "AppmeshRouteSpecHttp2RouteMatchQueryParameter",
    "AppmeshRouteSpecHttp2RouteMatchQueryParameterList",
    "AppmeshRouteSpecHttp2RouteMatchQueryParameterMatch",
    "AppmeshRouteSpecHttp2RouteMatchQueryParameterMatchOutputReference",
    "AppmeshRouteSpecHttp2RouteMatchQueryParameterOutputReference",
    "AppmeshRouteSpecHttp2RouteOutputReference",
    "AppmeshRouteSpecHttp2RouteRetryPolicy",
    "AppmeshRouteSpecHttp2RouteRetryPolicyOutputReference",
    "AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeout",
    "AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeoutOutputReference",
    "AppmeshRouteSpecHttp2RouteTimeout",
    "AppmeshRouteSpecHttp2RouteTimeoutIdle",
    "AppmeshRouteSpecHttp2RouteTimeoutIdleOutputReference",
    "AppmeshRouteSpecHttp2RouteTimeoutOutputReference",
    "AppmeshRouteSpecHttp2RouteTimeoutPerRequest",
    "AppmeshRouteSpecHttp2RouteTimeoutPerRequestOutputReference",
    "AppmeshRouteSpecHttpRoute",
    "AppmeshRouteSpecHttpRouteAction",
    "AppmeshRouteSpecHttpRouteActionOutputReference",
    "AppmeshRouteSpecHttpRouteActionWeightedTarget",
    "AppmeshRouteSpecHttpRouteActionWeightedTargetList",
    "AppmeshRouteSpecHttpRouteActionWeightedTargetOutputReference",
    "AppmeshRouteSpecHttpRouteMatch",
    "AppmeshRouteSpecHttpRouteMatchHeader",
    "AppmeshRouteSpecHttpRouteMatchHeaderList",
    "AppmeshRouteSpecHttpRouteMatchHeaderMatch",
    "AppmeshRouteSpecHttpRouteMatchHeaderMatchOutputReference",
    "AppmeshRouteSpecHttpRouteMatchHeaderMatchRange",
    "AppmeshRouteSpecHttpRouteMatchHeaderMatchRangeOutputReference",
    "AppmeshRouteSpecHttpRouteMatchHeaderOutputReference",
    "AppmeshRouteSpecHttpRouteMatchOutputReference",
    "AppmeshRouteSpecHttpRouteMatchPath",
    "AppmeshRouteSpecHttpRouteMatchPathOutputReference",
    "AppmeshRouteSpecHttpRouteMatchQueryParameter",
    "AppmeshRouteSpecHttpRouteMatchQueryParameterList",
    "AppmeshRouteSpecHttpRouteMatchQueryParameterMatch",
    "AppmeshRouteSpecHttpRouteMatchQueryParameterMatchOutputReference",
    "AppmeshRouteSpecHttpRouteMatchQueryParameterOutputReference",
    "AppmeshRouteSpecHttpRouteOutputReference",
    "AppmeshRouteSpecHttpRouteRetryPolicy",
    "AppmeshRouteSpecHttpRouteRetryPolicyOutputReference",
    "AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeout",
    "AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeoutOutputReference",
    "AppmeshRouteSpecHttpRouteTimeout",
    "AppmeshRouteSpecHttpRouteTimeoutIdle",
    "AppmeshRouteSpecHttpRouteTimeoutIdleOutputReference",
    "AppmeshRouteSpecHttpRouteTimeoutOutputReference",
    "AppmeshRouteSpecHttpRouteTimeoutPerRequest",
    "AppmeshRouteSpecHttpRouteTimeoutPerRequestOutputReference",
    "AppmeshRouteSpecOutputReference",
    "AppmeshRouteSpecTcpRoute",
    "AppmeshRouteSpecTcpRouteAction",
    "AppmeshRouteSpecTcpRouteActionOutputReference",
    "AppmeshRouteSpecTcpRouteActionWeightedTarget",
    "AppmeshRouteSpecTcpRouteActionWeightedTargetList",
    "AppmeshRouteSpecTcpRouteActionWeightedTargetOutputReference",
    "AppmeshRouteSpecTcpRouteMatch",
    "AppmeshRouteSpecTcpRouteMatchOutputReference",
    "AppmeshRouteSpecTcpRouteOutputReference",
    "AppmeshRouteSpecTcpRouteTimeout",
    "AppmeshRouteSpecTcpRouteTimeoutIdle",
    "AppmeshRouteSpecTcpRouteTimeoutIdleOutputReference",
    "AppmeshRouteSpecTcpRouteTimeoutOutputReference",
]

publication.publish()

def _typecheckingstub__6a3d1e8f00e7393411b9d39f2b5a5cae13649e67c30f4bd45f2ae0cab466e731(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    mesh_name: builtins.str,
    name: builtins.str,
    spec: typing.Union[AppmeshRouteSpec, typing.Dict[builtins.str, typing.Any]],
    virtual_router_name: builtins.str,
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

def _typecheckingstub__bd4c812dab29251147c0e210e3992ed465b70982ef907190ff0b1f7b1f49d098(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bbb86ef48f5e66a8f9e96bfda342822896d8f89473aebd47bae203d647f649e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38d7920f7b0e09f8a9fb3068b8ef2ca1b2af99f5836896ac875bcc4c189e0064(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8376b6eda9798ea8c8004001a86b19e8477c2f36eb79ab18f97afa72e4fc4e15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8ac8aeede9bc80adf88bf720d9fc9b9aa54d16aa1b85fcb7fb33de2d1c8d21c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901ff726f6a5ac0a43c6bb05381528ab4c76a9d541d8b199454dcb65123a5e9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec08557560c171f930b6ed653d656e953bd699422f8d8115589d4d05ed89c93(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1a9d6e6ba102d7306d444664b0d60be0ef5f225adf2995d6c4e1776a490a1f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25dfb3c4ac950ac1c2e0fa910890189a4ab244c65085ae3c95b39fa596b98782(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aacd234c84e88200dcb33f0b26ea493962eec03fd601fad4fe6745b80aef5d49(
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
    spec: typing.Union[AppmeshRouteSpec, typing.Dict[builtins.str, typing.Any]],
    virtual_router_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    mesh_owner: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a23f8a7f95fddce21fb15c452d84d6e5f0c4fd98291a7d2d51f5dbfb1987b66d(
    *,
    grpc_route: typing.Optional[typing.Union[AppmeshRouteSpecGrpcRoute, typing.Dict[builtins.str, typing.Any]]] = None,
    http2_route: typing.Optional[typing.Union[AppmeshRouteSpecHttp2Route, typing.Dict[builtins.str, typing.Any]]] = None,
    http_route: typing.Optional[typing.Union[AppmeshRouteSpecHttpRoute, typing.Dict[builtins.str, typing.Any]]] = None,
    priority: typing.Optional[jsii.Number] = None,
    tcp_route: typing.Optional[typing.Union[AppmeshRouteSpecTcpRoute, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__416ab6b26121fac56a5841b675bf17558b9a0ef2e6cf723cd684f4a35909866d(
    *,
    action: typing.Union[AppmeshRouteSpecGrpcRouteAction, typing.Dict[builtins.str, typing.Any]],
    match: typing.Optional[typing.Union[AppmeshRouteSpecGrpcRouteMatch, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_policy: typing.Optional[typing.Union[AppmeshRouteSpecGrpcRouteRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[typing.Union[AppmeshRouteSpecGrpcRouteTimeout, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa16bd6f237b42ac82923061e008316f759e460bcd9f5c6478a9464de2996374(
    *,
    weighted_target: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecGrpcRouteActionWeightedTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c16ad4b289be210eacef1d8cd4feeca2f3f6ca1718b337bfa71d2107de3639d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a042d94a351ff117f86dbd4e030edd48cff9841ba494323f53d380a4a3038e52(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecGrpcRouteActionWeightedTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2476ec4ebaec04d18402d7d67f629ef03e28e33f5ada3f1844d3447488fa0582(
    value: typing.Optional[AppmeshRouteSpecGrpcRouteAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee4b2e07e641d56f267a75d27d99382e3c035a0976a0746688b0737cb322a3fc(
    *,
    virtual_node: builtins.str,
    weight: jsii.Number,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab97bf7e32f67dfb81acc05186eddbe05696e4616b305441beaac6beedd35e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__129bc1b89ad93b81fd640f74bc0a569aebd115080984b42440462370826cd674(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3c232d4e0d82fbebcb4ccabad4994dd27b7b576485f14627f2ce9f03543644(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e54122e8c4f18026a3a41f10dddc541bb0014f21c438961c4205bc7fc0ff16f9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0d047f0f98e5bcb9cbb8fc00a391480b9cd8c1d952f08e0a47718bc7eb9b1a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa4fd4fa74bd45fe7403ccd9a50952ebd6e510918aa8c7df518c50feca9ad46(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecGrpcRouteActionWeightedTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec7837978ef66f9d8703ab0f611e559914c2413c84b8f02d79a3ebf6640b7f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7518a71a47b1a8e722dfabb0fa256f64536c5d2a257337cce7470461c9e4ffe7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a2df39475addc715646a369d33668a464ed17a3c3e73004991ccb7392e26450(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb6771292d43f7b268a19f36e303e167e8c62809479b91d4daa958a93a780ab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbacae1069530782a6fd186c77fd0f4302ea7eb62ec3f2f4b889ddaec375a4ab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecGrpcRouteActionWeightedTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5e53d2f4f0cc057be5ce75e6758e2e69f237c790c20d5bd4dc221679759d79(
    *,
    metadata: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecGrpcRouteMatchMetadata, typing.Dict[builtins.str, typing.Any]]]]] = None,
    method_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    prefix: typing.Optional[builtins.str] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb5a3a43fbca2f34120501278e299e1351568a09679a0408140d8fbbca2809f(
    *,
    name: builtins.str,
    invert: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    match: typing.Optional[typing.Union[AppmeshRouteSpecGrpcRouteMatchMetadataMatch, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821848d703ad5c8c30aace203ec5c8ba97a14ed30807f54c5420e9130c3f5f2c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ffd1d244346d31940f77946d701fbd1740ebb538e6fd91201f1272e360204a8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02711fe0e9aacc7cc436604e633b75078d885f4d0f6ebb22be58abb1fd9294fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf08ffefb19d9b279f5b5d65b0bc7294acbdf6c3c4208149ce5320facd9b514(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8e19f67b41d0dd51ed249a2355ed43b8a80dfff4c130b42c2d489a5716ab77b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a993d3cc071522faf2b8100bc5a083c1f1ae994e5058d2489bfacfb2792f40f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecGrpcRouteMatchMetadata]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ccaa662486807dc3d3cc1286b54fabbd3e426bfb036a0ca92608bcdc6f50b8(
    *,
    exact: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    range: typing.Optional[typing.Union[AppmeshRouteSpecGrpcRouteMatchMetadataMatchRange, typing.Dict[builtins.str, typing.Any]]] = None,
    regex: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5436a17a8f2ed8b0c5c7f4448a97d532a519691d1f9577db674776853844697(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076dfab0fe5ed583c8ff3df7e04b0f2ec1b20c8cbcfbe9facd3e97a7cbea19dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f60a88939bfe0f76d6208de0085bb5ffbb27650b8b6af31a91e4606529dfcf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51b997205ef710953fbe5998f28a0c15ae0196d23b4809b705ecd2088b827631(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e99c7a0ca095d684c0598a8671b818ec3ecc472b88689c7a1db17c4664b82ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4da8bbc75427b47ea3e69851eff4c4567fe6473076c3fb8f457c9c14d10d7f(
    value: typing.Optional[AppmeshRouteSpecGrpcRouteMatchMetadataMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0afc9bf99631ae435b63555729c9537664ff68511dae32039f7cf65602346810(
    *,
    end: jsii.Number,
    start: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b927e72155afbff00900149665f192e3025c856f9de21a473e995aa1ce552f83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176a41e5f7f96cf10a88d7cce1d26a8d3e7251e817c6af8a08b2d00941c6d2ad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa813ff4c66187af0957a5b5177b33b46e759341e7b0a27c74c1960314e98da(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff81a6a7b5b3ca08ce0d096ae4a8095dedc54f6bbdd4fd4580b403e5560a22a(
    value: typing.Optional[AppmeshRouteSpecGrpcRouteMatchMetadataMatchRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96c6d1d7d98f50a67e0c915737628648c622ffb3cfefbff1e7634fee48a30bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd65ecda8bfb888114eebed6f54ba7d55dca8d4e9f7dce5924a255caf2b9d01(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68e3f55e451503587a7a02d1239dc0733e5a0a679a801d07589d690563d4391(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4885a1e6bf19eb126e3dea53f7968a053102b2f8c435a543a4a9f23982016f32(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecGrpcRouteMatchMetadata]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c93808ac81c6d8a0a147e6f123969c2c83810dcf16e6c61e6dbbc31099382f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb682750ec8f5325c77bd1fae818fe8b4b96ac08d52a8841971dc7a53c5f3aa0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecGrpcRouteMatchMetadata, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d0d1155d384ce658672d4aeeda93ca40ab3aa2f58f390afd3b6981840f9fea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36260ab3804278d6a85014446cefdc16ed82a3bfb7efbe1f9d3bb07b1533ac30(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f12263cd2fa6fe7293641a4af91eaf1eec2924518f83b187291ee452ec5752(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e628707ea5bda1bd3c44e121c7475d450aebad6b175388a753f6dd1a94339d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__564fb493defb927787b1aa151425ee094c12c4ffb9bd6031eaec2c0c2f141d5e(
    value: typing.Optional[AppmeshRouteSpecGrpcRouteMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b35d4980808fa13346415b4625ea4ab779b882299a7f163eb152629201a92113(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a4e65229082dd588d61cbbf6b97debb811e1466a642e2fbeb1b038071d88c9(
    value: typing.Optional[AppmeshRouteSpecGrpcRoute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1413e14fc93eee39effb0388fc7806e69c59c54e7c8dc92ee6744441b59511d0(
    *,
    max_retries: jsii.Number,
    per_retry_timeout: typing.Union[AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeout, typing.Dict[builtins.str, typing.Any]],
    grpc_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    http_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    tcp_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12633761a61cd1b9bd3f50e5c72239c1785914487615c95a738695991998c196(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b53bc0789436d1d403e3df3e4330c8812a5d816b6d2e49139c443ca339c586(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49a46f530cb45dc6d27f3d8695bbd59dcee6b3d3ed6f0d224e28640a095d703(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a68afb5c0fba10bc486f6bf464340d98ebbca868482eb677e2665bc1d88345e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a41e1e8602d39cf4cc4fff814300c8d62dd8c6612edeaa3dbd83f59caf89b29(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dbc37cdaef7efbd19bcce2c5913e4a165d6cddefc3bd2090a1c6eb11e327ce6(
    value: typing.Optional[AppmeshRouteSpecGrpcRouteRetryPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29069b88535700ed2c40fccfea8a93b670dddd37990b9d5d93315adc0a05c984(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c9409b046efa07342acfb09ce20d326b100976a1d28d3f83f1648ad43ce6b5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e894b042718ea1a964677555cfda28823d8e0ccd619c52a5bd04e6c38d2af5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e739b5f8c223c828c9bcf6de124db52980d98c4ccf01d8b76285f79c6f755f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de61cbadbb11247d6c15ab3a62daf7627d8713c96898b736c85c918c00970073(
    value: typing.Optional[AppmeshRouteSpecGrpcRouteRetryPolicyPerRetryTimeout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c41f32f021e11d212657a0631f8f42b4958347cb0a710d7d1c7916de02e5226a(
    *,
    idle: typing.Optional[typing.Union[AppmeshRouteSpecGrpcRouteTimeoutIdle, typing.Dict[builtins.str, typing.Any]]] = None,
    per_request: typing.Optional[typing.Union[AppmeshRouteSpecGrpcRouteTimeoutPerRequest, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d978bfd027c4091fc971fd1866f671e266e844391cfb00b87fcc45cf56ea0817(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3021067b06938b60431fe973a7ef6ead090e9833569b75200fb75c4bdcb06ecd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d15d8771b3d2e9d104827cc6f6a8de69b76c0f93e0e94b9378e96378bde89b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b1dab5d6b710f98f1feb16793a9c8f0e908e831613875bbef6af3c74b0c1be(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2374f7b9bba56b2eb62b4acc3bdfa01fa2e0894e75587683a6bff6b94750f1(
    value: typing.Optional[AppmeshRouteSpecGrpcRouteTimeoutIdle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01d33039640ecda9b3b76d7f69fc66195da2824dd28267c0fc55a6db1b65da2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e091e7c58a9991f89fcd4eb2b98c88ba17c0110ed897a66f6e1db1b7bf2cf517(
    value: typing.Optional[AppmeshRouteSpecGrpcRouteTimeout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a4f0282d54764fcd61590a1475f483dc86ccda93340f602acf64ef95f7ac8c(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41352030233c811872c72c477068ad76d334e80460b07fdfa0cb6123e6e840c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d833788d3c3c2fd1a3d5cee31f8c20dab691bfce9bca1e66676c14c7e166d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a3281a7f9b8f320e3db729460a6c7d702d6cd1ebdaec6db6f9a16350ac0e7f6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65a389f957c16b81a207d2337f22c526b6bab0455fb3847227423e191454b2d(
    value: typing.Optional[AppmeshRouteSpecGrpcRouteTimeoutPerRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b55473d58b24eb99f14e4767c2ecb182cedb5421369433c9d494f01a48fa6af3(
    *,
    action: typing.Union[AppmeshRouteSpecHttp2RouteAction, typing.Dict[builtins.str, typing.Any]],
    match: typing.Union[AppmeshRouteSpecHttp2RouteMatch, typing.Dict[builtins.str, typing.Any]],
    retry_policy: typing.Optional[typing.Union[AppmeshRouteSpecHttp2RouteRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[typing.Union[AppmeshRouteSpecHttp2RouteTimeout, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee933731b1f1c9d5181adbbd7974dffdbf4c1098b0e757a4e079473541bdda4c(
    *,
    weighted_target: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttp2RouteActionWeightedTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472759fedc8cfed1768db3b72f072cc2d021e46d60aa192bf2bb54846d426f29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8832c4bcb2f0755791fa169c2762e33900e467b01e36a34eb755f0cbcf465111(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttp2RouteActionWeightedTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d602da6abb850b8ed8f9c96d2af4d544e11dfb386c2985ebc5345a123524ec(
    value: typing.Optional[AppmeshRouteSpecHttp2RouteAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e8a70d302cd479cfef42fb68244d48ba18d2a9c2ff219cf827863825018356(
    *,
    virtual_node: builtins.str,
    weight: jsii.Number,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d14a096d9af81255e02d51030e03510a9ebbed88045e1cd7c39d14d4061ec525(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc27cf9de415893f678ede7a69207fe17b9bc24a1ba610d4fcc7b5b47050fc23(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ca5385e4baa90a0debf168d4a55d79f8e276099036aec2fec5c24a83779857(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917dfb2604b07ca24209b59c5209759a05cc5008d076ba3803da125b08ce6ad2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b0e1ef154e3d64507b9c1b95c2b68157535666f243019b293ad578269841a3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9692d7275530748b2983052ce6d1511384310760481804bd596a0c82fde47e07(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttp2RouteActionWeightedTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a3b3881e7e158b22d676a0388fcefe4498fafe7b3be1f2ddf4c2f3b899de41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645173082439041f2b981f02b0e150a242d179acd78474da81000158e276ebae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70db9bf493b0eeaeb2dd9d67692446514b2959473f03442cdb3b4ef2c0e2faf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d51aa1d05b02e1b0e214d85c98e8c29c90697e41513e2e7ea7efc1f434fa1ed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e027421aded2ad8ee90b7b6d1b809aebeea89cc4da25d03b5a2d959daebf665(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttp2RouteActionWeightedTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc12609ffd8b048bbe0f2ed51abf848d9e1f9eb551f602b1b0c708a734c083ef(
    *,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttp2RouteMatchHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    method: typing.Optional[builtins.str] = None,
    path: typing.Optional[typing.Union[AppmeshRouteSpecHttp2RouteMatchPath, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[jsii.Number] = None,
    prefix: typing.Optional[builtins.str] = None,
    query_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttp2RouteMatchQueryParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scheme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031e0801333c9ab9e4f6abd1a89222fbe64d9c4d9cfa7241db26dc3b3790b402(
    *,
    name: builtins.str,
    invert: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    match: typing.Optional[typing.Union[AppmeshRouteSpecHttp2RouteMatchHeaderMatch, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2beaccb0552b637a178cab9bd23969f32aaf8dd6a4124a1cd2df1b2f923762(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc3447db7abe177279ff32397bcd35318ca3635633d30c5449c937de8bb17bc1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da385d5b84908dc6b204e29b350fae231a430cc07fd19bedc6961c7412636c74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec786c788b414c4b9ff1069c0b48970e70eddc47a31109586770e8b11519147(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c41bfa1737a6ac02941ea2191c76c7f0ced764a93596fa4dbe00d333b647575(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7234348140d715ec2d4a451243f4fd83048a6c2203dad838574ed46abafa3c22(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttp2RouteMatchHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9e7fd0b4dc814fe78cc27cd28fe0ecac9f9bc0f9ffb0ad2e1afb9439ba706c(
    *,
    exact: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    range: typing.Optional[typing.Union[AppmeshRouteSpecHttp2RouteMatchHeaderMatchRange, typing.Dict[builtins.str, typing.Any]]] = None,
    regex: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82ee4e09122f9143698676a7b184b54d20f933d73070b38b7555e5b8c551e8d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2439f994bedda0e589fafbc1170b8c1ab52411d5f2ffc5f274b424d6dac6e054(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e972cd9e5c05b16e57e5cca53eae075f4290e621b59f22dac2d5c96be7c15e1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef77c116e38dcf36e873eda242ea9485c5886736c2d9a77a1311476389e68f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4668bb1c7260f11280e11751d681f1b440f8a8cee515eb555968c0f95d844397(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3f4cb1e49dfc248926045706d736637be6be2d129c268f22f135bef9240efd(
    value: typing.Optional[AppmeshRouteSpecHttp2RouteMatchHeaderMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6669eacf273560fbc62e70a5a73ead3467504890c5279260563af593c2ed63a7(
    *,
    end: jsii.Number,
    start: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ec4ad9cac2f951d9203410e2e3ba065ce44d801ce7ec33c9b984ead9172b50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5a870752783485f225d0a8eeadc397d24b2938462f40a23e644be8f8febd17(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e3af8905d8013299291de419526b302d19c4658ebd58efc3da026ca52832af(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f837abf20a511cf3a7a1e66f2f034919550d5c13998ca8b9f5210cb881eacfc(
    value: typing.Optional[AppmeshRouteSpecHttp2RouteMatchHeaderMatchRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f29845cc7b8245ad3dcfbbc9b8852656c4d8b420e4c26c8efa4f263bdb333b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e81867a18cce568e1c95df44f8f30d5e5265e62b3d8df53a520d8d71e83245(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f14b2b02027a355eebc7b40b17eae2a87ee8eb70952150a336152bf4b826beb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd5f1a556ab1af8704508935cf82c244b7d93f4bf7eeccc0f072665740c6b9a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttp2RouteMatchHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f608bc2a25d3733ffe02c05799b4a512bed0800987a629f4b0861ea7e518450(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e7e1ccd2d7f402760325ae8c221bc0a07acc1caa32fbdf3ee993d2572e364f3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttp2RouteMatchHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d95db041f2718d04864fbcdca9c1f9cc1cd24e458f743ab87786820722eda9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttp2RouteMatchQueryParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24714c82e2dd390f5c66a0243193419db81241d0e9848c1f8d4e32927c89f8b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7029381d454584e5b347857c8e3449fbf87ddcb36683e02d39ed16c9cc3b3284(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17069898db90cf2d541c809e43d39b59a15aa68e854854835f5e413df12a9de0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0448ace646e446805908877f5f16d1acd03ee380d09146e2c1155e4aec43b86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c03bf2eba240dc2dd683446a542049ae66764978c65536f64d18e47feb2387(
    value: typing.Optional[AppmeshRouteSpecHttp2RouteMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2034d172255f6a6ad1dd4802d1141f0b25707c417a6587c2fe5508cfe4292d8d(
    *,
    exact: typing.Optional[builtins.str] = None,
    regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ac777135aeb245dd7e477f79cbf034335e9d89c63e787e2d403fa9ac8f1e004(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f281521f7071b05bce0e0c48f21b7d2188e5e4ade06c9812db508d24850c13a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__974975e54c0bab42a3c327755573ec2838dc45cf63431d12efa91e48b9f1dae4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04aea31e5992318a2e7f9f851af7e34b36864bcf3ae285189a22ce79ff707a1(
    value: typing.Optional[AppmeshRouteSpecHttp2RouteMatchPath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a7964da47fa649d7d27de019a8282ec7afb82edeb3ee44364431ab64185c99(
    *,
    name: builtins.str,
    match: typing.Optional[typing.Union[AppmeshRouteSpecHttp2RouteMatchQueryParameterMatch, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4966074ce864e7f11915a9fd74d4ab3b02090829bd5de8f15b0f65260bf0b4c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475ac4e9de7acb4d025f1092af7e047f4ed1c7419819a8df667f1d2855a153e5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4700d2be3f51357d0dbbb19dc407e3765aeb93205a508d3f52ab09fc1ceaa90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb4f3caaf3faab5d87a7a132ecfc4ce46e5828b19e48f2a32db6d4c6289abbee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644c72048e79eec062854f516d2f179237a586db108b2cb28bdbed3206e92fce(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac4705e8751dc879a602b31d60cc40d717782bb784a3bc1c1ef466e8e5a81ac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttp2RouteMatchQueryParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caf734ac2f04e5ddb5b1823e7e9ba0a6460fcfeb35c604ac07163319c5a15a1b(
    *,
    exact: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87799587782a5506e64bbe1b94800a489031d0d540b5ab3fd540c7ea24281af1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20dcc629254c49ba98be81294bc088954650bfba614abc1d28a8e723b88156a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f34dee27fbb937b65c4c614b9ca03bf074dd4f017483ad08c3197398908d28b(
    value: typing.Optional[AppmeshRouteSpecHttp2RouteMatchQueryParameterMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673ed2c0d5e42d2b225824c1e1fe32f4494329a7ca886517b98e3b2789b6987b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8578f8fdd0d1df8cf5ac04440807f08e0d36b7e78a6ee333c08ccdb0effccb88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__885847ae6d8157267114372a428307738bd3a8e904610b44b1a0ff472c8f446f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttp2RouteMatchQueryParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8309f6847ec7b0d02d47517e09b26a6bbc9d092a33d95b51c961cb7b7bec25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5197336aaad2f09bbe1770c9efdb3dd136f8bf32aa873f570c1e80c1600268b8(
    value: typing.Optional[AppmeshRouteSpecHttp2Route],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b28cbc45eed18fea697098861e1b58ca77a0744d0222e846f112f26ef982fc5(
    *,
    max_retries: jsii.Number,
    per_retry_timeout: typing.Union[AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeout, typing.Dict[builtins.str, typing.Any]],
    http_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    tcp_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47a405eb13bcfb096e04f299d88244757b36b77bddfcb249d140fe3d2e8257a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4092a8975d9c3089886373e47f3e1ef7a45be63a9ab0d6f1f1171b88614d798(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6e6e469c0bf256e7fd8c6ccc5741d6bc0513baed4b605f4d8a358b25ca1f2e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c71a4cf6b846278c9cccc418af3411331f486ed885423ec258ecc26c5162d28(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb639ea1b797ba9d53b454336e9d153d1717d4faabb123104d27d55a0d22869d(
    value: typing.Optional[AppmeshRouteSpecHttp2RouteRetryPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93d208ab9afa282e201344e3a9091c40a6915548d7dec71f75ded404cdf7c9c(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd16df750740a8312f27750ff370bb070afbe7f094088932796de8818e0d10d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e0a92b2e11a60d8a9b2b936926e82e3dec2b1403c57a4225437c18dd6666372(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b2dae1977eac86ea18d75b282b90a9db9f4347592bd8e80e5151df0c9acadac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51137cc26698cc683bdf74d67cbd8ca5350ca075f2a18d11d94a7b1951c23c68(
    value: typing.Optional[AppmeshRouteSpecHttp2RouteRetryPolicyPerRetryTimeout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c4e4580ffce5a359985ad1c622877b5b5dea44afb003f629117153ee78f6e0f(
    *,
    idle: typing.Optional[typing.Union[AppmeshRouteSpecHttp2RouteTimeoutIdle, typing.Dict[builtins.str, typing.Any]]] = None,
    per_request: typing.Optional[typing.Union[AppmeshRouteSpecHttp2RouteTimeoutPerRequest, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f054045eb3f2f888eeac53d5da8a08011b72e4c4189fa08da256417dd90f1269(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c89a1262682abadee4a1ab5ebdcba062685671e6bc677766b59909e3db08de04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4192c3f3efd34974f8bef6932b264ab617e564f3655c2ecef2757afed234f8d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783189080c91d0d33f0f12822880d6aea831b63fa9def6adf70bb19203249568(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d4f749db2bf258291c735b21603c87d80197492de3b26727cde709afca67fa(
    value: typing.Optional[AppmeshRouteSpecHttp2RouteTimeoutIdle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e585f731b1c5cfa5d41c15e5cd3176b5f49680613b40183d690e9d1ed41cf975(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85afec4678c8c274dd949d30a97872d2a23b8f105cae162a4165ccf5de7176b0(
    value: typing.Optional[AppmeshRouteSpecHttp2RouteTimeout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87958a800ce8ace76d2e22933b50ade55632674b126bcf471a478e9b75281e01(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f8a45b35bfa0d0bb55f67339705be710eb69506430f33093e355948620ce727(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ca74766c75908c5591ae627bdc65d55b1ac46f94a329ef83244df6e645f871(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c953f1727ff2eb5339645fcb376f3be3f25352040e3739568f0c7131395e6220(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c19d79cbbc5d7e923154c5b277977a80e973a19a3ab5ed4b98faa8926181cc7(
    value: typing.Optional[AppmeshRouteSpecHttp2RouteTimeoutPerRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7930fa2166cd452f4e1aa39651007958ef8bd300329cabc184222c59544395(
    *,
    action: typing.Union[AppmeshRouteSpecHttpRouteAction, typing.Dict[builtins.str, typing.Any]],
    match: typing.Union[AppmeshRouteSpecHttpRouteMatch, typing.Dict[builtins.str, typing.Any]],
    retry_policy: typing.Optional[typing.Union[AppmeshRouteSpecHttpRouteRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[typing.Union[AppmeshRouteSpecHttpRouteTimeout, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d31e4597376e085d0af5420c1198bede0d33ffa0a267d1f045eaee405e9ccbe(
    *,
    weighted_target: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttpRouteActionWeightedTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be419beef886e9c00417f10990b2371c03e7fce3645769fe2aa5408370ed365(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26770e486a9ea18ecf303d9fa21efcaa600a0ed8f6eebb73362b8d20c05ef374(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttpRouteActionWeightedTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__954071da1ac8490efcf5e341d99a94f5be52f702363f4533d0ea11ce50cf378a(
    value: typing.Optional[AppmeshRouteSpecHttpRouteAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac67c263c605cfb4c48f02f6f4d87ec6cdbfb55eac4a32958ac48c469ebc8e04(
    *,
    virtual_node: builtins.str,
    weight: jsii.Number,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5de54ccd7ce2a19db9888887668b198e615e1d1ab6a673aaa366ec89e3e46c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0af28306e1ab624cae0fcaf9e0be94ba165022e4035ec19abca8f845f8e282(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd76d9d4bfba2b0c7f00909ba8380a103f71181dd95481767cd980ce75b7b22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__651c563955443401cc93dee361623695edd87c944ab501c9abda685ec3f94272(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e8feab02d526a06a30e22c5c569f6e4b459323e00e22766912e2141d747c93(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbda95e2ea447b212550d7352140e041b3778ebd35b61a447ad2de40dd40c94c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttpRouteActionWeightedTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af8863ebce1975149ef25b440ee2b15c9881cead2778465233ddc68264a83a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb83b7ed6c376f2988db4e3f889d43e8f4e426f147ae19ab377eb400c7605ea3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad96cf5c78c1ffba755ab024ebefe37c625a19166b0ece097b0db206cea7d745(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__729b3db763c92807b6e1a6d963caa0412dd79f98cdbac4af522fd47a05b37646(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4ac75dc73343b79e72d689d64e776954b2b1e8ef9a91a5885aa328e17cfc37(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttpRouteActionWeightedTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0ee0c10eb43c2d0dc559e3903c8fbb7c5b315ac9d5dce74930ad334a2894c2e(
    *,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttpRouteMatchHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    method: typing.Optional[builtins.str] = None,
    path: typing.Optional[typing.Union[AppmeshRouteSpecHttpRouteMatchPath, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[jsii.Number] = None,
    prefix: typing.Optional[builtins.str] = None,
    query_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttpRouteMatchQueryParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scheme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f6f3ea747c177546e59f7c0d28309d9df9e6c5fd405bccda45a6839c7b21966(
    *,
    name: builtins.str,
    invert: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    match: typing.Optional[typing.Union[AppmeshRouteSpecHttpRouteMatchHeaderMatch, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a4cfb36a0302e6b23ff644c93c48e8de5156a4d2148ad406b3354d2ad0a6b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8a34ed551fe42adb96c4e94502e24453468a9a347c1294acee1ea5f654c7ef(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__597245a7aeb72e1c4db15570871f4734db394bc7e2c1a2c17d4fda884af0c93a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57bf7800a4f44f50c43363a69715d9779316d777c63d0479a8d54930c3bc7d0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900ea21a9901850dab17bf7854bc33c58cbd2b5f440081d7ed0f0280522dbf02(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9427242acc76105159ca812aacaae6103cee776dbcf5bccaa9ae234a59edc58(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttpRouteMatchHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ca6d960d48974787c055af36a19eb553340dce11f0bc7e81ddeab59d1e83a9(
    *,
    exact: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    range: typing.Optional[typing.Union[AppmeshRouteSpecHttpRouteMatchHeaderMatchRange, typing.Dict[builtins.str, typing.Any]]] = None,
    regex: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f850dab62d4feb700eddec38170b64f884d1e30e3188ad3183e8470b71203a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d3e068182fb545b1c6fe6762476c3b188b0a7107a3892c898ddbd69e2d2b5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff1ed940296510df7e3b5f948d160c6f090af7f12717b4658c171e19c262548(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b52d5960dacea8e13afff6fc543ed7968cda227d47e15b9724ec4d409d0d3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783ae0df655142df3571a0f6fcc55217a54ac75a154851a9fa96e26511b0b874(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3548cc817f92838c1161438e2ccdabee9441f78713844091f3de5e9327a7d7ad(
    value: typing.Optional[AppmeshRouteSpecHttpRouteMatchHeaderMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c0db3c1f2d51e8289724914d1d00e6adb1ea27366f62bb524a720fe89ea173(
    *,
    end: jsii.Number,
    start: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cda08f5abe5cc919e61200bb84b2b72825d68c9f9634b8f4ff0f6a4df53936e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077e8a9887bd5d093f9b63473086f74f4d9753122850e20f71a4a548c7288c65(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd5c4d8477614fd8f68612feaf970ba76ec5d7fb5acb2741ae282790153b5a3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16dec92c602dedc4a4113da19cbe88cee8f562b2c2f851f5db3c4a9ddc83a7af(
    value: typing.Optional[AppmeshRouteSpecHttpRouteMatchHeaderMatchRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1d86bf3613f908ed6e7f4619e83c1492bf7d03cd2d4a324bfb28170dc40a8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26945025bc90487e65d93f17d1eb9c5ed447e57c0e130db2c4567b4db22b7ded(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2c4c65d4bf3eb0c04acf7f626a4d79f7bda00e9a3236244bb86f3140b39e9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df3d0a8aebf16bf3c7a297ef7ed7975db37838c3c8133b8159d3ce0827607bb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttpRouteMatchHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c504916fcf15926e346acc6546b507cec460813af926b1acd71c567c865e768a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40386425c5522c187bf7ea6682f55a905a268018d95d1ceb0a1078acc499262d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttpRouteMatchHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c6df5cc4ad3ac88f4890c4ce6c4af5b1da22f79188edeaae8a84d2a002a3bf0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecHttpRouteMatchQueryParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3d0cd483b88fbb27cafb9c91d0afd3f712a6b2610793b529ed03f96264b89c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa855eb0a3e2af2f78aa9a5b946e8c97bcca8f41e76df67990ffd9300b18c432(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35aa0a2f05868c454f348a3aecc34da3f9c04d2c5dec41360c32c70233820cf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d693a9fff8210cfdde70f7421b2b80a308f408078dde9c69bba5f3a6a518f029(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7945c47d176ebcc630436809f77263f70113eee019e48c30a5b27ba13e036be9(
    value: typing.Optional[AppmeshRouteSpecHttpRouteMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__386dd3f1d54d7764c2fb79c578434a4fca96312d19825df959beb9dba7f878e8(
    *,
    exact: typing.Optional[builtins.str] = None,
    regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba140aaeafceb32af1ea290e424e0b1cbfda3ce006919f3f1c0c344e07b0ceb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44646f2d3ca9884fe989a5deff426eb129f52b7c1adb815b57a23c2f947af43f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c742ed9bd82e0e5a0d69ee23fac8a2178711c5ca6b88e9bbe7368713c9cb32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2edf4c5edfdd8e8e4de245dbdfd38a1efd3bf07bff81a3532b343980204b7836(
    value: typing.Optional[AppmeshRouteSpecHttpRouteMatchPath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7949aeba96ac899e2debadeee3437126266e92f22169f9e7ae10d22612623220(
    *,
    name: builtins.str,
    match: typing.Optional[typing.Union[AppmeshRouteSpecHttpRouteMatchQueryParameterMatch, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e76cebed0c233224593b657e28433d1a8873e586fd0f66db486357d6aceba39e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a470337e261208eadaced7c1f8ff22b43fe386be850d4d5abc74d49f54b608e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b32577bbb81a1ab4d3fb511bca36bf2e25eb224a6e25a26f41244832eba5cdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e055b05fc62fdaca497fb6dd8e7ae15711e99901dd040a9f13a62f79fbceee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd54993b0b66e5daf85f7f03f2a8579143422a8bacdf5f2e831db8110935fa3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967945011fb08aeee5ce6d847c8581fd4f841210866c27ea2cd0762c3e7695a0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecHttpRouteMatchQueryParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154dc2045978c0c8d3fe01fbe00bf23e313ce3fdb85f0929780cf68f9285ac24(
    *,
    exact: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf059865295e413c8d73f8a3c5eaf8213c3b618684fec32abd4428dc344373bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4f2a42b8c530d6c7ef18201b355a93069cfd2e5840bc76ae7b23c30d865337(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c0c5309ef6c1dd744ce4ad70250643b08e4e5a77a1b4f6b1c1534a8da92f64(
    value: typing.Optional[AppmeshRouteSpecHttpRouteMatchQueryParameterMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34c20a2239aa5ec31f350676011fc78c9d96af8ea33002b41d8b5fd55135419(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9d96837d98017f39391bc4b57bc6412f47ed18202da2383260e0c330098a97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8fe7db8681acd798e9981c43bf17335e3fd16932393de6577a1ad69141d9590(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecHttpRouteMatchQueryParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab561648cce4fe32654e0e8fc05cbb3653932bccea5241f1e213302a2e27b08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c15e14160ac590d64c4f74d06768eee7b1636adbcb95499729aa60e8b09192(
    value: typing.Optional[AppmeshRouteSpecHttpRoute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ec91a888af4f04e7277e29ed4ece2f49b0333e7f215e07cc6d3b65227fa7a0(
    *,
    max_retries: jsii.Number,
    per_retry_timeout: typing.Union[AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeout, typing.Dict[builtins.str, typing.Any]],
    http_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    tcp_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9736df1f0db389a407d000cd5caed1ace56f465a010bda96e3adbe7ef7131320(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63f390b268f7b2d6b4b5dee1842380d3b4e7730081ef66949f55c36e2045a3a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e5148dd78ddb0e80665adda7b5da76cb634862e767dbdf55e923442f45fadfd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb7016021ad9d37b73740289fc23ff7086b38cfbba001ffbafcd55b1db4ccb3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4f7e342b138d5d75891c536b27ef74e5d3fccc3dd5e1b067f76b6bc2ce1e77(
    value: typing.Optional[AppmeshRouteSpecHttpRouteRetryPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682362f24be54d0e19972a101d7f9dde431bf5e95dbbbdf9c0f60cce4661c544(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c508f07ec94f4cde89d5f3e05cbf556465bc8bedd65c026be34ba7f3147353f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__562fad77fcfd4d8820456c317b8dbcb8842ec0bf373923769f64d4d370c61d98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f26303511dae6582fc42421a714b256001b74e7ef97dd584a3faf4e4b35041b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85bba9e6ec2e9bc2b1ec3bd8c1df3a0ffbcd02da5e684f3b0f92206029c6dbcf(
    value: typing.Optional[AppmeshRouteSpecHttpRouteRetryPolicyPerRetryTimeout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8dd91686009ccb38892245af94aaf9be74a12709d89911c13229e13370b1cf5(
    *,
    idle: typing.Optional[typing.Union[AppmeshRouteSpecHttpRouteTimeoutIdle, typing.Dict[builtins.str, typing.Any]]] = None,
    per_request: typing.Optional[typing.Union[AppmeshRouteSpecHttpRouteTimeoutPerRequest, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7502a4614c8554b87e268f5b08b030712f75f9a2ddf043458ebb0e8741a464f(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b79bf1fcc9775f2f3c8c4075922d4e0a00fd4c65d85cbc2125e91d74367bb30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157398d66a69b9a72d4bbc2cb4573f46965089d9b34d09428ec8eaf748ccc7fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64361ac2032e80b56a8daa333008ed74833458741a7c392ec6869216b9444dbc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301f18cfd6de60f067d17936dcc2f59ce4d513efb4258211e625c70602d7a502(
    value: typing.Optional[AppmeshRouteSpecHttpRouteTimeoutIdle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bead220bbdfc7db744cd5d0b1a3589aa67308d757a0f9d53f9bd942600e8463(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d86a8e60dc03608ddc154a25643bee8afb5b86a6a6b000a22b38f8e8b7023803(
    value: typing.Optional[AppmeshRouteSpecHttpRouteTimeout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809efb7371f5eddea62355e228e3cdec882d12f27c0c66100c64f6cc61ac9690(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea9924362ab990ae2142fa0f858ddd6b654595b546a6e8b6445163831120ee79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55856b39ae0c949646ad9f2586b1fbef11f30072be7608c6ebed0e76f435f51c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab3b778b284ecb74403213c2a7cb2376e81dada5b60403c6696175e2ff04305(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95902367a2f4739cff73bd0c59581d7c99fb2c8beb267e468e2c93be25146f60(
    value: typing.Optional[AppmeshRouteSpecHttpRouteTimeoutPerRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be05e114dfc82871af07555aa0ef90ead01713dddf262b61c539cae3ab7563db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f3a7f497b8cfd3864376dea93dd4b81210340fe9e84a485a97914b6b0e3c1f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd98829ca5e7873ce33af4d201f9b76a8f3391578ae8ad1c5418cbde2be47af(
    value: typing.Optional[AppmeshRouteSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e6e1ef12dcb7151a933e653626162ac46b6f229570ca1c73fa645e3f011838(
    *,
    action: typing.Union[AppmeshRouteSpecTcpRouteAction, typing.Dict[builtins.str, typing.Any]],
    match: typing.Optional[typing.Union[AppmeshRouteSpecTcpRouteMatch, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[typing.Union[AppmeshRouteSpecTcpRouteTimeout, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0148b4b88e44780d90bb44cafddd150bef658d239f9e140db3ac2dc2d9a4229f(
    *,
    weighted_target: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecTcpRouteActionWeightedTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb7c5a6158eedd5ea1c025d8b291d35f8aef6090e6079252ccd4a46396ade24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b001c3796bcb77ed55e3b6d996f2cd4939b5b739583d9445798669e10bdb0a2f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshRouteSpecTcpRouteActionWeightedTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d629a54c124fe59e0bb5d902a9be240fb41039f7f7bb69607af97b12e91ab7(
    value: typing.Optional[AppmeshRouteSpecTcpRouteAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a2af743b94d37fd770aa8894d2467781f44c6a9af68223bf1b732dfab474d7d(
    *,
    virtual_node: builtins.str,
    weight: jsii.Number,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8402c3953905b127ebc8d5b70fdb06e859ab86047ba0ea0ee29cee8e942b715(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a917af99700ef5aa1b221f0d4405dcd442f18c2be2dbe4cbcb7acfd1e183c0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba5416320c8999a769905c2adc0bd9c2cea95bba70d7e28d78c8c4fcfb5a2d3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4441966f095aaf79acfe6d73ff473dc9547920519b78734e4a90d19d60835da(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__343e1e1951c6313afbbabc6d07533378c2d8bb5d85c1bdf78e4479416c8de58b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d865bc09beb2ac1e904e0e0c3fe66a8bb62bade042f8887b9a0b4c78f4b6d35c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshRouteSpecTcpRouteActionWeightedTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff0a024cefb45407f34dd29ddca430203b21aa26b24ae75cefc868e32fd62572(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c0b85be3e76bf2655c9f887382a2a546486ce76e58e1e110bdf780fa38e2ed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d083c0ccf00532371eb0b5e33aa5b644d78cfbc47b3cf864a18b82d4ecff4fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f53e68e565616eae40b4b04e12f53944972459271277d88ddfbd72bc1d5f0a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b671069293e879312213439ad0744d01ddc1bcc6eb85126bea8608311c933e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshRouteSpecTcpRouteActionWeightedTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d2cb0e764df058f7fe25455c4595f84a79211cce613a13777100c6d1e55cb5(
    *,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ed49715f320a0c9aac2143bff63b7204eb734eb7d77853f312321aa59cb6cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70bf56afeb23875c5dbd8871d31d2054d729b2d46ecb79475f1e9c434f69ce13(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7999fbf1e92a49043135338006cc436096ce8f553bdb1a83d2f74e66a9f6f2ca(
    value: typing.Optional[AppmeshRouteSpecTcpRouteMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc02c41c21bbfc4ed37b2ebbb5f6ba182a9063c1576b54d66efe46ce93298449(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd5ddab1fa8ad066ddd6c2cbd958859eeef58f6e5417a9aea5d1edb2a272f11(
    value: typing.Optional[AppmeshRouteSpecTcpRoute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7bd10a1662109307e887da024a981109aed11bccea9901f0246e97c6054a50a(
    *,
    idle: typing.Optional[typing.Union[AppmeshRouteSpecTcpRouteTimeoutIdle, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9167ae58021d3e1b85d428bfb9e78d6c8a92dd5dbfda42f099912bb930623290(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8624033283cd9364a296af242dcfe745f8c9b9cdd3ea96af22971a73bfcc51b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc970a10e3d759cd76b32a786f4d4715b43d0c1def170ebacd7a174321d9355a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f42abcfd2a263ab56341506033786caa4dded4c98e8cd9ed3480a6332e8aec(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ca1437abf1a5b56ddef87993e6f01e2acf3fa7e1a5731ac263e7042ce09c05(
    value: typing.Optional[AppmeshRouteSpecTcpRouteTimeoutIdle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36547f33a3e60c74040d1d92a8e4a244a754497c8116ce63af66a56218eda97b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1089d4502013843e91c177fb51c26e1dd9f9c563ea8fb0f53ad45b6271af3418(
    value: typing.Optional[AppmeshRouteSpecTcpRouteTimeout],
) -> None:
    """Type checking stubs"""
    pass
