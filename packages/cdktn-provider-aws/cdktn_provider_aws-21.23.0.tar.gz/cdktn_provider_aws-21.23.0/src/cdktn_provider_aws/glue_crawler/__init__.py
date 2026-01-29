r'''
# `aws_glue_crawler`

Refer to the Terraform Registry for docs: [`aws_glue_crawler`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler).
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


class GlueCrawler(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawler",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler aws_glue_crawler}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database_name: builtins.str,
        name: builtins.str,
        role: builtins.str,
        catalog_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerCatalogTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        configuration: typing.Optional[builtins.str] = None,
        delta_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerDeltaTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        dynamodb_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerDynamodbTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        hudi_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerHudiTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        iceberg_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerIcebergTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        jdbc_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerJdbcTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lake_formation_configuration: typing.Optional[typing.Union["GlueCrawlerLakeFormationConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        lineage_configuration: typing.Optional[typing.Union["GlueCrawlerLineageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        mongodb_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerMongodbTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        recrawl_policy: typing.Optional[typing.Union["GlueCrawlerRecrawlPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        s3_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerS3Target", typing.Dict[builtins.str, typing.Any]]]]] = None,
        schedule: typing.Optional[builtins.str] = None,
        schema_change_policy: typing.Optional[typing.Union["GlueCrawlerSchemaChangePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        table_prefix: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler aws_glue_crawler} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#database_name GlueCrawler#database_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#name GlueCrawler#name}.
        :param role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#role GlueCrawler#role}.
        :param catalog_target: catalog_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#catalog_target GlueCrawler#catalog_target}
        :param classifiers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#classifiers GlueCrawler#classifiers}.
        :param configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#configuration GlueCrawler#configuration}.
        :param delta_target: delta_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#delta_target GlueCrawler#delta_target}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#description GlueCrawler#description}.
        :param dynamodb_target: dynamodb_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#dynamodb_target GlueCrawler#dynamodb_target}
        :param hudi_target: hudi_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#hudi_target GlueCrawler#hudi_target}
        :param iceberg_target: iceberg_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#iceberg_target GlueCrawler#iceberg_target}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#id GlueCrawler#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jdbc_target: jdbc_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#jdbc_target GlueCrawler#jdbc_target}
        :param lake_formation_configuration: lake_formation_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#lake_formation_configuration GlueCrawler#lake_formation_configuration}
        :param lineage_configuration: lineage_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#lineage_configuration GlueCrawler#lineage_configuration}
        :param mongodb_target: mongodb_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#mongodb_target GlueCrawler#mongodb_target}
        :param recrawl_policy: recrawl_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#recrawl_policy GlueCrawler#recrawl_policy}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#region GlueCrawler#region}
        :param s3_target: s3_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#s3_target GlueCrawler#s3_target}
        :param schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#schedule GlueCrawler#schedule}.
        :param schema_change_policy: schema_change_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#schema_change_policy GlueCrawler#schema_change_policy}
        :param security_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#security_configuration GlueCrawler#security_configuration}.
        :param table_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#table_prefix GlueCrawler#table_prefix}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#tags GlueCrawler#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#tags_all GlueCrawler#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9342e177a78396a7b848137db6443e1db1eb2a226eb6fe1faee18c9485ddf52a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GlueCrawlerConfig(
            database_name=database_name,
            name=name,
            role=role,
            catalog_target=catalog_target,
            classifiers=classifiers,
            configuration=configuration,
            delta_target=delta_target,
            description=description,
            dynamodb_target=dynamodb_target,
            hudi_target=hudi_target,
            iceberg_target=iceberg_target,
            id=id,
            jdbc_target=jdbc_target,
            lake_formation_configuration=lake_formation_configuration,
            lineage_configuration=lineage_configuration,
            mongodb_target=mongodb_target,
            recrawl_policy=recrawl_policy,
            region=region,
            s3_target=s3_target,
            schedule=schedule,
            schema_change_policy=schema_change_policy,
            security_configuration=security_configuration,
            table_prefix=table_prefix,
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
        '''Generates CDKTF code for importing a GlueCrawler resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GlueCrawler to import.
        :param import_from_id: The id of the existing GlueCrawler that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GlueCrawler to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__843c03e084cfff4cb7010269fd3b18bd6d2e18b451c83bc239a5f4664c0b6a94)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCatalogTarget")
    def put_catalog_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerCatalogTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25e35ea1e7a62dab3a0fa78084f4179320473349d73e5f6e1da0dc8f4e22ec21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCatalogTarget", [value]))

    @jsii.member(jsii_name="putDeltaTarget")
    def put_delta_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerDeltaTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b921de2a18091d891c30fe8fc28de1107efa726b0fcf67ebf1fbdf8c218c5ee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeltaTarget", [value]))

    @jsii.member(jsii_name="putDynamodbTarget")
    def put_dynamodb_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerDynamodbTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d597ae5ced4f6a5aa1899d0986926ac6158a7d3bfec9f8fe47291acb0b1666b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDynamodbTarget", [value]))

    @jsii.member(jsii_name="putHudiTarget")
    def put_hudi_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerHudiTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e931238953c83be390bca1f370319edc42ddbda53962daaf30653b9824e402f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHudiTarget", [value]))

    @jsii.member(jsii_name="putIcebergTarget")
    def put_iceberg_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerIcebergTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__626299f69cd643d0a0b39a9d823e614685542e47a4f63e419f90a4aee698e083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIcebergTarget", [value]))

    @jsii.member(jsii_name="putJdbcTarget")
    def put_jdbc_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerJdbcTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8607e964faaf25843223ade1468e1f2d7f94aca4ab41643acbf1f2d07822962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putJdbcTarget", [value]))

    @jsii.member(jsii_name="putLakeFormationConfiguration")
    def put_lake_formation_configuration(
        self,
        *,
        account_id: typing.Optional[builtins.str] = None,
        use_lake_formation_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#account_id GlueCrawler#account_id}.
        :param use_lake_formation_credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#use_lake_formation_credentials GlueCrawler#use_lake_formation_credentials}.
        '''
        value = GlueCrawlerLakeFormationConfiguration(
            account_id=account_id,
            use_lake_formation_credentials=use_lake_formation_credentials,
        )

        return typing.cast(None, jsii.invoke(self, "putLakeFormationConfiguration", [value]))

    @jsii.member(jsii_name="putLineageConfiguration")
    def put_lineage_configuration(
        self,
        *,
        crawler_lineage_settings: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param crawler_lineage_settings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#crawler_lineage_settings GlueCrawler#crawler_lineage_settings}.
        '''
        value = GlueCrawlerLineageConfiguration(
            crawler_lineage_settings=crawler_lineage_settings
        )

        return typing.cast(None, jsii.invoke(self, "putLineageConfiguration", [value]))

    @jsii.member(jsii_name="putMongodbTarget")
    def put_mongodb_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerMongodbTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4627c7953694e8289aa9c567604dca9e7bc9dc38d90fba814b3010ef04a67604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMongodbTarget", [value]))

    @jsii.member(jsii_name="putRecrawlPolicy")
    def put_recrawl_policy(
        self,
        *,
        recrawl_behavior: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recrawl_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#recrawl_behavior GlueCrawler#recrawl_behavior}.
        '''
        value = GlueCrawlerRecrawlPolicy(recrawl_behavior=recrawl_behavior)

        return typing.cast(None, jsii.invoke(self, "putRecrawlPolicy", [value]))

    @jsii.member(jsii_name="putS3Target")
    def put_s3_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerS3Target", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d358cb176ea11745d81429f7690a95e0edc60a3a89e91df9eaf353c61b9d36e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putS3Target", [value]))

    @jsii.member(jsii_name="putSchemaChangePolicy")
    def put_schema_change_policy(
        self,
        *,
        delete_behavior: typing.Optional[builtins.str] = None,
        update_behavior: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delete_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#delete_behavior GlueCrawler#delete_behavior}.
        :param update_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#update_behavior GlueCrawler#update_behavior}.
        '''
        value = GlueCrawlerSchemaChangePolicy(
            delete_behavior=delete_behavior, update_behavior=update_behavior
        )

        return typing.cast(None, jsii.invoke(self, "putSchemaChangePolicy", [value]))

    @jsii.member(jsii_name="resetCatalogTarget")
    def reset_catalog_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCatalogTarget", []))

    @jsii.member(jsii_name="resetClassifiers")
    def reset_classifiers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClassifiers", []))

    @jsii.member(jsii_name="resetConfiguration")
    def reset_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfiguration", []))

    @jsii.member(jsii_name="resetDeltaTarget")
    def reset_delta_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeltaTarget", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDynamodbTarget")
    def reset_dynamodb_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamodbTarget", []))

    @jsii.member(jsii_name="resetHudiTarget")
    def reset_hudi_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHudiTarget", []))

    @jsii.member(jsii_name="resetIcebergTarget")
    def reset_iceberg_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIcebergTarget", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetJdbcTarget")
    def reset_jdbc_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJdbcTarget", []))

    @jsii.member(jsii_name="resetLakeFormationConfiguration")
    def reset_lake_formation_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLakeFormationConfiguration", []))

    @jsii.member(jsii_name="resetLineageConfiguration")
    def reset_lineage_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLineageConfiguration", []))

    @jsii.member(jsii_name="resetMongodbTarget")
    def reset_mongodb_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMongodbTarget", []))

    @jsii.member(jsii_name="resetRecrawlPolicy")
    def reset_recrawl_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecrawlPolicy", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetS3Target")
    def reset_s3_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Target", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetSchemaChangePolicy")
    def reset_schema_change_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaChangePolicy", []))

    @jsii.member(jsii_name="resetSecurityConfiguration")
    def reset_security_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityConfiguration", []))

    @jsii.member(jsii_name="resetTablePrefix")
    def reset_table_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTablePrefix", []))

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
    @jsii.member(jsii_name="catalogTarget")
    def catalog_target(self) -> "GlueCrawlerCatalogTargetList":
        return typing.cast("GlueCrawlerCatalogTargetList", jsii.get(self, "catalogTarget"))

    @builtins.property
    @jsii.member(jsii_name="deltaTarget")
    def delta_target(self) -> "GlueCrawlerDeltaTargetList":
        return typing.cast("GlueCrawlerDeltaTargetList", jsii.get(self, "deltaTarget"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbTarget")
    def dynamodb_target(self) -> "GlueCrawlerDynamodbTargetList":
        return typing.cast("GlueCrawlerDynamodbTargetList", jsii.get(self, "dynamodbTarget"))

    @builtins.property
    @jsii.member(jsii_name="hudiTarget")
    def hudi_target(self) -> "GlueCrawlerHudiTargetList":
        return typing.cast("GlueCrawlerHudiTargetList", jsii.get(self, "hudiTarget"))

    @builtins.property
    @jsii.member(jsii_name="icebergTarget")
    def iceberg_target(self) -> "GlueCrawlerIcebergTargetList":
        return typing.cast("GlueCrawlerIcebergTargetList", jsii.get(self, "icebergTarget"))

    @builtins.property
    @jsii.member(jsii_name="jdbcTarget")
    def jdbc_target(self) -> "GlueCrawlerJdbcTargetList":
        return typing.cast("GlueCrawlerJdbcTargetList", jsii.get(self, "jdbcTarget"))

    @builtins.property
    @jsii.member(jsii_name="lakeFormationConfiguration")
    def lake_formation_configuration(
        self,
    ) -> "GlueCrawlerLakeFormationConfigurationOutputReference":
        return typing.cast("GlueCrawlerLakeFormationConfigurationOutputReference", jsii.get(self, "lakeFormationConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="lineageConfiguration")
    def lineage_configuration(self) -> "GlueCrawlerLineageConfigurationOutputReference":
        return typing.cast("GlueCrawlerLineageConfigurationOutputReference", jsii.get(self, "lineageConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="mongodbTarget")
    def mongodb_target(self) -> "GlueCrawlerMongodbTargetList":
        return typing.cast("GlueCrawlerMongodbTargetList", jsii.get(self, "mongodbTarget"))

    @builtins.property
    @jsii.member(jsii_name="recrawlPolicy")
    def recrawl_policy(self) -> "GlueCrawlerRecrawlPolicyOutputReference":
        return typing.cast("GlueCrawlerRecrawlPolicyOutputReference", jsii.get(self, "recrawlPolicy"))

    @builtins.property
    @jsii.member(jsii_name="s3Target")
    def s3_target(self) -> "GlueCrawlerS3TargetList":
        return typing.cast("GlueCrawlerS3TargetList", jsii.get(self, "s3Target"))

    @builtins.property
    @jsii.member(jsii_name="schemaChangePolicy")
    def schema_change_policy(self) -> "GlueCrawlerSchemaChangePolicyOutputReference":
        return typing.cast("GlueCrawlerSchemaChangePolicyOutputReference", jsii.get(self, "schemaChangePolicy"))

    @builtins.property
    @jsii.member(jsii_name="catalogTargetInput")
    def catalog_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerCatalogTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerCatalogTarget"]]], jsii.get(self, "catalogTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="classifiersInput")
    def classifiers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "classifiersInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationInput")
    def configuration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configurationInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="deltaTargetInput")
    def delta_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerDeltaTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerDeltaTarget"]]], jsii.get(self, "deltaTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbTargetInput")
    def dynamodb_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerDynamodbTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerDynamodbTarget"]]], jsii.get(self, "dynamodbTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="hudiTargetInput")
    def hudi_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerHudiTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerHudiTarget"]]], jsii.get(self, "hudiTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="icebergTargetInput")
    def iceberg_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerIcebergTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerIcebergTarget"]]], jsii.get(self, "icebergTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="jdbcTargetInput")
    def jdbc_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerJdbcTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerJdbcTarget"]]], jsii.get(self, "jdbcTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="lakeFormationConfigurationInput")
    def lake_formation_configuration_input(
        self,
    ) -> typing.Optional["GlueCrawlerLakeFormationConfiguration"]:
        return typing.cast(typing.Optional["GlueCrawlerLakeFormationConfiguration"], jsii.get(self, "lakeFormationConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="lineageConfigurationInput")
    def lineage_configuration_input(
        self,
    ) -> typing.Optional["GlueCrawlerLineageConfiguration"]:
        return typing.cast(typing.Optional["GlueCrawlerLineageConfiguration"], jsii.get(self, "lineageConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="mongodbTargetInput")
    def mongodb_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerMongodbTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerMongodbTarget"]]], jsii.get(self, "mongodbTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="recrawlPolicyInput")
    def recrawl_policy_input(self) -> typing.Optional["GlueCrawlerRecrawlPolicy"]:
        return typing.cast(typing.Optional["GlueCrawlerRecrawlPolicy"], jsii.get(self, "recrawlPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleInput"))

    @builtins.property
    @jsii.member(jsii_name="s3TargetInput")
    def s3_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerS3Target"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerS3Target"]]], jsii.get(self, "s3TargetInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaChangePolicyInput")
    def schema_change_policy_input(
        self,
    ) -> typing.Optional["GlueCrawlerSchemaChangePolicy"]:
        return typing.cast(typing.Optional["GlueCrawlerSchemaChangePolicy"], jsii.get(self, "schemaChangePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="securityConfigurationInput")
    def security_configuration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="tablePrefixInput")
    def table_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tablePrefixInput"))

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
    @jsii.member(jsii_name="classifiers")
    def classifiers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "classifiers"))

    @classifiers.setter
    def classifiers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f1cde679930ebfc64ea847b09f9423bff9e3e5a16fdb64c3d1137e13dfeb970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classifiers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4872a4b8d15330badec53d7fccd19f911acc088f581a940ea63599df1bd2f34a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e09f10e91f9bf8a15bc800fa50ddac2995e1a6896ce7ed97e2e68a10afc49c7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c8e1b5803b587057a927ad56fd1237153ef2bb420b511255643c0cbe4e4d8a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53dbb5e1d80a9440dba144aa4391c67b615c96ba5537738919426203a30cb979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25b86930fa88f2fdb4ec8224bdcc523fdf39b73759600f3d9d75b257738587b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a13bfa32b6c33d84017eefd19f7d97cde52270a3caa7d62237d6fdfb795c2808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b96afd618317b9204ea2cc8fc1554ba569002149bf895cb438fdce6f1e2202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59dbf75748872a604c64c479be4e2cc659d1f8ed4bcbe2d8d10789ad8ca2278e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityConfiguration")
    def security_configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityConfiguration"))

    @security_configuration.setter
    def security_configuration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88348629df01d984a206a26a4b3c82aaa4a84d87fd70158aec7778cdca6b949)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tablePrefix")
    def table_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tablePrefix"))

    @table_prefix.setter
    def table_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e1b7d5a5c3799ccc794f42b1b19d96b3f345efd6aa19892b00ca64fd88ea055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tablePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__687196ab3514bb5c6eaa4a28fc892e2a399ced1a1ad2986119819fa1c03f2029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f802ab49447ab6bdc32f9667239e3da8b9ff8c5bf12fd07ffbbaaa240156a33b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerCatalogTarget",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "tables": "tables",
        "connection_name": "connectionName",
        "dlq_event_queue_arn": "dlqEventQueueArn",
        "event_queue_arn": "eventQueueArn",
    },
)
class GlueCrawlerCatalogTarget:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        tables: typing.Sequence[builtins.str],
        connection_name: typing.Optional[builtins.str] = None,
        dlq_event_queue_arn: typing.Optional[builtins.str] = None,
        event_queue_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#database_name GlueCrawler#database_name}.
        :param tables: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#tables GlueCrawler#tables}.
        :param connection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.
        :param dlq_event_queue_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#dlq_event_queue_arn GlueCrawler#dlq_event_queue_arn}.
        :param event_queue_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#event_queue_arn GlueCrawler#event_queue_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e18320e195d1e429d110039366eba3068a794d4e05763bc426083767d614e2f4)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument tables", value=tables, expected_type=type_hints["tables"])
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument dlq_event_queue_arn", value=dlq_event_queue_arn, expected_type=type_hints["dlq_event_queue_arn"])
            check_type(argname="argument event_queue_arn", value=event_queue_arn, expected_type=type_hints["event_queue_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "tables": tables,
        }
        if connection_name is not None:
            self._values["connection_name"] = connection_name
        if dlq_event_queue_arn is not None:
            self._values["dlq_event_queue_arn"] = dlq_event_queue_arn
        if event_queue_arn is not None:
            self._values["event_queue_arn"] = event_queue_arn

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#database_name GlueCrawler#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tables(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#tables GlueCrawler#tables}.'''
        result = self._values.get("tables")
        assert result is not None, "Required property 'tables' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def connection_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.'''
        result = self._values.get("connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dlq_event_queue_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#dlq_event_queue_arn GlueCrawler#dlq_event_queue_arn}.'''
        result = self._values.get("dlq_event_queue_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_queue_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#event_queue_arn GlueCrawler#event_queue_arn}.'''
        result = self._values.get("event_queue_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerCatalogTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerCatalogTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerCatalogTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33412f84a65f1b6fc7f8c226b029f3ce68edef7b85d87e5b57a8dc4537a00f3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GlueCrawlerCatalogTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76beba61f0436f0423d9bc1b705ed31d0503add70842741ebcdce5787814bef3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GlueCrawlerCatalogTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c1d79f81263dd1fb7197402d84ee50af398ade773997551c3319cd5554f056)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f97c4fe973adb3abb04bf437b6f3ac3e567236663936b65044c0e5fc845d3a9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__897a43c8b6356b14f990f499d098b851b2b4d27d450d69ce8c7ec84f4b8db681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerCatalogTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerCatalogTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerCatalogTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d882f172d80679d08ef99ff12ead9a2ef88305ead06134d60dea1f57a802002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GlueCrawlerCatalogTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerCatalogTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__860260ad8dc8f5d451af06a5b30adec86d88c50bac159e0da23119e06b7bd8ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConnectionName")
    def reset_connection_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionName", []))

    @jsii.member(jsii_name="resetDlqEventQueueArn")
    def reset_dlq_event_queue_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDlqEventQueueArn", []))

    @jsii.member(jsii_name="resetEventQueueArn")
    def reset_event_queue_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventQueueArn", []))

    @builtins.property
    @jsii.member(jsii_name="connectionNameInput")
    def connection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dlqEventQueueArnInput")
    def dlq_event_queue_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dlqEventQueueArnInput"))

    @builtins.property
    @jsii.member(jsii_name="eventQueueArnInput")
    def event_queue_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventQueueArnInput"))

    @builtins.property
    @jsii.member(jsii_name="tablesInput")
    def tables_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tablesInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @connection_name.setter
    def connection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__517d5457a6e169ff39193c93bb493a47a61b5fd8123630c947e364bfc04f3689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a952d5aca77d68c8f7fed5428a6a23718140611b5cf8dd648b8a412b7f05a4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dlqEventQueueArn")
    def dlq_event_queue_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dlqEventQueueArn"))

    @dlq_event_queue_arn.setter
    def dlq_event_queue_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10c2aaa116a5aac48b1f0fd55466d4ca5b876525a19bbd7fc089d6b88bbea857)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dlqEventQueueArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventQueueArn")
    def event_queue_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventQueueArn"))

    @event_queue_arn.setter
    def event_queue_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18836f545db1f9ee1c4d2861cd0d6478159aa852585237dda0e91329d700075a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventQueueArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tables")
    def tables(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tables"))

    @tables.setter
    def tables(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ded589d521c6a3823d50d83063f4a9fd0dac0a09ca00645e39812ae9ba0d8bb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerCatalogTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerCatalogTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerCatalogTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39161dab9eca223e01c0f16f0e9fbf48cea575f0fd085ee20d5bcf314d05f230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "database_name": "databaseName",
        "name": "name",
        "role": "role",
        "catalog_target": "catalogTarget",
        "classifiers": "classifiers",
        "configuration": "configuration",
        "delta_target": "deltaTarget",
        "description": "description",
        "dynamodb_target": "dynamodbTarget",
        "hudi_target": "hudiTarget",
        "iceberg_target": "icebergTarget",
        "id": "id",
        "jdbc_target": "jdbcTarget",
        "lake_formation_configuration": "lakeFormationConfiguration",
        "lineage_configuration": "lineageConfiguration",
        "mongodb_target": "mongodbTarget",
        "recrawl_policy": "recrawlPolicy",
        "region": "region",
        "s3_target": "s3Target",
        "schedule": "schedule",
        "schema_change_policy": "schemaChangePolicy",
        "security_configuration": "securityConfiguration",
        "table_prefix": "tablePrefix",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class GlueCrawlerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        database_name: builtins.str,
        name: builtins.str,
        role: builtins.str,
        catalog_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerCatalogTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
        classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        configuration: typing.Optional[builtins.str] = None,
        delta_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerDeltaTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        dynamodb_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerDynamodbTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        hudi_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerHudiTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        iceberg_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerIcebergTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        jdbc_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerJdbcTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lake_formation_configuration: typing.Optional[typing.Union["GlueCrawlerLakeFormationConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        lineage_configuration: typing.Optional[typing.Union["GlueCrawlerLineageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        mongodb_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerMongodbTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        recrawl_policy: typing.Optional[typing.Union["GlueCrawlerRecrawlPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        s3_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerS3Target", typing.Dict[builtins.str, typing.Any]]]]] = None,
        schedule: typing.Optional[builtins.str] = None,
        schema_change_policy: typing.Optional[typing.Union["GlueCrawlerSchemaChangePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        table_prefix: typing.Optional[builtins.str] = None,
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
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#database_name GlueCrawler#database_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#name GlueCrawler#name}.
        :param role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#role GlueCrawler#role}.
        :param catalog_target: catalog_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#catalog_target GlueCrawler#catalog_target}
        :param classifiers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#classifiers GlueCrawler#classifiers}.
        :param configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#configuration GlueCrawler#configuration}.
        :param delta_target: delta_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#delta_target GlueCrawler#delta_target}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#description GlueCrawler#description}.
        :param dynamodb_target: dynamodb_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#dynamodb_target GlueCrawler#dynamodb_target}
        :param hudi_target: hudi_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#hudi_target GlueCrawler#hudi_target}
        :param iceberg_target: iceberg_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#iceberg_target GlueCrawler#iceberg_target}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#id GlueCrawler#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jdbc_target: jdbc_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#jdbc_target GlueCrawler#jdbc_target}
        :param lake_formation_configuration: lake_formation_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#lake_formation_configuration GlueCrawler#lake_formation_configuration}
        :param lineage_configuration: lineage_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#lineage_configuration GlueCrawler#lineage_configuration}
        :param mongodb_target: mongodb_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#mongodb_target GlueCrawler#mongodb_target}
        :param recrawl_policy: recrawl_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#recrawl_policy GlueCrawler#recrawl_policy}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#region GlueCrawler#region}
        :param s3_target: s3_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#s3_target GlueCrawler#s3_target}
        :param schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#schedule GlueCrawler#schedule}.
        :param schema_change_policy: schema_change_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#schema_change_policy GlueCrawler#schema_change_policy}
        :param security_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#security_configuration GlueCrawler#security_configuration}.
        :param table_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#table_prefix GlueCrawler#table_prefix}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#tags GlueCrawler#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#tags_all GlueCrawler#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(lake_formation_configuration, dict):
            lake_formation_configuration = GlueCrawlerLakeFormationConfiguration(**lake_formation_configuration)
        if isinstance(lineage_configuration, dict):
            lineage_configuration = GlueCrawlerLineageConfiguration(**lineage_configuration)
        if isinstance(recrawl_policy, dict):
            recrawl_policy = GlueCrawlerRecrawlPolicy(**recrawl_policy)
        if isinstance(schema_change_policy, dict):
            schema_change_policy = GlueCrawlerSchemaChangePolicy(**schema_change_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c16f8ab600ac86666d9e7bfc8576b6b7a636f7445b069196bdb9126361fdb0a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument catalog_target", value=catalog_target, expected_type=type_hints["catalog_target"])
            check_type(argname="argument classifiers", value=classifiers, expected_type=type_hints["classifiers"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument delta_target", value=delta_target, expected_type=type_hints["delta_target"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dynamodb_target", value=dynamodb_target, expected_type=type_hints["dynamodb_target"])
            check_type(argname="argument hudi_target", value=hudi_target, expected_type=type_hints["hudi_target"])
            check_type(argname="argument iceberg_target", value=iceberg_target, expected_type=type_hints["iceberg_target"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument jdbc_target", value=jdbc_target, expected_type=type_hints["jdbc_target"])
            check_type(argname="argument lake_formation_configuration", value=lake_formation_configuration, expected_type=type_hints["lake_formation_configuration"])
            check_type(argname="argument lineage_configuration", value=lineage_configuration, expected_type=type_hints["lineage_configuration"])
            check_type(argname="argument mongodb_target", value=mongodb_target, expected_type=type_hints["mongodb_target"])
            check_type(argname="argument recrawl_policy", value=recrawl_policy, expected_type=type_hints["recrawl_policy"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument s3_target", value=s3_target, expected_type=type_hints["s3_target"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument schema_change_policy", value=schema_change_policy, expected_type=type_hints["schema_change_policy"])
            check_type(argname="argument security_configuration", value=security_configuration, expected_type=type_hints["security_configuration"])
            check_type(argname="argument table_prefix", value=table_prefix, expected_type=type_hints["table_prefix"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "name": name,
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
        if catalog_target is not None:
            self._values["catalog_target"] = catalog_target
        if classifiers is not None:
            self._values["classifiers"] = classifiers
        if configuration is not None:
            self._values["configuration"] = configuration
        if delta_target is not None:
            self._values["delta_target"] = delta_target
        if description is not None:
            self._values["description"] = description
        if dynamodb_target is not None:
            self._values["dynamodb_target"] = dynamodb_target
        if hudi_target is not None:
            self._values["hudi_target"] = hudi_target
        if iceberg_target is not None:
            self._values["iceberg_target"] = iceberg_target
        if id is not None:
            self._values["id"] = id
        if jdbc_target is not None:
            self._values["jdbc_target"] = jdbc_target
        if lake_formation_configuration is not None:
            self._values["lake_formation_configuration"] = lake_formation_configuration
        if lineage_configuration is not None:
            self._values["lineage_configuration"] = lineage_configuration
        if mongodb_target is not None:
            self._values["mongodb_target"] = mongodb_target
        if recrawl_policy is not None:
            self._values["recrawl_policy"] = recrawl_policy
        if region is not None:
            self._values["region"] = region
        if s3_target is not None:
            self._values["s3_target"] = s3_target
        if schedule is not None:
            self._values["schedule"] = schedule
        if schema_change_policy is not None:
            self._values["schema_change_policy"] = schema_change_policy
        if security_configuration is not None:
            self._values["security_configuration"] = security_configuration
        if table_prefix is not None:
            self._values["table_prefix"] = table_prefix
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
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#database_name GlueCrawler#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#name GlueCrawler#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#role GlueCrawler#role}.'''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def catalog_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerCatalogTarget]]]:
        '''catalog_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#catalog_target GlueCrawler#catalog_target}
        '''
        result = self._values.get("catalog_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerCatalogTarget]]], result)

    @builtins.property
    def classifiers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#classifiers GlueCrawler#classifiers}.'''
        result = self._values.get("classifiers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def configuration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#configuration GlueCrawler#configuration}.'''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delta_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerDeltaTarget"]]]:
        '''delta_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#delta_target GlueCrawler#delta_target}
        '''
        result = self._values.get("delta_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerDeltaTarget"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#description GlueCrawler#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynamodb_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerDynamodbTarget"]]]:
        '''dynamodb_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#dynamodb_target GlueCrawler#dynamodb_target}
        '''
        result = self._values.get("dynamodb_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerDynamodbTarget"]]], result)

    @builtins.property
    def hudi_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerHudiTarget"]]]:
        '''hudi_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#hudi_target GlueCrawler#hudi_target}
        '''
        result = self._values.get("hudi_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerHudiTarget"]]], result)

    @builtins.property
    def iceberg_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerIcebergTarget"]]]:
        '''iceberg_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#iceberg_target GlueCrawler#iceberg_target}
        '''
        result = self._values.get("iceberg_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerIcebergTarget"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#id GlueCrawler#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jdbc_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerJdbcTarget"]]]:
        '''jdbc_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#jdbc_target GlueCrawler#jdbc_target}
        '''
        result = self._values.get("jdbc_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerJdbcTarget"]]], result)

    @builtins.property
    def lake_formation_configuration(
        self,
    ) -> typing.Optional["GlueCrawlerLakeFormationConfiguration"]:
        '''lake_formation_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#lake_formation_configuration GlueCrawler#lake_formation_configuration}
        '''
        result = self._values.get("lake_formation_configuration")
        return typing.cast(typing.Optional["GlueCrawlerLakeFormationConfiguration"], result)

    @builtins.property
    def lineage_configuration(
        self,
    ) -> typing.Optional["GlueCrawlerLineageConfiguration"]:
        '''lineage_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#lineage_configuration GlueCrawler#lineage_configuration}
        '''
        result = self._values.get("lineage_configuration")
        return typing.cast(typing.Optional["GlueCrawlerLineageConfiguration"], result)

    @builtins.property
    def mongodb_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerMongodbTarget"]]]:
        '''mongodb_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#mongodb_target GlueCrawler#mongodb_target}
        '''
        result = self._values.get("mongodb_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerMongodbTarget"]]], result)

    @builtins.property
    def recrawl_policy(self) -> typing.Optional["GlueCrawlerRecrawlPolicy"]:
        '''recrawl_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#recrawl_policy GlueCrawler#recrawl_policy}
        '''
        result = self._values.get("recrawl_policy")
        return typing.cast(typing.Optional["GlueCrawlerRecrawlPolicy"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#region GlueCrawler#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerS3Target"]]]:
        '''s3_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#s3_target GlueCrawler#s3_target}
        '''
        result = self._values.get("s3_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerS3Target"]]], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#schedule GlueCrawler#schedule}.'''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_change_policy(self) -> typing.Optional["GlueCrawlerSchemaChangePolicy"]:
        '''schema_change_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#schema_change_policy GlueCrawler#schema_change_policy}
        '''
        result = self._values.get("schema_change_policy")
        return typing.cast(typing.Optional["GlueCrawlerSchemaChangePolicy"], result)

    @builtins.property
    def security_configuration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#security_configuration GlueCrawler#security_configuration}.'''
        result = self._values.get("security_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#table_prefix GlueCrawler#table_prefix}.'''
        result = self._values.get("table_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#tags GlueCrawler#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#tags_all GlueCrawler#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerDeltaTarget",
    jsii_struct_bases=[],
    name_mapping={
        "delta_tables": "deltaTables",
        "write_manifest": "writeManifest",
        "connection_name": "connectionName",
        "create_native_delta_table": "createNativeDeltaTable",
    },
)
class GlueCrawlerDeltaTarget:
    def __init__(
        self,
        *,
        delta_tables: typing.Sequence[builtins.str],
        write_manifest: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        connection_name: typing.Optional[builtins.str] = None,
        create_native_delta_table: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param delta_tables: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#delta_tables GlueCrawler#delta_tables}.
        :param write_manifest: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#write_manifest GlueCrawler#write_manifest}.
        :param connection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.
        :param create_native_delta_table: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#create_native_delta_table GlueCrawler#create_native_delta_table}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6abb7e8205f260da59e1fc1658f9ef55dc44e814d7c3962ce661697312bf912d)
            check_type(argname="argument delta_tables", value=delta_tables, expected_type=type_hints["delta_tables"])
            check_type(argname="argument write_manifest", value=write_manifest, expected_type=type_hints["write_manifest"])
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument create_native_delta_table", value=create_native_delta_table, expected_type=type_hints["create_native_delta_table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delta_tables": delta_tables,
            "write_manifest": write_manifest,
        }
        if connection_name is not None:
            self._values["connection_name"] = connection_name
        if create_native_delta_table is not None:
            self._values["create_native_delta_table"] = create_native_delta_table

    @builtins.property
    def delta_tables(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#delta_tables GlueCrawler#delta_tables}.'''
        result = self._values.get("delta_tables")
        assert result is not None, "Required property 'delta_tables' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def write_manifest(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#write_manifest GlueCrawler#write_manifest}.'''
        result = self._values.get("write_manifest")
        assert result is not None, "Required property 'write_manifest' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def connection_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.'''
        result = self._values.get("connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_native_delta_table(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#create_native_delta_table GlueCrawler#create_native_delta_table}.'''
        result = self._values.get("create_native_delta_table")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerDeltaTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerDeltaTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerDeltaTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd416b56c346042b18734f1467c6705f3fa17c66521bd114d14569403c4440d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GlueCrawlerDeltaTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2c8e4382adb258e7c43bbe42570477e89aeb83b833bd5791266cd291cf7025f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GlueCrawlerDeltaTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__589615d3cf4780809e35a5dfecc484ee572bf69b2e7b00eefd813a7f8461eae3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44260ca4a812fcd7ba7bf456e82492a1eae6d44253b4628e568b428f98683cf8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b250a6cac4fb12711fad944a60608bb7e7b324f347f480121b015e4d8ead7b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerDeltaTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerDeltaTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerDeltaTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fbff3b3cc5808de9d4df17288d0defc16229b55bd241fb09329a5e802d83ed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GlueCrawlerDeltaTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerDeltaTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a153bbb2d73cca354612e9e67a97250d3f73d9b5d1d0f44ab40cd40010b1041)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConnectionName")
    def reset_connection_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionName", []))

    @jsii.member(jsii_name="resetCreateNativeDeltaTable")
    def reset_create_native_delta_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateNativeDeltaTable", []))

    @builtins.property
    @jsii.member(jsii_name="connectionNameInput")
    def connection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="createNativeDeltaTableInput")
    def create_native_delta_table_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "createNativeDeltaTableInput"))

    @builtins.property
    @jsii.member(jsii_name="deltaTablesInput")
    def delta_tables_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "deltaTablesInput"))

    @builtins.property
    @jsii.member(jsii_name="writeManifestInput")
    def write_manifest_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "writeManifestInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @connection_name.setter
    def connection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dba6218e6acb59298a4cabd1cb2aea8ce7deead75a13403a679101f9da329931)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createNativeDeltaTable")
    def create_native_delta_table(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "createNativeDeltaTable"))

    @create_native_delta_table.setter
    def create_native_delta_table(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94411a986a1b70d1b7ebebe2c818329148f0703767e830b546d8e29bb7ac3f42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createNativeDeltaTable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deltaTables")
    def delta_tables(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "deltaTables"))

    @delta_tables.setter
    def delta_tables(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__050a728b4555fe806bdeccb9811145f125bb2a01aefc1d591054f08834cf2e58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deltaTables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeManifest")
    def write_manifest(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "writeManifest"))

    @write_manifest.setter
    def write_manifest(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a4fa8d20d780d02cc1822d16228326a9aff89692b493ada209765a2ba2ce514)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeManifest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerDeltaTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerDeltaTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerDeltaTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81416e96988fdff91947852ad536bcb89746d35f095f20bc39e17231272b5671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerDynamodbTarget",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "scan_all": "scanAll", "scan_rate": "scanRate"},
)
class GlueCrawlerDynamodbTarget:
    def __init__(
        self,
        *,
        path: builtins.str,
        scan_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scan_rate: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#path GlueCrawler#path}.
        :param scan_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#scan_all GlueCrawler#scan_all}.
        :param scan_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#scan_rate GlueCrawler#scan_rate}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1257288b62d7e36ff488452712ca6f1a192fee17e2c8d654d8560df7e09c860)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument scan_all", value=scan_all, expected_type=type_hints["scan_all"])
            check_type(argname="argument scan_rate", value=scan_rate, expected_type=type_hints["scan_rate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if scan_all is not None:
            self._values["scan_all"] = scan_all
        if scan_rate is not None:
            self._values["scan_rate"] = scan_rate

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#path GlueCrawler#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scan_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#scan_all GlueCrawler#scan_all}.'''
        result = self._values.get("scan_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scan_rate(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#scan_rate GlueCrawler#scan_rate}.'''
        result = self._values.get("scan_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerDynamodbTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerDynamodbTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerDynamodbTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86c72ab1c7651e738b5cef3b47bbcf765a14af23c79a936cdac4bc9b087da190)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GlueCrawlerDynamodbTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82d51c8334902653cfe969db52b3fd23e0c11c498e2a652c88bc44d9054dd7b9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GlueCrawlerDynamodbTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec696b28e599d82a65c77c81ae00117e1811e254fe2ad2b7d3b356eeb849089)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3da742a3d7fcde47559f76a80ff4997576e2a44df07f07f15d1add4d7b621271)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85b1e96a1d4a973d624cacfe4aba49754fd598b903257de79f14b7fe5d1b3682)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerDynamodbTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerDynamodbTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerDynamodbTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6ff18a10fa354912b3374eb69eccf83099f996eb161385dc43b8b66e292af3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GlueCrawlerDynamodbTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerDynamodbTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6aed0e19e9c15de4e448c0a12c4e1722624ed52f2d00d2524fe1f304e410455)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetScanAll")
    def reset_scan_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScanAll", []))

    @jsii.member(jsii_name="resetScanRate")
    def reset_scan_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScanRate", []))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="scanAllInput")
    def scan_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "scanAllInput"))

    @builtins.property
    @jsii.member(jsii_name="scanRateInput")
    def scan_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scanRateInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e65a7dbfa2d63280480e1c7c8d481ab8873f75187cb3e2dd16bce4b1d8e4a613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scanAll")
    def scan_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "scanAll"))

    @scan_all.setter
    def scan_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f12040d1a8d70acc010ce7975834b9dc627bff284792ce712d1c7bdf7fa4aac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scanAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scanRate")
    def scan_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scanRate"))

    @scan_rate.setter
    def scan_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0b5f63bc66922b45b4fc34188f9d671fe41782d3436176bacb067a6729b2ae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scanRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerDynamodbTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerDynamodbTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerDynamodbTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8401143ee11113f15fe4eacdee509dddfab70be1315f7f7b3b55cada9fcfa081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerHudiTarget",
    jsii_struct_bases=[],
    name_mapping={
        "maximum_traversal_depth": "maximumTraversalDepth",
        "paths": "paths",
        "connection_name": "connectionName",
        "exclusions": "exclusions",
    },
)
class GlueCrawlerHudiTarget:
    def __init__(
        self,
        *,
        maximum_traversal_depth: jsii.Number,
        paths: typing.Sequence[builtins.str],
        connection_name: typing.Optional[builtins.str] = None,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param maximum_traversal_depth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#maximum_traversal_depth GlueCrawler#maximum_traversal_depth}.
        :param paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#paths GlueCrawler#paths}.
        :param connection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.
        :param exclusions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#exclusions GlueCrawler#exclusions}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e535794f4fe62e14310ac01d601213ef31d8d6f75259ff5a9c90c2a0d02e3873)
            check_type(argname="argument maximum_traversal_depth", value=maximum_traversal_depth, expected_type=type_hints["maximum_traversal_depth"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "maximum_traversal_depth": maximum_traversal_depth,
            "paths": paths,
        }
        if connection_name is not None:
            self._values["connection_name"] = connection_name
        if exclusions is not None:
            self._values["exclusions"] = exclusions

    @builtins.property
    def maximum_traversal_depth(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#maximum_traversal_depth GlueCrawler#maximum_traversal_depth}.'''
        result = self._values.get("maximum_traversal_depth")
        assert result is not None, "Required property 'maximum_traversal_depth' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def paths(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#paths GlueCrawler#paths}.'''
        result = self._values.get("paths")
        assert result is not None, "Required property 'paths' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def connection_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.'''
        result = self._values.get("connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#exclusions GlueCrawler#exclusions}.'''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerHudiTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerHudiTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerHudiTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6f8aebbbf71670ad3eedc6c5e9bca410e5880dbac72461d6ea928d867d23623)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GlueCrawlerHudiTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cefbb0d9ef03934dba47e303a92f637861c07170f9d7515141f2be70b0c840e6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GlueCrawlerHudiTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574f6a96799a05da4f376d25a7ee20be1610c86e1814654dfc744a2d60764e71)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76801b893f0b8c468d0ffc2d326d15c654a1c4ab090f69fd371fead83c9f5468)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7ad821d69668c62e97856d47e6d7b7b69a11416290c1c73f7d147e0854676e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerHudiTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerHudiTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerHudiTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__004ecac499692d7b8c1b71521c230a8af2f8553176b73f62632111f4bcaab583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GlueCrawlerHudiTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerHudiTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33e8539344c04ae52ee54037acbbe190d70a1501018ad45ef65debafe89d9b05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConnectionName")
    def reset_connection_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionName", []))

    @jsii.member(jsii_name="resetExclusions")
    def reset_exclusions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusions", []))

    @builtins.property
    @jsii.member(jsii_name="connectionNameInput")
    def connection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionsInput")
    def exclusions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exclusionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumTraversalDepthInput")
    def maximum_traversal_depth_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumTraversalDepthInput"))

    @builtins.property
    @jsii.member(jsii_name="pathsInput")
    def paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pathsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @connection_name.setter
    def connection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcdc29dfc42d3cc8a9a84f0e4f82592fbd47d04a7cdaa30757c8215f4bc59577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusions")
    def exclusions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclusions"))

    @exclusions.setter
    def exclusions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3151bcd31c3bd649c8e1f47333b678aaa47ec5788b447ec4c0334108be219ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumTraversalDepth")
    def maximum_traversal_depth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumTraversalDepth"))

    @maximum_traversal_depth.setter
    def maximum_traversal_depth(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97bdbb61c5b606d4373cff278f9915acc72ffb17a13c488f99d42145bc891688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumTraversalDepth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @paths.setter
    def paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37f39b6f459aad8ef1ea3477896eb25055bd473fb94b5d585103ff755e15a734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerHudiTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerHudiTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerHudiTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51076e5c7d8b596f4e3519cd49a8523f97f1bab3a489c7a47622e5f04839679c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerIcebergTarget",
    jsii_struct_bases=[],
    name_mapping={
        "maximum_traversal_depth": "maximumTraversalDepth",
        "paths": "paths",
        "connection_name": "connectionName",
        "exclusions": "exclusions",
    },
)
class GlueCrawlerIcebergTarget:
    def __init__(
        self,
        *,
        maximum_traversal_depth: jsii.Number,
        paths: typing.Sequence[builtins.str],
        connection_name: typing.Optional[builtins.str] = None,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param maximum_traversal_depth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#maximum_traversal_depth GlueCrawler#maximum_traversal_depth}.
        :param paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#paths GlueCrawler#paths}.
        :param connection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.
        :param exclusions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#exclusions GlueCrawler#exclusions}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55a18cf01f5e2978aa667b22c9bc2ed9f136e124db1b5305ef67bf1389d4e325)
            check_type(argname="argument maximum_traversal_depth", value=maximum_traversal_depth, expected_type=type_hints["maximum_traversal_depth"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "maximum_traversal_depth": maximum_traversal_depth,
            "paths": paths,
        }
        if connection_name is not None:
            self._values["connection_name"] = connection_name
        if exclusions is not None:
            self._values["exclusions"] = exclusions

    @builtins.property
    def maximum_traversal_depth(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#maximum_traversal_depth GlueCrawler#maximum_traversal_depth}.'''
        result = self._values.get("maximum_traversal_depth")
        assert result is not None, "Required property 'maximum_traversal_depth' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def paths(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#paths GlueCrawler#paths}.'''
        result = self._values.get("paths")
        assert result is not None, "Required property 'paths' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def connection_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.'''
        result = self._values.get("connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#exclusions GlueCrawler#exclusions}.'''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerIcebergTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerIcebergTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerIcebergTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b295e0ecdeb563346849ef8326e95d7e36b820f622ec0c5436f36b5a12a9884)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GlueCrawlerIcebergTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34948b364c04aa652db84c595301d6247b4867d9c9c209ad2b502befca8a60f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GlueCrawlerIcebergTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd47fecdf18c15328be00ca06bd08e14bb98dc178afac3c0ddaf09af18f704a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4712aca835fa25ab8515a63b398c52099ef11747137a14240bfe1929f2b7fd43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cdbda0223882642a020da5d79072ae5e9f749fed222ee0e4b75b960bde7b18a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerIcebergTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerIcebergTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerIcebergTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8137fad03d8a0cc6c9acf0551442f616e667846f6a548dfcae02abd0e888bad0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GlueCrawlerIcebergTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerIcebergTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ef1992c65bde8d1590024221b11ba44a63073c5bfd6a705bd1b5f3956b236c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConnectionName")
    def reset_connection_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionName", []))

    @jsii.member(jsii_name="resetExclusions")
    def reset_exclusions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusions", []))

    @builtins.property
    @jsii.member(jsii_name="connectionNameInput")
    def connection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionsInput")
    def exclusions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exclusionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumTraversalDepthInput")
    def maximum_traversal_depth_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumTraversalDepthInput"))

    @builtins.property
    @jsii.member(jsii_name="pathsInput")
    def paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pathsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @connection_name.setter
    def connection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e583eb5e30cb6d773d4c9cec9acc798426c704b29441b5cdf3e020cb5aacc90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusions")
    def exclusions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclusions"))

    @exclusions.setter
    def exclusions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c88f6afdfc8342e7d7262934a54f531103496eb732e3ec911ab2614621ce32ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumTraversalDepth")
    def maximum_traversal_depth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumTraversalDepth"))

    @maximum_traversal_depth.setter
    def maximum_traversal_depth(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1725ecfd4697ff2b3730572cce87e2b99472ef00754875d16376d35c03bd8049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumTraversalDepth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @paths.setter
    def paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81ed337e42563e80522e2823e07dafa38140e6fc4ff1d67c7fc6a28841ba36b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerIcebergTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerIcebergTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerIcebergTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f69fb5b5cf3e30b0d2626ff7a727c41ad5dbb1d8a2d5398f180b673371c299)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerJdbcTarget",
    jsii_struct_bases=[],
    name_mapping={
        "connection_name": "connectionName",
        "path": "path",
        "enable_additional_metadata": "enableAdditionalMetadata",
        "exclusions": "exclusions",
    },
)
class GlueCrawlerJdbcTarget:
    def __init__(
        self,
        *,
        connection_name: builtins.str,
        path: builtins.str,
        enable_additional_metadata: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#path GlueCrawler#path}.
        :param enable_additional_metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#enable_additional_metadata GlueCrawler#enable_additional_metadata}.
        :param exclusions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#exclusions GlueCrawler#exclusions}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fc26fa41ea360e5535776041ff2c01f56b1a10c40b3f3ae677b7bd5089cb4f4)
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument enable_additional_metadata", value=enable_additional_metadata, expected_type=type_hints["enable_additional_metadata"])
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_name": connection_name,
            "path": path,
        }
        if enable_additional_metadata is not None:
            self._values["enable_additional_metadata"] = enable_additional_metadata
        if exclusions is not None:
            self._values["exclusions"] = exclusions

    @builtins.property
    def connection_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.'''
        result = self._values.get("connection_name")
        assert result is not None, "Required property 'connection_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#path GlueCrawler#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enable_additional_metadata(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#enable_additional_metadata GlueCrawler#enable_additional_metadata}.'''
        result = self._values.get("enable_additional_metadata")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#exclusions GlueCrawler#exclusions}.'''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerJdbcTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerJdbcTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerJdbcTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__839e465b236137f3859e9d935653ea71e62aeb0ea82a1840028b28086a905cb7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GlueCrawlerJdbcTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb2525f45e33940df56fce74016f2f2b9974ec26ebaf223ce800b4c7c4323b7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GlueCrawlerJdbcTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94c03311d75ff03fdec281f2586247613207ad32b343c124873497c847d8232f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b9c6efe11a65118b95646e5ba5852e9acce37dbe133e6c2bd923838cd0f1fd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c2849f09f4d675dae3674a5172f32176b990e563dd34b85dd5c666f10910060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerJdbcTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerJdbcTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerJdbcTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1832a421af38f42fd38e34a746534431df931f53cb70912dfbe0ec7a12481f59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GlueCrawlerJdbcTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerJdbcTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd405bbe462f7f546e18fc0768c1df602790128bed18d3889e9848a42ad8fb44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnableAdditionalMetadata")
    def reset_enable_additional_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAdditionalMetadata", []))

    @jsii.member(jsii_name="resetExclusions")
    def reset_exclusions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusions", []))

    @builtins.property
    @jsii.member(jsii_name="connectionNameInput")
    def connection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAdditionalMetadataInput")
    def enable_additional_metadata_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "enableAdditionalMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionsInput")
    def exclusions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exclusionsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @connection_name.setter
    def connection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad57b9c8268ddbaa8d8f919de1ed4f51437b0800954ae994ca7f6a0514b481d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableAdditionalMetadata")
    def enable_additional_metadata(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "enableAdditionalMetadata"))

    @enable_additional_metadata.setter
    def enable_additional_metadata(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f646f6d2fdb1677ed706e2bdd4c662d062dc4fdbb8e83986ea8114be445dd98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAdditionalMetadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusions")
    def exclusions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclusions"))

    @exclusions.setter
    def exclusions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2245361f610e7411595b00b9c995d2f92b4e77b804ec7d8b1894d58def90059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72e53b8ba5c7315b339a569ecabf84a76d0da70038502c362e6ca248c103f6df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerJdbcTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerJdbcTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerJdbcTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a3ce186670dda4af2e36f62a2769bc1f90e46705ef839bb23e579494838e4be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerLakeFormationConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "use_lake_formation_credentials": "useLakeFormationCredentials",
    },
)
class GlueCrawlerLakeFormationConfiguration:
    def __init__(
        self,
        *,
        account_id: typing.Optional[builtins.str] = None,
        use_lake_formation_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#account_id GlueCrawler#account_id}.
        :param use_lake_formation_credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#use_lake_formation_credentials GlueCrawler#use_lake_formation_credentials}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31bc026d64f479762934528b7ff44e4ea410775655abcc0f7a73e1a527d4ac4e)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument use_lake_formation_credentials", value=use_lake_formation_credentials, expected_type=type_hints["use_lake_formation_credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_id is not None:
            self._values["account_id"] = account_id
        if use_lake_formation_credentials is not None:
            self._values["use_lake_formation_credentials"] = use_lake_formation_credentials

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#account_id GlueCrawler#account_id}.'''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_lake_formation_credentials(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#use_lake_formation_credentials GlueCrawler#use_lake_formation_credentials}.'''
        result = self._values.get("use_lake_formation_credentials")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerLakeFormationConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerLakeFormationConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerLakeFormationConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6b188925e8ef3c1c19c3b74037dbe5e2b450c368cdee3ff8b88c4b95e92958a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetUseLakeFormationCredentials")
    def reset_use_lake_formation_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseLakeFormationCredentials", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="useLakeFormationCredentialsInput")
    def use_lake_formation_credentials_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useLakeFormationCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c33e1e92a57a30dec143aebe694bffeaf61f19d73d0eabd09cebd7fb6499869)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useLakeFormationCredentials")
    def use_lake_formation_credentials(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useLakeFormationCredentials"))

    @use_lake_formation_credentials.setter
    def use_lake_formation_credentials(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17c78ff4525b7b0c98eff0c51a21a58379cc26c1e573b0478fc9379eded7886a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useLakeFormationCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueCrawlerLakeFormationConfiguration]:
        return typing.cast(typing.Optional[GlueCrawlerLakeFormationConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GlueCrawlerLakeFormationConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab03275921c23a03fc71bebeb0b487f50b546e97ce675f501d933010647d401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerLineageConfiguration",
    jsii_struct_bases=[],
    name_mapping={"crawler_lineage_settings": "crawlerLineageSettings"},
)
class GlueCrawlerLineageConfiguration:
    def __init__(
        self,
        *,
        crawler_lineage_settings: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param crawler_lineage_settings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#crawler_lineage_settings GlueCrawler#crawler_lineage_settings}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd751a5a1d877c8030fff4b03ae0f7fda59f8d3e028089a7f40e3deed92a4c32)
            check_type(argname="argument crawler_lineage_settings", value=crawler_lineage_settings, expected_type=type_hints["crawler_lineage_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if crawler_lineage_settings is not None:
            self._values["crawler_lineage_settings"] = crawler_lineage_settings

    @builtins.property
    def crawler_lineage_settings(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#crawler_lineage_settings GlueCrawler#crawler_lineage_settings}.'''
        result = self._values.get("crawler_lineage_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerLineageConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerLineageConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerLineageConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28654f664c9a793ff5f35528c1226bf19435c01245724eb85ee6e4ee8093bb5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCrawlerLineageSettings")
    def reset_crawler_lineage_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrawlerLineageSettings", []))

    @builtins.property
    @jsii.member(jsii_name="crawlerLineageSettingsInput")
    def crawler_lineage_settings_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crawlerLineageSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="crawlerLineageSettings")
    def crawler_lineage_settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crawlerLineageSettings"))

    @crawler_lineage_settings.setter
    def crawler_lineage_settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9da95fa7ae14c0ade6fe190cf4236e38864c58a21d977b9bb8fe19cb45e6f6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crawlerLineageSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueCrawlerLineageConfiguration]:
        return typing.cast(typing.Optional[GlueCrawlerLineageConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GlueCrawlerLineageConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6126283074b0247dd2fd367b814e0f684d8cb6cb8cad834bb884a9cdc8ceb3b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerMongodbTarget",
    jsii_struct_bases=[],
    name_mapping={
        "connection_name": "connectionName",
        "path": "path",
        "scan_all": "scanAll",
    },
)
class GlueCrawlerMongodbTarget:
    def __init__(
        self,
        *,
        connection_name: builtins.str,
        path: builtins.str,
        scan_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#path GlueCrawler#path}.
        :param scan_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#scan_all GlueCrawler#scan_all}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__185ed401fc9df1025023b569ba2a1c049f99f48d171bd227b4697940b8a85f26)
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument scan_all", value=scan_all, expected_type=type_hints["scan_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_name": connection_name,
            "path": path,
        }
        if scan_all is not None:
            self._values["scan_all"] = scan_all

    @builtins.property
    def connection_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.'''
        result = self._values.get("connection_name")
        assert result is not None, "Required property 'connection_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#path GlueCrawler#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scan_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#scan_all GlueCrawler#scan_all}.'''
        result = self._values.get("scan_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerMongodbTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerMongodbTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerMongodbTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c122b0be88d885f3a29574e8f997140452dd29ee7ca96288f3df3e0e8b2ffa4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GlueCrawlerMongodbTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__571d2db244586b5d3bd57b887822de333bf21a622e0a575df29bb5d55da4024f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GlueCrawlerMongodbTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e6a57541b2702a23fbb636b40ad0531237cf376ab5acdfa140319854c80ed6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f71ce6a4580e44b1de807f551d15d0aae3effffe97df9be7dd843593d2e249e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36c11894db9cc432f17dcec7a364293814165d7621cd71a4a352d878ae0a5d74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerMongodbTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerMongodbTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerMongodbTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d688e0de906e4b9e61ef189b6a4458a6928180d0b51bf26f6691116bca536a1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GlueCrawlerMongodbTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerMongodbTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de78a2e1532cdc995f8a61d0bd1ff3200c93e42a10347b9d1f4a7cac992a09ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetScanAll")
    def reset_scan_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScanAll", []))

    @builtins.property
    @jsii.member(jsii_name="connectionNameInput")
    def connection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="scanAllInput")
    def scan_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "scanAllInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @connection_name.setter
    def connection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5884f9475bd6120efcaa693f16279d5f99ed1d955aaa5065fba8cac9c7ca2cd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb847160b25f7651883ee8d8aa3fcb80005e4e062b03ab478279cecc33083c2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scanAll")
    def scan_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "scanAll"))

    @scan_all.setter
    def scan_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19b708a2ec3309942e4359fbc09c660d6d64cafa923736adf98db4a53ebdabe9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scanAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerMongodbTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerMongodbTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerMongodbTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3fa78b6469b5a124eddf1cdea34074ccc521a932da5b76f420edd08d6f4d59c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerRecrawlPolicy",
    jsii_struct_bases=[],
    name_mapping={"recrawl_behavior": "recrawlBehavior"},
)
class GlueCrawlerRecrawlPolicy:
    def __init__(
        self,
        *,
        recrawl_behavior: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recrawl_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#recrawl_behavior GlueCrawler#recrawl_behavior}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7af532d479d23fb1690132481a86a42b4821edc89274a5b8d94b85e469b583)
            check_type(argname="argument recrawl_behavior", value=recrawl_behavior, expected_type=type_hints["recrawl_behavior"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if recrawl_behavior is not None:
            self._values["recrawl_behavior"] = recrawl_behavior

    @builtins.property
    def recrawl_behavior(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#recrawl_behavior GlueCrawler#recrawl_behavior}.'''
        result = self._values.get("recrawl_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerRecrawlPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerRecrawlPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerRecrawlPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4b1b39d12a7f369b0d512e3def73e37d3dc19d012846127a0a68c782a794aa5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRecrawlBehavior")
    def reset_recrawl_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecrawlBehavior", []))

    @builtins.property
    @jsii.member(jsii_name="recrawlBehaviorInput")
    def recrawl_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recrawlBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="recrawlBehavior")
    def recrawl_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recrawlBehavior"))

    @recrawl_behavior.setter
    def recrawl_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31ecf991041f17ce4cfe802720759b2364d2f019a4bda1d7da1f808b78627faa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recrawlBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueCrawlerRecrawlPolicy]:
        return typing.cast(typing.Optional[GlueCrawlerRecrawlPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GlueCrawlerRecrawlPolicy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d24654141ae4e508e3b1fc6ec4458f60b52486d34b2a113e792681e449f8584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerS3Target",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "connection_name": "connectionName",
        "dlq_event_queue_arn": "dlqEventQueueArn",
        "event_queue_arn": "eventQueueArn",
        "exclusions": "exclusions",
        "sample_size": "sampleSize",
    },
)
class GlueCrawlerS3Target:
    def __init__(
        self,
        *,
        path: builtins.str,
        connection_name: typing.Optional[builtins.str] = None,
        dlq_event_queue_arn: typing.Optional[builtins.str] = None,
        event_queue_arn: typing.Optional[builtins.str] = None,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
        sample_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#path GlueCrawler#path}.
        :param connection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.
        :param dlq_event_queue_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#dlq_event_queue_arn GlueCrawler#dlq_event_queue_arn}.
        :param event_queue_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#event_queue_arn GlueCrawler#event_queue_arn}.
        :param exclusions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#exclusions GlueCrawler#exclusions}.
        :param sample_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#sample_size GlueCrawler#sample_size}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__196a191506f20ed408b8180693a74eb5323312a66a9617fd405b3394c4dbe208)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument dlq_event_queue_arn", value=dlq_event_queue_arn, expected_type=type_hints["dlq_event_queue_arn"])
            check_type(argname="argument event_queue_arn", value=event_queue_arn, expected_type=type_hints["event_queue_arn"])
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
            check_type(argname="argument sample_size", value=sample_size, expected_type=type_hints["sample_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if connection_name is not None:
            self._values["connection_name"] = connection_name
        if dlq_event_queue_arn is not None:
            self._values["dlq_event_queue_arn"] = dlq_event_queue_arn
        if event_queue_arn is not None:
            self._values["event_queue_arn"] = event_queue_arn
        if exclusions is not None:
            self._values["exclusions"] = exclusions
        if sample_size is not None:
            self._values["sample_size"] = sample_size

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#path GlueCrawler#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connection_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.'''
        result = self._values.get("connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dlq_event_queue_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#dlq_event_queue_arn GlueCrawler#dlq_event_queue_arn}.'''
        result = self._values.get("dlq_event_queue_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_queue_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#event_queue_arn GlueCrawler#event_queue_arn}.'''
        result = self._values.get("event_queue_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#exclusions GlueCrawler#exclusions}.'''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sample_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#sample_size GlueCrawler#sample_size}.'''
        result = self._values.get("sample_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerS3Target(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerS3TargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerS3TargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1965f2b7ad29fa25d50aabbacbd00341bfe08c92b76437a5fd285ed3c6cdb3b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GlueCrawlerS3TargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a05c3cc0c29a19d515fc64b14b4fd9d0e6c446fb85a39057938112c4ed3056fb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GlueCrawlerS3TargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a511187e32849cd5007bc0dabe9ae692be061c6339002bc0a9f121f98664cec7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__305120ce3578a50292d64039bf0d922c5ce2205085ed47a531341f967f2dff39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__324298780606919c51a2251799c6999e26f6a9128eb2a5560534bc35df0eacfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerS3Target]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerS3Target]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerS3Target]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1893934e8b4e560f19a687e32fb75623185e94b835463029f745acc15a8b8b2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GlueCrawlerS3TargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerS3TargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c82b77220cdd794a548d3c3622ebbf8987841b61cd41c403be8d5425bae21d30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConnectionName")
    def reset_connection_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionName", []))

    @jsii.member(jsii_name="resetDlqEventQueueArn")
    def reset_dlq_event_queue_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDlqEventQueueArn", []))

    @jsii.member(jsii_name="resetEventQueueArn")
    def reset_event_queue_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventQueueArn", []))

    @jsii.member(jsii_name="resetExclusions")
    def reset_exclusions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusions", []))

    @jsii.member(jsii_name="resetSampleSize")
    def reset_sample_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSampleSize", []))

    @builtins.property
    @jsii.member(jsii_name="connectionNameInput")
    def connection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dlqEventQueueArnInput")
    def dlq_event_queue_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dlqEventQueueArnInput"))

    @builtins.property
    @jsii.member(jsii_name="eventQueueArnInput")
    def event_queue_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventQueueArnInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionsInput")
    def exclusions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exclusionsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleSizeInput")
    def sample_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sampleSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @connection_name.setter
    def connection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e0da1cde4e2a6af097919ffb7abc4f8ca941c2c20d6ef4ce0654e2b4a5e2143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dlqEventQueueArn")
    def dlq_event_queue_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dlqEventQueueArn"))

    @dlq_event_queue_arn.setter
    def dlq_event_queue_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5214a81de32a450ee346422410e3f210150fc54e754b43b40e4fd6398677087a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dlqEventQueueArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventQueueArn")
    def event_queue_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventQueueArn"))

    @event_queue_arn.setter
    def event_queue_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7992dc12be305c2e89a90f64df73b19f321219d7b6c1f7a5f766f6a9dfb68404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventQueueArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusions")
    def exclusions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclusions"))

    @exclusions.setter
    def exclusions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec57224ee11971778036b848707afaa4123cff7f31d98c09080ceb63484d82c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd5f75502c46b8f5e613a23e6036601402072613a225a7590bab8d6c1ab5334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleSize")
    def sample_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleSize"))

    @sample_size.setter
    def sample_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df618cd3b7b9dcf60ccc63b103c6ef25b4ff2542080425ada8b0267b16855aeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerS3Target]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerS3Target]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerS3Target]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b4415c5b24993ce231d927ebf39bec6a05f7b038bd268ac7116c3463e44ce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerSchemaChangePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "delete_behavior": "deleteBehavior",
        "update_behavior": "updateBehavior",
    },
)
class GlueCrawlerSchemaChangePolicy:
    def __init__(
        self,
        *,
        delete_behavior: typing.Optional[builtins.str] = None,
        update_behavior: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delete_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#delete_behavior GlueCrawler#delete_behavior}.
        :param update_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#update_behavior GlueCrawler#update_behavior}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e85371961a9fc8f1e92c0f4679ff94b6ebf7d3088359ef71572268d6d1abe12)
            check_type(argname="argument delete_behavior", value=delete_behavior, expected_type=type_hints["delete_behavior"])
            check_type(argname="argument update_behavior", value=update_behavior, expected_type=type_hints["update_behavior"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delete_behavior is not None:
            self._values["delete_behavior"] = delete_behavior
        if update_behavior is not None:
            self._values["update_behavior"] = update_behavior

    @builtins.property
    def delete_behavior(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#delete_behavior GlueCrawler#delete_behavior}.'''
        result = self._values.get("delete_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update_behavior(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/glue_crawler#update_behavior GlueCrawler#update_behavior}.'''
        result = self._values.get("update_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerSchemaChangePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerSchemaChangePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.glueCrawler.GlueCrawlerSchemaChangePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2840bf30cedf3f7a229c8383531e56ca4e8cc9fac8e3582753cc2c22af762fa5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDeleteBehavior")
    def reset_delete_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteBehavior", []))

    @jsii.member(jsii_name="resetUpdateBehavior")
    def reset_update_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdateBehavior", []))

    @builtins.property
    @jsii.member(jsii_name="deleteBehaviorInput")
    def delete_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="updateBehaviorInput")
    def update_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteBehavior")
    def delete_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteBehavior"))

    @delete_behavior.setter
    def delete_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc6627396539229bf4e4b0c84b0c8fa21edfc25f8d9937be6135fa23fd9c00c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updateBehavior")
    def update_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateBehavior"))

    @update_behavior.setter
    def update_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19129165c45076014468276aa9d7c6263b35933e5bbfdaee91b852383b59cb80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueCrawlerSchemaChangePolicy]:
        return typing.cast(typing.Optional[GlueCrawlerSchemaChangePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GlueCrawlerSchemaChangePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e79da672cf026cbe43b3307a3a6796489654c3caae0aeae8db3a06c76b92b4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GlueCrawler",
    "GlueCrawlerCatalogTarget",
    "GlueCrawlerCatalogTargetList",
    "GlueCrawlerCatalogTargetOutputReference",
    "GlueCrawlerConfig",
    "GlueCrawlerDeltaTarget",
    "GlueCrawlerDeltaTargetList",
    "GlueCrawlerDeltaTargetOutputReference",
    "GlueCrawlerDynamodbTarget",
    "GlueCrawlerDynamodbTargetList",
    "GlueCrawlerDynamodbTargetOutputReference",
    "GlueCrawlerHudiTarget",
    "GlueCrawlerHudiTargetList",
    "GlueCrawlerHudiTargetOutputReference",
    "GlueCrawlerIcebergTarget",
    "GlueCrawlerIcebergTargetList",
    "GlueCrawlerIcebergTargetOutputReference",
    "GlueCrawlerJdbcTarget",
    "GlueCrawlerJdbcTargetList",
    "GlueCrawlerJdbcTargetOutputReference",
    "GlueCrawlerLakeFormationConfiguration",
    "GlueCrawlerLakeFormationConfigurationOutputReference",
    "GlueCrawlerLineageConfiguration",
    "GlueCrawlerLineageConfigurationOutputReference",
    "GlueCrawlerMongodbTarget",
    "GlueCrawlerMongodbTargetList",
    "GlueCrawlerMongodbTargetOutputReference",
    "GlueCrawlerRecrawlPolicy",
    "GlueCrawlerRecrawlPolicyOutputReference",
    "GlueCrawlerS3Target",
    "GlueCrawlerS3TargetList",
    "GlueCrawlerS3TargetOutputReference",
    "GlueCrawlerSchemaChangePolicy",
    "GlueCrawlerSchemaChangePolicyOutputReference",
]

publication.publish()

def _typecheckingstub__9342e177a78396a7b848137db6443e1db1eb2a226eb6fe1faee18c9485ddf52a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database_name: builtins.str,
    name: builtins.str,
    role: builtins.str,
    catalog_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerCatalogTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    configuration: typing.Optional[builtins.str] = None,
    delta_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerDeltaTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    dynamodb_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerDynamodbTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hudi_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerHudiTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    iceberg_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerIcebergTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    jdbc_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerJdbcTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lake_formation_configuration: typing.Optional[typing.Union[GlueCrawlerLakeFormationConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    lineage_configuration: typing.Optional[typing.Union[GlueCrawlerLineageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    mongodb_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerMongodbTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    recrawl_policy: typing.Optional[typing.Union[GlueCrawlerRecrawlPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    s3_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerS3Target, typing.Dict[builtins.str, typing.Any]]]]] = None,
    schedule: typing.Optional[builtins.str] = None,
    schema_change_policy: typing.Optional[typing.Union[GlueCrawlerSchemaChangePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    security_configuration: typing.Optional[builtins.str] = None,
    table_prefix: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__843c03e084cfff4cb7010269fd3b18bd6d2e18b451c83bc239a5f4664c0b6a94(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e35ea1e7a62dab3a0fa78084f4179320473349d73e5f6e1da0dc8f4e22ec21(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerCatalogTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b921de2a18091d891c30fe8fc28de1107efa726b0fcf67ebf1fbdf8c218c5ee0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerDeltaTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d597ae5ced4f6a5aa1899d0986926ac6158a7d3bfec9f8fe47291acb0b1666b9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerDynamodbTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e931238953c83be390bca1f370319edc42ddbda53962daaf30653b9824e402f3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerHudiTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626299f69cd643d0a0b39a9d823e614685542e47a4f63e419f90a4aee698e083(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerIcebergTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8607e964faaf25843223ade1468e1f2d7f94aca4ab41643acbf1f2d07822962(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerJdbcTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4627c7953694e8289aa9c567604dca9e7bc9dc38d90fba814b3010ef04a67604(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerMongodbTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d358cb176ea11745d81429f7690a95e0edc60a3a89e91df9eaf353c61b9d36e2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerS3Target, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f1cde679930ebfc64ea847b09f9423bff9e3e5a16fdb64c3d1137e13dfeb970(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4872a4b8d15330badec53d7fccd19f911acc088f581a940ea63599df1bd2f34a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09f10e91f9bf8a15bc800fa50ddac2995e1a6896ce7ed97e2e68a10afc49c7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8e1b5803b587057a927ad56fd1237153ef2bb420b511255643c0cbe4e4d8a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53dbb5e1d80a9440dba144aa4391c67b615c96ba5537738919426203a30cb979(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b86930fa88f2fdb4ec8224bdcc523fdf39b73759600f3d9d75b257738587b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a13bfa32b6c33d84017eefd19f7d97cde52270a3caa7d62237d6fdfb795c2808(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b96afd618317b9204ea2cc8fc1554ba569002149bf895cb438fdce6f1e2202(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59dbf75748872a604c64c479be4e2cc659d1f8ed4bcbe2d8d10789ad8ca2278e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88348629df01d984a206a26a4b3c82aaa4a84d87fd70158aec7778cdca6b949(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1b7d5a5c3799ccc794f42b1b19d96b3f345efd6aa19892b00ca64fd88ea055(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687196ab3514bb5c6eaa4a28fc892e2a399ced1a1ad2986119819fa1c03f2029(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f802ab49447ab6bdc32f9667239e3da8b9ff8c5bf12fd07ffbbaaa240156a33b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e18320e195d1e429d110039366eba3068a794d4e05763bc426083767d614e2f4(
    *,
    database_name: builtins.str,
    tables: typing.Sequence[builtins.str],
    connection_name: typing.Optional[builtins.str] = None,
    dlq_event_queue_arn: typing.Optional[builtins.str] = None,
    event_queue_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33412f84a65f1b6fc7f8c226b029f3ce68edef7b85d87e5b57a8dc4537a00f3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76beba61f0436f0423d9bc1b705ed31d0503add70842741ebcdce5787814bef3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c1d79f81263dd1fb7197402d84ee50af398ade773997551c3319cd5554f056(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f97c4fe973adb3abb04bf437b6f3ac3e567236663936b65044c0e5fc845d3a9a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897a43c8b6356b14f990f499d098b851b2b4d27d450d69ce8c7ec84f4b8db681(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d882f172d80679d08ef99ff12ead9a2ef88305ead06134d60dea1f57a802002(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerCatalogTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860260ad8dc8f5d451af06a5b30adec86d88c50bac159e0da23119e06b7bd8ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517d5457a6e169ff39193c93bb493a47a61b5fd8123630c947e364bfc04f3689(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a952d5aca77d68c8f7fed5428a6a23718140611b5cf8dd648b8a412b7f05a4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c2aaa116a5aac48b1f0fd55466d4ca5b876525a19bbd7fc089d6b88bbea857(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18836f545db1f9ee1c4d2861cd0d6478159aa852585237dda0e91329d700075a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded589d521c6a3823d50d83063f4a9fd0dac0a09ca00645e39812ae9ba0d8bb5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39161dab9eca223e01c0f16f0e9fbf48cea575f0fd085ee20d5bcf314d05f230(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerCatalogTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c16f8ab600ac86666d9e7bfc8576b6b7a636f7445b069196bdb9126361fdb0a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    database_name: builtins.str,
    name: builtins.str,
    role: builtins.str,
    catalog_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerCatalogTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    configuration: typing.Optional[builtins.str] = None,
    delta_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerDeltaTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    dynamodb_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerDynamodbTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hudi_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerHudiTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    iceberg_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerIcebergTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    jdbc_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerJdbcTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lake_formation_configuration: typing.Optional[typing.Union[GlueCrawlerLakeFormationConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    lineage_configuration: typing.Optional[typing.Union[GlueCrawlerLineageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    mongodb_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerMongodbTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    recrawl_policy: typing.Optional[typing.Union[GlueCrawlerRecrawlPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    s3_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerS3Target, typing.Dict[builtins.str, typing.Any]]]]] = None,
    schedule: typing.Optional[builtins.str] = None,
    schema_change_policy: typing.Optional[typing.Union[GlueCrawlerSchemaChangePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    security_configuration: typing.Optional[builtins.str] = None,
    table_prefix: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6abb7e8205f260da59e1fc1658f9ef55dc44e814d7c3962ce661697312bf912d(
    *,
    delta_tables: typing.Sequence[builtins.str],
    write_manifest: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    connection_name: typing.Optional[builtins.str] = None,
    create_native_delta_table: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd416b56c346042b18734f1467c6705f3fa17c66521bd114d14569403c4440d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c8e4382adb258e7c43bbe42570477e89aeb83b833bd5791266cd291cf7025f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__589615d3cf4780809e35a5dfecc484ee572bf69b2e7b00eefd813a7f8461eae3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44260ca4a812fcd7ba7bf456e82492a1eae6d44253b4628e568b428f98683cf8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b250a6cac4fb12711fad944a60608bb7e7b324f347f480121b015e4d8ead7b9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fbff3b3cc5808de9d4df17288d0defc16229b55bd241fb09329a5e802d83ed8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerDeltaTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a153bbb2d73cca354612e9e67a97250d3f73d9b5d1d0f44ab40cd40010b1041(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dba6218e6acb59298a4cabd1cb2aea8ce7deead75a13403a679101f9da329931(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94411a986a1b70d1b7ebebe2c818329148f0703767e830b546d8e29bb7ac3f42(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050a728b4555fe806bdeccb9811145f125bb2a01aefc1d591054f08834cf2e58(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4fa8d20d780d02cc1822d16228326a9aff89692b493ada209765a2ba2ce514(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81416e96988fdff91947852ad536bcb89746d35f095f20bc39e17231272b5671(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerDeltaTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1257288b62d7e36ff488452712ca6f1a192fee17e2c8d654d8560df7e09c860(
    *,
    path: builtins.str,
    scan_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scan_rate: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c72ab1c7651e738b5cef3b47bbcf765a14af23c79a936cdac4bc9b087da190(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82d51c8334902653cfe969db52b3fd23e0c11c498e2a652c88bc44d9054dd7b9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec696b28e599d82a65c77c81ae00117e1811e254fe2ad2b7d3b356eeb849089(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da742a3d7fcde47559f76a80ff4997576e2a44df07f07f15d1add4d7b621271(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b1e96a1d4a973d624cacfe4aba49754fd598b903257de79f14b7fe5d1b3682(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6ff18a10fa354912b3374eb69eccf83099f996eb161385dc43b8b66e292af3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerDynamodbTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6aed0e19e9c15de4e448c0a12c4e1722624ed52f2d00d2524fe1f304e410455(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e65a7dbfa2d63280480e1c7c8d481ab8873f75187cb3e2dd16bce4b1d8e4a613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f12040d1a8d70acc010ce7975834b9dc627bff284792ce712d1c7bdf7fa4aac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0b5f63bc66922b45b4fc34188f9d671fe41782d3436176bacb067a6729b2ae8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8401143ee11113f15fe4eacdee509dddfab70be1315f7f7b3b55cada9fcfa081(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerDynamodbTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e535794f4fe62e14310ac01d601213ef31d8d6f75259ff5a9c90c2a0d02e3873(
    *,
    maximum_traversal_depth: jsii.Number,
    paths: typing.Sequence[builtins.str],
    connection_name: typing.Optional[builtins.str] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f8aebbbf71670ad3eedc6c5e9bca410e5880dbac72461d6ea928d867d23623(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cefbb0d9ef03934dba47e303a92f637861c07170f9d7515141f2be70b0c840e6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574f6a96799a05da4f376d25a7ee20be1610c86e1814654dfc744a2d60764e71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76801b893f0b8c468d0ffc2d326d15c654a1c4ab090f69fd371fead83c9f5468(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ad821d69668c62e97856d47e6d7b7b69a11416290c1c73f7d147e0854676e5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__004ecac499692d7b8c1b71521c230a8af2f8553176b73f62632111f4bcaab583(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerHudiTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e8539344c04ae52ee54037acbbe190d70a1501018ad45ef65debafe89d9b05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcdc29dfc42d3cc8a9a84f0e4f82592fbd47d04a7cdaa30757c8215f4bc59577(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3151bcd31c3bd649c8e1f47333b678aaa47ec5788b447ec4c0334108be219ba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97bdbb61c5b606d4373cff278f9915acc72ffb17a13c488f99d42145bc891688(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f39b6f459aad8ef1ea3477896eb25055bd473fb94b5d585103ff755e15a734(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51076e5c7d8b596f4e3519cd49a8523f97f1bab3a489c7a47622e5f04839679c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerHudiTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a18cf01f5e2978aa667b22c9bc2ed9f136e124db1b5305ef67bf1389d4e325(
    *,
    maximum_traversal_depth: jsii.Number,
    paths: typing.Sequence[builtins.str],
    connection_name: typing.Optional[builtins.str] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b295e0ecdeb563346849ef8326e95d7e36b820f622ec0c5436f36b5a12a9884(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34948b364c04aa652db84c595301d6247b4867d9c9c209ad2b502befca8a60f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd47fecdf18c15328be00ca06bd08e14bb98dc178afac3c0ddaf09af18f704a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4712aca835fa25ab8515a63b398c52099ef11747137a14240bfe1929f2b7fd43(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cdbda0223882642a020da5d79072ae5e9f749fed222ee0e4b75b960bde7b18a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8137fad03d8a0cc6c9acf0551442f616e667846f6a548dfcae02abd0e888bad0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerIcebergTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef1992c65bde8d1590024221b11ba44a63073c5bfd6a705bd1b5f3956b236c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e583eb5e30cb6d773d4c9cec9acc798426c704b29441b5cdf3e020cb5aacc90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88f6afdfc8342e7d7262934a54f531103496eb732e3ec911ab2614621ce32ab(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1725ecfd4697ff2b3730572cce87e2b99472ef00754875d16376d35c03bd8049(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81ed337e42563e80522e2823e07dafa38140e6fc4ff1d67c7fc6a28841ba36b8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f69fb5b5cf3e30b0d2626ff7a727c41ad5dbb1d8a2d5398f180b673371c299(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerIcebergTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc26fa41ea360e5535776041ff2c01f56b1a10c40b3f3ae677b7bd5089cb4f4(
    *,
    connection_name: builtins.str,
    path: builtins.str,
    enable_additional_metadata: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839e465b236137f3859e9d935653ea71e62aeb0ea82a1840028b28086a905cb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb2525f45e33940df56fce74016f2f2b9974ec26ebaf223ce800b4c7c4323b7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c03311d75ff03fdec281f2586247613207ad32b343c124873497c847d8232f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b9c6efe11a65118b95646e5ba5852e9acce37dbe133e6c2bd923838cd0f1fd0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2849f09f4d675dae3674a5172f32176b990e563dd34b85dd5c666f10910060(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1832a421af38f42fd38e34a746534431df931f53cb70912dfbe0ec7a12481f59(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerJdbcTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd405bbe462f7f546e18fc0768c1df602790128bed18d3889e9848a42ad8fb44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad57b9c8268ddbaa8d8f919de1ed4f51437b0800954ae994ca7f6a0514b481d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f646f6d2fdb1677ed706e2bdd4c662d062dc4fdbb8e83986ea8114be445dd98(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2245361f610e7411595b00b9c995d2f92b4e77b804ec7d8b1894d58def90059(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e53b8ba5c7315b339a569ecabf84a76d0da70038502c362e6ca248c103f6df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3ce186670dda4af2e36f62a2769bc1f90e46705ef839bb23e579494838e4be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerJdbcTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31bc026d64f479762934528b7ff44e4ea410775655abcc0f7a73e1a527d4ac4e(
    *,
    account_id: typing.Optional[builtins.str] = None,
    use_lake_formation_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b188925e8ef3c1c19c3b74037dbe5e2b450c368cdee3ff8b88c4b95e92958a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c33e1e92a57a30dec143aebe694bffeaf61f19d73d0eabd09cebd7fb6499869(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c78ff4525b7b0c98eff0c51a21a58379cc26c1e573b0478fc9379eded7886a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab03275921c23a03fc71bebeb0b487f50b546e97ce675f501d933010647d401(
    value: typing.Optional[GlueCrawlerLakeFormationConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd751a5a1d877c8030fff4b03ae0f7fda59f8d3e028089a7f40e3deed92a4c32(
    *,
    crawler_lineage_settings: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28654f664c9a793ff5f35528c1226bf19435c01245724eb85ee6e4ee8093bb5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9da95fa7ae14c0ade6fe190cf4236e38864c58a21d977b9bb8fe19cb45e6f6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6126283074b0247dd2fd367b814e0f684d8cb6cb8cad834bb884a9cdc8ceb3b3(
    value: typing.Optional[GlueCrawlerLineageConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185ed401fc9df1025023b569ba2a1c049f99f48d171bd227b4697940b8a85f26(
    *,
    connection_name: builtins.str,
    path: builtins.str,
    scan_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c122b0be88d885f3a29574e8f997140452dd29ee7ca96288f3df3e0e8b2ffa4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__571d2db244586b5d3bd57b887822de333bf21a622e0a575df29bb5d55da4024f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e6a57541b2702a23fbb636b40ad0531237cf376ab5acdfa140319854c80ed6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f71ce6a4580e44b1de807f551d15d0aae3effffe97df9be7dd843593d2e249e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c11894db9cc432f17dcec7a364293814165d7621cd71a4a352d878ae0a5d74(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d688e0de906e4b9e61ef189b6a4458a6928180d0b51bf26f6691116bca536a1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerMongodbTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de78a2e1532cdc995f8a61d0bd1ff3200c93e42a10347b9d1f4a7cac992a09ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5884f9475bd6120efcaa693f16279d5f99ed1d955aaa5065fba8cac9c7ca2cd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb847160b25f7651883ee8d8aa3fcb80005e4e062b03ab478279cecc33083c2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b708a2ec3309942e4359fbc09c660d6d64cafa923736adf98db4a53ebdabe9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3fa78b6469b5a124eddf1cdea34074ccc521a932da5b76f420edd08d6f4d59c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerMongodbTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7af532d479d23fb1690132481a86a42b4821edc89274a5b8d94b85e469b583(
    *,
    recrawl_behavior: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b1b39d12a7f369b0d512e3def73e37d3dc19d012846127a0a68c782a794aa5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ecf991041f17ce4cfe802720759b2364d2f019a4bda1d7da1f808b78627faa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d24654141ae4e508e3b1fc6ec4458f60b52486d34b2a113e792681e449f8584(
    value: typing.Optional[GlueCrawlerRecrawlPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__196a191506f20ed408b8180693a74eb5323312a66a9617fd405b3394c4dbe208(
    *,
    path: builtins.str,
    connection_name: typing.Optional[builtins.str] = None,
    dlq_event_queue_arn: typing.Optional[builtins.str] = None,
    event_queue_arn: typing.Optional[builtins.str] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    sample_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1965f2b7ad29fa25d50aabbacbd00341bfe08c92b76437a5fd285ed3c6cdb3b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a05c3cc0c29a19d515fc64b14b4fd9d0e6c446fb85a39057938112c4ed3056fb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a511187e32849cd5007bc0dabe9ae692be061c6339002bc0a9f121f98664cec7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305120ce3578a50292d64039bf0d922c5ce2205085ed47a531341f967f2dff39(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324298780606919c51a2251799c6999e26f6a9128eb2a5560534bc35df0eacfd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1893934e8b4e560f19a687e32fb75623185e94b835463029f745acc15a8b8b2e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerS3Target]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82b77220cdd794a548d3c3622ebbf8987841b61cd41c403be8d5425bae21d30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0da1cde4e2a6af097919ffb7abc4f8ca941c2c20d6ef4ce0654e2b4a5e2143(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5214a81de32a450ee346422410e3f210150fc54e754b43b40e4fd6398677087a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7992dc12be305c2e89a90f64df73b19f321219d7b6c1f7a5f766f6a9dfb68404(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec57224ee11971778036b848707afaa4123cff7f31d98c09080ceb63484d82c5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd5f75502c46b8f5e613a23e6036601402072613a225a7590bab8d6c1ab5334(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df618cd3b7b9dcf60ccc63b103c6ef25b4ff2542080425ada8b0267b16855aeb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b4415c5b24993ce231d927ebf39bec6a05f7b038bd268ac7116c3463e44ce6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerS3Target]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e85371961a9fc8f1e92c0f4679ff94b6ebf7d3088359ef71572268d6d1abe12(
    *,
    delete_behavior: typing.Optional[builtins.str] = None,
    update_behavior: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2840bf30cedf3f7a229c8383531e56ca4e8cc9fac8e3582753cc2c22af762fa5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6627396539229bf4e4b0c84b0c8fa21edfc25f8d9937be6135fa23fd9c00c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19129165c45076014468276aa9d7c6263b35933e5bbfdaee91b852383b59cb80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e79da672cf026cbe43b3307a3a6796489654c3caae0aeae8db3a06c76b92b4d(
    value: typing.Optional[GlueCrawlerSchemaChangePolicy],
) -> None:
    """Type checking stubs"""
    pass
