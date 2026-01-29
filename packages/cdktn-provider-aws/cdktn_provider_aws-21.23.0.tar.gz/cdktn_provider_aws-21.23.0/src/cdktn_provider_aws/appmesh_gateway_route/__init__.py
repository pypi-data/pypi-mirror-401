r'''
# `aws_appmesh_gateway_route`

Refer to the Terraform Registry for docs: [`aws_appmesh_gateway_route`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route).
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


class AppmeshGatewayRoute(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRoute",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route aws_appmesh_gateway_route}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        mesh_name: builtins.str,
        name: builtins.str,
        spec: typing.Union["AppmeshGatewayRouteSpec", typing.Dict[builtins.str, typing.Any]],
        virtual_gateway_name: builtins.str,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route aws_appmesh_gateway_route} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param mesh_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#mesh_name AppmeshGatewayRoute#mesh_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#name AppmeshGatewayRoute#name}.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#spec AppmeshGatewayRoute#spec}
        :param virtual_gateway_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_gateway_name AppmeshGatewayRoute#virtual_gateway_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#id AppmeshGatewayRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mesh_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#mesh_owner AppmeshGatewayRoute#mesh_owner}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#region AppmeshGatewayRoute#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#tags AppmeshGatewayRoute#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#tags_all AppmeshGatewayRoute#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71605d0cfc835df02a6eb58ec98914fb41a5ad1ad6142f35efa733ef3c9a17f4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppmeshGatewayRouteConfig(
            mesh_name=mesh_name,
            name=name,
            spec=spec,
            virtual_gateway_name=virtual_gateway_name,
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
        '''Generates CDKTF code for importing a AppmeshGatewayRoute resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppmeshGatewayRoute to import.
        :param import_from_id: The id of the existing AppmeshGatewayRoute that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppmeshGatewayRoute to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd167cadd43b9b6a9a055106fd07c9d785034491550a7271e5031ea534dd78d8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        grpc_route: typing.Optional[typing.Union["AppmeshGatewayRouteSpecGrpcRoute", typing.Dict[builtins.str, typing.Any]]] = None,
        http2_route: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2Route", typing.Dict[builtins.str, typing.Any]]] = None,
        http_route: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRoute", typing.Dict[builtins.str, typing.Any]]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param grpc_route: grpc_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#grpc_route AppmeshGatewayRoute#grpc_route}
        :param http2_route: http2_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#http2_route AppmeshGatewayRoute#http2_route}
        :param http_route: http_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#http_route AppmeshGatewayRoute#http_route}
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#priority AppmeshGatewayRoute#priority}.
        '''
        value = AppmeshGatewayRouteSpec(
            grpc_route=grpc_route,
            http2_route=http2_route,
            http_route=http_route,
            priority=priority,
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
    def spec(self) -> "AppmeshGatewayRouteSpecOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecOutputReference", jsii.get(self, "spec"))

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
    def spec_input(self) -> typing.Optional["AppmeshGatewayRouteSpec"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpec"], jsii.get(self, "specInput"))

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
    @jsii.member(jsii_name="virtualGatewayNameInput")
    def virtual_gateway_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualGatewayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f955106c7704247db649cba0a2b011de285cf334fc170743cad7ded32b59d8e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "meshName"))

    @mesh_name.setter
    def mesh_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae056571d2e9919c7d4157db4bd24dffb1e11566824a57653793c16690a72274)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "meshName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="meshOwner")
    def mesh_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "meshOwner"))

    @mesh_owner.setter
    def mesh_owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03f302a89565af4646a2abd7e2cffff77bdf336724092ec6493498c67d3d9a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "meshOwner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd1383610c7cb74dca7add1b992cf2f8db1aa5b2a8ec60e2cd5e1405d277bffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10ba9fa1418b5841be08d0743d97f4e56372b92e9cd9e3985687810957f77f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5263d195de4831d3039e1a8584aaabfc1c92f8a76dee0772fe44f4091e3e740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a6b9ffc93d0c18434b41dd70a3d015a59e697e6f5decd706ef2697d4737d83a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualGatewayName")
    def virtual_gateway_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualGatewayName"))

    @virtual_gateway_name.setter
    def virtual_gateway_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7d3f5c1d84e00e817ff3af699ed68898c7decea29c9c33b342419241b44cc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualGatewayName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteConfig",
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
        "virtual_gateway_name": "virtualGatewayName",
        "id": "id",
        "mesh_owner": "meshOwner",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class AppmeshGatewayRouteConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        spec: typing.Union["AppmeshGatewayRouteSpec", typing.Dict[builtins.str, typing.Any]],
        virtual_gateway_name: builtins.str,
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
        :param mesh_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#mesh_name AppmeshGatewayRoute#mesh_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#name AppmeshGatewayRoute#name}.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#spec AppmeshGatewayRoute#spec}
        :param virtual_gateway_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_gateway_name AppmeshGatewayRoute#virtual_gateway_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#id AppmeshGatewayRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mesh_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#mesh_owner AppmeshGatewayRoute#mesh_owner}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#region AppmeshGatewayRoute#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#tags AppmeshGatewayRoute#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#tags_all AppmeshGatewayRoute#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(spec, dict):
            spec = AppmeshGatewayRouteSpec(**spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21345109a23d44f663c5073e6d0b03ec8d36266fd94ba9462386baf1c030a4d0)
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
            check_type(argname="argument virtual_gateway_name", value=virtual_gateway_name, expected_type=type_hints["virtual_gateway_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument mesh_owner", value=mesh_owner, expected_type=type_hints["mesh_owner"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mesh_name": mesh_name,
            "name": name,
            "spec": spec,
            "virtual_gateway_name": virtual_gateway_name,
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#mesh_name AppmeshGatewayRoute#mesh_name}.'''
        result = self._values.get("mesh_name")
        assert result is not None, "Required property 'mesh_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#name AppmeshGatewayRoute#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spec(self) -> "AppmeshGatewayRouteSpec":
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#spec AppmeshGatewayRoute#spec}
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast("AppmeshGatewayRouteSpec", result)

    @builtins.property
    def virtual_gateway_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_gateway_name AppmeshGatewayRoute#virtual_gateway_name}.'''
        result = self._values.get("virtual_gateway_name")
        assert result is not None, "Required property 'virtual_gateway_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#id AppmeshGatewayRoute#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#mesh_owner AppmeshGatewayRoute#mesh_owner}.'''
        result = self._values.get("mesh_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#region AppmeshGatewayRoute#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#tags AppmeshGatewayRoute#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#tags_all AppmeshGatewayRoute#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpec",
    jsii_struct_bases=[],
    name_mapping={
        "grpc_route": "grpcRoute",
        "http2_route": "http2Route",
        "http_route": "httpRoute",
        "priority": "priority",
    },
)
class AppmeshGatewayRouteSpec:
    def __init__(
        self,
        *,
        grpc_route: typing.Optional[typing.Union["AppmeshGatewayRouteSpecGrpcRoute", typing.Dict[builtins.str, typing.Any]]] = None,
        http2_route: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2Route", typing.Dict[builtins.str, typing.Any]]] = None,
        http_route: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRoute", typing.Dict[builtins.str, typing.Any]]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param grpc_route: grpc_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#grpc_route AppmeshGatewayRoute#grpc_route}
        :param http2_route: http2_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#http2_route AppmeshGatewayRoute#http2_route}
        :param http_route: http_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#http_route AppmeshGatewayRoute#http_route}
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#priority AppmeshGatewayRoute#priority}.
        '''
        if isinstance(grpc_route, dict):
            grpc_route = AppmeshGatewayRouteSpecGrpcRoute(**grpc_route)
        if isinstance(http2_route, dict):
            http2_route = AppmeshGatewayRouteSpecHttp2Route(**http2_route)
        if isinstance(http_route, dict):
            http_route = AppmeshGatewayRouteSpecHttpRoute(**http_route)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aa6e16fc2b5355afafd3d1d1cfe177b6c14891b00f5264ff3f832e81bef71cf)
            check_type(argname="argument grpc_route", value=grpc_route, expected_type=type_hints["grpc_route"])
            check_type(argname="argument http2_route", value=http2_route, expected_type=type_hints["http2_route"])
            check_type(argname="argument http_route", value=http_route, expected_type=type_hints["http_route"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if grpc_route is not None:
            self._values["grpc_route"] = grpc_route
        if http2_route is not None:
            self._values["http2_route"] = http2_route
        if http_route is not None:
            self._values["http_route"] = http_route
        if priority is not None:
            self._values["priority"] = priority

    @builtins.property
    def grpc_route(self) -> typing.Optional["AppmeshGatewayRouteSpecGrpcRoute"]:
        '''grpc_route block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#grpc_route AppmeshGatewayRoute#grpc_route}
        '''
        result = self._values.get("grpc_route")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecGrpcRoute"], result)

    @builtins.property
    def http2_route(self) -> typing.Optional["AppmeshGatewayRouteSpecHttp2Route"]:
        '''http2_route block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#http2_route AppmeshGatewayRoute#http2_route}
        '''
        result = self._values.get("http2_route")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2Route"], result)

    @builtins.property
    def http_route(self) -> typing.Optional["AppmeshGatewayRouteSpecHttpRoute"]:
        '''http_route block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#http_route AppmeshGatewayRoute#http_route}
        '''
        result = self._values.get("http_route")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRoute"], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#priority AppmeshGatewayRoute#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRoute",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "match": "match"},
)
class AppmeshGatewayRouteSpecGrpcRoute:
    def __init__(
        self,
        *,
        action: typing.Union["AppmeshGatewayRouteSpecGrpcRouteAction", typing.Dict[builtins.str, typing.Any]],
        match: typing.Union["AppmeshGatewayRouteSpecGrpcRouteMatch", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#action AppmeshGatewayRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        if isinstance(action, dict):
            action = AppmeshGatewayRouteSpecGrpcRouteAction(**action)
        if isinstance(match, dict):
            match = AppmeshGatewayRouteSpecGrpcRouteMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b96549ad2947aac6499dd44b143729e0789802479065bf473cd38bcfd0f94b6b)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "match": match,
        }

    @builtins.property
    def action(self) -> "AppmeshGatewayRouteSpecGrpcRouteAction":
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#action AppmeshGatewayRoute#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("AppmeshGatewayRouteSpecGrpcRouteAction", result)

    @builtins.property
    def match(self) -> "AppmeshGatewayRouteSpecGrpcRouteMatch":
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("AppmeshGatewayRouteSpecGrpcRouteMatch", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecGrpcRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRouteAction",
    jsii_struct_bases=[],
    name_mapping={"target": "target"},
)
class AppmeshGatewayRouteSpecGrpcRouteAction:
    def __init__(
        self,
        *,
        target: typing.Union["AppmeshGatewayRouteSpecGrpcRouteActionTarget", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#target AppmeshGatewayRoute#target}
        '''
        if isinstance(target, dict):
            target = AppmeshGatewayRouteSpecGrpcRouteActionTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c484c38458daf8e3d693834279aa7ca4825e5a3a33473194d087fb33db930958)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
        }

    @builtins.property
    def target(self) -> "AppmeshGatewayRouteSpecGrpcRouteActionTarget":
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#target AppmeshGatewayRoute#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast("AppmeshGatewayRouteSpecGrpcRouteActionTarget", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecGrpcRouteAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecGrpcRouteActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRouteActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65ee0db815f6748954350906a496e842d75f6695eb19b2b7fb408b74e854048f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        virtual_service: typing.Union["AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService", typing.Dict[builtins.str, typing.Any]],
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param virtual_service: virtual_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_service AppmeshGatewayRoute#virtual_service}
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#port AppmeshGatewayRoute#port}.
        '''
        value = AppmeshGatewayRouteSpecGrpcRouteActionTarget(
            virtual_service=virtual_service, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putTarget", [value]))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "AppmeshGatewayRouteSpecGrpcRouteActionTargetOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecGrpcRouteActionTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecGrpcRouteActionTarget"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecGrpcRouteActionTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshGatewayRouteSpecGrpcRouteAction]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecGrpcRouteAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecGrpcRouteAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aec5eee6bd59d71de28adb44cb12816b2dc1f54958885e4b836718040f5afa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRouteActionTarget",
    jsii_struct_bases=[],
    name_mapping={"virtual_service": "virtualService", "port": "port"},
)
class AppmeshGatewayRouteSpecGrpcRouteActionTarget:
    def __init__(
        self,
        *,
        virtual_service: typing.Union["AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService", typing.Dict[builtins.str, typing.Any]],
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param virtual_service: virtual_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_service AppmeshGatewayRoute#virtual_service}
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#port AppmeshGatewayRoute#port}.
        '''
        if isinstance(virtual_service, dict):
            virtual_service = AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService(**virtual_service)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fa3298a1a80e7261452681b5738c6e38ac7b76c8da6eb0020c4141a4f1253c)
            check_type(argname="argument virtual_service", value=virtual_service, expected_type=type_hints["virtual_service"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_service": virtual_service,
        }
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def virtual_service(
        self,
    ) -> "AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService":
        '''virtual_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_service AppmeshGatewayRoute#virtual_service}
        '''
        result = self._values.get("virtual_service")
        assert result is not None, "Required property 'virtual_service' is missing"
        return typing.cast("AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService", result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#port AppmeshGatewayRoute#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecGrpcRouteActionTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecGrpcRouteActionTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRouteActionTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1054e1c8689890d8d4e417c912d61263a4d1a9f8daef8626ca24cac57209fa4a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVirtualService")
    def put_virtual_service(self, *, virtual_service_name: builtins.str) -> None:
        '''
        :param virtual_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_service_name AppmeshGatewayRoute#virtual_service_name}.
        '''
        value = AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService(
            virtual_service_name=virtual_service_name
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualService", [value]))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="virtualService")
    def virtual_service(
        self,
    ) -> "AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualServiceOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualServiceOutputReference", jsii.get(self, "virtualService"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualServiceInput")
    def virtual_service_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService"], jsii.get(self, "virtualServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff5fb51761fe2c06857003ad920e6e29294c7ad0db437bb1807c9328e5fa042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecGrpcRouteActionTarget]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecGrpcRouteActionTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecGrpcRouteActionTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16130a541c5a389e5d089893945106396979d8f0303490e16f159e7576f534aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService",
    jsii_struct_bases=[],
    name_mapping={"virtual_service_name": "virtualServiceName"},
)
class AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService:
    def __init__(self, *, virtual_service_name: builtins.str) -> None:
        '''
        :param virtual_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_service_name AppmeshGatewayRoute#virtual_service_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc976a29cf7e296d1f0c04c61c4929fcb590377fc003298bdeba0354b3c466de)
            check_type(argname="argument virtual_service_name", value=virtual_service_name, expected_type=type_hints["virtual_service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_service_name": virtual_service_name,
        }

    @builtins.property
    def virtual_service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_service_name AppmeshGatewayRoute#virtual_service_name}.'''
        result = self._values.get("virtual_service_name")
        assert result is not None, "Required property 'virtual_service_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ee5e7f45dc4afa79500c7968b7da2d2f07893f25ce6aeabf76ccb1bf622f0d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__59ae7aae7c64a87f083527beb951bb4d34141d72870f75e213910064fa0f4e33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b6702836e48f383477acad0a9e315bf167769b66f1b025e3c8967c74038188d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRouteMatch",
    jsii_struct_bases=[],
    name_mapping={"service_name": "serviceName", "port": "port"},
)
class AppmeshGatewayRouteSpecGrpcRouteMatch:
    def __init__(
        self,
        *,
        service_name: builtins.str,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#service_name AppmeshGatewayRoute#service_name}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#port AppmeshGatewayRoute#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40de0102cd2d5d605aa0be5f934208ac347b887efc61e27a23946ab22837ffac)
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_name": service_name,
        }
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#service_name AppmeshGatewayRoute#service_name}.'''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#port AppmeshGatewayRoute#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecGrpcRouteMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecGrpcRouteMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRouteMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9d0895b5eacf6a21b1bf49dedc480c6cc50253d61739f498b5aa9168e5f0c52)
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
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78757209859f38fb94e3d9aa1ac643a76d3e00bebd35b30a529d1116e3a009cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b6ce2f4e3ba46542305436b9171a4d945b1e8ca59dfe06d7ce8e053bae3d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshGatewayRouteSpecGrpcRouteMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecGrpcRouteMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecGrpcRouteMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9823d555507f5e7183867ae39cca97ab17de339f5a82a07e553d557b85302074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshGatewayRouteSpecGrpcRouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRouteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec1ce1fba46c8f382fdca493a6dc1d6b27e9cbba37e694b41c753b4e07b5a834)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        target: typing.Union[AppmeshGatewayRouteSpecGrpcRouteActionTarget, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#target AppmeshGatewayRoute#target}
        '''
        value = AppmeshGatewayRouteSpecGrpcRouteAction(target=target)

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        service_name: builtins.str,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#service_name AppmeshGatewayRoute#service_name}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#port AppmeshGatewayRoute#port}.
        '''
        value = AppmeshGatewayRouteSpecGrpcRouteMatch(
            service_name=service_name, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> AppmeshGatewayRouteSpecGrpcRouteActionOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecGrpcRouteActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> AppmeshGatewayRouteSpecGrpcRouteMatchOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecGrpcRouteMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[AppmeshGatewayRouteSpecGrpcRouteAction]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecGrpcRouteAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[AppmeshGatewayRouteSpecGrpcRouteMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecGrpcRouteMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshGatewayRouteSpecGrpcRoute]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecGrpcRoute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecGrpcRoute],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a98c6e86fd5c86992e4e6bb3888876f74031fcff7ab7a3591cfd50fe5443117d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2Route",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "match": "match"},
)
class AppmeshGatewayRouteSpecHttp2Route:
    def __init__(
        self,
        *,
        action: typing.Union["AppmeshGatewayRouteSpecHttp2RouteAction", typing.Dict[builtins.str, typing.Any]],
        match: typing.Union["AppmeshGatewayRouteSpecHttp2RouteMatch", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#action AppmeshGatewayRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        if isinstance(action, dict):
            action = AppmeshGatewayRouteSpecHttp2RouteAction(**action)
        if isinstance(match, dict):
            match = AppmeshGatewayRouteSpecHttp2RouteMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398bd04f75dccf1dd0e84f24f8e8e600323f74251dd7bdbc90139881e74c83f5)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "match": match,
        }

    @builtins.property
    def action(self) -> "AppmeshGatewayRouteSpecHttp2RouteAction":
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#action AppmeshGatewayRoute#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteAction", result)

    @builtins.property
    def match(self) -> "AppmeshGatewayRouteSpecHttp2RouteMatch":
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteMatch", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2Route(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteAction",
    jsii_struct_bases=[],
    name_mapping={"target": "target", "rewrite": "rewrite"},
)
class AppmeshGatewayRouteSpecHttp2RouteAction:
    def __init__(
        self,
        *,
        target: typing.Union["AppmeshGatewayRouteSpecHttp2RouteActionTarget", typing.Dict[builtins.str, typing.Any]],
        rewrite: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2RouteActionRewrite", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#target AppmeshGatewayRoute#target}
        :param rewrite: rewrite block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#rewrite AppmeshGatewayRoute#rewrite}
        '''
        if isinstance(target, dict):
            target = AppmeshGatewayRouteSpecHttp2RouteActionTarget(**target)
        if isinstance(rewrite, dict):
            rewrite = AppmeshGatewayRouteSpecHttp2RouteActionRewrite(**rewrite)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9e6d0ee4b7f8a29be864299fa4898257e11839eb054e34307ded7a320432e2)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument rewrite", value=rewrite, expected_type=type_hints["rewrite"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
        }
        if rewrite is not None:
            self._values["rewrite"] = rewrite

    @builtins.property
    def target(self) -> "AppmeshGatewayRouteSpecHttp2RouteActionTarget":
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#target AppmeshGatewayRoute#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteActionTarget", result)

    @builtins.property
    def rewrite(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewrite"]:
        '''rewrite block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#rewrite AppmeshGatewayRoute#rewrite}
        '''
        result = self._values.get("rewrite")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewrite"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b54ff59cfe3baad02c915968be5a053f772595246473d265932e454093fa39a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRewrite")
    def put_rewrite(
        self,
        *,
        hostname: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2RouteActionRewritePath", typing.Dict[builtins.str, typing.Any]]] = None,
        prefix: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hostname: hostname block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        :param path: path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#path AppmeshGatewayRoute#path}
        :param prefix: prefix block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteActionRewrite(
            hostname=hostname, path=path, prefix=prefix
        )

        return typing.cast(None, jsii.invoke(self, "putRewrite", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        virtual_service: typing.Union["AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService", typing.Dict[builtins.str, typing.Any]],
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param virtual_service: virtual_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_service AppmeshGatewayRoute#virtual_service}
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#port AppmeshGatewayRoute#port}.
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteActionTarget(
            virtual_service=virtual_service, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putTarget", [value]))

    @jsii.member(jsii_name="resetRewrite")
    def reset_rewrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRewrite", []))

    @builtins.property
    @jsii.member(jsii_name="rewrite")
    def rewrite(
        self,
    ) -> "AppmeshGatewayRouteSpecHttp2RouteActionRewriteOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteActionRewriteOutputReference", jsii.get(self, "rewrite"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "AppmeshGatewayRouteSpecHttp2RouteActionTargetOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteActionTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="rewriteInput")
    def rewrite_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewrite"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewrite"], jsii.get(self, "rewriteInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionTarget"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteAction]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ca20e7cb9e201f3610378cf21a423a04a42693765dfd1599803b54767b619a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionRewrite",
    jsii_struct_bases=[],
    name_mapping={"hostname": "hostname", "path": "path", "prefix": "prefix"},
)
class AppmeshGatewayRouteSpecHttp2RouteActionRewrite:
    def __init__(
        self,
        *,
        hostname: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2RouteActionRewritePath", typing.Dict[builtins.str, typing.Any]]] = None,
        prefix: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hostname: hostname block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        :param path: path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#path AppmeshGatewayRoute#path}
        :param prefix: prefix block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}
        '''
        if isinstance(hostname, dict):
            hostname = AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname(**hostname)
        if isinstance(path, dict):
            path = AppmeshGatewayRouteSpecHttp2RouteActionRewritePath(**path)
        if isinstance(prefix, dict):
            prefix = AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix(**prefix)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c54c563414948f4ba1ec87ed89da70a0b12db85e2daf56652b54cb401d839566)
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hostname is not None:
            self._values["hostname"] = hostname
        if path is not None:
            self._values["path"] = path
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def hostname(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname"]:
        '''hostname block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname"], result)

    @builtins.property
    def path(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewritePath"]:
        '''path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#path AppmeshGatewayRoute#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewritePath"], result)

    @builtins.property
    def prefix(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix"]:
        '''prefix block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteActionRewrite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname",
    jsii_struct_bases=[],
    name_mapping={"default_target_hostname": "defaultTargetHostname"},
)
class AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname:
    def __init__(self, *, default_target_hostname: builtins.str) -> None:
        '''
        :param default_target_hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#default_target_hostname AppmeshGatewayRoute#default_target_hostname}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e62c5328e5c8e60371e866d7973ce174a43ac5610c5d35887fd4dba33b7b6e)
            check_type(argname="argument default_target_hostname", value=default_target_hostname, expected_type=type_hints["default_target_hostname"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_target_hostname": default_target_hostname,
        }

    @builtins.property
    def default_target_hostname(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#default_target_hostname AppmeshGatewayRoute#default_target_hostname}.'''
        result = self._values.get("default_target_hostname")
        assert result is not None, "Required property 'default_target_hostname' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostnameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostnameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d50f8d08cefa567a2422114c205123ec5cbcda2d1ea6b373df997891eff61370)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="defaultTargetHostnameInput")
    def default_target_hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTargetHostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTargetHostname")
    def default_target_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultTargetHostname"))

    @default_target_hostname.setter
    def default_target_hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe9125612ba4aa4198be4d4dc597cf801f05443e6ebeab926119cb7fc0067ab6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTargetHostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d972992a4c5163ae3418b3d1c379910524091af3492f8f1528ebc817c1fe17ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshGatewayRouteSpecHttp2RouteActionRewriteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionRewriteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c1ac777fe94a623e74bdd9d75b8b077c7a000a4d99e486ca7d83251ebab1019)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHostname")
    def put_hostname(self, *, default_target_hostname: builtins.str) -> None:
        '''
        :param default_target_hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#default_target_hostname AppmeshGatewayRoute#default_target_hostname}.
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname(
            default_target_hostname=default_target_hostname
        )

        return typing.cast(None, jsii.invoke(self, "putHostname", [value]))

    @jsii.member(jsii_name="putPath")
    def put_path(self, *, exact: builtins.str) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteActionRewritePath(exact=exact)

        return typing.cast(None, jsii.invoke(self, "putPath", [value]))

    @jsii.member(jsii_name="putPrefix")
    def put_prefix(
        self,
        *,
        default_prefix: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#default_prefix AppmeshGatewayRoute#default_prefix}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#value AppmeshGatewayRoute#value}.
        '''
        value_ = AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix(
            default_prefix=default_prefix, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putPrefix", [value_]))

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(
        self,
    ) -> AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostnameOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostnameOutputReference, jsii.get(self, "hostname"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(
        self,
    ) -> "AppmeshGatewayRouteSpecHttp2RouteActionRewritePathOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteActionRewritePathOutputReference", jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(
        self,
    ) -> "AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefixOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefixOutputReference", jsii.get(self, "prefix"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewritePath"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewritePath"], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix"], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewrite]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewrite], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewrite],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__884c097d665f923c5824c4981072f5d5d8eb821f098259124287f12f693e855c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionRewritePath",
    jsii_struct_bases=[],
    name_mapping={"exact": "exact"},
)
class AppmeshGatewayRouteSpecHttp2RouteActionRewritePath:
    def __init__(self, *, exact: builtins.str) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e63ad52fecd4936df7fdac6cd46b837f29f7533c127fb15589e5e469f828d533)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "exact": exact,
        }

    @builtins.property
    def exact(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.'''
        result = self._values.get("exact")
        assert result is not None, "Required property 'exact' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteActionRewritePath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteActionRewritePathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionRewritePathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91008bfadbcf1aa8256c0554b2e1f180a2d7b3ef930f3ab299c8ba89ff8a5133)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__53797ef412bc84d53d9a0bfafbfc21271d18d4c253b8cb95b014dac0560e963f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewritePath]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewritePath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewritePath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__799b1904bb68f74ee4e2d88b2fbee4ec40d08cd4975844170f6dd7ee83b29e70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix",
    jsii_struct_bases=[],
    name_mapping={"default_prefix": "defaultPrefix", "value": "value"},
)
class AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix:
    def __init__(
        self,
        *,
        default_prefix: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#default_prefix AppmeshGatewayRoute#default_prefix}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#value AppmeshGatewayRoute#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22c5f264b887fcba654a7c55e2c638057f7c760ac0e8d42f4157b542bb59a408)
            check_type(argname="argument default_prefix", value=default_prefix, expected_type=type_hints["default_prefix"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_prefix is not None:
            self._values["default_prefix"] = default_prefix
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def default_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#default_prefix AppmeshGatewayRoute#default_prefix}.'''
        result = self._values.get("default_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#value AppmeshGatewayRoute#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefixOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefixOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c8a56538ad123093f49a711efbc34fc2e886592ae10276876f5d478f8cb6196)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDefaultPrefix")
    def reset_default_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultPrefix", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="defaultPrefixInput")
    def default_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultPrefix")
    def default_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultPrefix"))

    @default_prefix.setter
    def default_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70c0d75c69431458f2ca3ee15a987f07c82908e05b6d163b0393396362d67512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e0e94836e8e777525252704aa30cd8342a498751db6bec83c3d094931f0cd3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e640208b87e4103b661d91366165c86d2dc7e51a6ac152db0f3afe85daa0369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionTarget",
    jsii_struct_bases=[],
    name_mapping={"virtual_service": "virtualService", "port": "port"},
)
class AppmeshGatewayRouteSpecHttp2RouteActionTarget:
    def __init__(
        self,
        *,
        virtual_service: typing.Union["AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService", typing.Dict[builtins.str, typing.Any]],
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param virtual_service: virtual_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_service AppmeshGatewayRoute#virtual_service}
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#port AppmeshGatewayRoute#port}.
        '''
        if isinstance(virtual_service, dict):
            virtual_service = AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService(**virtual_service)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d23ae279732eb4d457d545234e75092a216323410c89b2b1527d342e34e10c1c)
            check_type(argname="argument virtual_service", value=virtual_service, expected_type=type_hints["virtual_service"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_service": virtual_service,
        }
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def virtual_service(
        self,
    ) -> "AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService":
        '''virtual_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_service AppmeshGatewayRoute#virtual_service}
        '''
        result = self._values.get("virtual_service")
        assert result is not None, "Required property 'virtual_service' is missing"
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService", result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#port AppmeshGatewayRoute#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteActionTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteActionTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35ba16721fe7ad03d7efb6ff0518554aeb9945827248ad825acef2a3f24c4f43)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVirtualService")
    def put_virtual_service(self, *, virtual_service_name: builtins.str) -> None:
        '''
        :param virtual_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_service_name AppmeshGatewayRoute#virtual_service_name}.
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService(
            virtual_service_name=virtual_service_name
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualService", [value]))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="virtualService")
    def virtual_service(
        self,
    ) -> "AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualServiceOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualServiceOutputReference", jsii.get(self, "virtualService"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualServiceInput")
    def virtual_service_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService"], jsii.get(self, "virtualServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0dd2796c2e826d724212e5920e4108b0b11a869f55feb9fcd05ebff0438b6d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionTarget]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e10e2905098d210e913764992ad2d2469fbb4bad7e18be1580bc15a4280501fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService",
    jsii_struct_bases=[],
    name_mapping={"virtual_service_name": "virtualServiceName"},
)
class AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService:
    def __init__(self, *, virtual_service_name: builtins.str) -> None:
        '''
        :param virtual_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_service_name AppmeshGatewayRoute#virtual_service_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe54f39c40d22adc366e2a748ba11fdab06a7ef19279d2ffe3fd25dfe39d02aa)
            check_type(argname="argument virtual_service_name", value=virtual_service_name, expected_type=type_hints["virtual_service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_service_name": virtual_service_name,
        }

    @builtins.property
    def virtual_service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_service_name AppmeshGatewayRoute#virtual_service_name}.'''
        result = self._values.get("virtual_service_name")
        assert result is not None, "Required property 'virtual_service_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe169db7ec1265d8a7526ee4d327bb087d30742ea095dd839d14f51853e2b325)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__5ad1f008a33f95b9c12256e5606f10e19027625be6ca1065095f7477787f71a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9091629b50fbeca94ef48ec60d49c86d906e2cd13343c38dfbaff6cd41c20d47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatch",
    jsii_struct_bases=[],
    name_mapping={
        "header": "header",
        "hostname": "hostname",
        "path": "path",
        "port": "port",
        "prefix": "prefix",
        "query_parameter": "queryParameter",
    },
)
class AppmeshGatewayRouteSpecHttp2RouteMatch:
    def __init__(
        self,
        *,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshGatewayRouteSpecHttp2RouteMatchHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        hostname: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2RouteMatchHostname", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2RouteMatchPath", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        prefix: typing.Optional[builtins.str] = None,
        query_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#header AppmeshGatewayRoute#header}
        :param hostname: hostname block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        :param path: path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#path AppmeshGatewayRoute#path}
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#port AppmeshGatewayRoute#port}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}.
        :param query_parameter: query_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#query_parameter AppmeshGatewayRoute#query_parameter}
        '''
        if isinstance(hostname, dict):
            hostname = AppmeshGatewayRouteSpecHttp2RouteMatchHostname(**hostname)
        if isinstance(path, dict):
            path = AppmeshGatewayRouteSpecHttp2RouteMatchPath(**path)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e59d404ab1ae07612011f1434f2c0e138b16e2faccf45fa7815264b8ef794062)
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument query_parameter", value=query_parameter, expected_type=type_hints["query_parameter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header is not None:
            self._values["header"] = header
        if hostname is not None:
            self._values["hostname"] = hostname
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if prefix is not None:
            self._values["prefix"] = prefix
        if query_parameter is not None:
            self._values["query_parameter"] = query_parameter

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshGatewayRouteSpecHttp2RouteMatchHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#header AppmeshGatewayRoute#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshGatewayRouteSpecHttp2RouteMatchHeader"]]], result)

    @builtins.property
    def hostname(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteMatchHostname"]:
        '''hostname block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteMatchHostname"], result)

    @builtins.property
    def path(self) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteMatchPath"]:
        '''path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#path AppmeshGatewayRoute#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteMatchPath"], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#port AppmeshGatewayRoute#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter"]]]:
        '''query_parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#query_parameter AppmeshGatewayRoute#query_parameter}
        '''
        result = self._values.get("query_parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "invert": "invert", "match": "match"},
)
class AppmeshGatewayRouteSpecHttp2RouteMatchHeader:
    def __init__(
        self,
        *,
        name: builtins.str,
        invert: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        match: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatch", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#name AppmeshGatewayRoute#name}.
        :param invert: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#invert AppmeshGatewayRoute#invert}.
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        if isinstance(match, dict):
            match = AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d785e8a03019ef300851e67124eae3cf06785469edeaa7db858b7e19fc6336c6)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#name AppmeshGatewayRoute#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def invert(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#invert AppmeshGatewayRoute#invert}.'''
        result = self._values.get("invert")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def match(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatch"]:
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatch"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteMatchHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteMatchHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf5788a8a2df7b151ab73f745bc5e7cc81cf11a99e5b4ae39a0c566a7373945d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppmeshGatewayRouteSpecHttp2RouteMatchHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__429bca5fdc5ce8b4d73d2e48594ac754b94f781895a4be2fc5dc07829ee7689f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteMatchHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb912779519972e42d19ff7c19e247b8002e5cd168929da2553513a8ce5eb0c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f787ac3825460a3101f269fc5d4c2d2e560ec24e5fd008985726312d49f6444f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6852dd50cd5bfe57d918a3816306f77655eb07fc9720dcf835c21c9f0bfe8a2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttp2RouteMatchHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttp2RouteMatchHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttp2RouteMatchHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee06470aafe08ad9fd540f4d8084b4458b49621a3e7ef6f2a0821f8bc79257b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatch",
    jsii_struct_bases=[],
    name_mapping={
        "exact": "exact",
        "prefix": "prefix",
        "range": "range",
        "regex": "regex",
        "suffix": "suffix",
    },
)
class AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatch:
    def __init__(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        range: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRange", typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}.
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#range AppmeshGatewayRoute#range}
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#regex AppmeshGatewayRoute#regex}.
        :param suffix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#suffix AppmeshGatewayRoute#suffix}.
        '''
        if isinstance(range, dict):
            range = AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRange(**range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5bf33544b07b4f593c9f07d57b35e35c9c7e6189e656c3f2e519daa2399fd96)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.'''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRange"]:
        '''range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#range AppmeshGatewayRoute#range}
        '''
        result = self._values.get("range")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRange"], result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#regex AppmeshGatewayRoute#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#suffix AppmeshGatewayRoute#suffix}.'''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c49a663c7fe1854ba52c8a1a63d50e629cd54633375481c566c7394fd525234e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRange")
    def put_range(self, *, end: jsii.Number, start: jsii.Number) -> None:
        '''
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#end AppmeshGatewayRoute#end}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#start AppmeshGatewayRoute#start}.
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRange(
            end=end, start=start
        )

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
    ) -> "AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRangeOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRangeOutputReference", jsii.get(self, "range"))

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
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRange"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRange"], jsii.get(self, "rangeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d670dd5f6d208251ab061a2949e587376712333cea775d5bda1974033592e998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd906d687ec9e35e108c2eb29f45cb472a2b42bff4c0672b064f2e3200355163)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fde6990f369288d9e20153edc39ec1f97948df0bacd62324518ec6381d2aa85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7bdd536da8e658c3e54798b5c769783ea7a252b8e17d114834a0ba460c02151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b32324d2aff42bb40c86b5e9012d4d375335ef26a40179c3e357a80339286f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRange",
    jsii_struct_bases=[],
    name_mapping={"end": "end", "start": "start"},
)
class AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRange:
    def __init__(self, *, end: jsii.Number, start: jsii.Number) -> None:
        '''
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#end AppmeshGatewayRoute#end}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#start AppmeshGatewayRoute#start}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc2945d86f27725c86196ccf3ef2b16ae33d61a5f152899cc72cb5bbbbb571d)
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end": end,
            "start": start,
        }

    @builtins.property
    def end(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#end AppmeshGatewayRoute#end}.'''
        result = self._values.get("end")
        assert result is not None, "Required property 'end' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#start AppmeshGatewayRoute#start}.'''
        result = self._values.get("start")
        assert result is not None, "Required property 'start' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__886c39c40f8038d364d0120cacd3a6bc2fe098e2e224f2cba75c643029023839)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ace3afb3d4995692cfd7df2898bd80ec3368a586c48eae93410c5690275e7d1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "start"))

    @start.setter
    def start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9af5b3b4dea80720fb548557662fe8fa131fc6a5ea69b024fb4daab109b49454)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRange]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b9650bf8d0ca459abaf691573c13a41491f008e4de69a83771da29d622a1ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshGatewayRouteSpecHttp2RouteMatchHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8ac99d0ea7d7990e2934d027af1d92ae2b0b3ffedfd8a29f0f4f679feb25ca5)
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
        range: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRange, typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}.
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#range AppmeshGatewayRoute#range}
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#regex AppmeshGatewayRoute#regex}.
        :param suffix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#suffix AppmeshGatewayRoute#suffix}.
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatch(
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
    def match(self) -> AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchOutputReference, jsii.get(self, "match"))

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
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatch], jsii.get(self, "matchInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f53b4fcad053a0d9c7bc7e16632b23ff414bab3bbcea1abcdd86f7fcc0bf32a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e803319e58efe0010bd6239df5aa00f1e31af7769dac355fb5fb7ac518df264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshGatewayRouteSpecHttp2RouteMatchHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshGatewayRouteSpecHttp2RouteMatchHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshGatewayRouteSpecHttp2RouteMatchHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7e957750cfd0e6fdf96d557812a9bc2260f4dfee533b927639735314213ff63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchHostname",
    jsii_struct_bases=[],
    name_mapping={"exact": "exact", "suffix": "suffix"},
)
class AppmeshGatewayRouteSpecHttp2RouteMatchHostname:
    def __init__(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        :param suffix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#suffix AppmeshGatewayRoute#suffix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dbdb201bf33e07408e5372be866a244d6c00a798c28188768dbb170d7fa4585)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exact is not None:
            self._values["exact"] = exact
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.'''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#suffix AppmeshGatewayRoute#suffix}.'''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteMatchHostname(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteMatchHostnameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchHostnameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a86f7add122516887ce551d363bafce0779b0eb89015a78f170cef97514b11ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetSuffix")
    def reset_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8cd9f2dc0e1a721141b5a59d1413a0d3fb60b2a39bb92639dd4da21a2b1ba847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9de98c27506e552826c3518cae1d26eb6ac806c91015f3c33ed409f01e3e79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHostname]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHostname], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHostname],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b8de4acb8e4c1b56e33a8b1360fa243bf2fd1db9c88912e06f3e0c0259bdd1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshGatewayRouteSpecHttp2RouteMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9fe8805ff8f62384bced1984c9fd98182845eeddb8017e9910254d689eb86d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatchHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0f82f4b4950a7c85f3376529bf2593142f58316c807b448592aa0d67e5993e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="putHostname")
    def put_hostname(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        :param suffix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#suffix AppmeshGatewayRoute#suffix}.
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteMatchHostname(
            exact=exact, suffix=suffix
        )

        return typing.cast(None, jsii.invoke(self, "putHostname", [value]))

    @jsii.member(jsii_name="putPath")
    def put_path(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#regex AppmeshGatewayRoute#regex}.
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteMatchPath(exact=exact, regex=regex)

        return typing.cast(None, jsii.invoke(self, "putPath", [value]))

    @jsii.member(jsii_name="putQueryParameter")
    def put_query_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be668200bc09c3fb7973c6058d3cdd3c9ac333acbd0bac92b3ab55bfc1cb00e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQueryParameter", [value]))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

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

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> AppmeshGatewayRouteSpecHttp2RouteMatchHeaderList:
        return typing.cast(AppmeshGatewayRouteSpecHttp2RouteMatchHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> AppmeshGatewayRouteSpecHttp2RouteMatchHostnameOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttp2RouteMatchHostnameOutputReference, jsii.get(self, "hostname"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> "AppmeshGatewayRouteSpecHttp2RouteMatchPathOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteMatchPathOutputReference", jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="queryParameter")
    def query_parameter(
        self,
    ) -> "AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterList":
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterList", jsii.get(self, "queryParameter"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttp2RouteMatchHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttp2RouteMatchHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHostname]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHostname], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteMatchPath"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteMatchPath"], jsii.get(self, "pathInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter"]]], jsii.get(self, "queryParameterInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebe8ed75fd4b433157349a94cb13b34453703b8408b8b58390612d40b3a80fe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4345e0496395986271436ffae44294b1bfdf18c3f3c0e9b8a8faa61eabb7425)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56a42f415c0ccecb84872ca6a53f5e8d5e7aa2193877dca7203bd25f706262d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchPath",
    jsii_struct_bases=[],
    name_mapping={"exact": "exact", "regex": "regex"},
)
class AppmeshGatewayRouteSpecHttp2RouteMatchPath:
    def __init__(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#regex AppmeshGatewayRoute#regex}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a8c1a61794ebc6f6d684c218fef9d373333f2f7c3f0c4b81f6ba246becb0ca4)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exact is not None:
            self._values["exact"] = exact
        if regex is not None:
            self._values["regex"] = regex

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.'''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#regex AppmeshGatewayRoute#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteMatchPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteMatchPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__111643caefbaa692891573213698da1d5168242748f10be78a72743ae5e06012)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b602a7d6440c662782cc93cc3981fbe8d5b1b1cce029c3b9f6d85977149266a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f11dfafeed0923fad72d823cd1c06b26147849b2820ad03e46ef25369d216aba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchPath]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchPath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81186c21c0dcf9e2d3ca75aabd738ceedd68ea91792304d98ee05a254fc9d2a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "match": "match"},
)
class AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter:
    def __init__(
        self,
        *,
        name: builtins.str,
        match: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatch", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#name AppmeshGatewayRoute#name}.
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        if isinstance(match, dict):
            match = AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7afbea58c03f88afbb4b54bcff6a4675bca35e13e7212186aa7318461eaa1212)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if match is not None:
            self._values["match"] = match

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#name AppmeshGatewayRoute#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatch"]:
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatch"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ae14a8ce49c6d1f7b67ecd4acd1e78df16e6bb4e7dd5e5a4ab442ecdc1c7a01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b490c6ae8297a16bc39e4749b6b0d9a5e07fa1beba2b94409bae0cea332a30b7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ec35f02107fd95cdf162ce03dab1fba7102ce61f0c4cf0bf1dc2ae9a44dc74a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e2275a02d74713967d2fa96db84c2b041f276fa5e2e3ee75f6ccc8d7ad6e081)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab4ced80ab28b0299b8b504b3f7d98ee9fe5169a7cb7bf2f699a90e9b94154fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ce10d9f4f5d8b20b94e68430cc3d1eb5968e1477f2abd5e26872e1b1e153ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatch",
    jsii_struct_bases=[],
    name_mapping={"exact": "exact"},
)
class AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatch:
    def __init__(self, *, exact: typing.Optional[builtins.str] = None) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42d16adbbe304128f8651d3f6e64f9e816511d6545b6527e4be261112bd3350c)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exact is not None:
            self._values["exact"] = exact

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.'''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a882724e491bca091b2facdd69dac5514700a45b88ff73216db7e6fc27bcd41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__578ed17c0d4cbec2f78ab3e310c4735b3ee6d0fbc8a99d3dbfe4caf07753319b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb932b8b1f03e13e52ff99c3183a284fbbf94d5161d0d7dd2e53f940bfac1dc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfef4e9ad040557f336ff4c5cadf93ad3c8c674ed49a6170b88ab8e155911f8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatch")
    def put_match(self, *, exact: typing.Optional[builtins.str] = None) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatch(exact=exact)

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(
        self,
    ) -> AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatchOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatch], jsii.get(self, "matchInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e3c157f7919f619f774a8b2ad48d0b79f8adc82ca5c66fe36aef4208f30911fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fadaea8d2aa5d5b5eae3ef48f10ea294439000bfe589cb97521a04be9fe79473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshGatewayRouteSpecHttp2RouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7476e00e4c0834a840dbc84e04575f621d350cd569d73bde3fd5d0089e098e90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        target: typing.Union[AppmeshGatewayRouteSpecHttp2RouteActionTarget, typing.Dict[builtins.str, typing.Any]],
        rewrite: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteActionRewrite, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#target AppmeshGatewayRoute#target}
        :param rewrite: rewrite block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#rewrite AppmeshGatewayRoute#rewrite}
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteAction(target=target, rewrite=rewrite)

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatchHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
        hostname: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatchHostname, typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatchPath, typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        prefix: typing.Optional[builtins.str] = None,
        query_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#header AppmeshGatewayRoute#header}
        :param hostname: hostname block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        :param path: path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#path AppmeshGatewayRoute#path}
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#port AppmeshGatewayRoute#port}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}.
        :param query_parameter: query_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#query_parameter AppmeshGatewayRoute#query_parameter}
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteMatch(
            header=header,
            hostname=hostname,
            path=path,
            port=port,
            prefix=prefix,
            query_parameter=query_parameter,
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> AppmeshGatewayRouteSpecHttp2RouteActionOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttp2RouteActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> AppmeshGatewayRouteSpecHttp2RouteMatchOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttp2RouteMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteAction]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshGatewayRouteSpecHttp2Route]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2Route], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2Route],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bf9e4017efb65bfb30ea999d7c2a643753edb48521f2166a976f61a3afdfd9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRoute",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "match": "match"},
)
class AppmeshGatewayRouteSpecHttpRoute:
    def __init__(
        self,
        *,
        action: typing.Union["AppmeshGatewayRouteSpecHttpRouteAction", typing.Dict[builtins.str, typing.Any]],
        match: typing.Union["AppmeshGatewayRouteSpecHttpRouteMatch", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#action AppmeshGatewayRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        if isinstance(action, dict):
            action = AppmeshGatewayRouteSpecHttpRouteAction(**action)
        if isinstance(match, dict):
            match = AppmeshGatewayRouteSpecHttpRouteMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3dad8721a921fa93b8a067552a823f04ce40750f97be510a26083d7bd37905)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "match": match,
        }

    @builtins.property
    def action(self) -> "AppmeshGatewayRouteSpecHttpRouteAction":
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#action AppmeshGatewayRoute#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteAction", result)

    @builtins.property
    def match(self) -> "AppmeshGatewayRouteSpecHttpRouteMatch":
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteMatch", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteAction",
    jsii_struct_bases=[],
    name_mapping={"target": "target", "rewrite": "rewrite"},
)
class AppmeshGatewayRouteSpecHttpRouteAction:
    def __init__(
        self,
        *,
        target: typing.Union["AppmeshGatewayRouteSpecHttpRouteActionTarget", typing.Dict[builtins.str, typing.Any]],
        rewrite: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRouteActionRewrite", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#target AppmeshGatewayRoute#target}
        :param rewrite: rewrite block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#rewrite AppmeshGatewayRoute#rewrite}
        '''
        if isinstance(target, dict):
            target = AppmeshGatewayRouteSpecHttpRouteActionTarget(**target)
        if isinstance(rewrite, dict):
            rewrite = AppmeshGatewayRouteSpecHttpRouteActionRewrite(**rewrite)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15f22a260078a24d170ff86b15997470d867193964e1c0bb5ddccc1e058da761)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument rewrite", value=rewrite, expected_type=type_hints["rewrite"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
        }
        if rewrite is not None:
            self._values["rewrite"] = rewrite

    @builtins.property
    def target(self) -> "AppmeshGatewayRouteSpecHttpRouteActionTarget":
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#target AppmeshGatewayRoute#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteActionTarget", result)

    @builtins.property
    def rewrite(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewrite"]:
        '''rewrite block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#rewrite AppmeshGatewayRoute#rewrite}
        '''
        result = self._values.get("rewrite")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewrite"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de5d9d3d90233afdc804c5ca0095b37611b01f16e27849616cae0541ef8bc15b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRewrite")
    def put_rewrite(
        self,
        *,
        hostname: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRouteActionRewritePath", typing.Dict[builtins.str, typing.Any]]] = None,
        prefix: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hostname: hostname block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        :param path: path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#path AppmeshGatewayRoute#path}
        :param prefix: prefix block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}
        '''
        value = AppmeshGatewayRouteSpecHttpRouteActionRewrite(
            hostname=hostname, path=path, prefix=prefix
        )

        return typing.cast(None, jsii.invoke(self, "putRewrite", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        virtual_service: typing.Union["AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService", typing.Dict[builtins.str, typing.Any]],
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param virtual_service: virtual_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_service AppmeshGatewayRoute#virtual_service}
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#port AppmeshGatewayRoute#port}.
        '''
        value = AppmeshGatewayRouteSpecHttpRouteActionTarget(
            virtual_service=virtual_service, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putTarget", [value]))

    @jsii.member(jsii_name="resetRewrite")
    def reset_rewrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRewrite", []))

    @builtins.property
    @jsii.member(jsii_name="rewrite")
    def rewrite(self) -> "AppmeshGatewayRouteSpecHttpRouteActionRewriteOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteActionRewriteOutputReference", jsii.get(self, "rewrite"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "AppmeshGatewayRouteSpecHttpRouteActionTargetOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteActionTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="rewriteInput")
    def rewrite_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewrite"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewrite"], jsii.get(self, "rewriteInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionTarget"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteAction]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d76f3b607c21443cff0c0e2e97261514164473f188ab2222079ca4f031ef005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionRewrite",
    jsii_struct_bases=[],
    name_mapping={"hostname": "hostname", "path": "path", "prefix": "prefix"},
)
class AppmeshGatewayRouteSpecHttpRouteActionRewrite:
    def __init__(
        self,
        *,
        hostname: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRouteActionRewritePath", typing.Dict[builtins.str, typing.Any]]] = None,
        prefix: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hostname: hostname block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        :param path: path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#path AppmeshGatewayRoute#path}
        :param prefix: prefix block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}
        '''
        if isinstance(hostname, dict):
            hostname = AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname(**hostname)
        if isinstance(path, dict):
            path = AppmeshGatewayRouteSpecHttpRouteActionRewritePath(**path)
        if isinstance(prefix, dict):
            prefix = AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix(**prefix)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f7c2832f8b020f8f4ffc3675092860e7300caa107f6a69b033f97b8b59e322d)
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hostname is not None:
            self._values["hostname"] = hostname
        if path is not None:
            self._values["path"] = path
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def hostname(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname"]:
        '''hostname block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname"], result)

    @builtins.property
    def path(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewritePath"]:
        '''path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#path AppmeshGatewayRoute#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewritePath"], result)

    @builtins.property
    def prefix(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix"]:
        '''prefix block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteActionRewrite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname",
    jsii_struct_bases=[],
    name_mapping={"default_target_hostname": "defaultTargetHostname"},
)
class AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname:
    def __init__(self, *, default_target_hostname: builtins.str) -> None:
        '''
        :param default_target_hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#default_target_hostname AppmeshGatewayRoute#default_target_hostname}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd2168f97e67b561a3b74052ec6bf4cb95b45811638c7fc184a1d30be24ad8af)
            check_type(argname="argument default_target_hostname", value=default_target_hostname, expected_type=type_hints["default_target_hostname"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_target_hostname": default_target_hostname,
        }

    @builtins.property
    def default_target_hostname(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#default_target_hostname AppmeshGatewayRoute#default_target_hostname}.'''
        result = self._values.get("default_target_hostname")
        assert result is not None, "Required property 'default_target_hostname' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteActionRewriteHostnameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionRewriteHostnameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__934c5fb3024722668e2b64c78a2f5b5ab6d7e858a90e298eb2c2d00a2d44afb6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="defaultTargetHostnameInput")
    def default_target_hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTargetHostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTargetHostname")
    def default_target_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultTargetHostname"))

    @default_target_hostname.setter
    def default_target_hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d97d7a0073292da166027ecb21e5cca1c7db8f7bdeb2d94330a015414044c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTargetHostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f7491b4f03d76976a4b4e234cf4a22e222133d1566adca6f2c178fde8530557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshGatewayRouteSpecHttpRouteActionRewriteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionRewriteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8f088c59d94fdc6d0137c7bd0d418f2e1588fb20b90bd82f4b49a9f79bf9d7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHostname")
    def put_hostname(self, *, default_target_hostname: builtins.str) -> None:
        '''
        :param default_target_hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#default_target_hostname AppmeshGatewayRoute#default_target_hostname}.
        '''
        value = AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname(
            default_target_hostname=default_target_hostname
        )

        return typing.cast(None, jsii.invoke(self, "putHostname", [value]))

    @jsii.member(jsii_name="putPath")
    def put_path(self, *, exact: builtins.str) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        '''
        value = AppmeshGatewayRouteSpecHttpRouteActionRewritePath(exact=exact)

        return typing.cast(None, jsii.invoke(self, "putPath", [value]))

    @jsii.member(jsii_name="putPrefix")
    def put_prefix(
        self,
        *,
        default_prefix: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#default_prefix AppmeshGatewayRoute#default_prefix}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#value AppmeshGatewayRoute#value}.
        '''
        value_ = AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix(
            default_prefix=default_prefix, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putPrefix", [value_]))

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(
        self,
    ) -> AppmeshGatewayRouteSpecHttpRouteActionRewriteHostnameOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttpRouteActionRewriteHostnameOutputReference, jsii.get(self, "hostname"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(
        self,
    ) -> "AppmeshGatewayRouteSpecHttpRouteActionRewritePathOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteActionRewritePathOutputReference", jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(
        self,
    ) -> "AppmeshGatewayRouteSpecHttpRouteActionRewritePrefixOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteActionRewritePrefixOutputReference", jsii.get(self, "prefix"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewritePath"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewritePath"], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix"], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewrite]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewrite], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewrite],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a911b4d463b6c58432e9c745917f6a6bd33ba0ff4c9b7aeb8c7b532d4a30fbcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionRewritePath",
    jsii_struct_bases=[],
    name_mapping={"exact": "exact"},
)
class AppmeshGatewayRouteSpecHttpRouteActionRewritePath:
    def __init__(self, *, exact: builtins.str) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31f60cb26eef51b8abcf6891474012fcff7481304716e9fffdb99dbb0d599ec)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "exact": exact,
        }

    @builtins.property
    def exact(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.'''
        result = self._values.get("exact")
        assert result is not None, "Required property 'exact' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteActionRewritePath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteActionRewritePathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionRewritePathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e843e8ef686010bd6d07eb07a584f071f29af52b3be5853e1f0d0b5e2cf069a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__cb89046758071c17d02ca9e2c6a5e35c3dffc85ebf10be1614f1c7858790ca0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewritePath]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewritePath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewritePath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fed9c31ac361769c8f4516b50aa1b48dc8674f68880e846721ebda2b7dd9fb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix",
    jsii_struct_bases=[],
    name_mapping={"default_prefix": "defaultPrefix", "value": "value"},
)
class AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix:
    def __init__(
        self,
        *,
        default_prefix: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#default_prefix AppmeshGatewayRoute#default_prefix}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#value AppmeshGatewayRoute#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41c066ffa731a7729e31708b244e1e2c609375ad0ff5ca741d784d622afc8076)
            check_type(argname="argument default_prefix", value=default_prefix, expected_type=type_hints["default_prefix"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_prefix is not None:
            self._values["default_prefix"] = default_prefix
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def default_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#default_prefix AppmeshGatewayRoute#default_prefix}.'''
        result = self._values.get("default_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#value AppmeshGatewayRoute#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteActionRewritePrefixOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionRewritePrefixOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52c05789a708f6a0634dbe2db648756eb7072f95f26a049c0262cbf949d2a672)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDefaultPrefix")
    def reset_default_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultPrefix", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="defaultPrefixInput")
    def default_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultPrefix")
    def default_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultPrefix"))

    @default_prefix.setter
    def default_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1687318704c3133baef5fdf4c0c10c173a06d7c877a177b319dbb55c38f56930)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417f7f9fc6cc29405d619d75892a4235aeea5d21a15379f88edf7e377c47062b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e1f382c0627570dfce3c9de55452b9db931ae2ace7ae609c0290d82fccb5a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionTarget",
    jsii_struct_bases=[],
    name_mapping={"virtual_service": "virtualService", "port": "port"},
)
class AppmeshGatewayRouteSpecHttpRouteActionTarget:
    def __init__(
        self,
        *,
        virtual_service: typing.Union["AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService", typing.Dict[builtins.str, typing.Any]],
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param virtual_service: virtual_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_service AppmeshGatewayRoute#virtual_service}
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#port AppmeshGatewayRoute#port}.
        '''
        if isinstance(virtual_service, dict):
            virtual_service = AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService(**virtual_service)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__835377e4110bb8bdfc923ee342d05e943cd49fe23968d7ead8df317883af8807)
            check_type(argname="argument virtual_service", value=virtual_service, expected_type=type_hints["virtual_service"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_service": virtual_service,
        }
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def virtual_service(
        self,
    ) -> "AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService":
        '''virtual_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_service AppmeshGatewayRoute#virtual_service}
        '''
        result = self._values.get("virtual_service")
        assert result is not None, "Required property 'virtual_service' is missing"
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService", result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#port AppmeshGatewayRoute#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteActionTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteActionTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db6df76a224767b7337a9f3c6202c5be2a8f131da46ee47bf04cb3008568b7d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVirtualService")
    def put_virtual_service(self, *, virtual_service_name: builtins.str) -> None:
        '''
        :param virtual_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_service_name AppmeshGatewayRoute#virtual_service_name}.
        '''
        value = AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService(
            virtual_service_name=virtual_service_name
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualService", [value]))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="virtualService")
    def virtual_service(
        self,
    ) -> "AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualServiceOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualServiceOutputReference", jsii.get(self, "virtualService"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualServiceInput")
    def virtual_service_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService"], jsii.get(self, "virtualServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcefcaaf56ef41cb70c8a837b1749f78b81b5f30ad295007bab703db1b867676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionTarget]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b29e566ca044c2a8f6fb73645bcf99f823254a5aa8202e82be3e813a17ba41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService",
    jsii_struct_bases=[],
    name_mapping={"virtual_service_name": "virtualServiceName"},
)
class AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService:
    def __init__(self, *, virtual_service_name: builtins.str) -> None:
        '''
        :param virtual_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_service_name AppmeshGatewayRoute#virtual_service_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3fc95db68cd1d66fa61b6cb270fc24f4ed497da3ec5f55d5a8963c0a582b1fa)
            check_type(argname="argument virtual_service_name", value=virtual_service_name, expected_type=type_hints["virtual_service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_service_name": virtual_service_name,
        }

    @builtins.property
    def virtual_service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#virtual_service_name AppmeshGatewayRoute#virtual_service_name}.'''
        result = self._values.get("virtual_service_name")
        assert result is not None, "Required property 'virtual_service_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__244dbb7167bf8224559e071d78d334138189116253a1458f47fab3a7ab7383b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__c5e35f2f9306d81002cf00fafcfa570589cd9a4962799d26bc9897ffa083bf83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f1df972c444ecdec022426761bd0ab9cc1ad94687910942c76fbb1f3d724c78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatch",
    jsii_struct_bases=[],
    name_mapping={
        "header": "header",
        "hostname": "hostname",
        "path": "path",
        "port": "port",
        "prefix": "prefix",
        "query_parameter": "queryParameter",
    },
)
class AppmeshGatewayRouteSpecHttpRouteMatch:
    def __init__(
        self,
        *,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshGatewayRouteSpecHttpRouteMatchHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        hostname: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRouteMatchHostname", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRouteMatchPath", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        prefix: typing.Optional[builtins.str] = None,
        query_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#header AppmeshGatewayRoute#header}
        :param hostname: hostname block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        :param path: path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#path AppmeshGatewayRoute#path}
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#port AppmeshGatewayRoute#port}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}.
        :param query_parameter: query_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#query_parameter AppmeshGatewayRoute#query_parameter}
        '''
        if isinstance(hostname, dict):
            hostname = AppmeshGatewayRouteSpecHttpRouteMatchHostname(**hostname)
        if isinstance(path, dict):
            path = AppmeshGatewayRouteSpecHttpRouteMatchPath(**path)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30bba9194ea0ec1171d29411f141af8e162fb9d56595d304f65694549c0d7722)
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument query_parameter", value=query_parameter, expected_type=type_hints["query_parameter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header is not None:
            self._values["header"] = header
        if hostname is not None:
            self._values["hostname"] = hostname
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if prefix is not None:
            self._values["prefix"] = prefix
        if query_parameter is not None:
            self._values["query_parameter"] = query_parameter

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshGatewayRouteSpecHttpRouteMatchHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#header AppmeshGatewayRoute#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshGatewayRouteSpecHttpRouteMatchHeader"]]], result)

    @builtins.property
    def hostname(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteMatchHostname"]:
        '''hostname block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteMatchHostname"], result)

    @builtins.property
    def path(self) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteMatchPath"]:
        '''path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#path AppmeshGatewayRoute#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteMatchPath"], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#port AppmeshGatewayRoute#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter"]]]:
        '''query_parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#query_parameter AppmeshGatewayRoute#query_parameter}
        '''
        result = self._values.get("query_parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "invert": "invert", "match": "match"},
)
class AppmeshGatewayRouteSpecHttpRouteMatchHeader:
    def __init__(
        self,
        *,
        name: builtins.str,
        invert: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        match: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatch", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#name AppmeshGatewayRoute#name}.
        :param invert: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#invert AppmeshGatewayRoute#invert}.
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        if isinstance(match, dict):
            match = AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f6ef3054223acc397f8be6f88239918fde795d017399e6505203e05f2a3dd82)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#name AppmeshGatewayRoute#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def invert(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#invert AppmeshGatewayRoute#invert}.'''
        result = self._values.get("invert")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def match(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatch"]:
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatch"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteMatchHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteMatchHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__685f050d086ea5ba5da48c9f61033091b21758c5340624379fd04212b361bcbe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppmeshGatewayRouteSpecHttpRouteMatchHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba93bb7d4df1eacffb623e9da1b206b364c461b1b730760965414dfc2003851)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteMatchHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0122a15f17313d53b67ef27a4d38735b6c25b5b2828684aac43f780d446b8f9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69aa405e22471498d22ad056c8912d0205d1e960832a8da57099b2c8db5dba8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae70445693f1a6c50b2a9f4c0ec46aa70e50a6067c1fc50724be713d2cf87686)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttpRouteMatchHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttpRouteMatchHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttpRouteMatchHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b560ba8046f777eab9758d6964eebed8044d4b21c9713d4fc216fefc7977d4ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatch",
    jsii_struct_bases=[],
    name_mapping={
        "exact": "exact",
        "prefix": "prefix",
        "range": "range",
        "regex": "regex",
        "suffix": "suffix",
    },
)
class AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatch:
    def __init__(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        range: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRange", typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}.
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#range AppmeshGatewayRoute#range}
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#regex AppmeshGatewayRoute#regex}.
        :param suffix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#suffix AppmeshGatewayRoute#suffix}.
        '''
        if isinstance(range, dict):
            range = AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRange(**range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183d3995beda12ce5d0d0819e66b846b595c4bba2b6a1ae966f8af0e89ab35bf)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.'''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRange"]:
        '''range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#range AppmeshGatewayRoute#range}
        '''
        result = self._values.get("range")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRange"], result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#regex AppmeshGatewayRoute#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#suffix AppmeshGatewayRoute#suffix}.'''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e9b247b3ef8543eaa39fe0a3407d6adbb70c5b34a41f46fc191c5b902c7b4c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRange")
    def put_range(self, *, end: jsii.Number, start: jsii.Number) -> None:
        '''
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#end AppmeshGatewayRoute#end}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#start AppmeshGatewayRoute#start}.
        '''
        value = AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRange(
            end=end, start=start
        )

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
    ) -> "AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRangeOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRangeOutputReference", jsii.get(self, "range"))

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
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRange"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRange"], jsii.get(self, "rangeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f08225b8a2010fd6e5731d1aec0ed9b1d75f9792beaf7beca40c7872f0d14060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f55f6b2a8d6ae6e63d59b3031cb5b9c06fee9312402e8144a204a731bd46bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa7232c56150318999ac4b66520c3ed550c2e6a962dcc12ce55cc9da50483046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe04b398f42c323077115943eb90f94d8a71a0f591fca9df6d3304a2a5d83f6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c54db7cfce66e2078578d471750495c880d5c71ade1d66222394ca9b3de531b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRange",
    jsii_struct_bases=[],
    name_mapping={"end": "end", "start": "start"},
)
class AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRange:
    def __init__(self, *, end: jsii.Number, start: jsii.Number) -> None:
        '''
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#end AppmeshGatewayRoute#end}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#start AppmeshGatewayRoute#start}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c25d27a9291b17c04e1ed7fef83eb814b838ce65c6b29016b457eba989a14a)
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end": end,
            "start": start,
        }

    @builtins.property
    def end(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#end AppmeshGatewayRoute#end}.'''
        result = self._values.get("end")
        assert result is not None, "Required property 'end' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#start AppmeshGatewayRoute#start}.'''
        result = self._values.get("start")
        assert result is not None, "Required property 'start' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94c4bd668756a25d6e810b741f183191a499681f258f2194e0eb233b494a3cd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e842635aa4108a3a5074522b43d8abf28739d42f612f623fb93dfcdc402c6925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "start"))

    @start.setter
    def start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aa2650138d1c28a5f91203a35393a35b83d588e134f47204418e280333e5a69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRange]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85a0009848fef778892184fdea9c3928e4f2ef6d1c75eec58291ff977a279fbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshGatewayRouteSpecHttpRouteMatchHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7547429ca3fe5c88074d5f6bc5754566ca404ea7558db42688ce4de0e745a63)
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
        range: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRange, typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}.
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#range AppmeshGatewayRoute#range}
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#regex AppmeshGatewayRoute#regex}.
        :param suffix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#suffix AppmeshGatewayRoute#suffix}.
        '''
        value = AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatch(
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
    def match(self) -> AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchOutputReference, jsii.get(self, "match"))

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
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatch], jsii.get(self, "matchInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3f441b7884a47f972ef9d2ec9a3fa3a845522092d7c68ac3edf9b20a716ab3f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d280aa82bff33e4552ebdb071a9fa2057936bdee5953a982e2dc1ca385bc980)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshGatewayRouteSpecHttpRouteMatchHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshGatewayRouteSpecHttpRouteMatchHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshGatewayRouteSpecHttpRouteMatchHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd876b38f9b33f67501034b4c2304120496ebc675a1b1907477b5b6d2474c9fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchHostname",
    jsii_struct_bases=[],
    name_mapping={"exact": "exact", "suffix": "suffix"},
)
class AppmeshGatewayRouteSpecHttpRouteMatchHostname:
    def __init__(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        :param suffix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#suffix AppmeshGatewayRoute#suffix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__793802822d0e6acf81cf63a2bb63f9ec209e48c84ef4801e72a6939879738f20)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exact is not None:
            self._values["exact"] = exact
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.'''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#suffix AppmeshGatewayRoute#suffix}.'''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteMatchHostname(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteMatchHostnameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchHostnameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1d1621f6ac728ec9b506b502a8cf07fd4fbdbb3e72f2c5ee90578c205db1603)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetSuffix")
    def reset_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4b7d864609e4ccb884c3ca0b95bf3dac555223d58c86a77183187f6d15cc6acc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88cc5b5827222dc14510a2f5d333501bc657da05309d5e163c6e0e921e791f27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHostname]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHostname], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHostname],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e4e24271d5af7a75e19b30e426a99602840e47e986fa44eaf6d640544eb5074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshGatewayRouteSpecHttpRouteMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1657e02a0c275e3b5a82a637d28d90e3ad18c9788cec2c25f9c96b5382036565)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshGatewayRouteSpecHttpRouteMatchHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__786d8e63e71b09778950b7aa9812e46e9fc7007af57b207ae4bac10620afd41a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="putHostname")
    def put_hostname(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        :param suffix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#suffix AppmeshGatewayRoute#suffix}.
        '''
        value = AppmeshGatewayRouteSpecHttpRouteMatchHostname(
            exact=exact, suffix=suffix
        )

        return typing.cast(None, jsii.invoke(self, "putHostname", [value]))

    @jsii.member(jsii_name="putPath")
    def put_path(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#regex AppmeshGatewayRoute#regex}.
        '''
        value = AppmeshGatewayRouteSpecHttpRouteMatchPath(exact=exact, regex=regex)

        return typing.cast(None, jsii.invoke(self, "putPath", [value]))

    @jsii.member(jsii_name="putQueryParameter")
    def put_query_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3812ab131f5afe487b495fb3895f313f3d5c04828b4f23de8077c8499a375b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQueryParameter", [value]))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

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

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> AppmeshGatewayRouteSpecHttpRouteMatchHeaderList:
        return typing.cast(AppmeshGatewayRouteSpecHttpRouteMatchHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> AppmeshGatewayRouteSpecHttpRouteMatchHostnameOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttpRouteMatchHostnameOutputReference, jsii.get(self, "hostname"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> "AppmeshGatewayRouteSpecHttpRouteMatchPathOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteMatchPathOutputReference", jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="queryParameter")
    def query_parameter(
        self,
    ) -> "AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterList":
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterList", jsii.get(self, "queryParameter"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttpRouteMatchHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttpRouteMatchHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHostname]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHostname], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteMatchPath"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteMatchPath"], jsii.get(self, "pathInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter"]]], jsii.get(self, "queryParameterInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f69f4352d1469b461469c2a9c381dcf77330d235407222f4ae37a61d51186e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__104e38627d233646d6ee88f562686f7f470efd29facc6c8488574389e925f974)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d2c53e237ef7a0fa72e5ffb3c5d6fe5ce5d7c698249e6973f8abc5b15c65c84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchPath",
    jsii_struct_bases=[],
    name_mapping={"exact": "exact", "regex": "regex"},
)
class AppmeshGatewayRouteSpecHttpRouteMatchPath:
    def __init__(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#regex AppmeshGatewayRoute#regex}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__535f8416152a43ab920965cb48a8a8175fb37749a9c46d14ae9439629b98e330)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exact is not None:
            self._values["exact"] = exact
        if regex is not None:
            self._values["regex"] = regex

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.'''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#regex AppmeshGatewayRoute#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteMatchPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteMatchPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a77fa4381ca8174db5e060e79d131d34510bb0a4fc101ab2400e380888546b41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e5eaba88527a9567c5f8a8d66c5bfa7b15cc91954a8a2c97fd14a8e2a85744b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fa9e80ef91295605fbc9e3a03c7008c29caf57fa62261c616e9ae9db1f27150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchPath]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchPath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0973d431af0e62b947ef0ead27d810880109a94cc84259d6e526576be1894c8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "match": "match"},
)
class AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter:
    def __init__(
        self,
        *,
        name: builtins.str,
        match: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatch", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#name AppmeshGatewayRoute#name}.
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        if isinstance(match, dict):
            match = AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8800468575ff456bb788f2ec36dc06f3439d0acf480c68a95b964a9d4ac86307)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if match is not None:
            self._values["match"] = match

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#name AppmeshGatewayRoute#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatch"]:
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatch"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d8e93a8f29ead40d8b284524b951202a769ca6f541c1285f4040b6b25de5095)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5357b16c2b71e7d78c61b271608ed5ec3cf0dec4ac40dc283cea3797a73bff9d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38c4173e50d93c90d6cca9b21405800ebc7c58cd638334709b4133d166e013ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c28b1644ce03a4499aa2fe83bcfa16ce64f15638a8f67ddaa936d68e7501cc4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1aa64f013e541fa7320fa1fc636bc0b6dd00f74c4e9442af08ee69dac7d0a725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59bbf96951682f359779e54589dfbfba57d3aef14332b6c6df8328fc71717d7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatch",
    jsii_struct_bases=[],
    name_mapping={"exact": "exact"},
)
class AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatch:
    def __init__(self, *, exact: typing.Optional[builtins.str] = None) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5155056e54f0799434ea1a2e06b96095e04f2f3fd1361dab0e0f30665c87c0ee)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exact is not None:
            self._values["exact"] = exact

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.'''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4290d0fe9e7a7d684b947deca28fde96f559c5abe11e208a21807e554d024b8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b640a6619b7ca604f818ed4d2fe9d887e53b0fbe80ac068fe2ab32a077af2872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ad874601ddd005bf172047bd2053970e81276d72abf54bc56cb828286785577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8afe9a5214044e56563335fe6003c16fa15214dca50bf76f71b2bc86ee757506)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatch")
    def put_match(self, *, exact: typing.Optional[builtins.str] = None) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        '''
        value = AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatch(exact=exact)

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(
        self,
    ) -> AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatchOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatch], jsii.get(self, "matchInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__59d45a5814080a36214738305bfbc721e9f2e120b3c9b5578e44529222b157d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ece5d3f5ca3677906e0c251759585ba86b7ec27f4d40d10106da6556621827f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshGatewayRouteSpecHttpRouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc58767620af19388a6375d92871b9066adca5df7b23ce38c5ae4547cfd04b77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        target: typing.Union[AppmeshGatewayRouteSpecHttpRouteActionTarget, typing.Dict[builtins.str, typing.Any]],
        rewrite: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteActionRewrite, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#target AppmeshGatewayRoute#target}
        :param rewrite: rewrite block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#rewrite AppmeshGatewayRoute#rewrite}
        '''
        value = AppmeshGatewayRouteSpecHttpRouteAction(target=target, rewrite=rewrite)

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshGatewayRouteSpecHttpRouteMatchHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
        hostname: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteMatchHostname, typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteMatchPath, typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        prefix: typing.Optional[builtins.str] = None,
        query_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#header AppmeshGatewayRoute#header}
        :param hostname: hostname block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        :param path: path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#path AppmeshGatewayRoute#path}
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#port AppmeshGatewayRoute#port}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}.
        :param query_parameter: query_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#query_parameter AppmeshGatewayRoute#query_parameter}
        '''
        value = AppmeshGatewayRouteSpecHttpRouteMatch(
            header=header,
            hostname=hostname,
            path=path,
            port=port,
            prefix=prefix,
            query_parameter=query_parameter,
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> AppmeshGatewayRouteSpecHttpRouteActionOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttpRouteActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> AppmeshGatewayRouteSpecHttpRouteMatchOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttpRouteMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteAction]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshGatewayRouteSpecHttpRoute]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRoute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRoute],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b08344006335662ee06c3c8bde78d108091cccfe2d3f954d4ac7b1b11c44d964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppmeshGatewayRouteSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ceb343971d88577d10e9ecf411d430c28e99eae604667bbc91dab19c3fb6217)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGrpcRoute")
    def put_grpc_route(
        self,
        *,
        action: typing.Union[AppmeshGatewayRouteSpecGrpcRouteAction, typing.Dict[builtins.str, typing.Any]],
        match: typing.Union[AppmeshGatewayRouteSpecGrpcRouteMatch, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#action AppmeshGatewayRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        value = AppmeshGatewayRouteSpecGrpcRoute(action=action, match=match)

        return typing.cast(None, jsii.invoke(self, "putGrpcRoute", [value]))

    @jsii.member(jsii_name="putHttp2Route")
    def put_http2_route(
        self,
        *,
        action: typing.Union[AppmeshGatewayRouteSpecHttp2RouteAction, typing.Dict[builtins.str, typing.Any]],
        match: typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatch, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#action AppmeshGatewayRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        value = AppmeshGatewayRouteSpecHttp2Route(action=action, match=match)

        return typing.cast(None, jsii.invoke(self, "putHttp2Route", [value]))

    @jsii.member(jsii_name="putHttpRoute")
    def put_http_route(
        self,
        *,
        action: typing.Union[AppmeshGatewayRouteSpecHttpRouteAction, typing.Dict[builtins.str, typing.Any]],
        match: typing.Union[AppmeshGatewayRouteSpecHttpRouteMatch, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#action AppmeshGatewayRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        value = AppmeshGatewayRouteSpecHttpRoute(action=action, match=match)

        return typing.cast(None, jsii.invoke(self, "putHttpRoute", [value]))

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

    @builtins.property
    @jsii.member(jsii_name="grpcRoute")
    def grpc_route(self) -> AppmeshGatewayRouteSpecGrpcRouteOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecGrpcRouteOutputReference, jsii.get(self, "grpcRoute"))

    @builtins.property
    @jsii.member(jsii_name="http2Route")
    def http2_route(self) -> AppmeshGatewayRouteSpecHttp2RouteOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttp2RouteOutputReference, jsii.get(self, "http2Route"))

    @builtins.property
    @jsii.member(jsii_name="httpRoute")
    def http_route(self) -> AppmeshGatewayRouteSpecHttpRouteOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttpRouteOutputReference, jsii.get(self, "httpRoute"))

    @builtins.property
    @jsii.member(jsii_name="grpcRouteInput")
    def grpc_route_input(self) -> typing.Optional[AppmeshGatewayRouteSpecGrpcRoute]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecGrpcRoute], jsii.get(self, "grpcRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="http2RouteInput")
    def http2_route_input(self) -> typing.Optional[AppmeshGatewayRouteSpecHttp2Route]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2Route], jsii.get(self, "http2RouteInput"))

    @builtins.property
    @jsii.member(jsii_name="httpRouteInput")
    def http_route_input(self) -> typing.Optional[AppmeshGatewayRouteSpecHttpRoute]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRoute], jsii.get(self, "httpRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__220c8db51bd13e75e68033b777e5ec2e9f14fe6b00f985be09e079a3e605c817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshGatewayRouteSpec]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AppmeshGatewayRouteSpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f7e8ebdd089d28c015ac3be196daa8d7c4fb367bc18bd969ff9debc38fbbe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppmeshGatewayRoute",
    "AppmeshGatewayRouteConfig",
    "AppmeshGatewayRouteSpec",
    "AppmeshGatewayRouteSpecGrpcRoute",
    "AppmeshGatewayRouteSpecGrpcRouteAction",
    "AppmeshGatewayRouteSpecGrpcRouteActionOutputReference",
    "AppmeshGatewayRouteSpecGrpcRouteActionTarget",
    "AppmeshGatewayRouteSpecGrpcRouteActionTargetOutputReference",
    "AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService",
    "AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualServiceOutputReference",
    "AppmeshGatewayRouteSpecGrpcRouteMatch",
    "AppmeshGatewayRouteSpecGrpcRouteMatchOutputReference",
    "AppmeshGatewayRouteSpecGrpcRouteOutputReference",
    "AppmeshGatewayRouteSpecHttp2Route",
    "AppmeshGatewayRouteSpecHttp2RouteAction",
    "AppmeshGatewayRouteSpecHttp2RouteActionOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteActionRewrite",
    "AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname",
    "AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostnameOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteActionRewriteOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteActionRewritePath",
    "AppmeshGatewayRouteSpecHttp2RouteActionRewritePathOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix",
    "AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefixOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteActionTarget",
    "AppmeshGatewayRouteSpecHttp2RouteActionTargetOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService",
    "AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualServiceOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteMatch",
    "AppmeshGatewayRouteSpecHttp2RouteMatchHeader",
    "AppmeshGatewayRouteSpecHttp2RouteMatchHeaderList",
    "AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatch",
    "AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRange",
    "AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRangeOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteMatchHeaderOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteMatchHostname",
    "AppmeshGatewayRouteSpecHttp2RouteMatchHostnameOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteMatchOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteMatchPath",
    "AppmeshGatewayRouteSpecHttp2RouteMatchPathOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter",
    "AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterList",
    "AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatch",
    "AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatchOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteOutputReference",
    "AppmeshGatewayRouteSpecHttpRoute",
    "AppmeshGatewayRouteSpecHttpRouteAction",
    "AppmeshGatewayRouteSpecHttpRouteActionOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteActionRewrite",
    "AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname",
    "AppmeshGatewayRouteSpecHttpRouteActionRewriteHostnameOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteActionRewriteOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteActionRewritePath",
    "AppmeshGatewayRouteSpecHttpRouteActionRewritePathOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix",
    "AppmeshGatewayRouteSpecHttpRouteActionRewritePrefixOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteActionTarget",
    "AppmeshGatewayRouteSpecHttpRouteActionTargetOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService",
    "AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualServiceOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteMatch",
    "AppmeshGatewayRouteSpecHttpRouteMatchHeader",
    "AppmeshGatewayRouteSpecHttpRouteMatchHeaderList",
    "AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatch",
    "AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRange",
    "AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRangeOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteMatchHeaderOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteMatchHostname",
    "AppmeshGatewayRouteSpecHttpRouteMatchHostnameOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteMatchOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteMatchPath",
    "AppmeshGatewayRouteSpecHttpRouteMatchPathOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter",
    "AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterList",
    "AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatch",
    "AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatchOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteOutputReference",
    "AppmeshGatewayRouteSpecOutputReference",
]

publication.publish()

def _typecheckingstub__71605d0cfc835df02a6eb58ec98914fb41a5ad1ad6142f35efa733ef3c9a17f4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    mesh_name: builtins.str,
    name: builtins.str,
    spec: typing.Union[AppmeshGatewayRouteSpec, typing.Dict[builtins.str, typing.Any]],
    virtual_gateway_name: builtins.str,
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

def _typecheckingstub__fd167cadd43b9b6a9a055106fd07c9d785034491550a7271e5031ea534dd78d8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f955106c7704247db649cba0a2b011de285cf334fc170743cad7ded32b59d8e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae056571d2e9919c7d4157db4bd24dffb1e11566824a57653793c16690a72274(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03f302a89565af4646a2abd7e2cffff77bdf336724092ec6493498c67d3d9a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd1383610c7cb74dca7add1b992cf2f8db1aa5b2a8ec60e2cd5e1405d277bffb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10ba9fa1418b5841be08d0743d97f4e56372b92e9cd9e3985687810957f77f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5263d195de4831d3039e1a8584aaabfc1c92f8a76dee0772fe44f4091e3e740(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6b9ffc93d0c18434b41dd70a3d015a59e697e6f5decd706ef2697d4737d83a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7d3f5c1d84e00e817ff3af699ed68898c7decea29c9c33b342419241b44cc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21345109a23d44f663c5073e6d0b03ec8d36266fd94ba9462386baf1c030a4d0(
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
    spec: typing.Union[AppmeshGatewayRouteSpec, typing.Dict[builtins.str, typing.Any]],
    virtual_gateway_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    mesh_owner: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aa6e16fc2b5355afafd3d1d1cfe177b6c14891b00f5264ff3f832e81bef71cf(
    *,
    grpc_route: typing.Optional[typing.Union[AppmeshGatewayRouteSpecGrpcRoute, typing.Dict[builtins.str, typing.Any]]] = None,
    http2_route: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2Route, typing.Dict[builtins.str, typing.Any]]] = None,
    http_route: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRoute, typing.Dict[builtins.str, typing.Any]]] = None,
    priority: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b96549ad2947aac6499dd44b143729e0789802479065bf473cd38bcfd0f94b6b(
    *,
    action: typing.Union[AppmeshGatewayRouteSpecGrpcRouteAction, typing.Dict[builtins.str, typing.Any]],
    match: typing.Union[AppmeshGatewayRouteSpecGrpcRouteMatch, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c484c38458daf8e3d693834279aa7ca4825e5a3a33473194d087fb33db930958(
    *,
    target: typing.Union[AppmeshGatewayRouteSpecGrpcRouteActionTarget, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ee0db815f6748954350906a496e842d75f6695eb19b2b7fb408b74e854048f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aec5eee6bd59d71de28adb44cb12816b2dc1f54958885e4b836718040f5afa0(
    value: typing.Optional[AppmeshGatewayRouteSpecGrpcRouteAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fa3298a1a80e7261452681b5738c6e38ac7b76c8da6eb0020c4141a4f1253c(
    *,
    virtual_service: typing.Union[AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService, typing.Dict[builtins.str, typing.Any]],
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1054e1c8689890d8d4e417c912d61263a4d1a9f8daef8626ca24cac57209fa4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff5fb51761fe2c06857003ad920e6e29294c7ad0db437bb1807c9328e5fa042(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16130a541c5a389e5d089893945106396979d8f0303490e16f159e7576f534aa(
    value: typing.Optional[AppmeshGatewayRouteSpecGrpcRouteActionTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc976a29cf7e296d1f0c04c61c4929fcb590377fc003298bdeba0354b3c466de(
    *,
    virtual_service_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee5e7f45dc4afa79500c7968b7da2d2f07893f25ce6aeabf76ccb1bf622f0d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ae7aae7c64a87f083527beb951bb4d34141d72870f75e213910064fa0f4e33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b6702836e48f383477acad0a9e315bf167769b66f1b025e3c8967c74038188d(
    value: typing.Optional[AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40de0102cd2d5d605aa0be5f934208ac347b887efc61e27a23946ab22837ffac(
    *,
    service_name: builtins.str,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9d0895b5eacf6a21b1bf49dedc480c6cc50253d61739f498b5aa9168e5f0c52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78757209859f38fb94e3d9aa1ac643a76d3e00bebd35b30a529d1116e3a009cf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b6ce2f4e3ba46542305436b9171a4d945b1e8ca59dfe06d7ce8e053bae3d96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9823d555507f5e7183867ae39cca97ab17de339f5a82a07e553d557b85302074(
    value: typing.Optional[AppmeshGatewayRouteSpecGrpcRouteMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1ce1fba46c8f382fdca493a6dc1d6b27e9cbba37e694b41c753b4e07b5a834(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a98c6e86fd5c86992e4e6bb3888876f74031fcff7ab7a3591cfd50fe5443117d(
    value: typing.Optional[AppmeshGatewayRouteSpecGrpcRoute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398bd04f75dccf1dd0e84f24f8e8e600323f74251dd7bdbc90139881e74c83f5(
    *,
    action: typing.Union[AppmeshGatewayRouteSpecHttp2RouteAction, typing.Dict[builtins.str, typing.Any]],
    match: typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatch, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9e6d0ee4b7f8a29be864299fa4898257e11839eb054e34307ded7a320432e2(
    *,
    target: typing.Union[AppmeshGatewayRouteSpecHttp2RouteActionTarget, typing.Dict[builtins.str, typing.Any]],
    rewrite: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteActionRewrite, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54ff59cfe3baad02c915968be5a053f772595246473d265932e454093fa39a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ca20e7cb9e201f3610378cf21a423a04a42693765dfd1599803b54767b619a(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54c563414948f4ba1ec87ed89da70a0b12db85e2daf56652b54cb401d839566(
    *,
    hostname: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteActionRewritePath, typing.Dict[builtins.str, typing.Any]]] = None,
    prefix: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e62c5328e5c8e60371e866d7973ce174a43ac5610c5d35887fd4dba33b7b6e(
    *,
    default_target_hostname: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50f8d08cefa567a2422114c205123ec5cbcda2d1ea6b373df997891eff61370(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe9125612ba4aa4198be4d4dc597cf801f05443e6ebeab926119cb7fc0067ab6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d972992a4c5163ae3418b3d1c379910524091af3492f8f1528ebc817c1fe17ed(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1ac777fe94a623e74bdd9d75b8b077c7a000a4d99e486ca7d83251ebab1019(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__884c097d665f923c5824c4981072f5d5d8eb821f098259124287f12f693e855c(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewrite],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63ad52fecd4936df7fdac6cd46b837f29f7533c127fb15589e5e469f828d533(
    *,
    exact: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91008bfadbcf1aa8256c0554b2e1f180a2d7b3ef930f3ab299c8ba89ff8a5133(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53797ef412bc84d53d9a0bfafbfc21271d18d4c253b8cb95b014dac0560e963f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799b1904bb68f74ee4e2d88b2fbee4ec40d08cd4975844170f6dd7ee83b29e70(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewritePath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c5f264b887fcba654a7c55e2c638057f7c760ac0e8d42f4157b542bb59a408(
    *,
    default_prefix: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8a56538ad123093f49a711efbc34fc2e886592ae10276876f5d478f8cb6196(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70c0d75c69431458f2ca3ee15a987f07c82908e05b6d163b0393396362d67512(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0e94836e8e777525252704aa30cd8342a498751db6bec83c3d094931f0cd3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e640208b87e4103b661d91366165c86d2dc7e51a6ac152db0f3afe85daa0369(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23ae279732eb4d457d545234e75092a216323410c89b2b1527d342e34e10c1c(
    *,
    virtual_service: typing.Union[AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService, typing.Dict[builtins.str, typing.Any]],
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ba16721fe7ad03d7efb6ff0518554aeb9945827248ad825acef2a3f24c4f43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0dd2796c2e826d724212e5920e4108b0b11a869f55feb9fcd05ebff0438b6d8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10e2905098d210e913764992ad2d2469fbb4bad7e18be1580bc15a4280501fc(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe54f39c40d22adc366e2a748ba11fdab06a7ef19279d2ffe3fd25dfe39d02aa(
    *,
    virtual_service_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe169db7ec1265d8a7526ee4d327bb087d30742ea095dd839d14f51853e2b325(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad1f008a33f95b9c12256e5606f10e19027625be6ca1065095f7477787f71a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9091629b50fbeca94ef48ec60d49c86d906e2cd13343c38dfbaff6cd41c20d47(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59d404ab1ae07612011f1434f2c0e138b16e2faccf45fa7815264b8ef794062(
    *,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatchHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hostname: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatchHostname, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatchPath, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[jsii.Number] = None,
    prefix: typing.Optional[builtins.str] = None,
    query_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d785e8a03019ef300851e67124eae3cf06785469edeaa7db858b7e19fc6336c6(
    *,
    name: builtins.str,
    invert: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    match: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatch, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf5788a8a2df7b151ab73f745bc5e7cc81cf11a99e5b4ae39a0c566a7373945d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__429bca5fdc5ce8b4d73d2e48594ac754b94f781895a4be2fc5dc07829ee7689f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb912779519972e42d19ff7c19e247b8002e5cd168929da2553513a8ce5eb0c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f787ac3825460a3101f269fc5d4c2d2e560ec24e5fd008985726312d49f6444f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6852dd50cd5bfe57d918a3816306f77655eb07fc9720dcf835c21c9f0bfe8a2b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee06470aafe08ad9fd540f4d8084b4458b49621a3e7ef6f2a0821f8bc79257b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttp2RouteMatchHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5bf33544b07b4f593c9f07d57b35e35c9c7e6189e656c3f2e519daa2399fd96(
    *,
    exact: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    range: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRange, typing.Dict[builtins.str, typing.Any]]] = None,
    regex: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c49a663c7fe1854ba52c8a1a63d50e629cd54633375481c566c7394fd525234e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d670dd5f6d208251ab061a2949e587376712333cea775d5bda1974033592e998(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd906d687ec9e35e108c2eb29f45cb472a2b42bff4c0672b064f2e3200355163(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fde6990f369288d9e20153edc39ec1f97948df0bacd62324518ec6381d2aa85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7bdd536da8e658c3e54798b5c769783ea7a252b8e17d114834a0ba460c02151(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b32324d2aff42bb40c86b5e9012d4d375335ef26a40179c3e357a80339286f(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc2945d86f27725c86196ccf3ef2b16ae33d61a5f152899cc72cb5bbbbb571d(
    *,
    end: jsii.Number,
    start: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__886c39c40f8038d364d0120cacd3a6bc2fe098e2e224f2cba75c643029023839(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace3afb3d4995692cfd7df2898bd80ec3368a586c48eae93410c5690275e7d1c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af5b3b4dea80720fb548557662fe8fa131fc6a5ea69b024fb4daab109b49454(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b9650bf8d0ca459abaf691573c13a41491f008e4de69a83771da29d622a1ee(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHeaderMatchRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8ac99d0ea7d7990e2934d027af1d92ae2b0b3ffedfd8a29f0f4f679feb25ca5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53b4fcad053a0d9c7bc7e16632b23ff414bab3bbcea1abcdd86f7fcc0bf32a4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e803319e58efe0010bd6239df5aa00f1e31af7769dac355fb5fb7ac518df264(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e957750cfd0e6fdf96d557812a9bc2260f4dfee533b927639735314213ff63(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshGatewayRouteSpecHttp2RouteMatchHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dbdb201bf33e07408e5372be866a244d6c00a798c28188768dbb170d7fa4585(
    *,
    exact: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a86f7add122516887ce551d363bafce0779b0eb89015a78f170cef97514b11ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd9f2dc0e1a721141b5a59d1413a0d3fb60b2a39bb92639dd4da21a2b1ba847(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9de98c27506e552826c3518cae1d26eb6ac806c91015f3c33ed409f01e3e79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b8de4acb8e4c1b56e33a8b1360fa243bf2fd1db9c88912e06f3e0c0259bdd1f(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHostname],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9fe8805ff8f62384bced1984c9fd98182845eeddb8017e9910254d689eb86d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0f82f4b4950a7c85f3376529bf2593142f58316c807b448592aa0d67e5993e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatchHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be668200bc09c3fb7973c6058d3cdd3c9ac333acbd0bac92b3ab55bfc1cb00e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe8ed75fd4b433157349a94cb13b34453703b8408b8b58390612d40b3a80fe3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4345e0496395986271436ffae44294b1bfdf18c3f3c0e9b8a8faa61eabb7425(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56a42f415c0ccecb84872ca6a53f5e8d5e7aa2193877dca7203bd25f706262d(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8c1a61794ebc6f6d684c218fef9d373333f2f7c3f0c4b81f6ba246becb0ca4(
    *,
    exact: typing.Optional[builtins.str] = None,
    regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__111643caefbaa692891573213698da1d5168242748f10be78a72743ae5e06012(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b602a7d6440c662782cc93cc3981fbe8d5b1b1cce029c3b9f6d85977149266a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f11dfafeed0923fad72d823cd1c06b26147849b2820ad03e46ef25369d216aba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81186c21c0dcf9e2d3ca75aabd738ceedd68ea91792304d98ee05a254fc9d2a8(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchPath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7afbea58c03f88afbb4b54bcff6a4675bca35e13e7212186aa7318461eaa1212(
    *,
    name: builtins.str,
    match: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatch, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae14a8ce49c6d1f7b67ecd4acd1e78df16e6bb4e7dd5e5a4ab442ecdc1c7a01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b490c6ae8297a16bc39e4749b6b0d9a5e07fa1beba2b94409bae0cea332a30b7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec35f02107fd95cdf162ce03dab1fba7102ce61f0c4cf0bf1dc2ae9a44dc74a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e2275a02d74713967d2fa96db84c2b041f276fa5e2e3ee75f6ccc8d7ad6e081(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab4ced80ab28b0299b8b504b3f7d98ee9fe5169a7cb7bf2f699a90e9b94154fe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ce10d9f4f5d8b20b94e68430cc3d1eb5968e1477f2abd5e26872e1b1e153ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42d16adbbe304128f8651d3f6e64f9e816511d6545b6527e4be261112bd3350c(
    *,
    exact: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a882724e491bca091b2facdd69dac5514700a45b88ff73216db7e6fc27bcd41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__578ed17c0d4cbec2f78ab3e310c4735b3ee6d0fbc8a99d3dbfe4caf07753319b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb932b8b1f03e13e52ff99c3183a284fbbf94d5161d0d7dd2e53f940bfac1dc3(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameterMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfef4e9ad040557f336ff4c5cadf93ad3c8c674ed49a6170b88ab8e155911f8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3c157f7919f619f774a8b2ad48d0b79f8adc82ca5c66fe36aef4208f30911fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fadaea8d2aa5d5b5eae3ef48f10ea294439000bfe589cb97521a04be9fe79473(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshGatewayRouteSpecHttp2RouteMatchQueryParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7476e00e4c0834a840dbc84e04575f621d350cd569d73bde3fd5d0089e098e90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf9e4017efb65bfb30ea999d7c2a643753edb48521f2166a976f61a3afdfd9b(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2Route],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3dad8721a921fa93b8a067552a823f04ce40750f97be510a26083d7bd37905(
    *,
    action: typing.Union[AppmeshGatewayRouteSpecHttpRouteAction, typing.Dict[builtins.str, typing.Any]],
    match: typing.Union[AppmeshGatewayRouteSpecHttpRouteMatch, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f22a260078a24d170ff86b15997470d867193964e1c0bb5ddccc1e058da761(
    *,
    target: typing.Union[AppmeshGatewayRouteSpecHttpRouteActionTarget, typing.Dict[builtins.str, typing.Any]],
    rewrite: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteActionRewrite, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de5d9d3d90233afdc804c5ca0095b37611b01f16e27849616cae0541ef8bc15b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d76f3b607c21443cff0c0e2e97261514164473f188ab2222079ca4f031ef005(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7c2832f8b020f8f4ffc3675092860e7300caa107f6a69b033f97b8b59e322d(
    *,
    hostname: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteActionRewritePath, typing.Dict[builtins.str, typing.Any]]] = None,
    prefix: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd2168f97e67b561a3b74052ec6bf4cb95b45811638c7fc184a1d30be24ad8af(
    *,
    default_target_hostname: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934c5fb3024722668e2b64c78a2f5b5ab6d7e858a90e298eb2c2d00a2d44afb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d97d7a0073292da166027ecb21e5cca1c7db8f7bdeb2d94330a015414044c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7491b4f03d76976a4b4e234cf4a22e222133d1566adca6f2c178fde8530557(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f088c59d94fdc6d0137c7bd0d418f2e1588fb20b90bd82f4b49a9f79bf9d7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a911b4d463b6c58432e9c745917f6a6bd33ba0ff4c9b7aeb8c7b532d4a30fbcd(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewrite],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31f60cb26eef51b8abcf6891474012fcff7481304716e9fffdb99dbb0d599ec(
    *,
    exact: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e843e8ef686010bd6d07eb07a584f071f29af52b3be5853e1f0d0b5e2cf069a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb89046758071c17d02ca9e2c6a5e35c3dffc85ebf10be1614f1c7858790ca0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fed9c31ac361769c8f4516b50aa1b48dc8674f68880e846721ebda2b7dd9fb3(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewritePath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c066ffa731a7729e31708b244e1e2c609375ad0ff5ca741d784d622afc8076(
    *,
    default_prefix: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52c05789a708f6a0634dbe2db648756eb7072f95f26a049c0262cbf949d2a672(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1687318704c3133baef5fdf4c0c10c173a06d7c877a177b319dbb55c38f56930(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417f7f9fc6cc29405d619d75892a4235aeea5d21a15379f88edf7e377c47062b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e1f382c0627570dfce3c9de55452b9db931ae2ace7ae609c0290d82fccb5a8(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835377e4110bb8bdfc923ee342d05e943cd49fe23968d7ead8df317883af8807(
    *,
    virtual_service: typing.Union[AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService, typing.Dict[builtins.str, typing.Any]],
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db6df76a224767b7337a9f3c6202c5be2a8f131da46ee47bf04cb3008568b7d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcefcaaf56ef41cb70c8a837b1749f78b81b5f30ad295007bab703db1b867676(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b29e566ca044c2a8f6fb73645bcf99f823254a5aa8202e82be3e813a17ba41(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3fc95db68cd1d66fa61b6cb270fc24f4ed497da3ec5f55d5a8963c0a582b1fa(
    *,
    virtual_service_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244dbb7167bf8224559e071d78d334138189116253a1458f47fab3a7ab7383b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e35f2f9306d81002cf00fafcfa570589cd9a4962799d26bc9897ffa083bf83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1df972c444ecdec022426761bd0ab9cc1ad94687910942c76fbb1f3d724c78(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30bba9194ea0ec1171d29411f141af8e162fb9d56595d304f65694549c0d7722(
    *,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshGatewayRouteSpecHttpRouteMatchHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hostname: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteMatchHostname, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteMatchPath, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[jsii.Number] = None,
    prefix: typing.Optional[builtins.str] = None,
    query_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f6ef3054223acc397f8be6f88239918fde795d017399e6505203e05f2a3dd82(
    *,
    name: builtins.str,
    invert: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    match: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatch, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685f050d086ea5ba5da48c9f61033091b21758c5340624379fd04212b361bcbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba93bb7d4df1eacffb623e9da1b206b364c461b1b730760965414dfc2003851(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0122a15f17313d53b67ef27a4d38735b6c25b5b2828684aac43f780d446b8f9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69aa405e22471498d22ad056c8912d0205d1e960832a8da57099b2c8db5dba8f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae70445693f1a6c50b2a9f4c0ec46aa70e50a6067c1fc50724be713d2cf87686(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b560ba8046f777eab9758d6964eebed8044d4b21c9713d4fc216fefc7977d4ec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttpRouteMatchHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183d3995beda12ce5d0d0819e66b846b595c4bba2b6a1ae966f8af0e89ab35bf(
    *,
    exact: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    range: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRange, typing.Dict[builtins.str, typing.Any]]] = None,
    regex: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e9b247b3ef8543eaa39fe0a3407d6adbb70c5b34a41f46fc191c5b902c7b4c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08225b8a2010fd6e5731d1aec0ed9b1d75f9792beaf7beca40c7872f0d14060(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f55f6b2a8d6ae6e63d59b3031cb5b9c06fee9312402e8144a204a731bd46bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa7232c56150318999ac4b66520c3ed550c2e6a962dcc12ce55cc9da50483046(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe04b398f42c323077115943eb90f94d8a71a0f591fca9df6d3304a2a5d83f6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54db7cfce66e2078578d471750495c880d5c71ade1d66222394ca9b3de531b1(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c25d27a9291b17c04e1ed7fef83eb814b838ce65c6b29016b457eba989a14a(
    *,
    end: jsii.Number,
    start: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c4bd668756a25d6e810b741f183191a499681f258f2194e0eb233b494a3cd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e842635aa4108a3a5074522b43d8abf28739d42f612f623fb93dfcdc402c6925(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa2650138d1c28a5f91203a35393a35b83d588e134f47204418e280333e5a69(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a0009848fef778892184fdea9c3928e4f2ef6d1c75eec58291ff977a279fbb(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHeaderMatchRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7547429ca3fe5c88074d5f6bc5754566ca404ea7558db42688ce4de0e745a63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f441b7884a47f972ef9d2ec9a3fa3a845522092d7c68ac3edf9b20a716ab3f5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d280aa82bff33e4552ebdb071a9fa2057936bdee5953a982e2dc1ca385bc980(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd876b38f9b33f67501034b4c2304120496ebc675a1b1907477b5b6d2474c9fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshGatewayRouteSpecHttpRouteMatchHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793802822d0e6acf81cf63a2bb63f9ec209e48c84ef4801e72a6939879738f20(
    *,
    exact: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d1621f6ac728ec9b506b502a8cf07fd4fbdbb3e72f2c5ee90578c205db1603(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7d864609e4ccb884c3ca0b95bf3dac555223d58c86a77183187f6d15cc6acc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88cc5b5827222dc14510a2f5d333501bc657da05309d5e163c6e0e921e791f27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4e24271d5af7a75e19b30e426a99602840e47e986fa44eaf6d640544eb5074(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHostname],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1657e02a0c275e3b5a82a637d28d90e3ad18c9788cec2c25f9c96b5382036565(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__786d8e63e71b09778950b7aa9812e46e9fc7007af57b207ae4bac10620afd41a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshGatewayRouteSpecHttpRouteMatchHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3812ab131f5afe487b495fb3895f313f3d5c04828b4f23de8077c8499a375b6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f69f4352d1469b461469c2a9c381dcf77330d235407222f4ae37a61d51186e4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__104e38627d233646d6ee88f562686f7f470efd29facc6c8488574389e925f974(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d2c53e237ef7a0fa72e5ffb3c5d6fe5ce5d7c698249e6973f8abc5b15c65c84(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__535f8416152a43ab920965cb48a8a8175fb37749a9c46d14ae9439629b98e330(
    *,
    exact: typing.Optional[builtins.str] = None,
    regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a77fa4381ca8174db5e060e79d131d34510bb0a4fc101ab2400e380888546b41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5eaba88527a9567c5f8a8d66c5bfa7b15cc91954a8a2c97fd14a8e2a85744b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa9e80ef91295605fbc9e3a03c7008c29caf57fa62261c616e9ae9db1f27150(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0973d431af0e62b947ef0ead27d810880109a94cc84259d6e526576be1894c8f(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchPath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8800468575ff456bb788f2ec36dc06f3439d0acf480c68a95b964a9d4ac86307(
    *,
    name: builtins.str,
    match: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatch, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d8e93a8f29ead40d8b284524b951202a769ca6f541c1285f4040b6b25de5095(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5357b16c2b71e7d78c61b271608ed5ec3cf0dec4ac40dc283cea3797a73bff9d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c4173e50d93c90d6cca9b21405800ebc7c58cd638334709b4133d166e013ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c28b1644ce03a4499aa2fe83bcfa16ce64f15638a8f67ddaa936d68e7501cc4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aa64f013e541fa7320fa1fc636bc0b6dd00f74c4e9442af08ee69dac7d0a725(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59bbf96951682f359779e54589dfbfba57d3aef14332b6c6df8328fc71717d7a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5155056e54f0799434ea1a2e06b96095e04f2f3fd1361dab0e0f30665c87c0ee(
    *,
    exact: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4290d0fe9e7a7d684b947deca28fde96f559c5abe11e208a21807e554d024b8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b640a6619b7ca604f818ed4d2fe9d887e53b0fbe80ac068fe2ab32a077af2872(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad874601ddd005bf172047bd2053970e81276d72abf54bc56cb828286785577(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchQueryParameterMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8afe9a5214044e56563335fe6003c16fa15214dca50bf76f71b2bc86ee757506(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d45a5814080a36214738305bfbc721e9f2e120b3c9b5578e44529222b157d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ece5d3f5ca3677906e0c251759585ba86b7ec27f4d40d10106da6556621827f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppmeshGatewayRouteSpecHttpRouteMatchQueryParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc58767620af19388a6375d92871b9066adca5df7b23ce38c5ae4547cfd04b77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b08344006335662ee06c3c8bde78d108091cccfe2d3f954d4ac7b1b11c44d964(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRoute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ceb343971d88577d10e9ecf411d430c28e99eae604667bbc91dab19c3fb6217(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__220c8db51bd13e75e68033b777e5ec2e9f14fe6b00f985be09e079a3e605c817(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f7e8ebdd089d28c015ac3be196daa8d7c4fb367bc18bd969ff9debc38fbbe1(
    value: typing.Optional[AppmeshGatewayRouteSpec],
) -> None:
    """Type checking stubs"""
    pass
