r'''
# `aws_glue_classifier`

Refer to the Terraform Registry for docs: [`aws_glue_classifier`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier).
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


class GlueClassifier(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueClassifier.GlueClassifier",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier aws_glue_classifier}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        csv_classifier: typing.Optional[typing.Union["GlueClassifierCsvClassifier", typing.Dict[builtins.str, typing.Any]]] = None,
        grok_classifier: typing.Optional[typing.Union["GlueClassifierGrokClassifier", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        json_classifier: typing.Optional[typing.Union["GlueClassifierJsonClassifier", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        xml_classifier: typing.Optional[typing.Union["GlueClassifierXmlClassifier", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier aws_glue_classifier} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#name GlueClassifier#name}.
        :param csv_classifier: csv_classifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#csv_classifier GlueClassifier#csv_classifier}
        :param grok_classifier: grok_classifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#grok_classifier GlueClassifier#grok_classifier}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#id GlueClassifier#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param json_classifier: json_classifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#json_classifier GlueClassifier#json_classifier}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#region GlueClassifier#region}
        :param xml_classifier: xml_classifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#xml_classifier GlueClassifier#xml_classifier}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06db9577d5b991e035c3b1435f7ec1ed5819e9f6241fbe0ab4587e9604d34c8e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GlueClassifierConfig(
            name=name,
            csv_classifier=csv_classifier,
            grok_classifier=grok_classifier,
            id=id,
            json_classifier=json_classifier,
            region=region,
            xml_classifier=xml_classifier,
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
        '''Generates CDKTF code for importing a GlueClassifier resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GlueClassifier to import.
        :param import_from_id: The id of the existing GlueClassifier that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GlueClassifier to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdbe4ee177cfb449c61451ebe729984bcdc0e11c8b50379ec18d553bb2c3f4aa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCsvClassifier")
    def put_csv_classifier(
        self,
        *,
        allow_single_column: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        contains_header: typing.Optional[builtins.str] = None,
        custom_datatype_configured: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_datatypes: typing.Optional[typing.Sequence[builtins.str]] = None,
        delimiter: typing.Optional[builtins.str] = None,
        disable_value_trimming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header: typing.Optional[typing.Sequence[builtins.str]] = None,
        quote_symbol: typing.Optional[builtins.str] = None,
        serde: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_single_column: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#allow_single_column GlueClassifier#allow_single_column}.
        :param contains_header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#contains_header GlueClassifier#contains_header}.
        :param custom_datatype_configured: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#custom_datatype_configured GlueClassifier#custom_datatype_configured}.
        :param custom_datatypes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#custom_datatypes GlueClassifier#custom_datatypes}.
        :param delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#delimiter GlueClassifier#delimiter}.
        :param disable_value_trimming: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#disable_value_trimming GlueClassifier#disable_value_trimming}.
        :param header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#header GlueClassifier#header}.
        :param quote_symbol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#quote_symbol GlueClassifier#quote_symbol}.
        :param serde: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#serde GlueClassifier#serde}.
        '''
        value = GlueClassifierCsvClassifier(
            allow_single_column=allow_single_column,
            contains_header=contains_header,
            custom_datatype_configured=custom_datatype_configured,
            custom_datatypes=custom_datatypes,
            delimiter=delimiter,
            disable_value_trimming=disable_value_trimming,
            header=header,
            quote_symbol=quote_symbol,
            serde=serde,
        )

        return typing.cast(None, jsii.invoke(self, "putCsvClassifier", [value]))

    @jsii.member(jsii_name="putGrokClassifier")
    def put_grok_classifier(
        self,
        *,
        classification: builtins.str,
        grok_pattern: builtins.str,
        custom_patterns: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param classification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#classification GlueClassifier#classification}.
        :param grok_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#grok_pattern GlueClassifier#grok_pattern}.
        :param custom_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#custom_patterns GlueClassifier#custom_patterns}.
        '''
        value = GlueClassifierGrokClassifier(
            classification=classification,
            grok_pattern=grok_pattern,
            custom_patterns=custom_patterns,
        )

        return typing.cast(None, jsii.invoke(self, "putGrokClassifier", [value]))

    @jsii.member(jsii_name="putJsonClassifier")
    def put_json_classifier(self, *, json_path: builtins.str) -> None:
        '''
        :param json_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#json_path GlueClassifier#json_path}.
        '''
        value = GlueClassifierJsonClassifier(json_path=json_path)

        return typing.cast(None, jsii.invoke(self, "putJsonClassifier", [value]))

    @jsii.member(jsii_name="putXmlClassifier")
    def put_xml_classifier(
        self,
        *,
        classification: builtins.str,
        row_tag: builtins.str,
    ) -> None:
        '''
        :param classification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#classification GlueClassifier#classification}.
        :param row_tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#row_tag GlueClassifier#row_tag}.
        '''
        value = GlueClassifierXmlClassifier(
            classification=classification, row_tag=row_tag
        )

        return typing.cast(None, jsii.invoke(self, "putXmlClassifier", [value]))

    @jsii.member(jsii_name="resetCsvClassifier")
    def reset_csv_classifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsvClassifier", []))

    @jsii.member(jsii_name="resetGrokClassifier")
    def reset_grok_classifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrokClassifier", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetJsonClassifier")
    def reset_json_classifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonClassifier", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetXmlClassifier")
    def reset_xml_classifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXmlClassifier", []))

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
    @jsii.member(jsii_name="csvClassifier")
    def csv_classifier(self) -> "GlueClassifierCsvClassifierOutputReference":
        return typing.cast("GlueClassifierCsvClassifierOutputReference", jsii.get(self, "csvClassifier"))

    @builtins.property
    @jsii.member(jsii_name="grokClassifier")
    def grok_classifier(self) -> "GlueClassifierGrokClassifierOutputReference":
        return typing.cast("GlueClassifierGrokClassifierOutputReference", jsii.get(self, "grokClassifier"))

    @builtins.property
    @jsii.member(jsii_name="jsonClassifier")
    def json_classifier(self) -> "GlueClassifierJsonClassifierOutputReference":
        return typing.cast("GlueClassifierJsonClassifierOutputReference", jsii.get(self, "jsonClassifier"))

    @builtins.property
    @jsii.member(jsii_name="xmlClassifier")
    def xml_classifier(self) -> "GlueClassifierXmlClassifierOutputReference":
        return typing.cast("GlueClassifierXmlClassifierOutputReference", jsii.get(self, "xmlClassifier"))

    @builtins.property
    @jsii.member(jsii_name="csvClassifierInput")
    def csv_classifier_input(self) -> typing.Optional["GlueClassifierCsvClassifier"]:
        return typing.cast(typing.Optional["GlueClassifierCsvClassifier"], jsii.get(self, "csvClassifierInput"))

    @builtins.property
    @jsii.member(jsii_name="grokClassifierInput")
    def grok_classifier_input(self) -> typing.Optional["GlueClassifierGrokClassifier"]:
        return typing.cast(typing.Optional["GlueClassifierGrokClassifier"], jsii.get(self, "grokClassifierInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonClassifierInput")
    def json_classifier_input(self) -> typing.Optional["GlueClassifierJsonClassifier"]:
        return typing.cast(typing.Optional["GlueClassifierJsonClassifier"], jsii.get(self, "jsonClassifierInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="xmlClassifierInput")
    def xml_classifier_input(self) -> typing.Optional["GlueClassifierXmlClassifier"]:
        return typing.cast(typing.Optional["GlueClassifierXmlClassifier"], jsii.get(self, "xmlClassifierInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f57a956f8aab410248c58fac4647e4d0e33bffb6bd66b60e42bbfb0f8da64251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e81ce6f0e9e7e3336cde372e3735f7e428985dd189969fe7b15e1edbcf1f6b11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c4cc4dfb38d9438d54c824dca6916bfafd2accca0c08dcc97cf89a74ff4cf48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.glueClassifier.GlueClassifierConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "csv_classifier": "csvClassifier",
        "grok_classifier": "grokClassifier",
        "id": "id",
        "json_classifier": "jsonClassifier",
        "region": "region",
        "xml_classifier": "xmlClassifier",
    },
)
class GlueClassifierConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        csv_classifier: typing.Optional[typing.Union["GlueClassifierCsvClassifier", typing.Dict[builtins.str, typing.Any]]] = None,
        grok_classifier: typing.Optional[typing.Union["GlueClassifierGrokClassifier", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        json_classifier: typing.Optional[typing.Union["GlueClassifierJsonClassifier", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        xml_classifier: typing.Optional[typing.Union["GlueClassifierXmlClassifier", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#name GlueClassifier#name}.
        :param csv_classifier: csv_classifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#csv_classifier GlueClassifier#csv_classifier}
        :param grok_classifier: grok_classifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#grok_classifier GlueClassifier#grok_classifier}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#id GlueClassifier#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param json_classifier: json_classifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#json_classifier GlueClassifier#json_classifier}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#region GlueClassifier#region}
        :param xml_classifier: xml_classifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#xml_classifier GlueClassifier#xml_classifier}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(csv_classifier, dict):
            csv_classifier = GlueClassifierCsvClassifier(**csv_classifier)
        if isinstance(grok_classifier, dict):
            grok_classifier = GlueClassifierGrokClassifier(**grok_classifier)
        if isinstance(json_classifier, dict):
            json_classifier = GlueClassifierJsonClassifier(**json_classifier)
        if isinstance(xml_classifier, dict):
            xml_classifier = GlueClassifierXmlClassifier(**xml_classifier)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b675136bea6f48352603df6ae1ca53e31650afb8d57b70f02fdb6e168b93d9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument csv_classifier", value=csv_classifier, expected_type=type_hints["csv_classifier"])
            check_type(argname="argument grok_classifier", value=grok_classifier, expected_type=type_hints["grok_classifier"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument json_classifier", value=json_classifier, expected_type=type_hints["json_classifier"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument xml_classifier", value=xml_classifier, expected_type=type_hints["xml_classifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if csv_classifier is not None:
            self._values["csv_classifier"] = csv_classifier
        if grok_classifier is not None:
            self._values["grok_classifier"] = grok_classifier
        if id is not None:
            self._values["id"] = id
        if json_classifier is not None:
            self._values["json_classifier"] = json_classifier
        if region is not None:
            self._values["region"] = region
        if xml_classifier is not None:
            self._values["xml_classifier"] = xml_classifier

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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#name GlueClassifier#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def csv_classifier(self) -> typing.Optional["GlueClassifierCsvClassifier"]:
        '''csv_classifier block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#csv_classifier GlueClassifier#csv_classifier}
        '''
        result = self._values.get("csv_classifier")
        return typing.cast(typing.Optional["GlueClassifierCsvClassifier"], result)

    @builtins.property
    def grok_classifier(self) -> typing.Optional["GlueClassifierGrokClassifier"]:
        '''grok_classifier block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#grok_classifier GlueClassifier#grok_classifier}
        '''
        result = self._values.get("grok_classifier")
        return typing.cast(typing.Optional["GlueClassifierGrokClassifier"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#id GlueClassifier#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def json_classifier(self) -> typing.Optional["GlueClassifierJsonClassifier"]:
        '''json_classifier block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#json_classifier GlueClassifier#json_classifier}
        '''
        result = self._values.get("json_classifier")
        return typing.cast(typing.Optional["GlueClassifierJsonClassifier"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#region GlueClassifier#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def xml_classifier(self) -> typing.Optional["GlueClassifierXmlClassifier"]:
        '''xml_classifier block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#xml_classifier GlueClassifier#xml_classifier}
        '''
        result = self._values.get("xml_classifier")
        return typing.cast(typing.Optional["GlueClassifierXmlClassifier"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueClassifierConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.glueClassifier.GlueClassifierCsvClassifier",
    jsii_struct_bases=[],
    name_mapping={
        "allow_single_column": "allowSingleColumn",
        "contains_header": "containsHeader",
        "custom_datatype_configured": "customDatatypeConfigured",
        "custom_datatypes": "customDatatypes",
        "delimiter": "delimiter",
        "disable_value_trimming": "disableValueTrimming",
        "header": "header",
        "quote_symbol": "quoteSymbol",
        "serde": "serde",
    },
)
class GlueClassifierCsvClassifier:
    def __init__(
        self,
        *,
        allow_single_column: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        contains_header: typing.Optional[builtins.str] = None,
        custom_datatype_configured: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_datatypes: typing.Optional[typing.Sequence[builtins.str]] = None,
        delimiter: typing.Optional[builtins.str] = None,
        disable_value_trimming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header: typing.Optional[typing.Sequence[builtins.str]] = None,
        quote_symbol: typing.Optional[builtins.str] = None,
        serde: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_single_column: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#allow_single_column GlueClassifier#allow_single_column}.
        :param contains_header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#contains_header GlueClassifier#contains_header}.
        :param custom_datatype_configured: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#custom_datatype_configured GlueClassifier#custom_datatype_configured}.
        :param custom_datatypes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#custom_datatypes GlueClassifier#custom_datatypes}.
        :param delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#delimiter GlueClassifier#delimiter}.
        :param disable_value_trimming: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#disable_value_trimming GlueClassifier#disable_value_trimming}.
        :param header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#header GlueClassifier#header}.
        :param quote_symbol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#quote_symbol GlueClassifier#quote_symbol}.
        :param serde: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#serde GlueClassifier#serde}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6ec247aa8a842aa7ebc50048759fb009e49ee93d9cf53b0186104f99345b88e)
            check_type(argname="argument allow_single_column", value=allow_single_column, expected_type=type_hints["allow_single_column"])
            check_type(argname="argument contains_header", value=contains_header, expected_type=type_hints["contains_header"])
            check_type(argname="argument custom_datatype_configured", value=custom_datatype_configured, expected_type=type_hints["custom_datatype_configured"])
            check_type(argname="argument custom_datatypes", value=custom_datatypes, expected_type=type_hints["custom_datatypes"])
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
            check_type(argname="argument disable_value_trimming", value=disable_value_trimming, expected_type=type_hints["disable_value_trimming"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument quote_symbol", value=quote_symbol, expected_type=type_hints["quote_symbol"])
            check_type(argname="argument serde", value=serde, expected_type=type_hints["serde"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_single_column is not None:
            self._values["allow_single_column"] = allow_single_column
        if contains_header is not None:
            self._values["contains_header"] = contains_header
        if custom_datatype_configured is not None:
            self._values["custom_datatype_configured"] = custom_datatype_configured
        if custom_datatypes is not None:
            self._values["custom_datatypes"] = custom_datatypes
        if delimiter is not None:
            self._values["delimiter"] = delimiter
        if disable_value_trimming is not None:
            self._values["disable_value_trimming"] = disable_value_trimming
        if header is not None:
            self._values["header"] = header
        if quote_symbol is not None:
            self._values["quote_symbol"] = quote_symbol
        if serde is not None:
            self._values["serde"] = serde

    @builtins.property
    def allow_single_column(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#allow_single_column GlueClassifier#allow_single_column}.'''
        result = self._values.get("allow_single_column")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def contains_header(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#contains_header GlueClassifier#contains_header}.'''
        result = self._values.get("contains_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_datatype_configured(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#custom_datatype_configured GlueClassifier#custom_datatype_configured}.'''
        result = self._values.get("custom_datatype_configured")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def custom_datatypes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#custom_datatypes GlueClassifier#custom_datatypes}.'''
        result = self._values.get("custom_datatypes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def delimiter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#delimiter GlueClassifier#delimiter}.'''
        result = self._values.get("delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_value_trimming(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#disable_value_trimming GlueClassifier#disable_value_trimming}.'''
        result = self._values.get("disable_value_trimming")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def header(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#header GlueClassifier#header}.'''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def quote_symbol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#quote_symbol GlueClassifier#quote_symbol}.'''
        result = self._values.get("quote_symbol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serde(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#serde GlueClassifier#serde}.'''
        result = self._values.get("serde")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueClassifierCsvClassifier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueClassifierCsvClassifierOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueClassifier.GlueClassifierCsvClassifierOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e864d30d06e491e6c77e311ed66a9f89e460e83ec4bc07c5d56e7f128730ee9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowSingleColumn")
    def reset_allow_single_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowSingleColumn", []))

    @jsii.member(jsii_name="resetContainsHeader")
    def reset_contains_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainsHeader", []))

    @jsii.member(jsii_name="resetCustomDatatypeConfigured")
    def reset_custom_datatype_configured(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomDatatypeConfigured", []))

    @jsii.member(jsii_name="resetCustomDatatypes")
    def reset_custom_datatypes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomDatatypes", []))

    @jsii.member(jsii_name="resetDelimiter")
    def reset_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelimiter", []))

    @jsii.member(jsii_name="resetDisableValueTrimming")
    def reset_disable_value_trimming(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableValueTrimming", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetQuoteSymbol")
    def reset_quote_symbol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuoteSymbol", []))

    @jsii.member(jsii_name="resetSerde")
    def reset_serde(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSerde", []))

    @builtins.property
    @jsii.member(jsii_name="allowSingleColumnInput")
    def allow_single_column_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowSingleColumnInput"))

    @builtins.property
    @jsii.member(jsii_name="containsHeaderInput")
    def contains_header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containsHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="customDatatypeConfiguredInput")
    def custom_datatype_configured_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "customDatatypeConfiguredInput"))

    @builtins.property
    @jsii.member(jsii_name="customDatatypesInput")
    def custom_datatypes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "customDatatypesInput"))

    @builtins.property
    @jsii.member(jsii_name="delimiterInput")
    def delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="disableValueTrimmingInput")
    def disable_value_trimming_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableValueTrimmingInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="quoteSymbolInput")
    def quote_symbol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quoteSymbolInput"))

    @builtins.property
    @jsii.member(jsii_name="serdeInput")
    def serde_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serdeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowSingleColumn")
    def allow_single_column(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowSingleColumn"))

    @allow_single_column.setter
    def allow_single_column(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__331411c51e2c1a15c1c8c9e1ab56c5ea801163b04b419acd7da1de65b4563880)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowSingleColumn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containsHeader")
    def contains_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containsHeader"))

    @contains_header.setter
    def contains_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efeaf2da3430faeab5afb370c3a01591f4058592b051637b496ade3e291396d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containsHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customDatatypeConfigured")
    def custom_datatype_configured(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "customDatatypeConfigured"))

    @custom_datatype_configured.setter
    def custom_datatype_configured(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e0bc1e5a650ca8b561db05e5fbc1dc86376686c854213b1b36ee75127cc88d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDatatypeConfigured", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customDatatypes")
    def custom_datatypes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customDatatypes"))

    @custom_datatypes.setter
    def custom_datatypes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d78eaa347df114f19d65bcc5fd0f05a44593d170e5952832b9ad4791673ff829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDatatypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delimiter")
    def delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delimiter"))

    @delimiter.setter
    def delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d57087ae0d715f10083061eaadb1db648e2299739267aaed147a6930823f0e75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableValueTrimming")
    def disable_value_trimming(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableValueTrimming"))

    @disable_value_trimming.setter
    def disable_value_trimming(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a63e078a5984c296432347934cc58166451bc6da406a84e55e505bf83cb1e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableValueTrimming", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "header"))

    @header.setter
    def header(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb2eedcb2ae04555d3afe41e2a5026fab7213fa11682861e8d9268a7954ec17a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "header", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quoteSymbol")
    def quote_symbol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quoteSymbol"))

    @quote_symbol.setter
    def quote_symbol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ee9fee5eabdb6edaa80887838b8919a4c9cf0bad3edce90618e3c7ab9c3ac52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quoteSymbol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serde")
    def serde(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serde"))

    @serde.setter
    def serde(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95d47758e005329ac457782bf4ef0828429c6a048fec2e00b83ab5324674bc0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serde", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueClassifierCsvClassifier]:
        return typing.cast(typing.Optional[GlueClassifierCsvClassifier], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GlueClassifierCsvClassifier],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cc90216fd4efa6aad186cf65d4290c35364091f7e7d2378744754641bb2091b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.glueClassifier.GlueClassifierGrokClassifier",
    jsii_struct_bases=[],
    name_mapping={
        "classification": "classification",
        "grok_pattern": "grokPattern",
        "custom_patterns": "customPatterns",
    },
)
class GlueClassifierGrokClassifier:
    def __init__(
        self,
        *,
        classification: builtins.str,
        grok_pattern: builtins.str,
        custom_patterns: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param classification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#classification GlueClassifier#classification}.
        :param grok_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#grok_pattern GlueClassifier#grok_pattern}.
        :param custom_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#custom_patterns GlueClassifier#custom_patterns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a5637422d6b2e219f84d2be95967a40401cf8a815c6e2317be1294e7b7c28df)
            check_type(argname="argument classification", value=classification, expected_type=type_hints["classification"])
            check_type(argname="argument grok_pattern", value=grok_pattern, expected_type=type_hints["grok_pattern"])
            check_type(argname="argument custom_patterns", value=custom_patterns, expected_type=type_hints["custom_patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "classification": classification,
            "grok_pattern": grok_pattern,
        }
        if custom_patterns is not None:
            self._values["custom_patterns"] = custom_patterns

    @builtins.property
    def classification(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#classification GlueClassifier#classification}.'''
        result = self._values.get("classification")
        assert result is not None, "Required property 'classification' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def grok_pattern(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#grok_pattern GlueClassifier#grok_pattern}.'''
        result = self._values.get("grok_pattern")
        assert result is not None, "Required property 'grok_pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_patterns(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#custom_patterns GlueClassifier#custom_patterns}.'''
        result = self._values.get("custom_patterns")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueClassifierGrokClassifier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueClassifierGrokClassifierOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueClassifier.GlueClassifierGrokClassifierOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d583fa079db9f24b3f8d6087b489ee090102fc6954baf27ee41c62dbdd9e33d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCustomPatterns")
    def reset_custom_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomPatterns", []))

    @builtins.property
    @jsii.member(jsii_name="classificationInput")
    def classification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "classificationInput"))

    @builtins.property
    @jsii.member(jsii_name="customPatternsInput")
    def custom_patterns_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="grokPatternInput")
    def grok_pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "grokPatternInput"))

    @builtins.property
    @jsii.member(jsii_name="classification")
    def classification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "classification"))

    @classification.setter
    def classification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8683d12fab0a70880968f891e33db3757fb3eff46f6bbd5c1136c43d7c4331e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customPatterns")
    def custom_patterns(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customPatterns"))

    @custom_patterns.setter
    def custom_patterns(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa082906b2e627d98cb048bff590f26d656962f3bcfa19f86cea43ddb627acdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customPatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="grokPattern")
    def grok_pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grokPattern"))

    @grok_pattern.setter
    def grok_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd3ae3558888b4db09e5b38e7638cde91b5b555a74e483a2137817c4d82ae04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grokPattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueClassifierGrokClassifier]:
        return typing.cast(typing.Optional[GlueClassifierGrokClassifier], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GlueClassifierGrokClassifier],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de7057b8ad6468dae76675d0d7b0b892ef9ae11b0e8d05ab8e52d50d26f3b624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.glueClassifier.GlueClassifierJsonClassifier",
    jsii_struct_bases=[],
    name_mapping={"json_path": "jsonPath"},
)
class GlueClassifierJsonClassifier:
    def __init__(self, *, json_path: builtins.str) -> None:
        '''
        :param json_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#json_path GlueClassifier#json_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23715933b08f471b4c10c9722292cf4594eae6e96b85dccec1cbffdecfcba8fd)
            check_type(argname="argument json_path", value=json_path, expected_type=type_hints["json_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "json_path": json_path,
        }

    @builtins.property
    def json_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#json_path GlueClassifier#json_path}.'''
        result = self._values.get("json_path")
        assert result is not None, "Required property 'json_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueClassifierJsonClassifier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueClassifierJsonClassifierOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueClassifier.GlueClassifierJsonClassifierOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78200257926a6ad132bad451dcef47a8755ac58275621548e84777ec68b26a3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="jsonPathInput")
    def json_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jsonPathInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonPath")
    def json_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jsonPath"))

    @json_path.setter
    def json_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22d0275c9e0093105e5a4d4c87227c9fc572daf85f45e848b924f963952b32b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueClassifierJsonClassifier]:
        return typing.cast(typing.Optional[GlueClassifierJsonClassifier], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GlueClassifierJsonClassifier],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95833bd6654d1337df6bc83f6bb05348926467e5d627b60b1965764cb1be9cd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.glueClassifier.GlueClassifierXmlClassifier",
    jsii_struct_bases=[],
    name_mapping={"classification": "classification", "row_tag": "rowTag"},
)
class GlueClassifierXmlClassifier:
    def __init__(self, *, classification: builtins.str, row_tag: builtins.str) -> None:
        '''
        :param classification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#classification GlueClassifier#classification}.
        :param row_tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#row_tag GlueClassifier#row_tag}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2964c124429eaa6e02ac9d54390cdae27554585b337c1b874dbd471b9ba3e33d)
            check_type(argname="argument classification", value=classification, expected_type=type_hints["classification"])
            check_type(argname="argument row_tag", value=row_tag, expected_type=type_hints["row_tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "classification": classification,
            "row_tag": row_tag,
        }

    @builtins.property
    def classification(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#classification GlueClassifier#classification}.'''
        result = self._values.get("classification")
        assert result is not None, "Required property 'classification' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def row_tag(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_classifier#row_tag GlueClassifier#row_tag}.'''
        result = self._values.get("row_tag")
        assert result is not None, "Required property 'row_tag' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueClassifierXmlClassifier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueClassifierXmlClassifierOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueClassifier.GlueClassifierXmlClassifierOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc68915fb03ac84de18172a11093fe8e3318fabafcfb560bae777f8de3c2f6d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="classificationInput")
    def classification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "classificationInput"))

    @builtins.property
    @jsii.member(jsii_name="rowTagInput")
    def row_tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rowTagInput"))

    @builtins.property
    @jsii.member(jsii_name="classification")
    def classification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "classification"))

    @classification.setter
    def classification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90cd07d063209434e6f74be5306f1afabb6099f0245343927bb1617284d23724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rowTag")
    def row_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rowTag"))

    @row_tag.setter
    def row_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f12e6a45468201040614bf55c43c653280dfcef3931b2db021d8a31bd2a21565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rowTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueClassifierXmlClassifier]:
        return typing.cast(typing.Optional[GlueClassifierXmlClassifier], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GlueClassifierXmlClassifier],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f7a7141dd7b8c3aecaba838803e0e82a6a3bf78cfe95eab8e879286433b430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GlueClassifier",
    "GlueClassifierConfig",
    "GlueClassifierCsvClassifier",
    "GlueClassifierCsvClassifierOutputReference",
    "GlueClassifierGrokClassifier",
    "GlueClassifierGrokClassifierOutputReference",
    "GlueClassifierJsonClassifier",
    "GlueClassifierJsonClassifierOutputReference",
    "GlueClassifierXmlClassifier",
    "GlueClassifierXmlClassifierOutputReference",
]

publication.publish()

def _typecheckingstub__06db9577d5b991e035c3b1435f7ec1ed5819e9f6241fbe0ab4587e9604d34c8e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    csv_classifier: typing.Optional[typing.Union[GlueClassifierCsvClassifier, typing.Dict[builtins.str, typing.Any]]] = None,
    grok_classifier: typing.Optional[typing.Union[GlueClassifierGrokClassifier, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    json_classifier: typing.Optional[typing.Union[GlueClassifierJsonClassifier, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    xml_classifier: typing.Optional[typing.Union[GlueClassifierXmlClassifier, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__fdbe4ee177cfb449c61451ebe729984bcdc0e11c8b50379ec18d553bb2c3f4aa(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f57a956f8aab410248c58fac4647e4d0e33bffb6bd66b60e42bbfb0f8da64251(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e81ce6f0e9e7e3336cde372e3735f7e428985dd189969fe7b15e1edbcf1f6b11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4cc4dfb38d9438d54c824dca6916bfafd2accca0c08dcc97cf89a74ff4cf48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b675136bea6f48352603df6ae1ca53e31650afb8d57b70f02fdb6e168b93d9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    csv_classifier: typing.Optional[typing.Union[GlueClassifierCsvClassifier, typing.Dict[builtins.str, typing.Any]]] = None,
    grok_classifier: typing.Optional[typing.Union[GlueClassifierGrokClassifier, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    json_classifier: typing.Optional[typing.Union[GlueClassifierJsonClassifier, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    xml_classifier: typing.Optional[typing.Union[GlueClassifierXmlClassifier, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ec247aa8a842aa7ebc50048759fb009e49ee93d9cf53b0186104f99345b88e(
    *,
    allow_single_column: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    contains_header: typing.Optional[builtins.str] = None,
    custom_datatype_configured: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    custom_datatypes: typing.Optional[typing.Sequence[builtins.str]] = None,
    delimiter: typing.Optional[builtins.str] = None,
    disable_value_trimming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    header: typing.Optional[typing.Sequence[builtins.str]] = None,
    quote_symbol: typing.Optional[builtins.str] = None,
    serde: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e864d30d06e491e6c77e311ed66a9f89e460e83ec4bc07c5d56e7f128730ee9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331411c51e2c1a15c1c8c9e1ab56c5ea801163b04b419acd7da1de65b4563880(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efeaf2da3430faeab5afb370c3a01591f4058592b051637b496ade3e291396d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e0bc1e5a650ca8b561db05e5fbc1dc86376686c854213b1b36ee75127cc88d7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d78eaa347df114f19d65bcc5fd0f05a44593d170e5952832b9ad4791673ff829(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57087ae0d715f10083061eaadb1db648e2299739267aaed147a6930823f0e75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a63e078a5984c296432347934cc58166451bc6da406a84e55e505bf83cb1e2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2eedcb2ae04555d3afe41e2a5026fab7213fa11682861e8d9268a7954ec17a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ee9fee5eabdb6edaa80887838b8919a4c9cf0bad3edce90618e3c7ab9c3ac52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d47758e005329ac457782bf4ef0828429c6a048fec2e00b83ab5324674bc0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cc90216fd4efa6aad186cf65d4290c35364091f7e7d2378744754641bb2091b(
    value: typing.Optional[GlueClassifierCsvClassifier],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a5637422d6b2e219f84d2be95967a40401cf8a815c6e2317be1294e7b7c28df(
    *,
    classification: builtins.str,
    grok_pattern: builtins.str,
    custom_patterns: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d583fa079db9f24b3f8d6087b489ee090102fc6954baf27ee41c62dbdd9e33d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8683d12fab0a70880968f891e33db3757fb3eff46f6bbd5c1136c43d7c4331e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa082906b2e627d98cb048bff590f26d656962f3bcfa19f86cea43ddb627acdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd3ae3558888b4db09e5b38e7638cde91b5b555a74e483a2137817c4d82ae04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de7057b8ad6468dae76675d0d7b0b892ef9ae11b0e8d05ab8e52d50d26f3b624(
    value: typing.Optional[GlueClassifierGrokClassifier],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23715933b08f471b4c10c9722292cf4594eae6e96b85dccec1cbffdecfcba8fd(
    *,
    json_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78200257926a6ad132bad451dcef47a8755ac58275621548e84777ec68b26a3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22d0275c9e0093105e5a4d4c87227c9fc572daf85f45e848b924f963952b32b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95833bd6654d1337df6bc83f6bb05348926467e5d627b60b1965764cb1be9cd0(
    value: typing.Optional[GlueClassifierJsonClassifier],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2964c124429eaa6e02ac9d54390cdae27554585b337c1b874dbd471b9ba3e33d(
    *,
    classification: builtins.str,
    row_tag: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc68915fb03ac84de18172a11093fe8e3318fabafcfb560bae777f8de3c2f6d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90cd07d063209434e6f74be5306f1afabb6099f0245343927bb1617284d23724(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12e6a45468201040614bf55c43c653280dfcef3931b2db021d8a31bd2a21565(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f7a7141dd7b8c3aecaba838803e0e82a6a3bf78cfe95eab8e879286433b430(
    value: typing.Optional[GlueClassifierXmlClassifier],
) -> None:
    """Type checking stubs"""
    pass
