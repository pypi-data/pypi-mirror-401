r'''
# `aws_connect_user_hierarchy_structure`

Refer to the Terraform Registry for docs: [`aws_connect_user_hierarchy_structure`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure).
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


class ConnectUserHierarchyStructure(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructure",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure aws_connect_user_hierarchy_structure}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        hierarchy_structure: typing.Union["ConnectUserHierarchyStructureHierarchyStructure", typing.Dict[builtins.str, typing.Any]],
        instance_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure aws_connect_user_hierarchy_structure} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param hierarchy_structure: hierarchy_structure block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#hierarchy_structure ConnectUserHierarchyStructure#hierarchy_structure}
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#instance_id ConnectUserHierarchyStructure#instance_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#id ConnectUserHierarchyStructure#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#region ConnectUserHierarchyStructure#region}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c9824bf05ad2fd32e94e3d261eddce68cb9d75fde36363e056568d2dbdf3aa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ConnectUserHierarchyStructureConfig(
            hierarchy_structure=hierarchy_structure,
            instance_id=instance_id,
            id=id,
            region=region,
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
        '''Generates CDKTF code for importing a ConnectUserHierarchyStructure resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ConnectUserHierarchyStructure to import.
        :param import_from_id: The id of the existing ConnectUserHierarchyStructure that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ConnectUserHierarchyStructure to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5d2d6a2c1d7d6a278479c50c24ad992f2241b11137f4ff1543cf68e9b13717)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putHierarchyStructure")
    def put_hierarchy_structure(
        self,
        *,
        level_five: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelFive", typing.Dict[builtins.str, typing.Any]]] = None,
        level_four: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelFour", typing.Dict[builtins.str, typing.Any]]] = None,
        level_one: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelOne", typing.Dict[builtins.str, typing.Any]]] = None,
        level_three: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelThree", typing.Dict[builtins.str, typing.Any]]] = None,
        level_two: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelTwo", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param level_five: level_five block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#level_five ConnectUserHierarchyStructure#level_five}
        :param level_four: level_four block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#level_four ConnectUserHierarchyStructure#level_four}
        :param level_one: level_one block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#level_one ConnectUserHierarchyStructure#level_one}
        :param level_three: level_three block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#level_three ConnectUserHierarchyStructure#level_three}
        :param level_two: level_two block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#level_two ConnectUserHierarchyStructure#level_two}
        '''
        value = ConnectUserHierarchyStructureHierarchyStructure(
            level_five=level_five,
            level_four=level_four,
            level_one=level_one,
            level_three=level_three,
            level_two=level_two,
        )

        return typing.cast(None, jsii.invoke(self, "putHierarchyStructure", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="hierarchyStructure")
    def hierarchy_structure(
        self,
    ) -> "ConnectUserHierarchyStructureHierarchyStructureOutputReference":
        return typing.cast("ConnectUserHierarchyStructureHierarchyStructureOutputReference", jsii.get(self, "hierarchyStructure"))

    @builtins.property
    @jsii.member(jsii_name="hierarchyStructureInput")
    def hierarchy_structure_input(
        self,
    ) -> typing.Optional["ConnectUserHierarchyStructureHierarchyStructure"]:
        return typing.cast(typing.Optional["ConnectUserHierarchyStructureHierarchyStructure"], jsii.get(self, "hierarchyStructureInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__232c43ab69a56b3ab55b3f3e2c978ec778933a5bee5a75715c6ba3b619795ccb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ada8cf72b52c05a90fe6220e050fdf65e7d6134726d7b7407df8db89ba0794d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e79170adaf65b2f7ba4b3eae7f34dcb11a13a2f7bb1f5182de05bbca1cbead80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "hierarchy_structure": "hierarchyStructure",
        "instance_id": "instanceId",
        "id": "id",
        "region": "region",
    },
)
class ConnectUserHierarchyStructureConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        hierarchy_structure: typing.Union["ConnectUserHierarchyStructureHierarchyStructure", typing.Dict[builtins.str, typing.Any]],
        instance_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param hierarchy_structure: hierarchy_structure block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#hierarchy_structure ConnectUserHierarchyStructure#hierarchy_structure}
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#instance_id ConnectUserHierarchyStructure#instance_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#id ConnectUserHierarchyStructure#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#region ConnectUserHierarchyStructure#region}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(hierarchy_structure, dict):
            hierarchy_structure = ConnectUserHierarchyStructureHierarchyStructure(**hierarchy_structure)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1e317793f8af730f4c5b9b4faae45ab214466fd80c155d1977e793efd811a1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument hierarchy_structure", value=hierarchy_structure, expected_type=type_hints["hierarchy_structure"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hierarchy_structure": hierarchy_structure,
            "instance_id": instance_id,
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
        if region is not None:
            self._values["region"] = region

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
    def hierarchy_structure(self) -> "ConnectUserHierarchyStructureHierarchyStructure":
        '''hierarchy_structure block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#hierarchy_structure ConnectUserHierarchyStructure#hierarchy_structure}
        '''
        result = self._values.get("hierarchy_structure")
        assert result is not None, "Required property 'hierarchy_structure' is missing"
        return typing.cast("ConnectUserHierarchyStructureHierarchyStructure", result)

    @builtins.property
    def instance_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#instance_id ConnectUserHierarchyStructure#instance_id}.'''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#id ConnectUserHierarchyStructure#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#region ConnectUserHierarchyStructure#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectUserHierarchyStructureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructure",
    jsii_struct_bases=[],
    name_mapping={
        "level_five": "levelFive",
        "level_four": "levelFour",
        "level_one": "levelOne",
        "level_three": "levelThree",
        "level_two": "levelTwo",
    },
)
class ConnectUserHierarchyStructureHierarchyStructure:
    def __init__(
        self,
        *,
        level_five: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelFive", typing.Dict[builtins.str, typing.Any]]] = None,
        level_four: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelFour", typing.Dict[builtins.str, typing.Any]]] = None,
        level_one: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelOne", typing.Dict[builtins.str, typing.Any]]] = None,
        level_three: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelThree", typing.Dict[builtins.str, typing.Any]]] = None,
        level_two: typing.Optional[typing.Union["ConnectUserHierarchyStructureHierarchyStructureLevelTwo", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param level_five: level_five block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#level_five ConnectUserHierarchyStructure#level_five}
        :param level_four: level_four block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#level_four ConnectUserHierarchyStructure#level_four}
        :param level_one: level_one block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#level_one ConnectUserHierarchyStructure#level_one}
        :param level_three: level_three block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#level_three ConnectUserHierarchyStructure#level_three}
        :param level_two: level_two block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#level_two ConnectUserHierarchyStructure#level_two}
        '''
        if isinstance(level_five, dict):
            level_five = ConnectUserHierarchyStructureHierarchyStructureLevelFive(**level_five)
        if isinstance(level_four, dict):
            level_four = ConnectUserHierarchyStructureHierarchyStructureLevelFour(**level_four)
        if isinstance(level_one, dict):
            level_one = ConnectUserHierarchyStructureHierarchyStructureLevelOne(**level_one)
        if isinstance(level_three, dict):
            level_three = ConnectUserHierarchyStructureHierarchyStructureLevelThree(**level_three)
        if isinstance(level_two, dict):
            level_two = ConnectUserHierarchyStructureHierarchyStructureLevelTwo(**level_two)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5983524592beaafe3e0750bea3ad9cfd2ed5b9a1016d0333c83c69acdce3f36e)
            check_type(argname="argument level_five", value=level_five, expected_type=type_hints["level_five"])
            check_type(argname="argument level_four", value=level_four, expected_type=type_hints["level_four"])
            check_type(argname="argument level_one", value=level_one, expected_type=type_hints["level_one"])
            check_type(argname="argument level_three", value=level_three, expected_type=type_hints["level_three"])
            check_type(argname="argument level_two", value=level_two, expected_type=type_hints["level_two"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if level_five is not None:
            self._values["level_five"] = level_five
        if level_four is not None:
            self._values["level_four"] = level_four
        if level_one is not None:
            self._values["level_one"] = level_one
        if level_three is not None:
            self._values["level_three"] = level_three
        if level_two is not None:
            self._values["level_two"] = level_two

    @builtins.property
    def level_five(
        self,
    ) -> typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelFive"]:
        '''level_five block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#level_five ConnectUserHierarchyStructure#level_five}
        '''
        result = self._values.get("level_five")
        return typing.cast(typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelFive"], result)

    @builtins.property
    def level_four(
        self,
    ) -> typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelFour"]:
        '''level_four block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#level_four ConnectUserHierarchyStructure#level_four}
        '''
        result = self._values.get("level_four")
        return typing.cast(typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelFour"], result)

    @builtins.property
    def level_one(
        self,
    ) -> typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelOne"]:
        '''level_one block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#level_one ConnectUserHierarchyStructure#level_one}
        '''
        result = self._values.get("level_one")
        return typing.cast(typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelOne"], result)

    @builtins.property
    def level_three(
        self,
    ) -> typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelThree"]:
        '''level_three block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#level_three ConnectUserHierarchyStructure#level_three}
        '''
        result = self._values.get("level_three")
        return typing.cast(typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelThree"], result)

    @builtins.property
    def level_two(
        self,
    ) -> typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelTwo"]:
        '''level_two block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#level_two ConnectUserHierarchyStructure#level_two}
        '''
        result = self._values.get("level_two")
        return typing.cast(typing.Optional["ConnectUserHierarchyStructureHierarchyStructureLevelTwo"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectUserHierarchyStructureHierarchyStructure(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelFive",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ConnectUserHierarchyStructureHierarchyStructureLevelFive:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acd70981898149cfceaef7504bb81afacf0850cc7d012c564d788dd0d7f2cea2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectUserHierarchyStructureHierarchyStructureLevelFive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConnectUserHierarchyStructureHierarchyStructureLevelFiveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelFiveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36247e1dca3a786bb8871eda57e641fd66ed0dab12ff6cfcb0864ade85cb01a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4f60e04470919676de25bc0dfd2bc8b171000c41ef67b9f456c5298814508e05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFive]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFive], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFive],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7317595633d41dc4b0caee24ad22b472d5c679633e21834c177176672ac189a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelFour",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ConnectUserHierarchyStructureHierarchyStructureLevelFour:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45b70353c068b622d6809fd5b396c68f69c91a8bcaf7523112198dd7c73ee57)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectUserHierarchyStructureHierarchyStructureLevelFour(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConnectUserHierarchyStructureHierarchyStructureLevelFourOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelFourOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d665c87345cb4ede9d497bd9f513d22194b6c02e12797b7c3b567963d8bae29)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__cabfe8749ea3acd20bdf3dbd027c31e7a75343d0486267d0799f8e4bfc5ac3d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFour]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFour], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFour],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__542bbe734cfd8186f4ae74a4122215b70d01039849b2c3597ca665cb82e293e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelOne",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ConnectUserHierarchyStructureHierarchyStructureLevelOne:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dad7bd45f5800e3ef2d24cced1cdc8c2fd6e9cbc7031a0729865621453d3d3b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectUserHierarchyStructureHierarchyStructureLevelOne(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConnectUserHierarchyStructureHierarchyStructureLevelOneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelOneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fd4b2b926be0b378b19cac4dab380e6a70ab9cac8f93d1d117133a0a5c82606)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d6c8846f1e0e892e44d8421218609c9e85a9e114cce39bb7f7a36ddab5af06d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelOne]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelOne], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelOne],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1da4c7ae25e8d263f2b87aeee03fcb16daa307ac7d9760a26029fc2bc4a2dc31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelThree",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ConnectUserHierarchyStructureHierarchyStructureLevelThree:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b60e5f7da69914898d8c9c286712a70d7c7e9c687f1a8b4b90b857465fbb015)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectUserHierarchyStructureHierarchyStructureLevelThree(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConnectUserHierarchyStructureHierarchyStructureLevelThreeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelThreeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a985f6bc26026256023c3bad56f8cc29118ad5b903fe71de9dbfb45833d6d5e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__754ff00db43f55929f7c99161e1f19260befd76fab9d48ca2006795e0deb4b4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelThree]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelThree], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelThree],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f379442b342b40b312b6e1181e0567804ac33ecef7047621c2cd85330b9707)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelTwo",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ConnectUserHierarchyStructureHierarchyStructureLevelTwo:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d43332b9fcbad8f95944cea4449351b6cb245233468f0ca07cb48cc3c63e27c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectUserHierarchyStructureHierarchyStructureLevelTwo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConnectUserHierarchyStructureHierarchyStructureLevelTwoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureLevelTwoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b83a7a68c8c5f731ec23fd2890e4abca7c3fb7d753fb399cc607f989355f3474)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d5a7ddc36008c80b84c68556213475a276c05bedf94b69fe45163c9fdaf89956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelTwo]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelTwo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelTwo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d776648f214ac6e8842259f814166ea20cbfed29ba696028f99ddc48c3be524a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ConnectUserHierarchyStructureHierarchyStructureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.connectUserHierarchyStructure.ConnectUserHierarchyStructureHierarchyStructureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35921d83fbc019897afe7acae9bc44d00e3fc32f525ae0c00aa34967e3f8852d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLevelFive")
    def put_level_five(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        value = ConnectUserHierarchyStructureHierarchyStructureLevelFive(name=name)

        return typing.cast(None, jsii.invoke(self, "putLevelFive", [value]))

    @jsii.member(jsii_name="putLevelFour")
    def put_level_four(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        value = ConnectUserHierarchyStructureHierarchyStructureLevelFour(name=name)

        return typing.cast(None, jsii.invoke(self, "putLevelFour", [value]))

    @jsii.member(jsii_name="putLevelOne")
    def put_level_one(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        value = ConnectUserHierarchyStructureHierarchyStructureLevelOne(name=name)

        return typing.cast(None, jsii.invoke(self, "putLevelOne", [value]))

    @jsii.member(jsii_name="putLevelThree")
    def put_level_three(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        value = ConnectUserHierarchyStructureHierarchyStructureLevelThree(name=name)

        return typing.cast(None, jsii.invoke(self, "putLevelThree", [value]))

    @jsii.member(jsii_name="putLevelTwo")
    def put_level_two(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/connect_user_hierarchy_structure#name ConnectUserHierarchyStructure#name}.
        '''
        value = ConnectUserHierarchyStructureHierarchyStructureLevelTwo(name=name)

        return typing.cast(None, jsii.invoke(self, "putLevelTwo", [value]))

    @jsii.member(jsii_name="resetLevelFive")
    def reset_level_five(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevelFive", []))

    @jsii.member(jsii_name="resetLevelFour")
    def reset_level_four(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevelFour", []))

    @jsii.member(jsii_name="resetLevelOne")
    def reset_level_one(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevelOne", []))

    @jsii.member(jsii_name="resetLevelThree")
    def reset_level_three(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevelThree", []))

    @jsii.member(jsii_name="resetLevelTwo")
    def reset_level_two(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevelTwo", []))

    @builtins.property
    @jsii.member(jsii_name="levelFive")
    def level_five(
        self,
    ) -> ConnectUserHierarchyStructureHierarchyStructureLevelFiveOutputReference:
        return typing.cast(ConnectUserHierarchyStructureHierarchyStructureLevelFiveOutputReference, jsii.get(self, "levelFive"))

    @builtins.property
    @jsii.member(jsii_name="levelFour")
    def level_four(
        self,
    ) -> ConnectUserHierarchyStructureHierarchyStructureLevelFourOutputReference:
        return typing.cast(ConnectUserHierarchyStructureHierarchyStructureLevelFourOutputReference, jsii.get(self, "levelFour"))

    @builtins.property
    @jsii.member(jsii_name="levelOne")
    def level_one(
        self,
    ) -> ConnectUserHierarchyStructureHierarchyStructureLevelOneOutputReference:
        return typing.cast(ConnectUserHierarchyStructureHierarchyStructureLevelOneOutputReference, jsii.get(self, "levelOne"))

    @builtins.property
    @jsii.member(jsii_name="levelThree")
    def level_three(
        self,
    ) -> ConnectUserHierarchyStructureHierarchyStructureLevelThreeOutputReference:
        return typing.cast(ConnectUserHierarchyStructureHierarchyStructureLevelThreeOutputReference, jsii.get(self, "levelThree"))

    @builtins.property
    @jsii.member(jsii_name="levelTwo")
    def level_two(
        self,
    ) -> ConnectUserHierarchyStructureHierarchyStructureLevelTwoOutputReference:
        return typing.cast(ConnectUserHierarchyStructureHierarchyStructureLevelTwoOutputReference, jsii.get(self, "levelTwo"))

    @builtins.property
    @jsii.member(jsii_name="levelFiveInput")
    def level_five_input(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFive]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFive], jsii.get(self, "levelFiveInput"))

    @builtins.property
    @jsii.member(jsii_name="levelFourInput")
    def level_four_input(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFour]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFour], jsii.get(self, "levelFourInput"))

    @builtins.property
    @jsii.member(jsii_name="levelOneInput")
    def level_one_input(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelOne]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelOne], jsii.get(self, "levelOneInput"))

    @builtins.property
    @jsii.member(jsii_name="levelThreeInput")
    def level_three_input(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelThree]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelThree], jsii.get(self, "levelThreeInput"))

    @builtins.property
    @jsii.member(jsii_name="levelTwoInput")
    def level_two_input(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelTwo]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelTwo], jsii.get(self, "levelTwoInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ConnectUserHierarchyStructureHierarchyStructure]:
        return typing.cast(typing.Optional[ConnectUserHierarchyStructureHierarchyStructure], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructure],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b671627791b61babc5f30ec562c26d2b4b2d86bd9f4074b7587373f9f761cc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ConnectUserHierarchyStructure",
    "ConnectUserHierarchyStructureConfig",
    "ConnectUserHierarchyStructureHierarchyStructure",
    "ConnectUserHierarchyStructureHierarchyStructureLevelFive",
    "ConnectUserHierarchyStructureHierarchyStructureLevelFiveOutputReference",
    "ConnectUserHierarchyStructureHierarchyStructureLevelFour",
    "ConnectUserHierarchyStructureHierarchyStructureLevelFourOutputReference",
    "ConnectUserHierarchyStructureHierarchyStructureLevelOne",
    "ConnectUserHierarchyStructureHierarchyStructureLevelOneOutputReference",
    "ConnectUserHierarchyStructureHierarchyStructureLevelThree",
    "ConnectUserHierarchyStructureHierarchyStructureLevelThreeOutputReference",
    "ConnectUserHierarchyStructureHierarchyStructureLevelTwo",
    "ConnectUserHierarchyStructureHierarchyStructureLevelTwoOutputReference",
    "ConnectUserHierarchyStructureHierarchyStructureOutputReference",
]

publication.publish()

def _typecheckingstub__01c9824bf05ad2fd32e94e3d261eddce68cb9d75fde36363e056568d2dbdf3aa(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    hierarchy_structure: typing.Union[ConnectUserHierarchyStructureHierarchyStructure, typing.Dict[builtins.str, typing.Any]],
    instance_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__9d5d2d6a2c1d7d6a278479c50c24ad992f2241b11137f4ff1543cf68e9b13717(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__232c43ab69a56b3ab55b3f3e2c978ec778933a5bee5a75715c6ba3b619795ccb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada8cf72b52c05a90fe6220e050fdf65e7d6134726d7b7407df8db89ba0794d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e79170adaf65b2f7ba4b3eae7f34dcb11a13a2f7bb1f5182de05bbca1cbead80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1e317793f8af730f4c5b9b4faae45ab214466fd80c155d1977e793efd811a1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hierarchy_structure: typing.Union[ConnectUserHierarchyStructureHierarchyStructure, typing.Dict[builtins.str, typing.Any]],
    instance_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5983524592beaafe3e0750bea3ad9cfd2ed5b9a1016d0333c83c69acdce3f36e(
    *,
    level_five: typing.Optional[typing.Union[ConnectUserHierarchyStructureHierarchyStructureLevelFive, typing.Dict[builtins.str, typing.Any]]] = None,
    level_four: typing.Optional[typing.Union[ConnectUserHierarchyStructureHierarchyStructureLevelFour, typing.Dict[builtins.str, typing.Any]]] = None,
    level_one: typing.Optional[typing.Union[ConnectUserHierarchyStructureHierarchyStructureLevelOne, typing.Dict[builtins.str, typing.Any]]] = None,
    level_three: typing.Optional[typing.Union[ConnectUserHierarchyStructureHierarchyStructureLevelThree, typing.Dict[builtins.str, typing.Any]]] = None,
    level_two: typing.Optional[typing.Union[ConnectUserHierarchyStructureHierarchyStructureLevelTwo, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd70981898149cfceaef7504bb81afacf0850cc7d012c564d788dd0d7f2cea2(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36247e1dca3a786bb8871eda57e641fd66ed0dab12ff6cfcb0864ade85cb01a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f60e04470919676de25bc0dfd2bc8b171000c41ef67b9f456c5298814508e05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7317595633d41dc4b0caee24ad22b472d5c679633e21834c177176672ac189a(
    value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFive],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45b70353c068b622d6809fd5b396c68f69c91a8bcaf7523112198dd7c73ee57(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d665c87345cb4ede9d497bd9f513d22194b6c02e12797b7c3b567963d8bae29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cabfe8749ea3acd20bdf3dbd027c31e7a75343d0486267d0799f8e4bfc5ac3d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__542bbe734cfd8186f4ae74a4122215b70d01039849b2c3597ca665cb82e293e6(
    value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelFour],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dad7bd45f5800e3ef2d24cced1cdc8c2fd6e9cbc7031a0729865621453d3d3b(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd4b2b926be0b378b19cac4dab380e6a70ab9cac8f93d1d117133a0a5c82606(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6c8846f1e0e892e44d8421218609c9e85a9e114cce39bb7f7a36ddab5af06d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da4c7ae25e8d263f2b87aeee03fcb16daa307ac7d9760a26029fc2bc4a2dc31(
    value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelOne],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b60e5f7da69914898d8c9c286712a70d7c7e9c687f1a8b4b90b857465fbb015(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a985f6bc26026256023c3bad56f8cc29118ad5b903fe71de9dbfb45833d6d5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754ff00db43f55929f7c99161e1f19260befd76fab9d48ca2006795e0deb4b4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f379442b342b40b312b6e1181e0567804ac33ecef7047621c2cd85330b9707(
    value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelThree],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d43332b9fcbad8f95944cea4449351b6cb245233468f0ca07cb48cc3c63e27c(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83a7a68c8c5f731ec23fd2890e4abca7c3fb7d753fb399cc607f989355f3474(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a7ddc36008c80b84c68556213475a276c05bedf94b69fe45163c9fdaf89956(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d776648f214ac6e8842259f814166ea20cbfed29ba696028f99ddc48c3be524a(
    value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructureLevelTwo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35921d83fbc019897afe7acae9bc44d00e3fc32f525ae0c00aa34967e3f8852d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b671627791b61babc5f30ec562c26d2b4b2d86bd9f4074b7587373f9f761cc1(
    value: typing.Optional[ConnectUserHierarchyStructureHierarchyStructure],
) -> None:
    """Type checking stubs"""
    pass
