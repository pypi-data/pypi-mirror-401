r'''
# `aws_quicksight_data_source`

Refer to the Terraform Registry for docs: [`aws_quicksight_data_source`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source).
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


class QuicksightDataSource(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSource",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source aws_quicksight_data_source}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_source_id: builtins.str,
        name: builtins.str,
        parameters: typing.Union["QuicksightDataSourceParameters", typing.Dict[builtins.str, typing.Any]],
        type: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[typing.Union["QuicksightDataSourceCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        permission: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSourcePermission", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        ssl_properties: typing.Optional[typing.Union["QuicksightDataSourceSslProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc_connection_properties: typing.Optional[typing.Union["QuicksightDataSourceVpcConnectionProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source aws_quicksight_data_source} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_source_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#data_source_id QuicksightDataSource#data_source_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#name QuicksightDataSource#name}.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#parameters QuicksightDataSource#parameters}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#type QuicksightDataSource#type}.
        :param aws_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#aws_account_id QuicksightDataSource#aws_account_id}.
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#credentials QuicksightDataSource#credentials}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#id QuicksightDataSource#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param permission: permission block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#permission QuicksightDataSource#permission}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#region QuicksightDataSource#region}
        :param ssl_properties: ssl_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#ssl_properties QuicksightDataSource#ssl_properties}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#tags QuicksightDataSource#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#tags_all QuicksightDataSource#tags_all}.
        :param vpc_connection_properties: vpc_connection_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#vpc_connection_properties QuicksightDataSource#vpc_connection_properties}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f521bc07fa829c901e7c259eae9c0bc5f2ff42d697340485acf176dbf2099e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = QuicksightDataSourceConfig(
            data_source_id=data_source_id,
            name=name,
            parameters=parameters,
            type=type,
            aws_account_id=aws_account_id,
            credentials=credentials,
            id=id,
            permission=permission,
            region=region,
            ssl_properties=ssl_properties,
            tags=tags,
            tags_all=tags_all,
            vpc_connection_properties=vpc_connection_properties,
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
        '''Generates CDKTF code for importing a QuicksightDataSource resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the QuicksightDataSource to import.
        :param import_from_id: The id of the existing QuicksightDataSource that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the QuicksightDataSource to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__408dccce1bea53b4774cc09246bf71527051f28c322afa2def65eaa2b397db34)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCredentials")
    def put_credentials(
        self,
        *,
        copy_source_arn: typing.Optional[builtins.str] = None,
        credential_pair: typing.Optional[typing.Union["QuicksightDataSourceCredentialsCredentialPair", typing.Dict[builtins.str, typing.Any]]] = None,
        secret_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param copy_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#copy_source_arn QuicksightDataSource#copy_source_arn}.
        :param credential_pair: credential_pair block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#credential_pair QuicksightDataSource#credential_pair}
        :param secret_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#secret_arn QuicksightDataSource#secret_arn}.
        '''
        value = QuicksightDataSourceCredentials(
            copy_source_arn=copy_source_arn,
            credential_pair=credential_pair,
            secret_arn=secret_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putCredentials", [value]))

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        *,
        amazon_elasticsearch: typing.Optional[typing.Union["QuicksightDataSourceParametersAmazonElasticsearch", typing.Dict[builtins.str, typing.Any]]] = None,
        athena: typing.Optional[typing.Union["QuicksightDataSourceParametersAthena", typing.Dict[builtins.str, typing.Any]]] = None,
        aurora: typing.Optional[typing.Union["QuicksightDataSourceParametersAurora", typing.Dict[builtins.str, typing.Any]]] = None,
        aurora_postgresql: typing.Optional[typing.Union["QuicksightDataSourceParametersAuroraPostgresql", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_iot_analytics: typing.Optional[typing.Union["QuicksightDataSourceParametersAwsIotAnalytics", typing.Dict[builtins.str, typing.Any]]] = None,
        databricks: typing.Optional[typing.Union["QuicksightDataSourceParametersDatabricks", typing.Dict[builtins.str, typing.Any]]] = None,
        jira: typing.Optional[typing.Union["QuicksightDataSourceParametersJira", typing.Dict[builtins.str, typing.Any]]] = None,
        maria_db: typing.Optional[typing.Union["QuicksightDataSourceParametersMariaDb", typing.Dict[builtins.str, typing.Any]]] = None,
        mysql: typing.Optional[typing.Union["QuicksightDataSourceParametersMysql", typing.Dict[builtins.str, typing.Any]]] = None,
        oracle: typing.Optional[typing.Union["QuicksightDataSourceParametersOracle", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql: typing.Optional[typing.Union["QuicksightDataSourceParametersPostgresql", typing.Dict[builtins.str, typing.Any]]] = None,
        presto: typing.Optional[typing.Union["QuicksightDataSourceParametersPresto", typing.Dict[builtins.str, typing.Any]]] = None,
        rds: typing.Optional[typing.Union["QuicksightDataSourceParametersRds", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift: typing.Optional[typing.Union["QuicksightDataSourceParametersRedshift", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["QuicksightDataSourceParametersS3", typing.Dict[builtins.str, typing.Any]]] = None,
        service_now: typing.Optional[typing.Union["QuicksightDataSourceParametersServiceNow", typing.Dict[builtins.str, typing.Any]]] = None,
        snowflake: typing.Optional[typing.Union["QuicksightDataSourceParametersSnowflake", typing.Dict[builtins.str, typing.Any]]] = None,
        spark: typing.Optional[typing.Union["QuicksightDataSourceParametersSpark", typing.Dict[builtins.str, typing.Any]]] = None,
        sql_server: typing.Optional[typing.Union["QuicksightDataSourceParametersSqlServer", typing.Dict[builtins.str, typing.Any]]] = None,
        teradata: typing.Optional[typing.Union["QuicksightDataSourceParametersTeradata", typing.Dict[builtins.str, typing.Any]]] = None,
        twitter: typing.Optional[typing.Union["QuicksightDataSourceParametersTwitter", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param amazon_elasticsearch: amazon_elasticsearch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#amazon_elasticsearch QuicksightDataSource#amazon_elasticsearch}
        :param athena: athena block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#athena QuicksightDataSource#athena}
        :param aurora: aurora block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#aurora QuicksightDataSource#aurora}
        :param aurora_postgresql: aurora_postgresql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#aurora_postgresql QuicksightDataSource#aurora_postgresql}
        :param aws_iot_analytics: aws_iot_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#aws_iot_analytics QuicksightDataSource#aws_iot_analytics}
        :param databricks: databricks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#databricks QuicksightDataSource#databricks}
        :param jira: jira block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#jira QuicksightDataSource#jira}
        :param maria_db: maria_db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#maria_db QuicksightDataSource#maria_db}
        :param mysql: mysql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#mysql QuicksightDataSource#mysql}
        :param oracle: oracle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#oracle QuicksightDataSource#oracle}
        :param postgresql: postgresql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#postgresql QuicksightDataSource#postgresql}
        :param presto: presto block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#presto QuicksightDataSource#presto}
        :param rds: rds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#rds QuicksightDataSource#rds}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#redshift QuicksightDataSource#redshift}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#s3 QuicksightDataSource#s3}
        :param service_now: service_now block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#service_now QuicksightDataSource#service_now}
        :param snowflake: snowflake block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#snowflake QuicksightDataSource#snowflake}
        :param spark: spark block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#spark QuicksightDataSource#spark}
        :param sql_server: sql_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#sql_server QuicksightDataSource#sql_server}
        :param teradata: teradata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#teradata QuicksightDataSource#teradata}
        :param twitter: twitter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#twitter QuicksightDataSource#twitter}
        '''
        value = QuicksightDataSourceParameters(
            amazon_elasticsearch=amazon_elasticsearch,
            athena=athena,
            aurora=aurora,
            aurora_postgresql=aurora_postgresql,
            aws_iot_analytics=aws_iot_analytics,
            databricks=databricks,
            jira=jira,
            maria_db=maria_db,
            mysql=mysql,
            oracle=oracle,
            postgresql=postgresql,
            presto=presto,
            rds=rds,
            redshift=redshift,
            s3=s3,
            service_now=service_now,
            snowflake=snowflake,
            spark=spark,
            sql_server=sql_server,
            teradata=teradata,
            twitter=twitter,
        )

        return typing.cast(None, jsii.invoke(self, "putParameters", [value]))

    @jsii.member(jsii_name="putPermission")
    def put_permission(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSourcePermission", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba7ea09652a0486acb873d7c8b0b9fddfd284bdeb1e90ff2614703e89d2848e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPermission", [value]))

    @jsii.member(jsii_name="putSslProperties")
    def put_ssl_properties(
        self,
        *,
        disable_ssl: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param disable_ssl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#disable_ssl QuicksightDataSource#disable_ssl}.
        '''
        value = QuicksightDataSourceSslProperties(disable_ssl=disable_ssl)

        return typing.cast(None, jsii.invoke(self, "putSslProperties", [value]))

    @jsii.member(jsii_name="putVpcConnectionProperties")
    def put_vpc_connection_properties(
        self,
        *,
        vpc_connection_arn: builtins.str,
    ) -> None:
        '''
        :param vpc_connection_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#vpc_connection_arn QuicksightDataSource#vpc_connection_arn}.
        '''
        value = QuicksightDataSourceVpcConnectionProperties(
            vpc_connection_arn=vpc_connection_arn
        )

        return typing.cast(None, jsii.invoke(self, "putVpcConnectionProperties", [value]))

    @jsii.member(jsii_name="resetAwsAccountId")
    def reset_aws_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAccountId", []))

    @jsii.member(jsii_name="resetCredentials")
    def reset_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentials", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPermission")
    def reset_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermission", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSslProperties")
    def reset_ssl_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslProperties", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetVpcConnectionProperties")
    def reset_vpc_connection_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcConnectionProperties", []))

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
    @jsii.member(jsii_name="credentials")
    def credentials(self) -> "QuicksightDataSourceCredentialsOutputReference":
        return typing.cast("QuicksightDataSourceCredentialsOutputReference", jsii.get(self, "credentials"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "QuicksightDataSourceParametersOutputReference":
        return typing.cast("QuicksightDataSourceParametersOutputReference", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> "QuicksightDataSourcePermissionList":
        return typing.cast("QuicksightDataSourcePermissionList", jsii.get(self, "permission"))

    @builtins.property
    @jsii.member(jsii_name="sslProperties")
    def ssl_properties(self) -> "QuicksightDataSourceSslPropertiesOutputReference":
        return typing.cast("QuicksightDataSourceSslPropertiesOutputReference", jsii.get(self, "sslProperties"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectionProperties")
    def vpc_connection_properties(
        self,
    ) -> "QuicksightDataSourceVpcConnectionPropertiesOutputReference":
        return typing.cast("QuicksightDataSourceVpcConnectionPropertiesOutputReference", jsii.get(self, "vpcConnectionProperties"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountIdInput")
    def aws_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(self) -> typing.Optional["QuicksightDataSourceCredentials"]:
        return typing.cast(typing.Optional["QuicksightDataSourceCredentials"], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceIdInput")
    def data_source_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(self) -> typing.Optional["QuicksightDataSourceParameters"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParameters"], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionInput")
    def permission_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSourcePermission"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSourcePermission"]]], jsii.get(self, "permissionInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="sslPropertiesInput")
    def ssl_properties_input(
        self,
    ) -> typing.Optional["QuicksightDataSourceSslProperties"]:
        return typing.cast(typing.Optional["QuicksightDataSourceSslProperties"], jsii.get(self, "sslPropertiesInput"))

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
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectionPropertiesInput")
    def vpc_connection_properties_input(
        self,
    ) -> typing.Optional["QuicksightDataSourceVpcConnectionProperties"]:
        return typing.cast(typing.Optional["QuicksightDataSourceVpcConnectionProperties"], jsii.get(self, "vpcConnectionPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @aws_account_id.setter
    def aws_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2916473405841ba70b3b1f14a52400b49570f7fd8fc33585a940cb55cf9bc02b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @data_source_id.setter
    def data_source_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a516abd158f8ea291013a0b7fbd247322a9a855ecd256325b2e2956ff5c459f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec9ad5f04327592fe6c5d9cfba051d3f76bb4a19153ef7d6606f335afbce8c41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c48b0bac5c0973ada5c09beafc86d6907857015261bffe13f762bbc9c20fd8ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5bac60893f0844b3c55429baa67300914fa11144929c8085fe862eec8cf49cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35426145e150c1a415a37a4115cd536b65c93c03842a0d698157f16fc3685432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d585b84b4899b7a959dd9d17c060aca1577309aea189ea1958d3f5e8194b2c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2bc4ba7ba524f30bc5fb619ef646769c07f1280ed315aa898af1e8e3db52227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_source_id": "dataSourceId",
        "name": "name",
        "parameters": "parameters",
        "type": "type",
        "aws_account_id": "awsAccountId",
        "credentials": "credentials",
        "id": "id",
        "permission": "permission",
        "region": "region",
        "ssl_properties": "sslProperties",
        "tags": "tags",
        "tags_all": "tagsAll",
        "vpc_connection_properties": "vpcConnectionProperties",
    },
)
class QuicksightDataSourceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        data_source_id: builtins.str,
        name: builtins.str,
        parameters: typing.Union["QuicksightDataSourceParameters", typing.Dict[builtins.str, typing.Any]],
        type: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[typing.Union["QuicksightDataSourceCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        permission: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSourcePermission", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        ssl_properties: typing.Optional[typing.Union["QuicksightDataSourceSslProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc_connection_properties: typing.Optional[typing.Union["QuicksightDataSourceVpcConnectionProperties", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_source_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#data_source_id QuicksightDataSource#data_source_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#name QuicksightDataSource#name}.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#parameters QuicksightDataSource#parameters}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#type QuicksightDataSource#type}.
        :param aws_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#aws_account_id QuicksightDataSource#aws_account_id}.
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#credentials QuicksightDataSource#credentials}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#id QuicksightDataSource#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param permission: permission block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#permission QuicksightDataSource#permission}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#region QuicksightDataSource#region}
        :param ssl_properties: ssl_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#ssl_properties QuicksightDataSource#ssl_properties}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#tags QuicksightDataSource#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#tags_all QuicksightDataSource#tags_all}.
        :param vpc_connection_properties: vpc_connection_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#vpc_connection_properties QuicksightDataSource#vpc_connection_properties}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(parameters, dict):
            parameters = QuicksightDataSourceParameters(**parameters)
        if isinstance(credentials, dict):
            credentials = QuicksightDataSourceCredentials(**credentials)
        if isinstance(ssl_properties, dict):
            ssl_properties = QuicksightDataSourceSslProperties(**ssl_properties)
        if isinstance(vpc_connection_properties, dict):
            vpc_connection_properties = QuicksightDataSourceVpcConnectionProperties(**vpc_connection_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b5e65d223b9f62b5aba18f661ee6a8e177d1db3ff5d7b3c20000625123ba15)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_source_id", value=data_source_id, expected_type=type_hints["data_source_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument ssl_properties", value=ssl_properties, expected_type=type_hints["ssl_properties"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument vpc_connection_properties", value=vpc_connection_properties, expected_type=type_hints["vpc_connection_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_source_id": data_source_id,
            "name": name,
            "parameters": parameters,
            "type": type,
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
        if aws_account_id is not None:
            self._values["aws_account_id"] = aws_account_id
        if credentials is not None:
            self._values["credentials"] = credentials
        if id is not None:
            self._values["id"] = id
        if permission is not None:
            self._values["permission"] = permission
        if region is not None:
            self._values["region"] = region
        if ssl_properties is not None:
            self._values["ssl_properties"] = ssl_properties
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if vpc_connection_properties is not None:
            self._values["vpc_connection_properties"] = vpc_connection_properties

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
    def data_source_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#data_source_id QuicksightDataSource#data_source_id}.'''
        result = self._values.get("data_source_id")
        assert result is not None, "Required property 'data_source_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#name QuicksightDataSource#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> "QuicksightDataSourceParameters":
        '''parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#parameters QuicksightDataSource#parameters}
        '''
        result = self._values.get("parameters")
        assert result is not None, "Required property 'parameters' is missing"
        return typing.cast("QuicksightDataSourceParameters", result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#type QuicksightDataSource#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#aws_account_id QuicksightDataSource#aws_account_id}.'''
        result = self._values.get("aws_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credentials(self) -> typing.Optional["QuicksightDataSourceCredentials"]:
        '''credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#credentials QuicksightDataSource#credentials}
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional["QuicksightDataSourceCredentials"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#id QuicksightDataSource#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSourcePermission"]]]:
        '''permission block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#permission QuicksightDataSource#permission}
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSourcePermission"]]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#region QuicksightDataSource#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_properties(self) -> typing.Optional["QuicksightDataSourceSslProperties"]:
        '''ssl_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#ssl_properties QuicksightDataSource#ssl_properties}
        '''
        result = self._values.get("ssl_properties")
        return typing.cast(typing.Optional["QuicksightDataSourceSslProperties"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#tags QuicksightDataSource#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#tags_all QuicksightDataSource#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vpc_connection_properties(
        self,
    ) -> typing.Optional["QuicksightDataSourceVpcConnectionProperties"]:
        '''vpc_connection_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#vpc_connection_properties QuicksightDataSource#vpc_connection_properties}
        '''
        result = self._values.get("vpc_connection_properties")
        return typing.cast(typing.Optional["QuicksightDataSourceVpcConnectionProperties"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "copy_source_arn": "copySourceArn",
        "credential_pair": "credentialPair",
        "secret_arn": "secretArn",
    },
)
class QuicksightDataSourceCredentials:
    def __init__(
        self,
        *,
        copy_source_arn: typing.Optional[builtins.str] = None,
        credential_pair: typing.Optional[typing.Union["QuicksightDataSourceCredentialsCredentialPair", typing.Dict[builtins.str, typing.Any]]] = None,
        secret_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param copy_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#copy_source_arn QuicksightDataSource#copy_source_arn}.
        :param credential_pair: credential_pair block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#credential_pair QuicksightDataSource#credential_pair}
        :param secret_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#secret_arn QuicksightDataSource#secret_arn}.
        '''
        if isinstance(credential_pair, dict):
            credential_pair = QuicksightDataSourceCredentialsCredentialPair(**credential_pair)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fdda683b4c66e6c67769671cd0821304896378bd29d76512782ab3286d179af)
            check_type(argname="argument copy_source_arn", value=copy_source_arn, expected_type=type_hints["copy_source_arn"])
            check_type(argname="argument credential_pair", value=credential_pair, expected_type=type_hints["credential_pair"])
            check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if copy_source_arn is not None:
            self._values["copy_source_arn"] = copy_source_arn
        if credential_pair is not None:
            self._values["credential_pair"] = credential_pair
        if secret_arn is not None:
            self._values["secret_arn"] = secret_arn

    @builtins.property
    def copy_source_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#copy_source_arn QuicksightDataSource#copy_source_arn}.'''
        result = self._values.get("copy_source_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credential_pair(
        self,
    ) -> typing.Optional["QuicksightDataSourceCredentialsCredentialPair"]:
        '''credential_pair block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#credential_pair QuicksightDataSource#credential_pair}
        '''
        result = self._values.get("credential_pair")
        return typing.cast(typing.Optional["QuicksightDataSourceCredentialsCredentialPair"], result)

    @builtins.property
    def secret_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#secret_arn QuicksightDataSource#secret_arn}.'''
        result = self._values.get("secret_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceCredentialsCredentialPair",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class QuicksightDataSourceCredentialsCredentialPair:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#password QuicksightDataSource#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#username QuicksightDataSource#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__655544d0fc3f46aa970f1c05d056414d75519ca6d1e12717d0f5cb7e6fa33b18)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#password QuicksightDataSource#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#username QuicksightDataSource#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceCredentialsCredentialPair(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceCredentialsCredentialPairOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceCredentialsCredentialPairOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84ff810aac227c9f6c13f30a934651d5eb64fcf21d82deb82aecb866236cace4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25ece8015f483c0fd0108901f83fe0cbbd6f9a7714f3c8423bd2092048a9445f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26e7e858542fb9a85cce7af109173acc3bb7049f2c2b0c6cb3e1b804cba6d5d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceCredentialsCredentialPair]:
        return typing.cast(typing.Optional[QuicksightDataSourceCredentialsCredentialPair], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceCredentialsCredentialPair],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae4e1398b4b8c5c1bcc281edf12bf9ed2e806364c42875d976e9e2e79c71478d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSourceCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f39de1b4f84809acac63c234315bcd4cd095f22190e3ffab778c44114fca6f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCredentialPair")
    def put_credential_pair(
        self,
        *,
        password: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#password QuicksightDataSource#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#username QuicksightDataSource#username}.
        '''
        value = QuicksightDataSourceCredentialsCredentialPair(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putCredentialPair", [value]))

    @jsii.member(jsii_name="resetCopySourceArn")
    def reset_copy_source_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopySourceArn", []))

    @jsii.member(jsii_name="resetCredentialPair")
    def reset_credential_pair(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentialPair", []))

    @jsii.member(jsii_name="resetSecretArn")
    def reset_secret_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretArn", []))

    @builtins.property
    @jsii.member(jsii_name="credentialPair")
    def credential_pair(
        self,
    ) -> QuicksightDataSourceCredentialsCredentialPairOutputReference:
        return typing.cast(QuicksightDataSourceCredentialsCredentialPairOutputReference, jsii.get(self, "credentialPair"))

    @builtins.property
    @jsii.member(jsii_name="copySourceArnInput")
    def copy_source_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "copySourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialPairInput")
    def credential_pair_input(
        self,
    ) -> typing.Optional[QuicksightDataSourceCredentialsCredentialPair]:
        return typing.cast(typing.Optional[QuicksightDataSourceCredentialsCredentialPair], jsii.get(self, "credentialPairInput"))

    @builtins.property
    @jsii.member(jsii_name="secretArnInput")
    def secret_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretArnInput"))

    @builtins.property
    @jsii.member(jsii_name="copySourceArn")
    def copy_source_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "copySourceArn"))

    @copy_source_arn.setter
    def copy_source_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cecf8239a5c5baf742c5965aefe0f3d2f677c4058e4cd68a713a3195102188c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copySourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretArn"))

    @secret_arn.setter
    def secret_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e3d3543d687d42f472eb50711fcc049eb121a59fe40d85505b5e7b2e58f0e92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceCredentials]:
        return typing.cast(typing.Optional[QuicksightDataSourceCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d68f942f3bb3858903f0195becb8cd647d696e099afbca763320e7aec094a0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParameters",
    jsii_struct_bases=[],
    name_mapping={
        "amazon_elasticsearch": "amazonElasticsearch",
        "athena": "athena",
        "aurora": "aurora",
        "aurora_postgresql": "auroraPostgresql",
        "aws_iot_analytics": "awsIotAnalytics",
        "databricks": "databricks",
        "jira": "jira",
        "maria_db": "mariaDb",
        "mysql": "mysql",
        "oracle": "oracle",
        "postgresql": "postgresql",
        "presto": "presto",
        "rds": "rds",
        "redshift": "redshift",
        "s3": "s3",
        "service_now": "serviceNow",
        "snowflake": "snowflake",
        "spark": "spark",
        "sql_server": "sqlServer",
        "teradata": "teradata",
        "twitter": "twitter",
    },
)
class QuicksightDataSourceParameters:
    def __init__(
        self,
        *,
        amazon_elasticsearch: typing.Optional[typing.Union["QuicksightDataSourceParametersAmazonElasticsearch", typing.Dict[builtins.str, typing.Any]]] = None,
        athena: typing.Optional[typing.Union["QuicksightDataSourceParametersAthena", typing.Dict[builtins.str, typing.Any]]] = None,
        aurora: typing.Optional[typing.Union["QuicksightDataSourceParametersAurora", typing.Dict[builtins.str, typing.Any]]] = None,
        aurora_postgresql: typing.Optional[typing.Union["QuicksightDataSourceParametersAuroraPostgresql", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_iot_analytics: typing.Optional[typing.Union["QuicksightDataSourceParametersAwsIotAnalytics", typing.Dict[builtins.str, typing.Any]]] = None,
        databricks: typing.Optional[typing.Union["QuicksightDataSourceParametersDatabricks", typing.Dict[builtins.str, typing.Any]]] = None,
        jira: typing.Optional[typing.Union["QuicksightDataSourceParametersJira", typing.Dict[builtins.str, typing.Any]]] = None,
        maria_db: typing.Optional[typing.Union["QuicksightDataSourceParametersMariaDb", typing.Dict[builtins.str, typing.Any]]] = None,
        mysql: typing.Optional[typing.Union["QuicksightDataSourceParametersMysql", typing.Dict[builtins.str, typing.Any]]] = None,
        oracle: typing.Optional[typing.Union["QuicksightDataSourceParametersOracle", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql: typing.Optional[typing.Union["QuicksightDataSourceParametersPostgresql", typing.Dict[builtins.str, typing.Any]]] = None,
        presto: typing.Optional[typing.Union["QuicksightDataSourceParametersPresto", typing.Dict[builtins.str, typing.Any]]] = None,
        rds: typing.Optional[typing.Union["QuicksightDataSourceParametersRds", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift: typing.Optional[typing.Union["QuicksightDataSourceParametersRedshift", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["QuicksightDataSourceParametersS3", typing.Dict[builtins.str, typing.Any]]] = None,
        service_now: typing.Optional[typing.Union["QuicksightDataSourceParametersServiceNow", typing.Dict[builtins.str, typing.Any]]] = None,
        snowflake: typing.Optional[typing.Union["QuicksightDataSourceParametersSnowflake", typing.Dict[builtins.str, typing.Any]]] = None,
        spark: typing.Optional[typing.Union["QuicksightDataSourceParametersSpark", typing.Dict[builtins.str, typing.Any]]] = None,
        sql_server: typing.Optional[typing.Union["QuicksightDataSourceParametersSqlServer", typing.Dict[builtins.str, typing.Any]]] = None,
        teradata: typing.Optional[typing.Union["QuicksightDataSourceParametersTeradata", typing.Dict[builtins.str, typing.Any]]] = None,
        twitter: typing.Optional[typing.Union["QuicksightDataSourceParametersTwitter", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param amazon_elasticsearch: amazon_elasticsearch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#amazon_elasticsearch QuicksightDataSource#amazon_elasticsearch}
        :param athena: athena block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#athena QuicksightDataSource#athena}
        :param aurora: aurora block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#aurora QuicksightDataSource#aurora}
        :param aurora_postgresql: aurora_postgresql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#aurora_postgresql QuicksightDataSource#aurora_postgresql}
        :param aws_iot_analytics: aws_iot_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#aws_iot_analytics QuicksightDataSource#aws_iot_analytics}
        :param databricks: databricks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#databricks QuicksightDataSource#databricks}
        :param jira: jira block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#jira QuicksightDataSource#jira}
        :param maria_db: maria_db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#maria_db QuicksightDataSource#maria_db}
        :param mysql: mysql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#mysql QuicksightDataSource#mysql}
        :param oracle: oracle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#oracle QuicksightDataSource#oracle}
        :param postgresql: postgresql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#postgresql QuicksightDataSource#postgresql}
        :param presto: presto block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#presto QuicksightDataSource#presto}
        :param rds: rds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#rds QuicksightDataSource#rds}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#redshift QuicksightDataSource#redshift}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#s3 QuicksightDataSource#s3}
        :param service_now: service_now block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#service_now QuicksightDataSource#service_now}
        :param snowflake: snowflake block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#snowflake QuicksightDataSource#snowflake}
        :param spark: spark block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#spark QuicksightDataSource#spark}
        :param sql_server: sql_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#sql_server QuicksightDataSource#sql_server}
        :param teradata: teradata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#teradata QuicksightDataSource#teradata}
        :param twitter: twitter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#twitter QuicksightDataSource#twitter}
        '''
        if isinstance(amazon_elasticsearch, dict):
            amazon_elasticsearch = QuicksightDataSourceParametersAmazonElasticsearch(**amazon_elasticsearch)
        if isinstance(athena, dict):
            athena = QuicksightDataSourceParametersAthena(**athena)
        if isinstance(aurora, dict):
            aurora = QuicksightDataSourceParametersAurora(**aurora)
        if isinstance(aurora_postgresql, dict):
            aurora_postgresql = QuicksightDataSourceParametersAuroraPostgresql(**aurora_postgresql)
        if isinstance(aws_iot_analytics, dict):
            aws_iot_analytics = QuicksightDataSourceParametersAwsIotAnalytics(**aws_iot_analytics)
        if isinstance(databricks, dict):
            databricks = QuicksightDataSourceParametersDatabricks(**databricks)
        if isinstance(jira, dict):
            jira = QuicksightDataSourceParametersJira(**jira)
        if isinstance(maria_db, dict):
            maria_db = QuicksightDataSourceParametersMariaDb(**maria_db)
        if isinstance(mysql, dict):
            mysql = QuicksightDataSourceParametersMysql(**mysql)
        if isinstance(oracle, dict):
            oracle = QuicksightDataSourceParametersOracle(**oracle)
        if isinstance(postgresql, dict):
            postgresql = QuicksightDataSourceParametersPostgresql(**postgresql)
        if isinstance(presto, dict):
            presto = QuicksightDataSourceParametersPresto(**presto)
        if isinstance(rds, dict):
            rds = QuicksightDataSourceParametersRds(**rds)
        if isinstance(redshift, dict):
            redshift = QuicksightDataSourceParametersRedshift(**redshift)
        if isinstance(s3, dict):
            s3 = QuicksightDataSourceParametersS3(**s3)
        if isinstance(service_now, dict):
            service_now = QuicksightDataSourceParametersServiceNow(**service_now)
        if isinstance(snowflake, dict):
            snowflake = QuicksightDataSourceParametersSnowflake(**snowflake)
        if isinstance(spark, dict):
            spark = QuicksightDataSourceParametersSpark(**spark)
        if isinstance(sql_server, dict):
            sql_server = QuicksightDataSourceParametersSqlServer(**sql_server)
        if isinstance(teradata, dict):
            teradata = QuicksightDataSourceParametersTeradata(**teradata)
        if isinstance(twitter, dict):
            twitter = QuicksightDataSourceParametersTwitter(**twitter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5dc542306c18fd4586ba7ca0319c9a34b53baf08d513f5945efc51008f9e55b)
            check_type(argname="argument amazon_elasticsearch", value=amazon_elasticsearch, expected_type=type_hints["amazon_elasticsearch"])
            check_type(argname="argument athena", value=athena, expected_type=type_hints["athena"])
            check_type(argname="argument aurora", value=aurora, expected_type=type_hints["aurora"])
            check_type(argname="argument aurora_postgresql", value=aurora_postgresql, expected_type=type_hints["aurora_postgresql"])
            check_type(argname="argument aws_iot_analytics", value=aws_iot_analytics, expected_type=type_hints["aws_iot_analytics"])
            check_type(argname="argument databricks", value=databricks, expected_type=type_hints["databricks"])
            check_type(argname="argument jira", value=jira, expected_type=type_hints["jira"])
            check_type(argname="argument maria_db", value=maria_db, expected_type=type_hints["maria_db"])
            check_type(argname="argument mysql", value=mysql, expected_type=type_hints["mysql"])
            check_type(argname="argument oracle", value=oracle, expected_type=type_hints["oracle"])
            check_type(argname="argument postgresql", value=postgresql, expected_type=type_hints["postgresql"])
            check_type(argname="argument presto", value=presto, expected_type=type_hints["presto"])
            check_type(argname="argument rds", value=rds, expected_type=type_hints["rds"])
            check_type(argname="argument redshift", value=redshift, expected_type=type_hints["redshift"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
            check_type(argname="argument snowflake", value=snowflake, expected_type=type_hints["snowflake"])
            check_type(argname="argument spark", value=spark, expected_type=type_hints["spark"])
            check_type(argname="argument sql_server", value=sql_server, expected_type=type_hints["sql_server"])
            check_type(argname="argument teradata", value=teradata, expected_type=type_hints["teradata"])
            check_type(argname="argument twitter", value=twitter, expected_type=type_hints["twitter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if amazon_elasticsearch is not None:
            self._values["amazon_elasticsearch"] = amazon_elasticsearch
        if athena is not None:
            self._values["athena"] = athena
        if aurora is not None:
            self._values["aurora"] = aurora
        if aurora_postgresql is not None:
            self._values["aurora_postgresql"] = aurora_postgresql
        if aws_iot_analytics is not None:
            self._values["aws_iot_analytics"] = aws_iot_analytics
        if databricks is not None:
            self._values["databricks"] = databricks
        if jira is not None:
            self._values["jira"] = jira
        if maria_db is not None:
            self._values["maria_db"] = maria_db
        if mysql is not None:
            self._values["mysql"] = mysql
        if oracle is not None:
            self._values["oracle"] = oracle
        if postgresql is not None:
            self._values["postgresql"] = postgresql
        if presto is not None:
            self._values["presto"] = presto
        if rds is not None:
            self._values["rds"] = rds
        if redshift is not None:
            self._values["redshift"] = redshift
        if s3 is not None:
            self._values["s3"] = s3
        if service_now is not None:
            self._values["service_now"] = service_now
        if snowflake is not None:
            self._values["snowflake"] = snowflake
        if spark is not None:
            self._values["spark"] = spark
        if sql_server is not None:
            self._values["sql_server"] = sql_server
        if teradata is not None:
            self._values["teradata"] = teradata
        if twitter is not None:
            self._values["twitter"] = twitter

    @builtins.property
    def amazon_elasticsearch(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersAmazonElasticsearch"]:
        '''amazon_elasticsearch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#amazon_elasticsearch QuicksightDataSource#amazon_elasticsearch}
        '''
        result = self._values.get("amazon_elasticsearch")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersAmazonElasticsearch"], result)

    @builtins.property
    def athena(self) -> typing.Optional["QuicksightDataSourceParametersAthena"]:
        '''athena block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#athena QuicksightDataSource#athena}
        '''
        result = self._values.get("athena")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersAthena"], result)

    @builtins.property
    def aurora(self) -> typing.Optional["QuicksightDataSourceParametersAurora"]:
        '''aurora block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#aurora QuicksightDataSource#aurora}
        '''
        result = self._values.get("aurora")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersAurora"], result)

    @builtins.property
    def aurora_postgresql(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersAuroraPostgresql"]:
        '''aurora_postgresql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#aurora_postgresql QuicksightDataSource#aurora_postgresql}
        '''
        result = self._values.get("aurora_postgresql")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersAuroraPostgresql"], result)

    @builtins.property
    def aws_iot_analytics(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersAwsIotAnalytics"]:
        '''aws_iot_analytics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#aws_iot_analytics QuicksightDataSource#aws_iot_analytics}
        '''
        result = self._values.get("aws_iot_analytics")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersAwsIotAnalytics"], result)

    @builtins.property
    def databricks(self) -> typing.Optional["QuicksightDataSourceParametersDatabricks"]:
        '''databricks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#databricks QuicksightDataSource#databricks}
        '''
        result = self._values.get("databricks")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersDatabricks"], result)

    @builtins.property
    def jira(self) -> typing.Optional["QuicksightDataSourceParametersJira"]:
        '''jira block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#jira QuicksightDataSource#jira}
        '''
        result = self._values.get("jira")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersJira"], result)

    @builtins.property
    def maria_db(self) -> typing.Optional["QuicksightDataSourceParametersMariaDb"]:
        '''maria_db block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#maria_db QuicksightDataSource#maria_db}
        '''
        result = self._values.get("maria_db")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersMariaDb"], result)

    @builtins.property
    def mysql(self) -> typing.Optional["QuicksightDataSourceParametersMysql"]:
        '''mysql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#mysql QuicksightDataSource#mysql}
        '''
        result = self._values.get("mysql")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersMysql"], result)

    @builtins.property
    def oracle(self) -> typing.Optional["QuicksightDataSourceParametersOracle"]:
        '''oracle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#oracle QuicksightDataSource#oracle}
        '''
        result = self._values.get("oracle")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersOracle"], result)

    @builtins.property
    def postgresql(self) -> typing.Optional["QuicksightDataSourceParametersPostgresql"]:
        '''postgresql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#postgresql QuicksightDataSource#postgresql}
        '''
        result = self._values.get("postgresql")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersPostgresql"], result)

    @builtins.property
    def presto(self) -> typing.Optional["QuicksightDataSourceParametersPresto"]:
        '''presto block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#presto QuicksightDataSource#presto}
        '''
        result = self._values.get("presto")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersPresto"], result)

    @builtins.property
    def rds(self) -> typing.Optional["QuicksightDataSourceParametersRds"]:
        '''rds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#rds QuicksightDataSource#rds}
        '''
        result = self._values.get("rds")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersRds"], result)

    @builtins.property
    def redshift(self) -> typing.Optional["QuicksightDataSourceParametersRedshift"]:
        '''redshift block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#redshift QuicksightDataSource#redshift}
        '''
        result = self._values.get("redshift")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersRedshift"], result)

    @builtins.property
    def s3(self) -> typing.Optional["QuicksightDataSourceParametersS3"]:
        '''s3 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#s3 QuicksightDataSource#s3}
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersS3"], result)

    @builtins.property
    def service_now(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersServiceNow"]:
        '''service_now block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#service_now QuicksightDataSource#service_now}
        '''
        result = self._values.get("service_now")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersServiceNow"], result)

    @builtins.property
    def snowflake(self) -> typing.Optional["QuicksightDataSourceParametersSnowflake"]:
        '''snowflake block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#snowflake QuicksightDataSource#snowflake}
        '''
        result = self._values.get("snowflake")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersSnowflake"], result)

    @builtins.property
    def spark(self) -> typing.Optional["QuicksightDataSourceParametersSpark"]:
        '''spark block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#spark QuicksightDataSource#spark}
        '''
        result = self._values.get("spark")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersSpark"], result)

    @builtins.property
    def sql_server(self) -> typing.Optional["QuicksightDataSourceParametersSqlServer"]:
        '''sql_server block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#sql_server QuicksightDataSource#sql_server}
        '''
        result = self._values.get("sql_server")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersSqlServer"], result)

    @builtins.property
    def teradata(self) -> typing.Optional["QuicksightDataSourceParametersTeradata"]:
        '''teradata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#teradata QuicksightDataSource#teradata}
        '''
        result = self._values.get("teradata")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersTeradata"], result)

    @builtins.property
    def twitter(self) -> typing.Optional["QuicksightDataSourceParametersTwitter"]:
        '''twitter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#twitter QuicksightDataSource#twitter}
        '''
        result = self._values.get("twitter")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersTwitter"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAmazonElasticsearch",
    jsii_struct_bases=[],
    name_mapping={"domain": "domain"},
)
class QuicksightDataSourceParametersAmazonElasticsearch:
    def __init__(self, *, domain: builtins.str) -> None:
        '''
        :param domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#domain QuicksightDataSource#domain}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e1ad4c1b5406e4bdecf0ceb2d174d2dfcf1564c92e7b2e420e08bea7a51d0e1)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain": domain,
        }

    @builtins.property
    def domain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#domain QuicksightDataSource#domain}.'''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersAmazonElasticsearch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersAmazonElasticsearchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAmazonElasticsearchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fd8975ff26c895407f477d9881e6e7c070cb109542239ef65d6fd93c5d5fbd7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7de59aaa73f3451a8d72c8247f87ff3e56a7281202491226593c7a6721c48402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersAmazonElasticsearch]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAmazonElasticsearch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersAmazonElasticsearch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d119b87f13560a3f3784bb4fa21d4ef5d8677343c689f0d228a6222928e0a6c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAthena",
    jsii_struct_bases=[],
    name_mapping={"work_group": "workGroup"},
)
class QuicksightDataSourceParametersAthena:
    def __init__(self, *, work_group: typing.Optional[builtins.str] = None) -> None:
        '''
        :param work_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#work_group QuicksightDataSource#work_group}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c077c45cd252f449b63f9b86646602aadbcf1076430b7c32885143b22072103)
            check_type(argname="argument work_group", value=work_group, expected_type=type_hints["work_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if work_group is not None:
            self._values["work_group"] = work_group

    @builtins.property
    def work_group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#work_group QuicksightDataSource#work_group}.'''
        result = self._values.get("work_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersAthena(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersAthenaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAthenaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5798b5af515369d6d6309fafa8f32187e909ffc4f9fee09dbef8da83639688d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetWorkGroup")
    def reset_work_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkGroup", []))

    @builtins.property
    @jsii.member(jsii_name="workGroupInput")
    def work_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="workGroup")
    def work_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workGroup"))

    @work_group.setter
    def work_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__059ad83ba75130c002f172ad741c0d5b40fd8b0894137e1572701e5bf72f0709)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersAthena]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAthena], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersAthena],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a035244c9f4c624cf8b4f7e99e56f8d2c71bf858f593a51cbd5af930f9f612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAurora",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "host": "host", "port": "port"},
)
class QuicksightDataSourceParametersAurora:
    def __init__(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3221be6928f939a463c60cae7c51be1bf2df85c20094a1989d4d11c1f8f839b)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "host": host,
            "port": port,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersAurora(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersAuroraOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAuroraOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8d27b5cde4e5e0e994872257f9a4d201e1edaa7972ae96fcb26da0ad4dc2be0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd317e60ab190286a3284066093c6a6fa47036de02b28471f327b4b70663587c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b1dc7725e2458be5f96b680432beb4b2e042545b93b067df3e920bad7722f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af15745ef0401f3ccb94bdbaa6438df62accfb427677b5fac8cd2a0270de9436)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersAurora]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAurora], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersAurora],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400d6e085900b9dab9a101f5edc79901b4f4f53767eeb7f764272d68c65f69c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAuroraPostgresql",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "host": "host", "port": "port"},
)
class QuicksightDataSourceParametersAuroraPostgresql:
    def __init__(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8544c718d7191887936e8eadaf2a886850f4c827922a5c81754ef804707dd3ca)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "host": host,
            "port": port,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersAuroraPostgresql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersAuroraPostgresqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAuroraPostgresqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1addd51dd4dd3f2e043db7af03edcd74c9ebdb4af984cc1cb412602629c5b20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba1ff93b802fb7be1778f311036e52d608e158b8b928a76e8500b6a2f509a731)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a94a40ab1611a5b78a8bc66bc7ebe07bf4eca55d53aded07c7e3252db8de7e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba2ba4aae3d853588fbdffc35aa12887ff41259657d2ed63d355a5e1aa03767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersAuroraPostgresql]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAuroraPostgresql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersAuroraPostgresql],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c82a7161f2eafa8a58a32db78333e4529c91afc61669babd0d0fa93f34019729)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAwsIotAnalytics",
    jsii_struct_bases=[],
    name_mapping={"data_set_name": "dataSetName"},
)
class QuicksightDataSourceParametersAwsIotAnalytics:
    def __init__(self, *, data_set_name: builtins.str) -> None:
        '''
        :param data_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#data_set_name QuicksightDataSource#data_set_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63889bea2a517e8bdd4c98b34a9c9703c0eb85113d20d65b2d0385367707d811)
            check_type(argname="argument data_set_name", value=data_set_name, expected_type=type_hints["data_set_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_set_name": data_set_name,
        }

    @builtins.property
    def data_set_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#data_set_name QuicksightDataSource#data_set_name}.'''
        result = self._values.get("data_set_name")
        assert result is not None, "Required property 'data_set_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersAwsIotAnalytics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersAwsIotAnalyticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAwsIotAnalyticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d00d0e66f6c14a4615b47c06e7ccfd5eb0bba68191afe6918980f7e6fd239189)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dataSetNameInput")
    def data_set_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSetName")
    def data_set_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSetName"))

    @data_set_name.setter
    def data_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c6e62106db8cbf842b878ba50a2595a868f3d652f4900ac550da632294e3da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersAwsIotAnalytics]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAwsIotAnalytics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersAwsIotAnalytics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d2dd483d2a862ab3df0d4dfd497eba01eb8c1f3b6fa4cf004d48108fddb28a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersDatabricks",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "port": "port",
        "sql_endpoint_path": "sqlEndpointPath",
    },
)
class QuicksightDataSourceParametersDatabricks:
    def __init__(
        self,
        *,
        host: builtins.str,
        port: jsii.Number,
        sql_endpoint_path: builtins.str,
    ) -> None:
        '''
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        :param sql_endpoint_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#sql_endpoint_path QuicksightDataSource#sql_endpoint_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb582731c89be5bbe2fa6dae0fd9389312f64bf1ec51a2ae6b35074b0bb8b49e)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument sql_endpoint_path", value=sql_endpoint_path, expected_type=type_hints["sql_endpoint_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host": host,
            "port": port,
            "sql_endpoint_path": sql_endpoint_path,
        }

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def sql_endpoint_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#sql_endpoint_path QuicksightDataSource#sql_endpoint_path}.'''
        result = self._values.get("sql_endpoint_path")
        assert result is not None, "Required property 'sql_endpoint_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersDatabricks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersDatabricksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersDatabricksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac1471a81a9ed6b0f01249ce8c09d37793fd22d22ac243443010ecdd1680aeb6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlEndpointPathInput")
    def sql_endpoint_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlEndpointPathInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f06286320f1df86b8de45df5d49e1681542353f42a185d950e497845916b05e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff35a6d4a5656dedb92f3c95405afe64a6413ab27723aead08c741f325c05cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlEndpointPath")
    def sql_endpoint_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlEndpointPath"))

    @sql_endpoint_path.setter
    def sql_endpoint_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__775f85e1ba2e5c958fe436cec7be516478046080c572939d5cc2f8fb9344d885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlEndpointPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersDatabricks]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersDatabricks], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersDatabricks],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edd4e49f798844aac9ca2563619a7043813eb8e016d157630b24ed375103192c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersJira",
    jsii_struct_bases=[],
    name_mapping={"site_base_url": "siteBaseUrl"},
)
class QuicksightDataSourceParametersJira:
    def __init__(self, *, site_base_url: builtins.str) -> None:
        '''
        :param site_base_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#site_base_url QuicksightDataSource#site_base_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__964013b854ba2012be363ce801df04e653468275c845d48236be41582c71dec9)
            check_type(argname="argument site_base_url", value=site_base_url, expected_type=type_hints["site_base_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "site_base_url": site_base_url,
        }

    @builtins.property
    def site_base_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#site_base_url QuicksightDataSource#site_base_url}.'''
        result = self._values.get("site_base_url")
        assert result is not None, "Required property 'site_base_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersJira(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersJiraOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersJiraOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37a38899644f2463e8b5cc48b06019d9bd759632ac1573b9c8971cc7be46dde7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="siteBaseUrlInput")
    def site_base_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "siteBaseUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="siteBaseUrl")
    def site_base_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "siteBaseUrl"))

    @site_base_url.setter
    def site_base_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bfe600077756344f430e2addc1521fbf203fd3be05924358c845c7213b28db1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "siteBaseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersJira]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersJira], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersJira],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21915c78d5c566eaefc6bc3a799235dae80d99ca2b75488b85ac08e1ded4c4c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersMariaDb",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "host": "host", "port": "port"},
)
class QuicksightDataSourceParametersMariaDb:
    def __init__(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b148b9b62fd8f193e172ce9b06ac8edd32ec05b0ff3de7e4557fd5707afa084)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "host": host,
            "port": port,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersMariaDb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersMariaDbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersMariaDbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c5193c093447891be793b068c5f6c57553362a84ad32f3c275fdabf826ab729)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d984081cee86f19ed164359a9b9d3cad4c1de5429c0fa386e67b828926b3f072)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb6f18561c876293f35a4ed91886810016b05f4a7782cb6670f880ae66a8bff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7362778103cbf953785d5bdee0fd3abbdb8752dd4fa92468add5a933ad0a6e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersMariaDb]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersMariaDb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersMariaDb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b581593ae61f7047f436577577aaddb62465998919c3289bfe43de96d7b44a34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersMysql",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "host": "host", "port": "port"},
)
class QuicksightDataSourceParametersMysql:
    def __init__(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1818c154cebbf509f7fa32d0cb6ed8ecec5838f7c1cc59bea9c63747a93c52c)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "host": host,
            "port": port,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersMysql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersMysqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersMysqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5244a4e66370b2b4ceebb1ae5d9fdefa0bde312cb1851455ea7d065121d84392)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b73fce73b2e735b9773a759b19abf744b09095390cf703099467fdc459edfa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77080187b76eaf902c026ef3576b988acfe9b6102b2544d8fa6334a5f5f9f3e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45d03a448c06b839402420f9d369608ffb6b3d6b29d72a359f57d7999d8df04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersMysql]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersMysql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersMysql],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37172d9b119ee851bf35415f95bdce1d948c89b37a284802dbe1d9e48392f42c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersOracle",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "host": "host", "port": "port"},
)
class QuicksightDataSourceParametersOracle:
    def __init__(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb61c51cd3a2cbd328150c747ce126091ff87b0fceb7f1ff3a3513d9a4e2d2ac)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "host": host,
            "port": port,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersOracle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersOracleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersOracleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad93c88e999616835212a8b9070e6de9101ff8a74688345d265bcf984704b1db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a68584119d7c6820b95812162d7596019418bea9cd5f1b1f7cb2e293173b40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0304244b16d4924b69f8bf3bd6e495182ba4e478e936d93f14acb483daa4380d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e6a034e6330bab4c619ce23183f5aa621843b34cb2f8e4780ba4879fef9499c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersOracle]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersOracle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersOracle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73ff31bdb7e292b70e534752ebc395db29e156640872b45bf44663a5cf3d67ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSourceParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00d32b3828798004ea6fb78a40b649c49512501ccb5c218bc2d4c8c526832811)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAmazonElasticsearch")
    def put_amazon_elasticsearch(self, *, domain: builtins.str) -> None:
        '''
        :param domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#domain QuicksightDataSource#domain}.
        '''
        value = QuicksightDataSourceParametersAmazonElasticsearch(domain=domain)

        return typing.cast(None, jsii.invoke(self, "putAmazonElasticsearch", [value]))

    @jsii.member(jsii_name="putAthena")
    def put_athena(self, *, work_group: typing.Optional[builtins.str] = None) -> None:
        '''
        :param work_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#work_group QuicksightDataSource#work_group}.
        '''
        value = QuicksightDataSourceParametersAthena(work_group=work_group)

        return typing.cast(None, jsii.invoke(self, "putAthena", [value]))

    @jsii.member(jsii_name="putAurora")
    def put_aurora(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersAurora(
            database=database, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putAurora", [value]))

    @jsii.member(jsii_name="putAuroraPostgresql")
    def put_aurora_postgresql(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersAuroraPostgresql(
            database=database, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putAuroraPostgresql", [value]))

    @jsii.member(jsii_name="putAwsIotAnalytics")
    def put_aws_iot_analytics(self, *, data_set_name: builtins.str) -> None:
        '''
        :param data_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#data_set_name QuicksightDataSource#data_set_name}.
        '''
        value = QuicksightDataSourceParametersAwsIotAnalytics(
            data_set_name=data_set_name
        )

        return typing.cast(None, jsii.invoke(self, "putAwsIotAnalytics", [value]))

    @jsii.member(jsii_name="putDatabricks")
    def put_databricks(
        self,
        *,
        host: builtins.str,
        port: jsii.Number,
        sql_endpoint_path: builtins.str,
    ) -> None:
        '''
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        :param sql_endpoint_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#sql_endpoint_path QuicksightDataSource#sql_endpoint_path}.
        '''
        value = QuicksightDataSourceParametersDatabricks(
            host=host, port=port, sql_endpoint_path=sql_endpoint_path
        )

        return typing.cast(None, jsii.invoke(self, "putDatabricks", [value]))

    @jsii.member(jsii_name="putJira")
    def put_jira(self, *, site_base_url: builtins.str) -> None:
        '''
        :param site_base_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#site_base_url QuicksightDataSource#site_base_url}.
        '''
        value = QuicksightDataSourceParametersJira(site_base_url=site_base_url)

        return typing.cast(None, jsii.invoke(self, "putJira", [value]))

    @jsii.member(jsii_name="putMariaDb")
    def put_maria_db(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersMariaDb(
            database=database, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putMariaDb", [value]))

    @jsii.member(jsii_name="putMysql")
    def put_mysql(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersMysql(
            database=database, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putMysql", [value]))

    @jsii.member(jsii_name="putOracle")
    def put_oracle(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersOracle(
            database=database, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putOracle", [value]))

    @jsii.member(jsii_name="putPostgresql")
    def put_postgresql(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersPostgresql(
            database=database, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putPostgresql", [value]))

    @jsii.member(jsii_name="putPresto")
    def put_presto(
        self,
        *,
        catalog: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param catalog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#catalog QuicksightDataSource#catalog}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersPresto(
            catalog=catalog, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putPresto", [value]))

    @jsii.member(jsii_name="putRds")
    def put_rds(self, *, database: builtins.str, instance_id: builtins.str) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#instance_id QuicksightDataSource#instance_id}.
        '''
        value = QuicksightDataSourceParametersRds(
            database=database, instance_id=instance_id
        )

        return typing.cast(None, jsii.invoke(self, "putRds", [value]))

    @jsii.member(jsii_name="putRedshift")
    def put_redshift(
        self,
        *,
        database: builtins.str,
        cluster_id: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#cluster_id QuicksightDataSource#cluster_id}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersRedshift(
            database=database, cluster_id=cluster_id, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putRedshift", [value]))

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        *,
        manifest_file_location: typing.Union["QuicksightDataSourceParametersS3ManifestFileLocation", typing.Dict[builtins.str, typing.Any]],
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param manifest_file_location: manifest_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#manifest_file_location QuicksightDataSource#manifest_file_location}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#role_arn QuicksightDataSource#role_arn}.
        '''
        value = QuicksightDataSourceParametersS3(
            manifest_file_location=manifest_file_location, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="putServiceNow")
    def put_service_now(self, *, site_base_url: builtins.str) -> None:
        '''
        :param site_base_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#site_base_url QuicksightDataSource#site_base_url}.
        '''
        value = QuicksightDataSourceParametersServiceNow(site_base_url=site_base_url)

        return typing.cast(None, jsii.invoke(self, "putServiceNow", [value]))

    @jsii.member(jsii_name="putSnowflake")
    def put_snowflake(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        warehouse: builtins.str,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param warehouse: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#warehouse QuicksightDataSource#warehouse}.
        '''
        value = QuicksightDataSourceParametersSnowflake(
            database=database, host=host, warehouse=warehouse
        )

        return typing.cast(None, jsii.invoke(self, "putSnowflake", [value]))

    @jsii.member(jsii_name="putSpark")
    def put_spark(self, *, host: builtins.str, port: jsii.Number) -> None:
        '''
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersSpark(host=host, port=port)

        return typing.cast(None, jsii.invoke(self, "putSpark", [value]))

    @jsii.member(jsii_name="putSqlServer")
    def put_sql_server(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersSqlServer(
            database=database, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putSqlServer", [value]))

    @jsii.member(jsii_name="putTeradata")
    def put_teradata(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersTeradata(
            database=database, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putTeradata", [value]))

    @jsii.member(jsii_name="putTwitter")
    def put_twitter(self, *, max_rows: jsii.Number, query: builtins.str) -> None:
        '''
        :param max_rows: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#max_rows QuicksightDataSource#max_rows}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#query QuicksightDataSource#query}.
        '''
        value = QuicksightDataSourceParametersTwitter(max_rows=max_rows, query=query)

        return typing.cast(None, jsii.invoke(self, "putTwitter", [value]))

    @jsii.member(jsii_name="resetAmazonElasticsearch")
    def reset_amazon_elasticsearch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmazonElasticsearch", []))

    @jsii.member(jsii_name="resetAthena")
    def reset_athena(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAthena", []))

    @jsii.member(jsii_name="resetAurora")
    def reset_aurora(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAurora", []))

    @jsii.member(jsii_name="resetAuroraPostgresql")
    def reset_aurora_postgresql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuroraPostgresql", []))

    @jsii.member(jsii_name="resetAwsIotAnalytics")
    def reset_aws_iot_analytics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsIotAnalytics", []))

    @jsii.member(jsii_name="resetDatabricks")
    def reset_databricks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabricks", []))

    @jsii.member(jsii_name="resetJira")
    def reset_jira(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJira", []))

    @jsii.member(jsii_name="resetMariaDb")
    def reset_maria_db(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMariaDb", []))

    @jsii.member(jsii_name="resetMysql")
    def reset_mysql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysql", []))

    @jsii.member(jsii_name="resetOracle")
    def reset_oracle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOracle", []))

    @jsii.member(jsii_name="resetPostgresql")
    def reset_postgresql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostgresql", []))

    @jsii.member(jsii_name="resetPresto")
    def reset_presto(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPresto", []))

    @jsii.member(jsii_name="resetRds")
    def reset_rds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRds", []))

    @jsii.member(jsii_name="resetRedshift")
    def reset_redshift(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedshift", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @jsii.member(jsii_name="resetServiceNow")
    def reset_service_now(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceNow", []))

    @jsii.member(jsii_name="resetSnowflake")
    def reset_snowflake(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnowflake", []))

    @jsii.member(jsii_name="resetSpark")
    def reset_spark(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpark", []))

    @jsii.member(jsii_name="resetSqlServer")
    def reset_sql_server(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlServer", []))

    @jsii.member(jsii_name="resetTeradata")
    def reset_teradata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeradata", []))

    @jsii.member(jsii_name="resetTwitter")
    def reset_twitter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTwitter", []))

    @builtins.property
    @jsii.member(jsii_name="amazonElasticsearch")
    def amazon_elasticsearch(
        self,
    ) -> QuicksightDataSourceParametersAmazonElasticsearchOutputReference:
        return typing.cast(QuicksightDataSourceParametersAmazonElasticsearchOutputReference, jsii.get(self, "amazonElasticsearch"))

    @builtins.property
    @jsii.member(jsii_name="athena")
    def athena(self) -> QuicksightDataSourceParametersAthenaOutputReference:
        return typing.cast(QuicksightDataSourceParametersAthenaOutputReference, jsii.get(self, "athena"))

    @builtins.property
    @jsii.member(jsii_name="aurora")
    def aurora(self) -> QuicksightDataSourceParametersAuroraOutputReference:
        return typing.cast(QuicksightDataSourceParametersAuroraOutputReference, jsii.get(self, "aurora"))

    @builtins.property
    @jsii.member(jsii_name="auroraPostgresql")
    def aurora_postgresql(
        self,
    ) -> QuicksightDataSourceParametersAuroraPostgresqlOutputReference:
        return typing.cast(QuicksightDataSourceParametersAuroraPostgresqlOutputReference, jsii.get(self, "auroraPostgresql"))

    @builtins.property
    @jsii.member(jsii_name="awsIotAnalytics")
    def aws_iot_analytics(
        self,
    ) -> QuicksightDataSourceParametersAwsIotAnalyticsOutputReference:
        return typing.cast(QuicksightDataSourceParametersAwsIotAnalyticsOutputReference, jsii.get(self, "awsIotAnalytics"))

    @builtins.property
    @jsii.member(jsii_name="databricks")
    def databricks(self) -> QuicksightDataSourceParametersDatabricksOutputReference:
        return typing.cast(QuicksightDataSourceParametersDatabricksOutputReference, jsii.get(self, "databricks"))

    @builtins.property
    @jsii.member(jsii_name="jira")
    def jira(self) -> QuicksightDataSourceParametersJiraOutputReference:
        return typing.cast(QuicksightDataSourceParametersJiraOutputReference, jsii.get(self, "jira"))

    @builtins.property
    @jsii.member(jsii_name="mariaDb")
    def maria_db(self) -> QuicksightDataSourceParametersMariaDbOutputReference:
        return typing.cast(QuicksightDataSourceParametersMariaDbOutputReference, jsii.get(self, "mariaDb"))

    @builtins.property
    @jsii.member(jsii_name="mysql")
    def mysql(self) -> QuicksightDataSourceParametersMysqlOutputReference:
        return typing.cast(QuicksightDataSourceParametersMysqlOutputReference, jsii.get(self, "mysql"))

    @builtins.property
    @jsii.member(jsii_name="oracle")
    def oracle(self) -> QuicksightDataSourceParametersOracleOutputReference:
        return typing.cast(QuicksightDataSourceParametersOracleOutputReference, jsii.get(self, "oracle"))

    @builtins.property
    @jsii.member(jsii_name="postgresql")
    def postgresql(self) -> "QuicksightDataSourceParametersPostgresqlOutputReference":
        return typing.cast("QuicksightDataSourceParametersPostgresqlOutputReference", jsii.get(self, "postgresql"))

    @builtins.property
    @jsii.member(jsii_name="presto")
    def presto(self) -> "QuicksightDataSourceParametersPrestoOutputReference":
        return typing.cast("QuicksightDataSourceParametersPrestoOutputReference", jsii.get(self, "presto"))

    @builtins.property
    @jsii.member(jsii_name="rds")
    def rds(self) -> "QuicksightDataSourceParametersRdsOutputReference":
        return typing.cast("QuicksightDataSourceParametersRdsOutputReference", jsii.get(self, "rds"))

    @builtins.property
    @jsii.member(jsii_name="redshift")
    def redshift(self) -> "QuicksightDataSourceParametersRedshiftOutputReference":
        return typing.cast("QuicksightDataSourceParametersRedshiftOutputReference", jsii.get(self, "redshift"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(self) -> "QuicksightDataSourceParametersS3OutputReference":
        return typing.cast("QuicksightDataSourceParametersS3OutputReference", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="serviceNow")
    def service_now(self) -> "QuicksightDataSourceParametersServiceNowOutputReference":
        return typing.cast("QuicksightDataSourceParametersServiceNowOutputReference", jsii.get(self, "serviceNow"))

    @builtins.property
    @jsii.member(jsii_name="snowflake")
    def snowflake(self) -> "QuicksightDataSourceParametersSnowflakeOutputReference":
        return typing.cast("QuicksightDataSourceParametersSnowflakeOutputReference", jsii.get(self, "snowflake"))

    @builtins.property
    @jsii.member(jsii_name="spark")
    def spark(self) -> "QuicksightDataSourceParametersSparkOutputReference":
        return typing.cast("QuicksightDataSourceParametersSparkOutputReference", jsii.get(self, "spark"))

    @builtins.property
    @jsii.member(jsii_name="sqlServer")
    def sql_server(self) -> "QuicksightDataSourceParametersSqlServerOutputReference":
        return typing.cast("QuicksightDataSourceParametersSqlServerOutputReference", jsii.get(self, "sqlServer"))

    @builtins.property
    @jsii.member(jsii_name="teradata")
    def teradata(self) -> "QuicksightDataSourceParametersTeradataOutputReference":
        return typing.cast("QuicksightDataSourceParametersTeradataOutputReference", jsii.get(self, "teradata"))

    @builtins.property
    @jsii.member(jsii_name="twitter")
    def twitter(self) -> "QuicksightDataSourceParametersTwitterOutputReference":
        return typing.cast("QuicksightDataSourceParametersTwitterOutputReference", jsii.get(self, "twitter"))

    @builtins.property
    @jsii.member(jsii_name="amazonElasticsearchInput")
    def amazon_elasticsearch_input(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersAmazonElasticsearch]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAmazonElasticsearch], jsii.get(self, "amazonElasticsearchInput"))

    @builtins.property
    @jsii.member(jsii_name="athenaInput")
    def athena_input(self) -> typing.Optional[QuicksightDataSourceParametersAthena]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAthena], jsii.get(self, "athenaInput"))

    @builtins.property
    @jsii.member(jsii_name="auroraInput")
    def aurora_input(self) -> typing.Optional[QuicksightDataSourceParametersAurora]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAurora], jsii.get(self, "auroraInput"))

    @builtins.property
    @jsii.member(jsii_name="auroraPostgresqlInput")
    def aurora_postgresql_input(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersAuroraPostgresql]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAuroraPostgresql], jsii.get(self, "auroraPostgresqlInput"))

    @builtins.property
    @jsii.member(jsii_name="awsIotAnalyticsInput")
    def aws_iot_analytics_input(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersAwsIotAnalytics]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAwsIotAnalytics], jsii.get(self, "awsIotAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="databricksInput")
    def databricks_input(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersDatabricks]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersDatabricks], jsii.get(self, "databricksInput"))

    @builtins.property
    @jsii.member(jsii_name="jiraInput")
    def jira_input(self) -> typing.Optional[QuicksightDataSourceParametersJira]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersJira], jsii.get(self, "jiraInput"))

    @builtins.property
    @jsii.member(jsii_name="mariaDbInput")
    def maria_db_input(self) -> typing.Optional[QuicksightDataSourceParametersMariaDb]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersMariaDb], jsii.get(self, "mariaDbInput"))

    @builtins.property
    @jsii.member(jsii_name="mysqlInput")
    def mysql_input(self) -> typing.Optional[QuicksightDataSourceParametersMysql]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersMysql], jsii.get(self, "mysqlInput"))

    @builtins.property
    @jsii.member(jsii_name="oracleInput")
    def oracle_input(self) -> typing.Optional[QuicksightDataSourceParametersOracle]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersOracle], jsii.get(self, "oracleInput"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlInput")
    def postgresql_input(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersPostgresql"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersPostgresql"], jsii.get(self, "postgresqlInput"))

    @builtins.property
    @jsii.member(jsii_name="prestoInput")
    def presto_input(self) -> typing.Optional["QuicksightDataSourceParametersPresto"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersPresto"], jsii.get(self, "prestoInput"))

    @builtins.property
    @jsii.member(jsii_name="rdsInput")
    def rds_input(self) -> typing.Optional["QuicksightDataSourceParametersRds"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersRds"], jsii.get(self, "rdsInput"))

    @builtins.property
    @jsii.member(jsii_name="redshiftInput")
    def redshift_input(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersRedshift"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersRedshift"], jsii.get(self, "redshiftInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(self) -> typing.Optional["QuicksightDataSourceParametersS3"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersS3"], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="serviceNowInput")
    def service_now_input(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersServiceNow"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersServiceNow"], jsii.get(self, "serviceNowInput"))

    @builtins.property
    @jsii.member(jsii_name="snowflakeInput")
    def snowflake_input(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersSnowflake"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersSnowflake"], jsii.get(self, "snowflakeInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkInput")
    def spark_input(self) -> typing.Optional["QuicksightDataSourceParametersSpark"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersSpark"], jsii.get(self, "sparkInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlServerInput")
    def sql_server_input(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersSqlServer"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersSqlServer"], jsii.get(self, "sqlServerInput"))

    @builtins.property
    @jsii.member(jsii_name="teradataInput")
    def teradata_input(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersTeradata"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersTeradata"], jsii.get(self, "teradataInput"))

    @builtins.property
    @jsii.member(jsii_name="twitterInput")
    def twitter_input(self) -> typing.Optional["QuicksightDataSourceParametersTwitter"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersTwitter"], jsii.get(self, "twitterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParameters]:
        return typing.cast(typing.Optional[QuicksightDataSourceParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5925b5222b000bb86e98781226059ca530391c1a9ad4dcb7b2b072ef820e5c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersPostgresql",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "host": "host", "port": "port"},
)
class QuicksightDataSourceParametersPostgresql:
    def __init__(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49ede637c834609ac19c7c37264b8eea95b4c09bf277afcf76535c94e4b07055)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "host": host,
            "port": port,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersPostgresql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersPostgresqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersPostgresqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c8163b487c8df91d4af15c8a955920b8aed486bf12be2960651c36a859e37de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed841cd94d51359a5faea3dcb8e659757ba9dee13bf68f336cce89878296620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15649ef402dd7ea3104178459df79d3d06d1640e45184e661bd3f0cb07963cdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a687051c9a593e67025502b3ab529ab67d32ce1d1599ce026010a19c5cda3e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersPostgresql]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersPostgresql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersPostgresql],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe5af0edb4ba008142164fd0dd3f10f58ada0f2177a9522325ac9f1947f6255)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersPresto",
    jsii_struct_bases=[],
    name_mapping={"catalog": "catalog", "host": "host", "port": "port"},
)
class QuicksightDataSourceParametersPresto:
    def __init__(
        self,
        *,
        catalog: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param catalog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#catalog QuicksightDataSource#catalog}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4ecc40b995d47c6273128b4b7ffa28501ca12f4f12272cc9fc77f5ea9033f1)
            check_type(argname="argument catalog", value=catalog, expected_type=type_hints["catalog"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "catalog": catalog,
            "host": host,
            "port": port,
        }

    @builtins.property
    def catalog(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#catalog QuicksightDataSource#catalog}.'''
        result = self._values.get("catalog")
        assert result is not None, "Required property 'catalog' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersPresto(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersPrestoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersPrestoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1383d7169bf7499bfe836062594192105d80cd580bae952cf04a049d49940bbd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="catalogInput")
    def catalog_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "catalogInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="catalog")
    def catalog(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalog"))

    @catalog.setter
    def catalog(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06827b5d5c97580028f66aaf8036388026e42900609435eaa597e3ac7622b895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ef13e1723b0dfb8b3ec1b4a97c75398e2173a038fe1de40149e0e7c5165655b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d161fc9681bfff0bd187e5ec589d97de1a1af51099e7fbd72105fe87b57eef4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersPresto]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersPresto], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersPresto],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e6fe5abd8302df73e47e9b2c6bab82ae7d8445d8090b2b8ba17e437300482f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersRds",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "instance_id": "instanceId"},
)
class QuicksightDataSourceParametersRds:
    def __init__(self, *, database: builtins.str, instance_id: builtins.str) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#instance_id QuicksightDataSource#instance_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eb8704106f444fe0984ec344fdeab88c7235aba0ae1a58d832932f29b8a30a6)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "instance_id": instance_id,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#instance_id QuicksightDataSource#instance_id}.'''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersRds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersRdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersRdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7dd9580842d726de1d1441c44409780f0b1420b96a0b130a80646dd6bb61e79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c654a16b0a55030733242b20785ec1b089ec89d97718a149ce0d8d1449307d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f809a452408c8c79c2fa239cc7a50cb4dd607b46146d8ba1cafb33774e6f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersRds]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersRds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersRds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9273bff13315e5fa941e41a3f8658e858460b56d388ae9096a0f26bbe593453c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersRedshift",
    jsii_struct_bases=[],
    name_mapping={
        "database": "database",
        "cluster_id": "clusterId",
        "host": "host",
        "port": "port",
    },
)
class QuicksightDataSourceParametersRedshift:
    def __init__(
        self,
        *,
        database: builtins.str,
        cluster_id: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#cluster_id QuicksightDataSource#cluster_id}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fab647b531b9647f0ab38a31f87a4d0b7ca4ec20d46460f99a78288f8d764bf)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
        }
        if cluster_id is not None:
            self._values["cluster_id"] = cluster_id
        if host is not None:
            self._values["host"] = host
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#cluster_id QuicksightDataSource#cluster_id}.'''
        result = self._values.get("cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersRedshift(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersRedshiftOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersRedshiftOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__750c31a337998a337228fda9a9a32754e4e7079619389f9ee3c987995a3c5c80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClusterId")
    def reset_cluster_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterId", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__061ea4b0a2d352d36baf58aec06837696343a5d297d8a062fc362b6a6190c67f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03054049f6a01daa53c0c8ec060f16859a8d3d2aa3b35e10ac706ecb6c55be62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bead7d2a902f24ef2492feb26daebe8edb0b8c970e1e79de1f18f9b65b9171c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1d253ee02b02bcffb52cbcf511b51e18eb2c7b2115dd1c9a1ed161c6e63b4bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersRedshift]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersRedshift], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersRedshift],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc2992a43c8eda8b51b685d54b69bf69547c3308a33e11742a1e3bb861ba2f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersS3",
    jsii_struct_bases=[],
    name_mapping={
        "manifest_file_location": "manifestFileLocation",
        "role_arn": "roleArn",
    },
)
class QuicksightDataSourceParametersS3:
    def __init__(
        self,
        *,
        manifest_file_location: typing.Union["QuicksightDataSourceParametersS3ManifestFileLocation", typing.Dict[builtins.str, typing.Any]],
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param manifest_file_location: manifest_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#manifest_file_location QuicksightDataSource#manifest_file_location}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#role_arn QuicksightDataSource#role_arn}.
        '''
        if isinstance(manifest_file_location, dict):
            manifest_file_location = QuicksightDataSourceParametersS3ManifestFileLocation(**manifest_file_location)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc9eedb5550a67107c3c55725c7f61b4bb801d6d451bae40f4fb359ab37cf18)
            check_type(argname="argument manifest_file_location", value=manifest_file_location, expected_type=type_hints["manifest_file_location"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "manifest_file_location": manifest_file_location,
        }
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def manifest_file_location(
        self,
    ) -> "QuicksightDataSourceParametersS3ManifestFileLocation":
        '''manifest_file_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#manifest_file_location QuicksightDataSource#manifest_file_location}
        '''
        result = self._values.get("manifest_file_location")
        assert result is not None, "Required property 'manifest_file_location' is missing"
        return typing.cast("QuicksightDataSourceParametersS3ManifestFileLocation", result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#role_arn QuicksightDataSource#role_arn}.'''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersS3ManifestFileLocation",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "key": "key"},
)
class QuicksightDataSourceParametersS3ManifestFileLocation:
    def __init__(self, *, bucket: builtins.str, key: builtins.str) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#bucket QuicksightDataSource#bucket}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#key QuicksightDataSource#key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2811c9075081fc5f5b9812fd36022c63aa01bb8fd113e289aa47c303827814e)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "key": key,
        }

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#bucket QuicksightDataSource#bucket}.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#key QuicksightDataSource#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersS3ManifestFileLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersS3ManifestFileLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersS3ManifestFileLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d67416bc254f9619786cfc760450814a14befe7058210f793a057c5071f1899d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__66733e93d37e469db205196fcc7688e6179ec0b66229e7679a6733a9c2bc9d16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbc5fe8c0520f025561849a21fdb2b0400e6d9be7ebbb58eedb742552e8bc9fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersS3ManifestFileLocation]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersS3ManifestFileLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersS3ManifestFileLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c33a90c395ed47c858a4ae8593ae0025adb8b600762d92b50e66775393c7797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSourceParametersS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersS3OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__245d6340d3005bc84312bfc9577e128b69e4db7d7fec9574824fa05333266cee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putManifestFileLocation")
    def put_manifest_file_location(
        self,
        *,
        bucket: builtins.str,
        key: builtins.str,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#bucket QuicksightDataSource#bucket}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#key QuicksightDataSource#key}.
        '''
        value = QuicksightDataSourceParametersS3ManifestFileLocation(
            bucket=bucket, key=key
        )

        return typing.cast(None, jsii.invoke(self, "putManifestFileLocation", [value]))

    @jsii.member(jsii_name="resetRoleArn")
    def reset_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleArn", []))

    @builtins.property
    @jsii.member(jsii_name="manifestFileLocation")
    def manifest_file_location(
        self,
    ) -> QuicksightDataSourceParametersS3ManifestFileLocationOutputReference:
        return typing.cast(QuicksightDataSourceParametersS3ManifestFileLocationOutputReference, jsii.get(self, "manifestFileLocation"))

    @builtins.property
    @jsii.member(jsii_name="manifestFileLocationInput")
    def manifest_file_location_input(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersS3ManifestFileLocation]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersS3ManifestFileLocation], jsii.get(self, "manifestFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69bcb2ab4a73b390f01dee7e8b63495984d37bffce5530a502d814ae15ad630a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersS3]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersS3], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersS3],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0bebe61ba2099dbfa0ae22561bfedeeca96950a645df74263a8831cadf381f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersServiceNow",
    jsii_struct_bases=[],
    name_mapping={"site_base_url": "siteBaseUrl"},
)
class QuicksightDataSourceParametersServiceNow:
    def __init__(self, *, site_base_url: builtins.str) -> None:
        '''
        :param site_base_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#site_base_url QuicksightDataSource#site_base_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60f68195b7b371dd96f4a7c04bbf5336d816f875a99cf3dd702959f7df5a3676)
            check_type(argname="argument site_base_url", value=site_base_url, expected_type=type_hints["site_base_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "site_base_url": site_base_url,
        }

    @builtins.property
    def site_base_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#site_base_url QuicksightDataSource#site_base_url}.'''
        result = self._values.get("site_base_url")
        assert result is not None, "Required property 'site_base_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersServiceNow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersServiceNowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersServiceNowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af521d3fa877cc0f56ccd1f468d56eea334021fc10aa2ab6675a646ba40271b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="siteBaseUrlInput")
    def site_base_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "siteBaseUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="siteBaseUrl")
    def site_base_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "siteBaseUrl"))

    @site_base_url.setter
    def site_base_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4784a9b76489e9e3a035dd0952ea938947a042ff8e54b76c8ff76770d5b0c12e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "siteBaseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersServiceNow]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersServiceNow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersServiceNow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68691fbf58f14e0a0f18003dd49ad6d170913e1fc3cb97087c1ebd976e8e797c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersSnowflake",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "host": "host", "warehouse": "warehouse"},
)
class QuicksightDataSourceParametersSnowflake:
    def __init__(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        warehouse: builtins.str,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param warehouse: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#warehouse QuicksightDataSource#warehouse}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73b603b1e7cd3a2e7cb36d00c2efe580915363f59448b3597cb2d0af50c8e8ae)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument warehouse", value=warehouse, expected_type=type_hints["warehouse"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "host": host,
            "warehouse": warehouse,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def warehouse(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#warehouse QuicksightDataSource#warehouse}.'''
        result = self._values.get("warehouse")
        assert result is not None, "Required property 'warehouse' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersSnowflake(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersSnowflakeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersSnowflakeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a16a1766a2f26219468c34993e63fa1264d496eb80bd0f6305d1e9e930937a24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="warehouseInput")
    def warehouse_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warehouseInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__424e21e684e3c57537f23fa27a4ebf146b0f43bfb2772943a2b623ead2079e17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60de28b9bdae4e33395415fb86a54cb6505c9f1e772738265e34581c972fc578)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warehouse")
    def warehouse(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warehouse"))

    @warehouse.setter
    def warehouse(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bcfb63df8a3c6769d30454ecd5b5a9ff5186b9f49670a07eed5a8f419f457e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warehouse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersSnowflake]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersSnowflake], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersSnowflake],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e9fbea334cbb53a594c9c34a830a38a8d780b940136d2833ec4e1aa34803e4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersSpark",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "port": "port"},
)
class QuicksightDataSourceParametersSpark:
    def __init__(self, *, host: builtins.str, port: jsii.Number) -> None:
        '''
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18088f365bb9402026e5c26c6966838bc9ef017647b3e5f318d2b76f9b1836bf)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host": host,
            "port": port,
        }

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersSpark(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersSparkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersSparkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4936200e9586b7be50b43cdf851d9fc696a7ce49e78ce0b088022b748187696f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e2905dd4c95d469b87945999cec9edfa22f53c57e3a980150770cf91e6b682)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b4837d4c28aca18d2bec35e8060a4058012584d63d1a07bf685c702cb0f946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersSpark]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersSpark], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersSpark],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__942b240ce9f4def0ec12e1b99c5c6b53c47d67b265802756b1d2183dda52b4aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersSqlServer",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "host": "host", "port": "port"},
)
class QuicksightDataSourceParametersSqlServer:
    def __init__(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56e01cb16b4b21272b2b61328039aad0a95b3707bacbb10507a6055fe52e3b3e)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "host": host,
            "port": port,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersSqlServer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersSqlServerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersSqlServerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fb0f6b2ad5f24e96ce461948e02c92e7ca9affb1cd8f0f3d9c545ff1bcb60b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2228f0daa944741a347c30fdb8a298949e131499f057ed23342c84903eb257ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98dae5c31777907c5f5432272122a13c154c50f06f1d51c94f6d4630c477e0dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d35ffeedab005afa598a7c9457c038416dbd876f38a4835bd2f067a4f188ea10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersSqlServer]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersSqlServer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersSqlServer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__628b7b446033f5b02b5fe9a22fe28891b34483fd978222cc5111802c41af3874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersTeradata",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "host": "host", "port": "port"},
)
class QuicksightDataSourceParametersTeradata:
    def __init__(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a181460efaa7db4be45c5bf5fa1045f79fdea53154bfd8bd65572ea1e03379fa)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "host": host,
            "port": port,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersTeradata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersTeradataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersTeradataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1dc71ae77656ac694ccfc193648282926df7f4acf1826d8683c15bf2902495e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b504fc33b874fd012ae4a64d61217aac0825e0126b8d130979cad4eeb06defc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__706bdb92fe06eb4bc1e4e37964df06ac085dc89e449c69b3d2274d1213535417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4006c0f2f6c16ff582d24438b1b9e5805c10a68fc2152b4cd0cef09155a1bacc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersTeradata]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersTeradata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersTeradata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9c7feb1f0e17a43d2121d25f1164c45e2411688a9939141e4970e1419d8171d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersTwitter",
    jsii_struct_bases=[],
    name_mapping={"max_rows": "maxRows", "query": "query"},
)
class QuicksightDataSourceParametersTwitter:
    def __init__(self, *, max_rows: jsii.Number, query: builtins.str) -> None:
        '''
        :param max_rows: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#max_rows QuicksightDataSource#max_rows}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#query QuicksightDataSource#query}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94aa9b7374586c3e44db31a527fb69c64693bb8c4856d74d4c03ea7e16779bd1)
            check_type(argname="argument max_rows", value=max_rows, expected_type=type_hints["max_rows"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_rows": max_rows,
            "query": query,
        }

    @builtins.property
    def max_rows(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#max_rows QuicksightDataSource#max_rows}.'''
        result = self._values.get("max_rows")
        assert result is not None, "Required property 'max_rows' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def query(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#query QuicksightDataSource#query}.'''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersTwitter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersTwitterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceParametersTwitterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9910709e3a6d08ee73b88b4d4f6ce6a792bd72deb2701f7d040a131fdac1ce0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maxRowsInput")
    def max_rows_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRowsInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRows")
    def max_rows(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRows"))

    @max_rows.setter
    def max_rows(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5855fac7a161c86fed1f7d93ce875a4bf818148555b52adb91fca78a5a66bdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRows", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8115db9a0410e3e8b7e4c888ed7949b23e6e192807b31795afa1ea4c33bd8da0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersTwitter]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersTwitter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersTwitter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34928ec47a62a2212dd0bd02f9dac82333a1246567118dd6d038598ff5600ff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourcePermission",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions", "principal": "principal"},
)
class QuicksightDataSourcePermission:
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        principal: builtins.str,
    ) -> None:
        '''
        :param actions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#actions QuicksightDataSource#actions}.
        :param principal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#principal QuicksightDataSource#principal}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de64c8173d3cfcda95dbbd937ab4fa5df84f3265abdb13f2daa2a08370d9afee)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "principal": principal,
        }

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#actions QuicksightDataSource#actions}.'''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def principal(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#principal QuicksightDataSource#principal}.'''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourcePermission(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourcePermissionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourcePermissionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3991ad96ec691c30aae6167c962dc47553dbaeca5db1ddc49307b078c7c7369)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSourcePermissionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e4492bf6f6dd92a9006ea8917d699e833f7edad195d6c17b825c9b895e39182)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSourcePermissionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__163cd5f574c1ce3dce18bdb08ecae2aab3f05f8b09dbd4dc46a784d8513acb5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b38be7824e2da3f043525ffd70cacfd44f01d430b12ab34c241c04777a0d608)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4642e8e105ec7b9e1f96c19f772b30f05f2cf212fe230abbade2bca2e4180502)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSourcePermission]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSourcePermission]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSourcePermission]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90a9400414e30016f6dad350de41725f5f164c4bf92f1032a790933c00f1eeb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSourcePermissionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourcePermissionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88b93d06dcea85a39e8d2fcdb109cf26ae71dc9d8da0d23d741760b95dfd29cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="principalInput")
    def principal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalInput"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0df5db82ef372d320b60ba6929105ac659005f3e16aaf2ff01eb23187cb2d5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principal"))

    @principal.setter
    def principal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__748a1f44547d4e6a6f0ef69fe2b29cd53a87f167cb53de716514f3fc3288dc5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSourcePermission]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSourcePermission]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSourcePermission]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0fcee57dfde015a004415cc74558381475abd75630f6435e575877b9ccdfc56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceSslProperties",
    jsii_struct_bases=[],
    name_mapping={"disable_ssl": "disableSsl"},
)
class QuicksightDataSourceSslProperties:
    def __init__(
        self,
        *,
        disable_ssl: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param disable_ssl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#disable_ssl QuicksightDataSource#disable_ssl}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14531cbe337c97469f531dcf9be55efdccd941ff41602a1731071f570c43b06c)
            check_type(argname="argument disable_ssl", value=disable_ssl, expected_type=type_hints["disable_ssl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disable_ssl": disable_ssl,
        }

    @builtins.property
    def disable_ssl(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#disable_ssl QuicksightDataSource#disable_ssl}.'''
        result = self._values.get("disable_ssl")
        assert result is not None, "Required property 'disable_ssl' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceSslProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceSslPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceSslPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__400c3340a96e323c705807fdd1dda59f9ecad81bd0e0232c75afd585df34b40d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="disableSslInput")
    def disable_ssl_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableSslInput"))

    @builtins.property
    @jsii.member(jsii_name="disableSsl")
    def disable_ssl(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableSsl"))

    @disable_ssl.setter
    def disable_ssl(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7293f0bea60140edc111fd83367ea6b0bb630bdf5ff1d7a1b6ed7001d44f8d3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableSsl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceSslProperties]:
        return typing.cast(typing.Optional[QuicksightDataSourceSslProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceSslProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f23e14727048b2115e9bfab96c3b50008adcde7654adae2e4d6aa1551ea8f53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceVpcConnectionProperties",
    jsii_struct_bases=[],
    name_mapping={"vpc_connection_arn": "vpcConnectionArn"},
)
class QuicksightDataSourceVpcConnectionProperties:
    def __init__(self, *, vpc_connection_arn: builtins.str) -> None:
        '''
        :param vpc_connection_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#vpc_connection_arn QuicksightDataSource#vpc_connection_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b9f88818c66a63f9d140a6a111c82e11f8931378ea9e7249a561565a541e766)
            check_type(argname="argument vpc_connection_arn", value=vpc_connection_arn, expected_type=type_hints["vpc_connection_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc_connection_arn": vpc_connection_arn,
        }

    @builtins.property
    def vpc_connection_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_source#vpc_connection_arn QuicksightDataSource#vpc_connection_arn}.'''
        result = self._values.get("vpc_connection_arn")
        assert result is not None, "Required property 'vpc_connection_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceVpcConnectionProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceVpcConnectionPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSource.QuicksightDataSourceVpcConnectionPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9602a2ad2336ea95849e2ead9f5de2efbc74d41fb50920d088e09e3da183a2f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="vpcConnectionArnInput")
    def vpc_connection_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcConnectionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectionArn")
    def vpc_connection_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcConnectionArn"))

    @vpc_connection_arn.setter
    def vpc_connection_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f58f96a18e17195d75ac7a41d012c77517c9d86105a8f8349fbbd7387450e940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConnectionArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceVpcConnectionProperties]:
        return typing.cast(typing.Optional[QuicksightDataSourceVpcConnectionProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceVpcConnectionProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9b6ca8a5e6d616f70d62abf6450fc74195a7a12aec611d4c91433d7da86dcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "QuicksightDataSource",
    "QuicksightDataSourceConfig",
    "QuicksightDataSourceCredentials",
    "QuicksightDataSourceCredentialsCredentialPair",
    "QuicksightDataSourceCredentialsCredentialPairOutputReference",
    "QuicksightDataSourceCredentialsOutputReference",
    "QuicksightDataSourceParameters",
    "QuicksightDataSourceParametersAmazonElasticsearch",
    "QuicksightDataSourceParametersAmazonElasticsearchOutputReference",
    "QuicksightDataSourceParametersAthena",
    "QuicksightDataSourceParametersAthenaOutputReference",
    "QuicksightDataSourceParametersAurora",
    "QuicksightDataSourceParametersAuroraOutputReference",
    "QuicksightDataSourceParametersAuroraPostgresql",
    "QuicksightDataSourceParametersAuroraPostgresqlOutputReference",
    "QuicksightDataSourceParametersAwsIotAnalytics",
    "QuicksightDataSourceParametersAwsIotAnalyticsOutputReference",
    "QuicksightDataSourceParametersDatabricks",
    "QuicksightDataSourceParametersDatabricksOutputReference",
    "QuicksightDataSourceParametersJira",
    "QuicksightDataSourceParametersJiraOutputReference",
    "QuicksightDataSourceParametersMariaDb",
    "QuicksightDataSourceParametersMariaDbOutputReference",
    "QuicksightDataSourceParametersMysql",
    "QuicksightDataSourceParametersMysqlOutputReference",
    "QuicksightDataSourceParametersOracle",
    "QuicksightDataSourceParametersOracleOutputReference",
    "QuicksightDataSourceParametersOutputReference",
    "QuicksightDataSourceParametersPostgresql",
    "QuicksightDataSourceParametersPostgresqlOutputReference",
    "QuicksightDataSourceParametersPresto",
    "QuicksightDataSourceParametersPrestoOutputReference",
    "QuicksightDataSourceParametersRds",
    "QuicksightDataSourceParametersRdsOutputReference",
    "QuicksightDataSourceParametersRedshift",
    "QuicksightDataSourceParametersRedshiftOutputReference",
    "QuicksightDataSourceParametersS3",
    "QuicksightDataSourceParametersS3ManifestFileLocation",
    "QuicksightDataSourceParametersS3ManifestFileLocationOutputReference",
    "QuicksightDataSourceParametersS3OutputReference",
    "QuicksightDataSourceParametersServiceNow",
    "QuicksightDataSourceParametersServiceNowOutputReference",
    "QuicksightDataSourceParametersSnowflake",
    "QuicksightDataSourceParametersSnowflakeOutputReference",
    "QuicksightDataSourceParametersSpark",
    "QuicksightDataSourceParametersSparkOutputReference",
    "QuicksightDataSourceParametersSqlServer",
    "QuicksightDataSourceParametersSqlServerOutputReference",
    "QuicksightDataSourceParametersTeradata",
    "QuicksightDataSourceParametersTeradataOutputReference",
    "QuicksightDataSourceParametersTwitter",
    "QuicksightDataSourceParametersTwitterOutputReference",
    "QuicksightDataSourcePermission",
    "QuicksightDataSourcePermissionList",
    "QuicksightDataSourcePermissionOutputReference",
    "QuicksightDataSourceSslProperties",
    "QuicksightDataSourceSslPropertiesOutputReference",
    "QuicksightDataSourceVpcConnectionProperties",
    "QuicksightDataSourceVpcConnectionPropertiesOutputReference",
]

publication.publish()

def _typecheckingstub__64f521bc07fa829c901e7c259eae9c0bc5f2ff42d697340485acf176dbf2099e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_source_id: builtins.str,
    name: builtins.str,
    parameters: typing.Union[QuicksightDataSourceParameters, typing.Dict[builtins.str, typing.Any]],
    type: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[typing.Union[QuicksightDataSourceCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    permission: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSourcePermission, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    ssl_properties: typing.Optional[typing.Union[QuicksightDataSourceSslProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc_connection_properties: typing.Optional[typing.Union[QuicksightDataSourceVpcConnectionProperties, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__408dccce1bea53b4774cc09246bf71527051f28c322afa2def65eaa2b397db34(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba7ea09652a0486acb873d7c8b0b9fddfd284bdeb1e90ff2614703e89d2848e9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSourcePermission, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2916473405841ba70b3b1f14a52400b49570f7fd8fc33585a940cb55cf9bc02b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a516abd158f8ea291013a0b7fbd247322a9a855ecd256325b2e2956ff5c459f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9ad5f04327592fe6c5d9cfba051d3f76bb4a19153ef7d6606f335afbce8c41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48b0bac5c0973ada5c09beafc86d6907857015261bffe13f762bbc9c20fd8ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5bac60893f0844b3c55429baa67300914fa11144929c8085fe862eec8cf49cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35426145e150c1a415a37a4115cd536b65c93c03842a0d698157f16fc3685432(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d585b84b4899b7a959dd9d17c060aca1577309aea189ea1958d3f5e8194b2c7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2bc4ba7ba524f30bc5fb619ef646769c07f1280ed315aa898af1e8e3db52227(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b5e65d223b9f62b5aba18f661ee6a8e177d1db3ff5d7b3c20000625123ba15(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_source_id: builtins.str,
    name: builtins.str,
    parameters: typing.Union[QuicksightDataSourceParameters, typing.Dict[builtins.str, typing.Any]],
    type: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[typing.Union[QuicksightDataSourceCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    permission: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSourcePermission, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    ssl_properties: typing.Optional[typing.Union[QuicksightDataSourceSslProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc_connection_properties: typing.Optional[typing.Union[QuicksightDataSourceVpcConnectionProperties, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fdda683b4c66e6c67769671cd0821304896378bd29d76512782ab3286d179af(
    *,
    copy_source_arn: typing.Optional[builtins.str] = None,
    credential_pair: typing.Optional[typing.Union[QuicksightDataSourceCredentialsCredentialPair, typing.Dict[builtins.str, typing.Any]]] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__655544d0fc3f46aa970f1c05d056414d75519ca6d1e12717d0f5cb7e6fa33b18(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ff810aac227c9f6c13f30a934651d5eb64fcf21d82deb82aecb866236cace4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ece8015f483c0fd0108901f83fe0cbbd6f9a7714f3c8423bd2092048a9445f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e7e858542fb9a85cce7af109173acc3bb7049f2c2b0c6cb3e1b804cba6d5d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4e1398b4b8c5c1bcc281edf12bf9ed2e806364c42875d976e9e2e79c71478d(
    value: typing.Optional[QuicksightDataSourceCredentialsCredentialPair],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f39de1b4f84809acac63c234315bcd4cd095f22190e3ffab778c44114fca6f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cecf8239a5c5baf742c5965aefe0f3d2f677c4058e4cd68a713a3195102188c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3d3543d687d42f472eb50711fcc049eb121a59fe40d85505b5e7b2e58f0e92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d68f942f3bb3858903f0195becb8cd647d696e099afbca763320e7aec094a0a(
    value: typing.Optional[QuicksightDataSourceCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5dc542306c18fd4586ba7ca0319c9a34b53baf08d513f5945efc51008f9e55b(
    *,
    amazon_elasticsearch: typing.Optional[typing.Union[QuicksightDataSourceParametersAmazonElasticsearch, typing.Dict[builtins.str, typing.Any]]] = None,
    athena: typing.Optional[typing.Union[QuicksightDataSourceParametersAthena, typing.Dict[builtins.str, typing.Any]]] = None,
    aurora: typing.Optional[typing.Union[QuicksightDataSourceParametersAurora, typing.Dict[builtins.str, typing.Any]]] = None,
    aurora_postgresql: typing.Optional[typing.Union[QuicksightDataSourceParametersAuroraPostgresql, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_iot_analytics: typing.Optional[typing.Union[QuicksightDataSourceParametersAwsIotAnalytics, typing.Dict[builtins.str, typing.Any]]] = None,
    databricks: typing.Optional[typing.Union[QuicksightDataSourceParametersDatabricks, typing.Dict[builtins.str, typing.Any]]] = None,
    jira: typing.Optional[typing.Union[QuicksightDataSourceParametersJira, typing.Dict[builtins.str, typing.Any]]] = None,
    maria_db: typing.Optional[typing.Union[QuicksightDataSourceParametersMariaDb, typing.Dict[builtins.str, typing.Any]]] = None,
    mysql: typing.Optional[typing.Union[QuicksightDataSourceParametersMysql, typing.Dict[builtins.str, typing.Any]]] = None,
    oracle: typing.Optional[typing.Union[QuicksightDataSourceParametersOracle, typing.Dict[builtins.str, typing.Any]]] = None,
    postgresql: typing.Optional[typing.Union[QuicksightDataSourceParametersPostgresql, typing.Dict[builtins.str, typing.Any]]] = None,
    presto: typing.Optional[typing.Union[QuicksightDataSourceParametersPresto, typing.Dict[builtins.str, typing.Any]]] = None,
    rds: typing.Optional[typing.Union[QuicksightDataSourceParametersRds, typing.Dict[builtins.str, typing.Any]]] = None,
    redshift: typing.Optional[typing.Union[QuicksightDataSourceParametersRedshift, typing.Dict[builtins.str, typing.Any]]] = None,
    s3: typing.Optional[typing.Union[QuicksightDataSourceParametersS3, typing.Dict[builtins.str, typing.Any]]] = None,
    service_now: typing.Optional[typing.Union[QuicksightDataSourceParametersServiceNow, typing.Dict[builtins.str, typing.Any]]] = None,
    snowflake: typing.Optional[typing.Union[QuicksightDataSourceParametersSnowflake, typing.Dict[builtins.str, typing.Any]]] = None,
    spark: typing.Optional[typing.Union[QuicksightDataSourceParametersSpark, typing.Dict[builtins.str, typing.Any]]] = None,
    sql_server: typing.Optional[typing.Union[QuicksightDataSourceParametersSqlServer, typing.Dict[builtins.str, typing.Any]]] = None,
    teradata: typing.Optional[typing.Union[QuicksightDataSourceParametersTeradata, typing.Dict[builtins.str, typing.Any]]] = None,
    twitter: typing.Optional[typing.Union[QuicksightDataSourceParametersTwitter, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1ad4c1b5406e4bdecf0ceb2d174d2dfcf1564c92e7b2e420e08bea7a51d0e1(
    *,
    domain: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fd8975ff26c895407f477d9881e6e7c070cb109542239ef65d6fd93c5d5fbd7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de59aaa73f3451a8d72c8247f87ff3e56a7281202491226593c7a6721c48402(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d119b87f13560a3f3784bb4fa21d4ef5d8677343c689f0d228a6222928e0a6c5(
    value: typing.Optional[QuicksightDataSourceParametersAmazonElasticsearch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c077c45cd252f449b63f9b86646602aadbcf1076430b7c32885143b22072103(
    *,
    work_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5798b5af515369d6d6309fafa8f32187e909ffc4f9fee09dbef8da83639688d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__059ad83ba75130c002f172ad741c0d5b40fd8b0894137e1572701e5bf72f0709(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a035244c9f4c624cf8b4f7e99e56f8d2c71bf858f593a51cbd5af930f9f612(
    value: typing.Optional[QuicksightDataSourceParametersAthena],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3221be6928f939a463c60cae7c51be1bf2df85c20094a1989d4d11c1f8f839b(
    *,
    database: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d27b5cde4e5e0e994872257f9a4d201e1edaa7972ae96fcb26da0ad4dc2be0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd317e60ab190286a3284066093c6a6fa47036de02b28471f327b4b70663587c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b1dc7725e2458be5f96b680432beb4b2e042545b93b067df3e920bad7722f44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af15745ef0401f3ccb94bdbaa6438df62accfb427677b5fac8cd2a0270de9436(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400d6e085900b9dab9a101f5edc79901b4f4f53767eeb7f764272d68c65f69c1(
    value: typing.Optional[QuicksightDataSourceParametersAurora],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8544c718d7191887936e8eadaf2a886850f4c827922a5c81754ef804707dd3ca(
    *,
    database: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1addd51dd4dd3f2e043db7af03edcd74c9ebdb4af984cc1cb412602629c5b20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba1ff93b802fb7be1778f311036e52d608e158b8b928a76e8500b6a2f509a731(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a94a40ab1611a5b78a8bc66bc7ebe07bf4eca55d53aded07c7e3252db8de7e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba2ba4aae3d853588fbdffc35aa12887ff41259657d2ed63d355a5e1aa03767(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82a7161f2eafa8a58a32db78333e4529c91afc61669babd0d0fa93f34019729(
    value: typing.Optional[QuicksightDataSourceParametersAuroraPostgresql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63889bea2a517e8bdd4c98b34a9c9703c0eb85113d20d65b2d0385367707d811(
    *,
    data_set_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00d0e66f6c14a4615b47c06e7ccfd5eb0bba68191afe6918980f7e6fd239189(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c6e62106db8cbf842b878ba50a2595a868f3d652f4900ac550da632294e3da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d2dd483d2a862ab3df0d4dfd497eba01eb8c1f3b6fa4cf004d48108fddb28a3(
    value: typing.Optional[QuicksightDataSourceParametersAwsIotAnalytics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb582731c89be5bbe2fa6dae0fd9389312f64bf1ec51a2ae6b35074b0bb8b49e(
    *,
    host: builtins.str,
    port: jsii.Number,
    sql_endpoint_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac1471a81a9ed6b0f01249ce8c09d37793fd22d22ac243443010ecdd1680aeb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06286320f1df86b8de45df5d49e1681542353f42a185d950e497845916b05e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff35a6d4a5656dedb92f3c95405afe64a6413ab27723aead08c741f325c05cb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775f85e1ba2e5c958fe436cec7be516478046080c572939d5cc2f8fb9344d885(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edd4e49f798844aac9ca2563619a7043813eb8e016d157630b24ed375103192c(
    value: typing.Optional[QuicksightDataSourceParametersDatabricks],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__964013b854ba2012be363ce801df04e653468275c845d48236be41582c71dec9(
    *,
    site_base_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a38899644f2463e8b5cc48b06019d9bd759632ac1573b9c8971cc7be46dde7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bfe600077756344f430e2addc1521fbf203fd3be05924358c845c7213b28db1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21915c78d5c566eaefc6bc3a799235dae80d99ca2b75488b85ac08e1ded4c4c4(
    value: typing.Optional[QuicksightDataSourceParametersJira],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b148b9b62fd8f193e172ce9b06ac8edd32ec05b0ff3de7e4557fd5707afa084(
    *,
    database: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c5193c093447891be793b068c5f6c57553362a84ad32f3c275fdabf826ab729(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d984081cee86f19ed164359a9b9d3cad4c1de5429c0fa386e67b828926b3f072(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb6f18561c876293f35a4ed91886810016b05f4a7782cb6670f880ae66a8bff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7362778103cbf953785d5bdee0fd3abbdb8752dd4fa92468add5a933ad0a6e6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b581593ae61f7047f436577577aaddb62465998919c3289bfe43de96d7b44a34(
    value: typing.Optional[QuicksightDataSourceParametersMariaDb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1818c154cebbf509f7fa32d0cb6ed8ecec5838f7c1cc59bea9c63747a93c52c(
    *,
    database: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5244a4e66370b2b4ceebb1ae5d9fdefa0bde312cb1851455ea7d065121d84392(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b73fce73b2e735b9773a759b19abf744b09095390cf703099467fdc459edfa9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77080187b76eaf902c026ef3576b988acfe9b6102b2544d8fa6334a5f5f9f3e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45d03a448c06b839402420f9d369608ffb6b3d6b29d72a359f57d7999d8df04(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37172d9b119ee851bf35415f95bdce1d948c89b37a284802dbe1d9e48392f42c(
    value: typing.Optional[QuicksightDataSourceParametersMysql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb61c51cd3a2cbd328150c747ce126091ff87b0fceb7f1ff3a3513d9a4e2d2ac(
    *,
    database: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad93c88e999616835212a8b9070e6de9101ff8a74688345d265bcf984704b1db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a68584119d7c6820b95812162d7596019418bea9cd5f1b1f7cb2e293173b40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0304244b16d4924b69f8bf3bd6e495182ba4e478e936d93f14acb483daa4380d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e6a034e6330bab4c619ce23183f5aa621843b34cb2f8e4780ba4879fef9499c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ff31bdb7e292b70e534752ebc395db29e156640872b45bf44663a5cf3d67ee(
    value: typing.Optional[QuicksightDataSourceParametersOracle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d32b3828798004ea6fb78a40b649c49512501ccb5c218bc2d4c8c526832811(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5925b5222b000bb86e98781226059ca530391c1a9ad4dcb7b2b072ef820e5c5(
    value: typing.Optional[QuicksightDataSourceParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ede637c834609ac19c7c37264b8eea95b4c09bf277afcf76535c94e4b07055(
    *,
    database: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8163b487c8df91d4af15c8a955920b8aed486bf12be2960651c36a859e37de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed841cd94d51359a5faea3dcb8e659757ba9dee13bf68f336cce89878296620(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15649ef402dd7ea3104178459df79d3d06d1640e45184e661bd3f0cb07963cdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a687051c9a593e67025502b3ab529ab67d32ce1d1599ce026010a19c5cda3e2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe5af0edb4ba008142164fd0dd3f10f58ada0f2177a9522325ac9f1947f6255(
    value: typing.Optional[QuicksightDataSourceParametersPostgresql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d4ecc40b995d47c6273128b4b7ffa28501ca12f4f12272cc9fc77f5ea9033f1(
    *,
    catalog: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1383d7169bf7499bfe836062594192105d80cd580bae952cf04a049d49940bbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06827b5d5c97580028f66aaf8036388026e42900609435eaa597e3ac7622b895(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef13e1723b0dfb8b3ec1b4a97c75398e2173a038fe1de40149e0e7c5165655b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d161fc9681bfff0bd187e5ec589d97de1a1af51099e7fbd72105fe87b57eef4f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e6fe5abd8302df73e47e9b2c6bab82ae7d8445d8090b2b8ba17e437300482f(
    value: typing.Optional[QuicksightDataSourceParametersPresto],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb8704106f444fe0984ec344fdeab88c7235aba0ae1a58d832932f29b8a30a6(
    *,
    database: builtins.str,
    instance_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7dd9580842d726de1d1441c44409780f0b1420b96a0b130a80646dd6bb61e79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c654a16b0a55030733242b20785ec1b089ec89d97718a149ce0d8d1449307d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f809a452408c8c79c2fa239cc7a50cb4dd607b46146d8ba1cafb33774e6f44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9273bff13315e5fa941e41a3f8658e858460b56d388ae9096a0f26bbe593453c(
    value: typing.Optional[QuicksightDataSourceParametersRds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fab647b531b9647f0ab38a31f87a4d0b7ca4ec20d46460f99a78288f8d764bf(
    *,
    database: builtins.str,
    cluster_id: typing.Optional[builtins.str] = None,
    host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__750c31a337998a337228fda9a9a32754e4e7079619389f9ee3c987995a3c5c80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061ea4b0a2d352d36baf58aec06837696343a5d297d8a062fc362b6a6190c67f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03054049f6a01daa53c0c8ec060f16859a8d3d2aa3b35e10ac706ecb6c55be62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bead7d2a902f24ef2492feb26daebe8edb0b8c970e1e79de1f18f9b65b9171c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d253ee02b02bcffb52cbcf511b51e18eb2c7b2115dd1c9a1ed161c6e63b4bc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc2992a43c8eda8b51b685d54b69bf69547c3308a33e11742a1e3bb861ba2f3(
    value: typing.Optional[QuicksightDataSourceParametersRedshift],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc9eedb5550a67107c3c55725c7f61b4bb801d6d451bae40f4fb359ab37cf18(
    *,
    manifest_file_location: typing.Union[QuicksightDataSourceParametersS3ManifestFileLocation, typing.Dict[builtins.str, typing.Any]],
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2811c9075081fc5f5b9812fd36022c63aa01bb8fd113e289aa47c303827814e(
    *,
    bucket: builtins.str,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67416bc254f9619786cfc760450814a14befe7058210f793a057c5071f1899d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66733e93d37e469db205196fcc7688e6179ec0b66229e7679a6733a9c2bc9d16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbc5fe8c0520f025561849a21fdb2b0400e6d9be7ebbb58eedb742552e8bc9fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c33a90c395ed47c858a4ae8593ae0025adb8b600762d92b50e66775393c7797(
    value: typing.Optional[QuicksightDataSourceParametersS3ManifestFileLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__245d6340d3005bc84312bfc9577e128b69e4db7d7fec9574824fa05333266cee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69bcb2ab4a73b390f01dee7e8b63495984d37bffce5530a502d814ae15ad630a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0bebe61ba2099dbfa0ae22561bfedeeca96950a645df74263a8831cadf381f6(
    value: typing.Optional[QuicksightDataSourceParametersS3],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f68195b7b371dd96f4a7c04bbf5336d816f875a99cf3dd702959f7df5a3676(
    *,
    site_base_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af521d3fa877cc0f56ccd1f468d56eea334021fc10aa2ab6675a646ba40271b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4784a9b76489e9e3a035dd0952ea938947a042ff8e54b76c8ff76770d5b0c12e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68691fbf58f14e0a0f18003dd49ad6d170913e1fc3cb97087c1ebd976e8e797c(
    value: typing.Optional[QuicksightDataSourceParametersServiceNow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b603b1e7cd3a2e7cb36d00c2efe580915363f59448b3597cb2d0af50c8e8ae(
    *,
    database: builtins.str,
    host: builtins.str,
    warehouse: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a16a1766a2f26219468c34993e63fa1264d496eb80bd0f6305d1e9e930937a24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424e21e684e3c57537f23fa27a4ebf146b0f43bfb2772943a2b623ead2079e17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60de28b9bdae4e33395415fb86a54cb6505c9f1e772738265e34581c972fc578(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bcfb63df8a3c6769d30454ecd5b5a9ff5186b9f49670a07eed5a8f419f457e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e9fbea334cbb53a594c9c34a830a38a8d780b940136d2833ec4e1aa34803e4e(
    value: typing.Optional[QuicksightDataSourceParametersSnowflake],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18088f365bb9402026e5c26c6966838bc9ef017647b3e5f318d2b76f9b1836bf(
    *,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4936200e9586b7be50b43cdf851d9fc696a7ce49e78ce0b088022b748187696f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e2905dd4c95d469b87945999cec9edfa22f53c57e3a980150770cf91e6b682(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b4837d4c28aca18d2bec35e8060a4058012584d63d1a07bf685c702cb0f946(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__942b240ce9f4def0ec12e1b99c5c6b53c47d67b265802756b1d2183dda52b4aa(
    value: typing.Optional[QuicksightDataSourceParametersSpark],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56e01cb16b4b21272b2b61328039aad0a95b3707bacbb10507a6055fe52e3b3e(
    *,
    database: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb0f6b2ad5f24e96ce461948e02c92e7ca9affb1cd8f0f3d9c545ff1bcb60b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2228f0daa944741a347c30fdb8a298949e131499f057ed23342c84903eb257ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98dae5c31777907c5f5432272122a13c154c50f06f1d51c94f6d4630c477e0dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35ffeedab005afa598a7c9457c038416dbd876f38a4835bd2f067a4f188ea10(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__628b7b446033f5b02b5fe9a22fe28891b34483fd978222cc5111802c41af3874(
    value: typing.Optional[QuicksightDataSourceParametersSqlServer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a181460efaa7db4be45c5bf5fa1045f79fdea53154bfd8bd65572ea1e03379fa(
    *,
    database: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1dc71ae77656ac694ccfc193648282926df7f4acf1826d8683c15bf2902495e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b504fc33b874fd012ae4a64d61217aac0825e0126b8d130979cad4eeb06defc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__706bdb92fe06eb4bc1e4e37964df06ac085dc89e449c69b3d2274d1213535417(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4006c0f2f6c16ff582d24438b1b9e5805c10a68fc2152b4cd0cef09155a1bacc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c7feb1f0e17a43d2121d25f1164c45e2411688a9939141e4970e1419d8171d(
    value: typing.Optional[QuicksightDataSourceParametersTeradata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94aa9b7374586c3e44db31a527fb69c64693bb8c4856d74d4c03ea7e16779bd1(
    *,
    max_rows: jsii.Number,
    query: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9910709e3a6d08ee73b88b4d4f6ce6a792bd72deb2701f7d040a131fdac1ce0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5855fac7a161c86fed1f7d93ce875a4bf818148555b52adb91fca78a5a66bdb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8115db9a0410e3e8b7e4c888ed7949b23e6e192807b31795afa1ea4c33bd8da0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34928ec47a62a2212dd0bd02f9dac82333a1246567118dd6d038598ff5600ff2(
    value: typing.Optional[QuicksightDataSourceParametersTwitter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de64c8173d3cfcda95dbbd937ab4fa5df84f3265abdb13f2daa2a08370d9afee(
    *,
    actions: typing.Sequence[builtins.str],
    principal: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3991ad96ec691c30aae6167c962dc47553dbaeca5db1ddc49307b078c7c7369(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4492bf6f6dd92a9006ea8917d699e833f7edad195d6c17b825c9b895e39182(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__163cd5f574c1ce3dce18bdb08ecae2aab3f05f8b09dbd4dc46a784d8513acb5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b38be7824e2da3f043525ffd70cacfd44f01d430b12ab34c241c04777a0d608(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4642e8e105ec7b9e1f96c19f772b30f05f2cf212fe230abbade2bca2e4180502(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90a9400414e30016f6dad350de41725f5f164c4bf92f1032a790933c00f1eeb6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSourcePermission]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b93d06dcea85a39e8d2fcdb109cf26ae71dc9d8da0d23d741760b95dfd29cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0df5db82ef372d320b60ba6929105ac659005f3e16aaf2ff01eb23187cb2d5f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748a1f44547d4e6a6f0ef69fe2b29cd53a87f167cb53de716514f3fc3288dc5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0fcee57dfde015a004415cc74558381475abd75630f6435e575877b9ccdfc56(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSourcePermission]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14531cbe337c97469f531dcf9be55efdccd941ff41602a1731071f570c43b06c(
    *,
    disable_ssl: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400c3340a96e323c705807fdd1dda59f9ecad81bd0e0232c75afd585df34b40d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7293f0bea60140edc111fd83367ea6b0bb630bdf5ff1d7a1b6ed7001d44f8d3e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f23e14727048b2115e9bfab96c3b50008adcde7654adae2e4d6aa1551ea8f53(
    value: typing.Optional[QuicksightDataSourceSslProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b9f88818c66a63f9d140a6a111c82e11f8931378ea9e7249a561565a541e766(
    *,
    vpc_connection_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9602a2ad2336ea95849e2ead9f5de2efbc74d41fb50920d088e09e3da183a2f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58f96a18e17195d75ac7a41d012c77517c9d86105a8f8349fbbd7387450e940(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9b6ca8a5e6d616f70d62abf6450fc74195a7a12aec611d4c91433d7da86dcc(
    value: typing.Optional[QuicksightDataSourceVpcConnectionProperties],
) -> None:
    """Type checking stubs"""
    pass
