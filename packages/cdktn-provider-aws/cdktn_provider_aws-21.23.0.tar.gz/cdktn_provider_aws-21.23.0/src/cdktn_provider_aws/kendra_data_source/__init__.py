r'''
# `aws_kendra_data_source`

Refer to the Terraform Registry for docs: [`aws_kendra_data_source`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source).
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


class KendraDataSource(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSource",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source aws_kendra_data_source}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        index_id: builtins.str,
        name: builtins.str,
        type: builtins.str,
        configuration: typing.Optional[typing.Union["KendraDataSourceConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_document_enrichment_configuration: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        language_code: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["KendraDataSourceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source aws_kendra_data_source} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param index_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#index_id KendraDataSource#index_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#name KendraDataSource#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#type KendraDataSource#type}.
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#configuration KendraDataSource#configuration}
        :param custom_document_enrichment_configuration: custom_document_enrichment_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#custom_document_enrichment_configuration KendraDataSource#custom_document_enrichment_configuration}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#description KendraDataSource#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#id KendraDataSource#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param language_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#language_code KendraDataSource#language_code}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#region KendraDataSource#region}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#role_arn KendraDataSource#role_arn}.
        :param schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#schedule KendraDataSource#schedule}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#tags KendraDataSource#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#tags_all KendraDataSource#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#timeouts KendraDataSource#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__601295c808dbd3bcca62f66fe95ad3079963a7a1605eeecc8ce27e49e7275101)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KendraDataSourceConfig(
            index_id=index_id,
            name=name,
            type=type,
            configuration=configuration,
            custom_document_enrichment_configuration=custom_document_enrichment_configuration,
            description=description,
            id=id,
            language_code=language_code,
            region=region,
            role_arn=role_arn,
            schedule=schedule,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a KendraDataSource resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KendraDataSource to import.
        :param import_from_id: The id of the existing KendraDataSource that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KendraDataSource to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e963f7af95b80df7f86dc0b492776c355f162e8a878a50d24dbe76becce79694)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfiguration")
    def put_configuration(
        self,
        *,
        s3_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationS3Configuration", typing.Dict[builtins.str, typing.Any]]] = None,
        template_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationTemplateConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        web_crawler_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param s3_configuration: s3_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#s3_configuration KendraDataSource#s3_configuration}
        :param template_configuration: template_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#template_configuration KendraDataSource#template_configuration}
        :param web_crawler_configuration: web_crawler_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#web_crawler_configuration KendraDataSource#web_crawler_configuration}
        '''
        value = KendraDataSourceConfiguration(
            s3_configuration=s3_configuration,
            template_configuration=template_configuration,
            web_crawler_configuration=web_crawler_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putConfiguration", [value]))

    @jsii.member(jsii_name="putCustomDocumentEnrichmentConfiguration")
    def put_custom_document_enrichment_configuration(
        self,
        *,
        inline_configurations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        post_extraction_hook_configuration: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        pre_extraction_hook_configuration: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param inline_configurations: inline_configurations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#inline_configurations KendraDataSource#inline_configurations}
        :param post_extraction_hook_configuration: post_extraction_hook_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#post_extraction_hook_configuration KendraDataSource#post_extraction_hook_configuration}
        :param pre_extraction_hook_configuration: pre_extraction_hook_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#pre_extraction_hook_configuration KendraDataSource#pre_extraction_hook_configuration}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#role_arn KendraDataSource#role_arn}.
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfiguration(
            inline_configurations=inline_configurations,
            post_extraction_hook_configuration=post_extraction_hook_configuration,
            pre_extraction_hook_configuration=pre_extraction_hook_configuration,
            role_arn=role_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomDocumentEnrichmentConfiguration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#create KendraDataSource#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#delete KendraDataSource#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#update KendraDataSource#update}.
        '''
        value = KendraDataSourceTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetConfiguration")
    def reset_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfiguration", []))

    @jsii.member(jsii_name="resetCustomDocumentEnrichmentConfiguration")
    def reset_custom_document_enrichment_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomDocumentEnrichmentConfiguration", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLanguageCode")
    def reset_language_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguageCode", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRoleArn")
    def reset_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleArn", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> "KendraDataSourceConfigurationOutputReference":
        return typing.cast("KendraDataSourceConfigurationOutputReference", jsii.get(self, "configuration"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="customDocumentEnrichmentConfiguration")
    def custom_document_enrichment_configuration(
        self,
    ) -> "KendraDataSourceCustomDocumentEnrichmentConfigurationOutputReference":
        return typing.cast("KendraDataSourceCustomDocumentEnrichmentConfigurationOutputReference", jsii.get(self, "customDocumentEnrichmentConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "KendraDataSourceTimeoutsOutputReference":
        return typing.cast("KendraDataSourceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="configurationInput")
    def configuration_input(self) -> typing.Optional["KendraDataSourceConfiguration"]:
        return typing.cast(typing.Optional["KendraDataSourceConfiguration"], jsii.get(self, "configurationInput"))

    @builtins.property
    @jsii.member(jsii_name="customDocumentEnrichmentConfigurationInput")
    def custom_document_enrichment_configuration_input(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfiguration"]:
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfiguration"], jsii.get(self, "customDocumentEnrichmentConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="indexIdInput")
    def index_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexIdInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCodeInput")
    def language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

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
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KendraDataSourceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KendraDataSourceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9414d39c9d6576175ef24b1024bef6f32dd09edb76f16c69d9ec3297f8bf425)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b96bd49078d7f4d10a29741fe638f3801b1c8a18571a79b4a755c7866b7f36e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indexId")
    def index_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indexId"))

    @index_id.setter
    def index_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25df564385bd9270144baba4898a615bffe610e051cb1d78c549a8b3950364c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a7ac653d97ee25f9b7d69e8ccfad0d3cdd2aeeabd6d536f876ba701c5562de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__872a4912312482ca4148d844cd46e8457c767f9de6968db2b33097b933a0599f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e8c2db16e35824e6ad3b3f5f1204dc838f1e484c339a21d0a008009472583d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a09669d2ae079be243e56fb3b0601954022448bc1cae527fb3664eb34a7ee44a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ea24ca14290c7461c6d94ccf34110b34c43ab860cbc9bb65e37e0645d92f02a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4809e09f1a3a0a07815d2be74e916e5539b1bcca9c246228cb0e69b6074344bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3237bb9bb1bb84fc3e627bd5c3f94146a44bb6e6c9d311e4bd09692d6ac40b7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bb088e6c51691fd60276568e5643c0999be4356f9b59787a8c0160aea574774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "index_id": "indexId",
        "name": "name",
        "type": "type",
        "configuration": "configuration",
        "custom_document_enrichment_configuration": "customDocumentEnrichmentConfiguration",
        "description": "description",
        "id": "id",
        "language_code": "languageCode",
        "region": "region",
        "role_arn": "roleArn",
        "schedule": "schedule",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class KendraDataSourceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        index_id: builtins.str,
        name: builtins.str,
        type: builtins.str,
        configuration: typing.Optional[typing.Union["KendraDataSourceConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_document_enrichment_configuration: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        language_code: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["KendraDataSourceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param index_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#index_id KendraDataSource#index_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#name KendraDataSource#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#type KendraDataSource#type}.
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#configuration KendraDataSource#configuration}
        :param custom_document_enrichment_configuration: custom_document_enrichment_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#custom_document_enrichment_configuration KendraDataSource#custom_document_enrichment_configuration}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#description KendraDataSource#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#id KendraDataSource#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param language_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#language_code KendraDataSource#language_code}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#region KendraDataSource#region}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#role_arn KendraDataSource#role_arn}.
        :param schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#schedule KendraDataSource#schedule}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#tags KendraDataSource#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#tags_all KendraDataSource#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#timeouts KendraDataSource#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(configuration, dict):
            configuration = KendraDataSourceConfiguration(**configuration)
        if isinstance(custom_document_enrichment_configuration, dict):
            custom_document_enrichment_configuration = KendraDataSourceCustomDocumentEnrichmentConfiguration(**custom_document_enrichment_configuration)
        if isinstance(timeouts, dict):
            timeouts = KendraDataSourceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afc7c62ed3175de52300a56dad30ffcc10d42233c9ce92d3d34ff144ce12dbec)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument index_id", value=index_id, expected_type=type_hints["index_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument custom_document_enrichment_configuration", value=custom_document_enrichment_configuration, expected_type=type_hints["custom_document_enrichment_configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "index_id": index_id,
            "name": name,
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
        if configuration is not None:
            self._values["configuration"] = configuration
        if custom_document_enrichment_configuration is not None:
            self._values["custom_document_enrichment_configuration"] = custom_document_enrichment_configuration
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if language_code is not None:
            self._values["language_code"] = language_code
        if region is not None:
            self._values["region"] = region
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if schedule is not None:
            self._values["schedule"] = schedule
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def index_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#index_id KendraDataSource#index_id}.'''
        result = self._values.get("index_id")
        assert result is not None, "Required property 'index_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#name KendraDataSource#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#type KendraDataSource#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration(self) -> typing.Optional["KendraDataSourceConfiguration"]:
        '''configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#configuration KendraDataSource#configuration}
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfiguration"], result)

    @builtins.property
    def custom_document_enrichment_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfiguration"]:
        '''custom_document_enrichment_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#custom_document_enrichment_configuration KendraDataSource#custom_document_enrichment_configuration}
        '''
        result = self._values.get("custom_document_enrichment_configuration")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfiguration"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#description KendraDataSource#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#id KendraDataSource#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def language_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#language_code KendraDataSource#language_code}.'''
        result = self._values.get("language_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#region KendraDataSource#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#role_arn KendraDataSource#role_arn}.'''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#schedule KendraDataSource#schedule}.'''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#tags KendraDataSource#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#tags_all KendraDataSource#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["KendraDataSourceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#timeouts KendraDataSource#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["KendraDataSourceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "s3_configuration": "s3Configuration",
        "template_configuration": "templateConfiguration",
        "web_crawler_configuration": "webCrawlerConfiguration",
    },
)
class KendraDataSourceConfiguration:
    def __init__(
        self,
        *,
        s3_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationS3Configuration", typing.Dict[builtins.str, typing.Any]]] = None,
        template_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationTemplateConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        web_crawler_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param s3_configuration: s3_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#s3_configuration KendraDataSource#s3_configuration}
        :param template_configuration: template_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#template_configuration KendraDataSource#template_configuration}
        :param web_crawler_configuration: web_crawler_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#web_crawler_configuration KendraDataSource#web_crawler_configuration}
        '''
        if isinstance(s3_configuration, dict):
            s3_configuration = KendraDataSourceConfigurationS3Configuration(**s3_configuration)
        if isinstance(template_configuration, dict):
            template_configuration = KendraDataSourceConfigurationTemplateConfiguration(**template_configuration)
        if isinstance(web_crawler_configuration, dict):
            web_crawler_configuration = KendraDataSourceConfigurationWebCrawlerConfiguration(**web_crawler_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33eed49f6ad43a0e4539a16e56a37e4add0430f2db747015aa1140e2a29b960d)
            check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
            check_type(argname="argument template_configuration", value=template_configuration, expected_type=type_hints["template_configuration"])
            check_type(argname="argument web_crawler_configuration", value=web_crawler_configuration, expected_type=type_hints["web_crawler_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3_configuration is not None:
            self._values["s3_configuration"] = s3_configuration
        if template_configuration is not None:
            self._values["template_configuration"] = template_configuration
        if web_crawler_configuration is not None:
            self._values["web_crawler_configuration"] = web_crawler_configuration

    @builtins.property
    def s3_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationS3Configuration"]:
        '''s3_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#s3_configuration KendraDataSource#s3_configuration}
        '''
        result = self._values.get("s3_configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfigurationS3Configuration"], result)

    @builtins.property
    def template_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationTemplateConfiguration"]:
        '''template_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#template_configuration KendraDataSource#template_configuration}
        '''
        result = self._values.get("template_configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfigurationTemplateConfiguration"], result)

    @builtins.property
    def web_crawler_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfiguration"]:
        '''web_crawler_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#web_crawler_configuration KendraDataSource#web_crawler_configuration}
        '''
        result = self._values.get("web_crawler_configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcae7d4a29d5adf2f7ed93c6062e00e741ae93a9f0fa425536e4aee08ffa5402)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putS3Configuration")
    def put_s3_configuration(
        self,
        *,
        bucket_name: builtins.str,
        access_control_list_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        documents_metadata_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#bucket_name KendraDataSource#bucket_name}.
        :param access_control_list_configuration: access_control_list_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#access_control_list_configuration KendraDataSource#access_control_list_configuration}
        :param documents_metadata_configuration: documents_metadata_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#documents_metadata_configuration KendraDataSource#documents_metadata_configuration}
        :param exclusion_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#exclusion_patterns KendraDataSource#exclusion_patterns}.
        :param inclusion_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#inclusion_patterns KendraDataSource#inclusion_patterns}.
        :param inclusion_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#inclusion_prefixes KendraDataSource#inclusion_prefixes}.
        '''
        value = KendraDataSourceConfigurationS3Configuration(
            bucket_name=bucket_name,
            access_control_list_configuration=access_control_list_configuration,
            documents_metadata_configuration=documents_metadata_configuration,
            exclusion_patterns=exclusion_patterns,
            inclusion_patterns=inclusion_patterns,
            inclusion_prefixes=inclusion_prefixes,
        )

        return typing.cast(None, jsii.invoke(self, "putS3Configuration", [value]))

    @jsii.member(jsii_name="putTemplateConfiguration")
    def put_template_configuration(self, *, template: builtins.str) -> None:
        '''
        :param template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#template KendraDataSource#template}.
        '''
        value = KendraDataSourceConfigurationTemplateConfiguration(template=template)

        return typing.cast(None, jsii.invoke(self, "putTemplateConfiguration", [value]))

    @jsii.member(jsii_name="putWebCrawlerConfiguration")
    def put_web_crawler_configuration(
        self,
        *,
        urls: typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationUrls", typing.Dict[builtins.str, typing.Any]],
        authentication_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        crawl_depth: typing.Optional[jsii.Number] = None,
        max_content_size_per_page_in_mega_bytes: typing.Optional[jsii.Number] = None,
        max_links_per_page: typing.Optional[jsii.Number] = None,
        max_urls_per_minute_crawl_rate: typing.Optional[jsii.Number] = None,
        proxy_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        url_exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        url_inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param urls: urls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#urls KendraDataSource#urls}
        :param authentication_configuration: authentication_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#authentication_configuration KendraDataSource#authentication_configuration}
        :param crawl_depth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#crawl_depth KendraDataSource#crawl_depth}.
        :param max_content_size_per_page_in_mega_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#max_content_size_per_page_in_mega_bytes KendraDataSource#max_content_size_per_page_in_mega_bytes}.
        :param max_links_per_page: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#max_links_per_page KendraDataSource#max_links_per_page}.
        :param max_urls_per_minute_crawl_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#max_urls_per_minute_crawl_rate KendraDataSource#max_urls_per_minute_crawl_rate}.
        :param proxy_configuration: proxy_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#proxy_configuration KendraDataSource#proxy_configuration}
        :param url_exclusion_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#url_exclusion_patterns KendraDataSource#url_exclusion_patterns}.
        :param url_inclusion_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#url_inclusion_patterns KendraDataSource#url_inclusion_patterns}.
        '''
        value = KendraDataSourceConfigurationWebCrawlerConfiguration(
            urls=urls,
            authentication_configuration=authentication_configuration,
            crawl_depth=crawl_depth,
            max_content_size_per_page_in_mega_bytes=max_content_size_per_page_in_mega_bytes,
            max_links_per_page=max_links_per_page,
            max_urls_per_minute_crawl_rate=max_urls_per_minute_crawl_rate,
            proxy_configuration=proxy_configuration,
            url_exclusion_patterns=url_exclusion_patterns,
            url_inclusion_patterns=url_inclusion_patterns,
        )

        return typing.cast(None, jsii.invoke(self, "putWebCrawlerConfiguration", [value]))

    @jsii.member(jsii_name="resetS3Configuration")
    def reset_s3_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Configuration", []))

    @jsii.member(jsii_name="resetTemplateConfiguration")
    def reset_template_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplateConfiguration", []))

    @jsii.member(jsii_name="resetWebCrawlerConfiguration")
    def reset_web_crawler_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebCrawlerConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="s3Configuration")
    def s3_configuration(
        self,
    ) -> "KendraDataSourceConfigurationS3ConfigurationOutputReference":
        return typing.cast("KendraDataSourceConfigurationS3ConfigurationOutputReference", jsii.get(self, "s3Configuration"))

    @builtins.property
    @jsii.member(jsii_name="templateConfiguration")
    def template_configuration(
        self,
    ) -> "KendraDataSourceConfigurationTemplateConfigurationOutputReference":
        return typing.cast("KendraDataSourceConfigurationTemplateConfigurationOutputReference", jsii.get(self, "templateConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="webCrawlerConfiguration")
    def web_crawler_configuration(
        self,
    ) -> "KendraDataSourceConfigurationWebCrawlerConfigurationOutputReference":
        return typing.cast("KendraDataSourceConfigurationWebCrawlerConfigurationOutputReference", jsii.get(self, "webCrawlerConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="s3ConfigurationInput")
    def s3_configuration_input(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationS3Configuration"]:
        return typing.cast(typing.Optional["KendraDataSourceConfigurationS3Configuration"], jsii.get(self, "s3ConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="templateConfigurationInput")
    def template_configuration_input(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationTemplateConfiguration"]:
        return typing.cast(typing.Optional["KendraDataSourceConfigurationTemplateConfiguration"], jsii.get(self, "templateConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="webCrawlerConfigurationInput")
    def web_crawler_configuration_input(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfiguration"]:
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfiguration"], jsii.get(self, "webCrawlerConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KendraDataSourceConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82184b8184002e7cf54975e92b3ada30847c0339924ed541a5ee2e5283f0541e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationS3Configuration",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "access_control_list_configuration": "accessControlListConfiguration",
        "documents_metadata_configuration": "documentsMetadataConfiguration",
        "exclusion_patterns": "exclusionPatterns",
        "inclusion_patterns": "inclusionPatterns",
        "inclusion_prefixes": "inclusionPrefixes",
    },
)
class KendraDataSourceConfigurationS3Configuration:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        access_control_list_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        documents_metadata_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#bucket_name KendraDataSource#bucket_name}.
        :param access_control_list_configuration: access_control_list_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#access_control_list_configuration KendraDataSource#access_control_list_configuration}
        :param documents_metadata_configuration: documents_metadata_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#documents_metadata_configuration KendraDataSource#documents_metadata_configuration}
        :param exclusion_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#exclusion_patterns KendraDataSource#exclusion_patterns}.
        :param inclusion_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#inclusion_patterns KendraDataSource#inclusion_patterns}.
        :param inclusion_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#inclusion_prefixes KendraDataSource#inclusion_prefixes}.
        '''
        if isinstance(access_control_list_configuration, dict):
            access_control_list_configuration = KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration(**access_control_list_configuration)
        if isinstance(documents_metadata_configuration, dict):
            documents_metadata_configuration = KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration(**documents_metadata_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5654b469bf49c68ede20f3759380d7ddb82296c368a806f5fa5ab9cc33a33d33)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument access_control_list_configuration", value=access_control_list_configuration, expected_type=type_hints["access_control_list_configuration"])
            check_type(argname="argument documents_metadata_configuration", value=documents_metadata_configuration, expected_type=type_hints["documents_metadata_configuration"])
            check_type(argname="argument exclusion_patterns", value=exclusion_patterns, expected_type=type_hints["exclusion_patterns"])
            check_type(argname="argument inclusion_patterns", value=inclusion_patterns, expected_type=type_hints["inclusion_patterns"])
            check_type(argname="argument inclusion_prefixes", value=inclusion_prefixes, expected_type=type_hints["inclusion_prefixes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
        }
        if access_control_list_configuration is not None:
            self._values["access_control_list_configuration"] = access_control_list_configuration
        if documents_metadata_configuration is not None:
            self._values["documents_metadata_configuration"] = documents_metadata_configuration
        if exclusion_patterns is not None:
            self._values["exclusion_patterns"] = exclusion_patterns
        if inclusion_patterns is not None:
            self._values["inclusion_patterns"] = inclusion_patterns
        if inclusion_prefixes is not None:
            self._values["inclusion_prefixes"] = inclusion_prefixes

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#bucket_name KendraDataSource#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_control_list_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration"]:
        '''access_control_list_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#access_control_list_configuration KendraDataSource#access_control_list_configuration}
        '''
        result = self._values.get("access_control_list_configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration"], result)

    @builtins.property
    def documents_metadata_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration"]:
        '''documents_metadata_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#documents_metadata_configuration KendraDataSource#documents_metadata_configuration}
        '''
        result = self._values.get("documents_metadata_configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration"], result)

    @builtins.property
    def exclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#exclusion_patterns KendraDataSource#exclusion_patterns}.'''
        result = self._values.get("exclusion_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def inclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#inclusion_patterns KendraDataSource#inclusion_patterns}.'''
        result = self._values.get("inclusion_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def inclusion_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#inclusion_prefixes KendraDataSource#inclusion_prefixes}.'''
        result = self._values.get("inclusion_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationS3Configuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration",
    jsii_struct_bases=[],
    name_mapping={"key_path": "keyPath"},
)
class KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration:
    def __init__(self, *, key_path: typing.Optional[builtins.str] = None) -> None:
        '''
        :param key_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#key_path KendraDataSource#key_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3ee47f4c373feeb2fb33e64b79bb9a36c6e2d2f93f1c632863030abfda18f97)
            check_type(argname="argument key_path", value=key_path, expected_type=type_hints["key_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key_path is not None:
            self._values["key_path"] = key_path

    @builtins.property
    def key_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#key_path KendraDataSource#key_path}.'''
        result = self._values.get("key_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceConfigurationS3ConfigurationAccessControlListConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationS3ConfigurationAccessControlListConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73b3bd03da2f48c60dea7a9713bd62c4719e64826f76b78d171b2bd921b928ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKeyPath")
    def reset_key_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyPath", []))

    @builtins.property
    @jsii.member(jsii_name="keyPathInput")
    def key_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyPathInput"))

    @builtins.property
    @jsii.member(jsii_name="keyPath")
    def key_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyPath"))

    @key_path.setter
    def key_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519e093483b2182bcd056509e206c2d9edb7f9afad6e90881504d2e576f9bd6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d400c32e303c3cdf06eaad204718a0d6f9156de2f0db39826deee2883872f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration",
    jsii_struct_bases=[],
    name_mapping={"s3_prefix": "s3Prefix"},
)
class KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration:
    def __init__(self, *, s3_prefix: typing.Optional[builtins.str] = None) -> None:
        '''
        :param s3_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#s3_prefix KendraDataSource#s3_prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e001b435b916cc761b681bafe11decf12fb4bbed0e488b8f4535018ead20364)
            check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3_prefix is not None:
            self._values["s3_prefix"] = s3_prefix

    @builtins.property
    def s3_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#s3_prefix KendraDataSource#s3_prefix}.'''
        result = self._values.get("s3_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdbe86ac294d08ae278bac22acf812dad89bca82bbcf2eac0e2fe6ba5e233492)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetS3Prefix")
    def reset_s3_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Prefix", []))

    @builtins.property
    @jsii.member(jsii_name="s3PrefixInput")
    def s3_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3PrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Prefix")
    def s3_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Prefix"))

    @s3_prefix.setter
    def s3_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088cb4e2599ef8f1d90ade9435dec1abe0a0de7a8ed5b39129bfa98a5708d594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86eb012b62a2e4423fdc38e0de0a49c458d1e83be06959084d49416e682e4322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceConfigurationS3ConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationS3ConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3caff72dccf4b5688c4ab1d9d855bc26d3aaf3f403aacbfbf7e4fb1a0ddd210b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccessControlListConfiguration")
    def put_access_control_list_configuration(
        self,
        *,
        key_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#key_path KendraDataSource#key_path}.
        '''
        value = KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration(
            key_path=key_path
        )

        return typing.cast(None, jsii.invoke(self, "putAccessControlListConfiguration", [value]))

    @jsii.member(jsii_name="putDocumentsMetadataConfiguration")
    def put_documents_metadata_configuration(
        self,
        *,
        s3_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#s3_prefix KendraDataSource#s3_prefix}.
        '''
        value = KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration(
            s3_prefix=s3_prefix
        )

        return typing.cast(None, jsii.invoke(self, "putDocumentsMetadataConfiguration", [value]))

    @jsii.member(jsii_name="resetAccessControlListConfiguration")
    def reset_access_control_list_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessControlListConfiguration", []))

    @jsii.member(jsii_name="resetDocumentsMetadataConfiguration")
    def reset_documents_metadata_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentsMetadataConfiguration", []))

    @jsii.member(jsii_name="resetExclusionPatterns")
    def reset_exclusion_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusionPatterns", []))

    @jsii.member(jsii_name="resetInclusionPatterns")
    def reset_inclusion_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInclusionPatterns", []))

    @jsii.member(jsii_name="resetInclusionPrefixes")
    def reset_inclusion_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInclusionPrefixes", []))

    @builtins.property
    @jsii.member(jsii_name="accessControlListConfiguration")
    def access_control_list_configuration(
        self,
    ) -> KendraDataSourceConfigurationS3ConfigurationAccessControlListConfigurationOutputReference:
        return typing.cast(KendraDataSourceConfigurationS3ConfigurationAccessControlListConfigurationOutputReference, jsii.get(self, "accessControlListConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="documentsMetadataConfiguration")
    def documents_metadata_configuration(
        self,
    ) -> KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfigurationOutputReference:
        return typing.cast(KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfigurationOutputReference, jsii.get(self, "documentsMetadataConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="accessControlListConfigurationInput")
    def access_control_list_configuration_input(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration], jsii.get(self, "accessControlListConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="documentsMetadataConfigurationInput")
    def documents_metadata_configuration_input(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration], jsii.get(self, "documentsMetadataConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionPatternsInput")
    def exclusion_patterns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exclusionPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="inclusionPatternsInput")
    def inclusion_patterns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inclusionPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="inclusionPrefixesInput")
    def inclusion_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inclusionPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58a44513c9920ef69f4327203b724a4a9c01b117bbcb5c8b65ffb86df6e2221b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusionPatterns")
    def exclusion_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclusionPatterns"))

    @exclusion_patterns.setter
    def exclusion_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9db6481adf1f0d50b5fd5ba965cc713429914c2a5f00f4a4897857c8487bb313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusionPatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inclusionPatterns")
    def inclusion_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inclusionPatterns"))

    @inclusion_patterns.setter
    def inclusion_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__058340ae8d0a950d65dc8a6b1e59070741a677a57a8c5367e0aa9f5d42e8a6be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inclusionPatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inclusionPrefixes")
    def inclusion_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inclusionPrefixes"))

    @inclusion_prefixes.setter
    def inclusion_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f992d3618c955055477da953edd2ea8732adcee2cb364330aa84f9291c0637)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inclusionPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationS3Configuration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationS3Configuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationS3Configuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__784da9c29762c81b7778c7b93d564fa0306c60b605462bb69fb017a3ac8ede93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationTemplateConfiguration",
    jsii_struct_bases=[],
    name_mapping={"template": "template"},
)
class KendraDataSourceConfigurationTemplateConfiguration:
    def __init__(self, *, template: builtins.str) -> None:
        '''
        :param template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#template KendraDataSource#template}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91fa636ebc2ae6e7965d921e82cf41bd2fe37ad098ea0b47061896e587717f5c)
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "template": template,
        }

    @builtins.property
    def template(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#template KendraDataSource#template}.'''
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationTemplateConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceConfigurationTemplateConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationTemplateConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b7284d709c85fec54bc7d29f2400dd8ceaed88dce678e577eb24499461f130c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="templateInput")
    def template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateInput"))

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "template"))

    @template.setter
    def template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32944546e297ba202cb4c6e9e42fd122251fa09703c504cfe3f3906caf538638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "template", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationTemplateConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationTemplateConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationTemplateConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b7ab5e46d70cbc67ec458900004b4abe6f5761e5f06a718cd0d5968f762ccc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "urls": "urls",
        "authentication_configuration": "authenticationConfiguration",
        "crawl_depth": "crawlDepth",
        "max_content_size_per_page_in_mega_bytes": "maxContentSizePerPageInMegaBytes",
        "max_links_per_page": "maxLinksPerPage",
        "max_urls_per_minute_crawl_rate": "maxUrlsPerMinuteCrawlRate",
        "proxy_configuration": "proxyConfiguration",
        "url_exclusion_patterns": "urlExclusionPatterns",
        "url_inclusion_patterns": "urlInclusionPatterns",
    },
)
class KendraDataSourceConfigurationWebCrawlerConfiguration:
    def __init__(
        self,
        *,
        urls: typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationUrls", typing.Dict[builtins.str, typing.Any]],
        authentication_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        crawl_depth: typing.Optional[jsii.Number] = None,
        max_content_size_per_page_in_mega_bytes: typing.Optional[jsii.Number] = None,
        max_links_per_page: typing.Optional[jsii.Number] = None,
        max_urls_per_minute_crawl_rate: typing.Optional[jsii.Number] = None,
        proxy_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        url_exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        url_inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param urls: urls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#urls KendraDataSource#urls}
        :param authentication_configuration: authentication_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#authentication_configuration KendraDataSource#authentication_configuration}
        :param crawl_depth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#crawl_depth KendraDataSource#crawl_depth}.
        :param max_content_size_per_page_in_mega_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#max_content_size_per_page_in_mega_bytes KendraDataSource#max_content_size_per_page_in_mega_bytes}.
        :param max_links_per_page: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#max_links_per_page KendraDataSource#max_links_per_page}.
        :param max_urls_per_minute_crawl_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#max_urls_per_minute_crawl_rate KendraDataSource#max_urls_per_minute_crawl_rate}.
        :param proxy_configuration: proxy_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#proxy_configuration KendraDataSource#proxy_configuration}
        :param url_exclusion_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#url_exclusion_patterns KendraDataSource#url_exclusion_patterns}.
        :param url_inclusion_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#url_inclusion_patterns KendraDataSource#url_inclusion_patterns}.
        '''
        if isinstance(urls, dict):
            urls = KendraDataSourceConfigurationWebCrawlerConfigurationUrls(**urls)
        if isinstance(authentication_configuration, dict):
            authentication_configuration = KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration(**authentication_configuration)
        if isinstance(proxy_configuration, dict):
            proxy_configuration = KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration(**proxy_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d144c53335874659fb463ef4fd40424ecf52fabcea8a246e4246b3b1477f4f)
            check_type(argname="argument urls", value=urls, expected_type=type_hints["urls"])
            check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
            check_type(argname="argument crawl_depth", value=crawl_depth, expected_type=type_hints["crawl_depth"])
            check_type(argname="argument max_content_size_per_page_in_mega_bytes", value=max_content_size_per_page_in_mega_bytes, expected_type=type_hints["max_content_size_per_page_in_mega_bytes"])
            check_type(argname="argument max_links_per_page", value=max_links_per_page, expected_type=type_hints["max_links_per_page"])
            check_type(argname="argument max_urls_per_minute_crawl_rate", value=max_urls_per_minute_crawl_rate, expected_type=type_hints["max_urls_per_minute_crawl_rate"])
            check_type(argname="argument proxy_configuration", value=proxy_configuration, expected_type=type_hints["proxy_configuration"])
            check_type(argname="argument url_exclusion_patterns", value=url_exclusion_patterns, expected_type=type_hints["url_exclusion_patterns"])
            check_type(argname="argument url_inclusion_patterns", value=url_inclusion_patterns, expected_type=type_hints["url_inclusion_patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "urls": urls,
        }
        if authentication_configuration is not None:
            self._values["authentication_configuration"] = authentication_configuration
        if crawl_depth is not None:
            self._values["crawl_depth"] = crawl_depth
        if max_content_size_per_page_in_mega_bytes is not None:
            self._values["max_content_size_per_page_in_mega_bytes"] = max_content_size_per_page_in_mega_bytes
        if max_links_per_page is not None:
            self._values["max_links_per_page"] = max_links_per_page
        if max_urls_per_minute_crawl_rate is not None:
            self._values["max_urls_per_minute_crawl_rate"] = max_urls_per_minute_crawl_rate
        if proxy_configuration is not None:
            self._values["proxy_configuration"] = proxy_configuration
        if url_exclusion_patterns is not None:
            self._values["url_exclusion_patterns"] = url_exclusion_patterns
        if url_inclusion_patterns is not None:
            self._values["url_inclusion_patterns"] = url_inclusion_patterns

    @builtins.property
    def urls(self) -> "KendraDataSourceConfigurationWebCrawlerConfigurationUrls":
        '''urls block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#urls KendraDataSource#urls}
        '''
        result = self._values.get("urls")
        assert result is not None, "Required property 'urls' is missing"
        return typing.cast("KendraDataSourceConfigurationWebCrawlerConfigurationUrls", result)

    @builtins.property
    def authentication_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration"]:
        '''authentication_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#authentication_configuration KendraDataSource#authentication_configuration}
        '''
        result = self._values.get("authentication_configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration"], result)

    @builtins.property
    def crawl_depth(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#crawl_depth KendraDataSource#crawl_depth}.'''
        result = self._values.get("crawl_depth")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_content_size_per_page_in_mega_bytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#max_content_size_per_page_in_mega_bytes KendraDataSource#max_content_size_per_page_in_mega_bytes}.'''
        result = self._values.get("max_content_size_per_page_in_mega_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_links_per_page(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#max_links_per_page KendraDataSource#max_links_per_page}.'''
        result = self._values.get("max_links_per_page")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_urls_per_minute_crawl_rate(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#max_urls_per_minute_crawl_rate KendraDataSource#max_urls_per_minute_crawl_rate}.'''
        result = self._values.get("max_urls_per_minute_crawl_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def proxy_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration"]:
        '''proxy_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#proxy_configuration KendraDataSource#proxy_configuration}
        '''
        result = self._values.get("proxy_configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration"], result)

    @builtins.property
    def url_exclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#url_exclusion_patterns KendraDataSource#url_exclusion_patterns}.'''
        result = self._values.get("url_exclusion_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def url_inclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#url_inclusion_patterns KendraDataSource#url_inclusion_patterns}.'''
        result = self._values.get("url_inclusion_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationWebCrawlerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration",
    jsii_struct_bases=[],
    name_mapping={"basic_authentication": "basicAuthentication"},
)
class KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration:
    def __init__(
        self,
        *,
        basic_authentication: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param basic_authentication: basic_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#basic_authentication KendraDataSource#basic_authentication}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1e97f4755f274ba94dd88edd04736dd486904719d36f3aad60be0fb7f363235)
            check_type(argname="argument basic_authentication", value=basic_authentication, expected_type=type_hints["basic_authentication"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if basic_authentication is not None:
            self._values["basic_authentication"] = basic_authentication

    @builtins.property
    def basic_authentication(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication"]]]:
        '''basic_authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#basic_authentication KendraDataSource#basic_authentication}
        '''
        result = self._values.get("basic_authentication")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication",
    jsii_struct_bases=[],
    name_mapping={"credentials": "credentials", "host": "host", "port": "port"},
)
class KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication:
    def __init__(
        self,
        *,
        credentials: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#credentials KendraDataSource#credentials}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#host KendraDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#port KendraDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dd7091456d97da8163fa071443c814eed0e781e9c658c9321b1caa4b47b15e0)
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "credentials": credentials,
            "host": host,
            "port": port,
        }

    @builtins.property
    def credentials(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#credentials KendraDataSource#credentials}.'''
        result = self._values.get("credentials")
        assert result is not None, "Required property 'credentials' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#host KendraDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#port KendraDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd8d0675a2489d557532b963438a4e7f1741f9d7bd3a4ee988bd6bf6cb6926ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef3344928d5e4a39c006d2855ea979a66b6713c99518f749fc7048789ea6e17)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2844c54df9e77c6fab64cb26397ee1846867b0507d1c7de1e690d6235ef1b086)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61be02f8426c0b3d8ae12a152b6d200ec02735098486bf892c6893f56459672b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__571e40fd4e84969ad128a64c32188b1f455348bd43be3c2455c8c49dd5361220)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac6366db632465583cf9805b93d636fab32eb73da11f63b6d8afed6182189b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__474b82d05f48a8067d93455691f788996b7b67250882f3d11f6d01bfff9a027d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentials"))

    @credentials.setter
    def credentials(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c31a7b783664f009fd82a188202f2c9734eaf8bca0c8e8f5baf10fa4446a71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fed15c788f9b45886942744d9b89aa7cc957575efa3dc85d44fe44f0755f04e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c89a29890fb37d66082e538322981c4c26b925ae37e9f9884452a09892ddc26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d0b5584f6dd37e8666d8fa92b5b45d88c3b7e5ce2e1334edb2a8f2903c2fa66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8212bcb25ffdd6ffe80c363d12b670004691c1bae617fe2871cbdfaf38d7b4f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBasicAuthentication")
    def put_basic_authentication(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc3335c826e986763e6d0d6f6191c3cf080accae9f3f79dd39d3011e30253c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBasicAuthentication", [value]))

    @jsii.member(jsii_name="resetBasicAuthentication")
    def reset_basic_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasicAuthentication", []))

    @builtins.property
    @jsii.member(jsii_name="basicAuthentication")
    def basic_authentication(
        self,
    ) -> KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationList:
        return typing.cast(KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationList, jsii.get(self, "basicAuthentication"))

    @builtins.property
    @jsii.member(jsii_name="basicAuthenticationInput")
    def basic_authentication_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]]], jsii.get(self, "basicAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__710933ed8c6cd0548401168f2f468825831122068a6cb617604df5d9d680ee33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceConfigurationWebCrawlerConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__866c491357da916c17bccfc78d328120007adc4308adc1a153722f6813d03390)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthenticationConfiguration")
    def put_authentication_configuration(
        self,
        *,
        basic_authentication: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param basic_authentication: basic_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#basic_authentication KendraDataSource#basic_authentication}
        '''
        value = KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration(
            basic_authentication=basic_authentication
        )

        return typing.cast(None, jsii.invoke(self, "putAuthenticationConfiguration", [value]))

    @jsii.member(jsii_name="putProxyConfiguration")
    def put_proxy_configuration(
        self,
        *,
        host: builtins.str,
        port: jsii.Number,
        credentials: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#host KendraDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#port KendraDataSource#port}.
        :param credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#credentials KendraDataSource#credentials}.
        '''
        value = KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration(
            host=host, port=port, credentials=credentials
        )

        return typing.cast(None, jsii.invoke(self, "putProxyConfiguration", [value]))

    @jsii.member(jsii_name="putUrls")
    def put_urls(
        self,
        *,
        seed_url_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        site_maps_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param seed_url_configuration: seed_url_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#seed_url_configuration KendraDataSource#seed_url_configuration}
        :param site_maps_configuration: site_maps_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#site_maps_configuration KendraDataSource#site_maps_configuration}
        '''
        value = KendraDataSourceConfigurationWebCrawlerConfigurationUrls(
            seed_url_configuration=seed_url_configuration,
            site_maps_configuration=site_maps_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putUrls", [value]))

    @jsii.member(jsii_name="resetAuthenticationConfiguration")
    def reset_authentication_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationConfiguration", []))

    @jsii.member(jsii_name="resetCrawlDepth")
    def reset_crawl_depth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrawlDepth", []))

    @jsii.member(jsii_name="resetMaxContentSizePerPageInMegaBytes")
    def reset_max_content_size_per_page_in_mega_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxContentSizePerPageInMegaBytes", []))

    @jsii.member(jsii_name="resetMaxLinksPerPage")
    def reset_max_links_per_page(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxLinksPerPage", []))

    @jsii.member(jsii_name="resetMaxUrlsPerMinuteCrawlRate")
    def reset_max_urls_per_minute_crawl_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUrlsPerMinuteCrawlRate", []))

    @jsii.member(jsii_name="resetProxyConfiguration")
    def reset_proxy_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyConfiguration", []))

    @jsii.member(jsii_name="resetUrlExclusionPatterns")
    def reset_url_exclusion_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlExclusionPatterns", []))

    @jsii.member(jsii_name="resetUrlInclusionPatterns")
    def reset_url_inclusion_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlInclusionPatterns", []))

    @builtins.property
    @jsii.member(jsii_name="authenticationConfiguration")
    def authentication_configuration(
        self,
    ) -> KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationOutputReference:
        return typing.cast(KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationOutputReference, jsii.get(self, "authenticationConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="proxyConfiguration")
    def proxy_configuration(
        self,
    ) -> "KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfigurationOutputReference":
        return typing.cast("KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfigurationOutputReference", jsii.get(self, "proxyConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="urls")
    def urls(
        self,
    ) -> "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsOutputReference":
        return typing.cast("KendraDataSourceConfigurationWebCrawlerConfigurationUrlsOutputReference", jsii.get(self, "urls"))

    @builtins.property
    @jsii.member(jsii_name="authenticationConfigurationInput")
    def authentication_configuration_input(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration], jsii.get(self, "authenticationConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="crawlDepthInput")
    def crawl_depth_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "crawlDepthInput"))

    @builtins.property
    @jsii.member(jsii_name="maxContentSizePerPageInMegaBytesInput")
    def max_content_size_per_page_in_mega_bytes_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxContentSizePerPageInMegaBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxLinksPerPageInput")
    def max_links_per_page_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxLinksPerPageInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUrlsPerMinuteCrawlRateInput")
    def max_urls_per_minute_crawl_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUrlsPerMinuteCrawlRateInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyConfigurationInput")
    def proxy_configuration_input(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration"]:
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration"], jsii.get(self, "proxyConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="urlExclusionPatternsInput")
    def url_exclusion_patterns_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "urlExclusionPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInclusionPatternsInput")
    def url_inclusion_patterns_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "urlInclusionPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="urlsInput")
    def urls_input(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrls"]:
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrls"], jsii.get(self, "urlsInput"))

    @builtins.property
    @jsii.member(jsii_name="crawlDepth")
    def crawl_depth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "crawlDepth"))

    @crawl_depth.setter
    def crawl_depth(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e9dac34c5d57775adf4bc377e8f66b12bef422671b9c6bd9b8ad2b1f07e24f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crawlDepth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxContentSizePerPageInMegaBytes")
    def max_content_size_per_page_in_mega_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxContentSizePerPageInMegaBytes"))

    @max_content_size_per_page_in_mega_bytes.setter
    def max_content_size_per_page_in_mega_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cc2f9e3c2f785444802290d916cde85ab211b3c6f031b994bf0605e106bbd9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxContentSizePerPageInMegaBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxLinksPerPage")
    def max_links_per_page(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxLinksPerPage"))

    @max_links_per_page.setter
    def max_links_per_page(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e058cccd6236ba019d6ab61110f97bcb63360aad4a075311fa2efb2193a4703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxLinksPerPage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUrlsPerMinuteCrawlRate")
    def max_urls_per_minute_crawl_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUrlsPerMinuteCrawlRate"))

    @max_urls_per_minute_crawl_rate.setter
    def max_urls_per_minute_crawl_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94da263da28e1a73baeda5f61bccba821de2a4939efd653a64f9d4b34042d11a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUrlsPerMinuteCrawlRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlExclusionPatterns")
    def url_exclusion_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "urlExclusionPatterns"))

    @url_exclusion_patterns.setter
    def url_exclusion_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1359e47f5ab59289fe97f62d8548b2271cfed31e48caabc78b1ef187debc2ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlExclusionPatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlInclusionPatterns")
    def url_inclusion_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "urlInclusionPatterns"))

    @url_inclusion_patterns.setter
    def url_inclusion_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7240999043e9642b77d04ed87f6ff2fb5885a55e3197241f64a8066021fec2e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlInclusionPatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationWebCrawlerConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationWebCrawlerConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6022cc606d532288d52b3147f1b9e3431f8934641d1ac5a38a71df419b6b1ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "port": "port", "credentials": "credentials"},
)
class KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration:
    def __init__(
        self,
        *,
        host: builtins.str,
        port: jsii.Number,
        credentials: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#host KendraDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#port KendraDataSource#port}.
        :param credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#credentials KendraDataSource#credentials}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf79b929cc438545112e015de37a4442c557fb9d160ce65459839f3427985b59)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host": host,
            "port": port,
        }
        if credentials is not None:
            self._values["credentials"] = credentials

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#host KendraDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#port KendraDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def credentials(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#credentials KendraDataSource#credentials}.'''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__542165a6e9b7fbe7e95e9d595dc77614d68f8fe2daf857184541d8c932c95b4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCredentials")
    def reset_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentials", []))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentials"))

    @credentials.setter
    def credentials(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__643b1cec3a3508cacba14267238ff0123666d7f1e29127367e9e507584aec044)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dfd45e47306f51796951958563e226d5daf731a1085eb3589ca59dc9ec1e3ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d09170888fcb6b9a2dffa7fae9c73ce1f4d6ba2a2dbe0dcf847363a9b34fb6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a69b26827ffd28bd95497eee2444098b7524d8dc3e7ae54572f32555c8ed832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationUrls",
    jsii_struct_bases=[],
    name_mapping={
        "seed_url_configuration": "seedUrlConfiguration",
        "site_maps_configuration": "siteMapsConfiguration",
    },
)
class KendraDataSourceConfigurationWebCrawlerConfigurationUrls:
    def __init__(
        self,
        *,
        seed_url_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        site_maps_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param seed_url_configuration: seed_url_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#seed_url_configuration KendraDataSource#seed_url_configuration}
        :param site_maps_configuration: site_maps_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#site_maps_configuration KendraDataSource#site_maps_configuration}
        '''
        if isinstance(seed_url_configuration, dict):
            seed_url_configuration = KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration(**seed_url_configuration)
        if isinstance(site_maps_configuration, dict):
            site_maps_configuration = KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration(**site_maps_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a5b5bd0b38657944a5a736a77dca494d87fa48392edff4fae2db1f3a49c0ab6)
            check_type(argname="argument seed_url_configuration", value=seed_url_configuration, expected_type=type_hints["seed_url_configuration"])
            check_type(argname="argument site_maps_configuration", value=site_maps_configuration, expected_type=type_hints["site_maps_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if seed_url_configuration is not None:
            self._values["seed_url_configuration"] = seed_url_configuration
        if site_maps_configuration is not None:
            self._values["site_maps_configuration"] = site_maps_configuration

    @builtins.property
    def seed_url_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration"]:
        '''seed_url_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#seed_url_configuration KendraDataSource#seed_url_configuration}
        '''
        result = self._values.get("seed_url_configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration"], result)

    @builtins.property
    def site_maps_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration"]:
        '''site_maps_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#site_maps_configuration KendraDataSource#site_maps_configuration}
        '''
        result = self._values.get("site_maps_configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationWebCrawlerConfigurationUrls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceConfigurationWebCrawlerConfigurationUrlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationUrlsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdb7938a1ff5bd2a4bc30eae53be45452b2e4058c9b8bdba2763aade34e4297b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSeedUrlConfiguration")
    def put_seed_url_configuration(
        self,
        *,
        seed_urls: typing.Sequence[builtins.str],
        web_crawler_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param seed_urls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#seed_urls KendraDataSource#seed_urls}.
        :param web_crawler_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#web_crawler_mode KendraDataSource#web_crawler_mode}.
        '''
        value = KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration(
            seed_urls=seed_urls, web_crawler_mode=web_crawler_mode
        )

        return typing.cast(None, jsii.invoke(self, "putSeedUrlConfiguration", [value]))

    @jsii.member(jsii_name="putSiteMapsConfiguration")
    def put_site_maps_configuration(
        self,
        *,
        site_maps: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param site_maps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#site_maps KendraDataSource#site_maps}.
        '''
        value = KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration(
            site_maps=site_maps
        )

        return typing.cast(None, jsii.invoke(self, "putSiteMapsConfiguration", [value]))

    @jsii.member(jsii_name="resetSeedUrlConfiguration")
    def reset_seed_url_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeedUrlConfiguration", []))

    @jsii.member(jsii_name="resetSiteMapsConfiguration")
    def reset_site_maps_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSiteMapsConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="seedUrlConfiguration")
    def seed_url_configuration(
        self,
    ) -> "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfigurationOutputReference":
        return typing.cast("KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfigurationOutputReference", jsii.get(self, "seedUrlConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="siteMapsConfiguration")
    def site_maps_configuration(
        self,
    ) -> "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfigurationOutputReference":
        return typing.cast("KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfigurationOutputReference", jsii.get(self, "siteMapsConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="seedUrlConfigurationInput")
    def seed_url_configuration_input(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration"]:
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration"], jsii.get(self, "seedUrlConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="siteMapsConfigurationInput")
    def site_maps_configuration_input(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration"]:
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration"], jsii.get(self, "siteMapsConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrls]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrls], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrls],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dfe8d333abe3ab104d6642d48ed467badcd419400f9a4f4f0468385cc39fd6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration",
    jsii_struct_bases=[],
    name_mapping={"seed_urls": "seedUrls", "web_crawler_mode": "webCrawlerMode"},
)
class KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration:
    def __init__(
        self,
        *,
        seed_urls: typing.Sequence[builtins.str],
        web_crawler_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param seed_urls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#seed_urls KendraDataSource#seed_urls}.
        :param web_crawler_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#web_crawler_mode KendraDataSource#web_crawler_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c54202180d4b019d797082e0eb1dede4db3daf9421f85e38432c97b2ac447c1b)
            check_type(argname="argument seed_urls", value=seed_urls, expected_type=type_hints["seed_urls"])
            check_type(argname="argument web_crawler_mode", value=web_crawler_mode, expected_type=type_hints["web_crawler_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "seed_urls": seed_urls,
        }
        if web_crawler_mode is not None:
            self._values["web_crawler_mode"] = web_crawler_mode

    @builtins.property
    def seed_urls(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#seed_urls KendraDataSource#seed_urls}.'''
        result = self._values.get("seed_urls")
        assert result is not None, "Required property 'seed_urls' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def web_crawler_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#web_crawler_mode KendraDataSource#web_crawler_mode}.'''
        result = self._values.get("web_crawler_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e24d546b778179da631a30aaebd65f91d7ad333af730909fd2dfdad605d11212)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetWebCrawlerMode")
    def reset_web_crawler_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebCrawlerMode", []))

    @builtins.property
    @jsii.member(jsii_name="seedUrlsInput")
    def seed_urls_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "seedUrlsInput"))

    @builtins.property
    @jsii.member(jsii_name="webCrawlerModeInput")
    def web_crawler_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webCrawlerModeInput"))

    @builtins.property
    @jsii.member(jsii_name="seedUrls")
    def seed_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "seedUrls"))

    @seed_urls.setter
    def seed_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__432a22fdfa3e19ca7927d2ea470eacbb462d7ef82088371b49172bdbce42ce3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seedUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webCrawlerMode")
    def web_crawler_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webCrawlerMode"))

    @web_crawler_mode.setter
    def web_crawler_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d2507d2c4e89e4fea23cbe3b30089bdac9198dbbf5937a7e4f1bae6ad5c20a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webCrawlerMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f43932b819ca4171775a6e97788069f0da982eb36d568d10cb4c136c499800b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration",
    jsii_struct_bases=[],
    name_mapping={"site_maps": "siteMaps"},
)
class KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration:
    def __init__(self, *, site_maps: typing.Sequence[builtins.str]) -> None:
        '''
        :param site_maps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#site_maps KendraDataSource#site_maps}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa2154379922e817b228479134a214055c882b865229a734fc9c6d64804a3f7)
            check_type(argname="argument site_maps", value=site_maps, expected_type=type_hints["site_maps"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "site_maps": site_maps,
        }

    @builtins.property
    def site_maps(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#site_maps KendraDataSource#site_maps}.'''
        result = self._values.get("site_maps")
        assert result is not None, "Required property 'site_maps' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22f902f3053b43ddef1661af2d0ae9a5b87eebf1bd0dcefc51d9d2f9e828191d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="siteMapsInput")
    def site_maps_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "siteMapsInput"))

    @builtins.property
    @jsii.member(jsii_name="siteMaps")
    def site_maps(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "siteMaps"))

    @site_maps.setter
    def site_maps(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d73a19261abd07a13a91b3cd5e2b01271dc4873988735cbf435bce7ce30439b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "siteMaps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0613039a34ef5e5372107bc57a0ec3fb3e811c0f188da8efe0e634cabe07f74d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "inline_configurations": "inlineConfigurations",
        "post_extraction_hook_configuration": "postExtractionHookConfiguration",
        "pre_extraction_hook_configuration": "preExtractionHookConfiguration",
        "role_arn": "roleArn",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfiguration:
    def __init__(
        self,
        *,
        inline_configurations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        post_extraction_hook_configuration: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        pre_extraction_hook_configuration: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param inline_configurations: inline_configurations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#inline_configurations KendraDataSource#inline_configurations}
        :param post_extraction_hook_configuration: post_extraction_hook_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#post_extraction_hook_configuration KendraDataSource#post_extraction_hook_configuration}
        :param pre_extraction_hook_configuration: pre_extraction_hook_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#pre_extraction_hook_configuration KendraDataSource#pre_extraction_hook_configuration}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#role_arn KendraDataSource#role_arn}.
        '''
        if isinstance(post_extraction_hook_configuration, dict):
            post_extraction_hook_configuration = KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration(**post_extraction_hook_configuration)
        if isinstance(pre_extraction_hook_configuration, dict):
            pre_extraction_hook_configuration = KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration(**pre_extraction_hook_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ec8fa87ec2b318982c6f4e0b5aa8badc1f8f9710bb2333b08f84cb4b6a7711)
            check_type(argname="argument inline_configurations", value=inline_configurations, expected_type=type_hints["inline_configurations"])
            check_type(argname="argument post_extraction_hook_configuration", value=post_extraction_hook_configuration, expected_type=type_hints["post_extraction_hook_configuration"])
            check_type(argname="argument pre_extraction_hook_configuration", value=pre_extraction_hook_configuration, expected_type=type_hints["pre_extraction_hook_configuration"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if inline_configurations is not None:
            self._values["inline_configurations"] = inline_configurations
        if post_extraction_hook_configuration is not None:
            self._values["post_extraction_hook_configuration"] = post_extraction_hook_configuration
        if pre_extraction_hook_configuration is not None:
            self._values["pre_extraction_hook_configuration"] = pre_extraction_hook_configuration
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def inline_configurations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations"]]]:
        '''inline_configurations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#inline_configurations KendraDataSource#inline_configurations}
        '''
        result = self._values.get("inline_configurations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations"]]], result)

    @builtins.property
    def post_extraction_hook_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration"]:
        '''post_extraction_hook_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#post_extraction_hook_configuration KendraDataSource#post_extraction_hook_configuration}
        '''
        result = self._values.get("post_extraction_hook_configuration")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration"], result)

    @builtins.property
    def pre_extraction_hook_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration"]:
        '''pre_extraction_hook_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#pre_extraction_hook_configuration KendraDataSource#pre_extraction_hook_configuration}
        '''
        result = self._values.get("pre_extraction_hook_configuration")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration"], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#role_arn KendraDataSource#role_arn}.'''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations",
    jsii_struct_bases=[],
    name_mapping={
        "condition": "condition",
        "document_content_deletion": "documentContentDeletion",
        "target": "target",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations:
    def __init__(
        self,
        *,
        condition: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        document_content_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        target: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition KendraDataSource#condition}
        :param document_content_deletion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#document_content_deletion KendraDataSource#document_content_deletion}.
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#target KendraDataSource#target}
        '''
        if isinstance(condition, dict):
            condition = KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition(**condition)
        if isinstance(target, dict):
            target = KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b94ddb9aa7fcd2a18c6af1b704eff87387748d47f4a51a2050668824402e17c5)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument document_content_deletion", value=document_content_deletion, expected_type=type_hints["document_content_deletion"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if condition is not None:
            self._values["condition"] = condition
        if document_content_deletion is not None:
            self._values["document_content_deletion"] = document_content_deletion
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition"]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition KendraDataSource#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition"], result)

    @builtins.property
    def document_content_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#document_content_deletion KendraDataSource#document_content_deletion}.'''
        result = self._values.get("document_content_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#target KendraDataSource#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition",
    jsii_struct_bases=[],
    name_mapping={
        "condition_document_attribute_key": "conditionDocumentAttributeKey",
        "operator": "operator",
        "condition_on_value": "conditionOnValue",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition:
    def __init__(
        self,
        *,
        condition_document_attribute_key: builtins.str,
        operator: builtins.str,
        condition_on_value: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param condition_document_attribute_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition_document_attribute_key KendraDataSource#condition_document_attribute_key}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#operator KendraDataSource#operator}.
        :param condition_on_value: condition_on_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition_on_value KendraDataSource#condition_on_value}
        '''
        if isinstance(condition_on_value, dict):
            condition_on_value = KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue(**condition_on_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8a2ec1e2925630cd2dfb24467fa944dcfc0109b856dcdfe7171d9874ae8dc93)
            check_type(argname="argument condition_document_attribute_key", value=condition_document_attribute_key, expected_type=type_hints["condition_document_attribute_key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument condition_on_value", value=condition_on_value, expected_type=type_hints["condition_on_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "condition_document_attribute_key": condition_document_attribute_key,
            "operator": operator,
        }
        if condition_on_value is not None:
            self._values["condition_on_value"] = condition_on_value

    @builtins.property
    def condition_document_attribute_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition_document_attribute_key KendraDataSource#condition_document_attribute_key}.'''
        result = self._values.get("condition_document_attribute_key")
        assert result is not None, "Required property 'condition_document_attribute_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#operator KendraDataSource#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition_on_value(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue"]:
        '''condition_on_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition_on_value KendraDataSource#condition_on_value}
        '''
        result = self._values.get("condition_on_value")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue",
    jsii_struct_bases=[],
    name_mapping={
        "date_value": "dateValue",
        "long_value": "longValue",
        "string_list_value": "stringListValue",
        "string_value": "stringValue",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue:
    def __init__(
        self,
        *,
        date_value: typing.Optional[builtins.str] = None,
        long_value: typing.Optional[jsii.Number] = None,
        string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.
        :param long_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.
        :param string_list_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.
        :param string_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__260aff2ce28269c651bca5ec8aee18f496fffa07097cf8dcb67bc4a5d9cc601a)
            check_type(argname="argument date_value", value=date_value, expected_type=type_hints["date_value"])
            check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
            check_type(argname="argument string_list_value", value=string_list_value, expected_type=type_hints["string_list_value"])
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if date_value is not None:
            self._values["date_value"] = date_value
        if long_value is not None:
            self._values["long_value"] = long_value
        if string_list_value is not None:
            self._values["string_list_value"] = string_list_value
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def date_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.'''
        result = self._values.get("date_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def long_value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.'''
        result = self._values.get("long_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def string_list_value(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.'''
        result = self._values.get("string_list_value")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.'''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1a038cf7fbdda5811f80e5f65f1a26f7e653723174cde0c18530d7eb79061ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDateValue")
    def reset_date_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateValue", []))

    @jsii.member(jsii_name="resetLongValue")
    def reset_long_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongValue", []))

    @jsii.member(jsii_name="resetStringListValue")
    def reset_string_list_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringListValue", []))

    @jsii.member(jsii_name="resetStringValue")
    def reset_string_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringValue", []))

    @builtins.property
    @jsii.member(jsii_name="dateValueInput")
    def date_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateValueInput"))

    @builtins.property
    @jsii.member(jsii_name="longValueInput")
    def long_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "longValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringListValueInput")
    def string_list_value_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "stringListValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringValueInput")
    def string_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stringValueInput"))

    @builtins.property
    @jsii.member(jsii_name="dateValue")
    def date_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateValue"))

    @date_value.setter
    def date_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49183218bf3ff207bd9a4ffdaf25f37ecbca97d1db0fb352fc73ff093b56db94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="longValue")
    def long_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "longValue"))

    @long_value.setter
    def long_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14e24acaff46b0e5f6b2f1d158dd8ad0a6cfeae0907b1908ecd685ed60f2613d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringListValue")
    def string_list_value(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stringListValue"))

    @string_list_value.setter
    def string_list_value(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e224790a7897b9bd09643042fea8fadd87c06cadd4053a4278ab5b934f9b8920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringListValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42f7898a7dc030a50f4a35ff01768ebd2471582250deea4fc1cac43ed16554fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6148319bc238e47971eeba6e654126a89997f44d3be6365bcadf2d086dfd405b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75131161df10301f370f878b0d3c76ffd13d2cd099863333a1617933e75646ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConditionOnValue")
    def put_condition_on_value(
        self,
        *,
        date_value: typing.Optional[builtins.str] = None,
        long_value: typing.Optional[jsii.Number] = None,
        string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.
        :param long_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.
        :param string_list_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.
        :param string_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue(
            date_value=date_value,
            long_value=long_value,
            string_list_value=string_list_value,
            string_value=string_value,
        )

        return typing.cast(None, jsii.invoke(self, "putConditionOnValue", [value]))

    @jsii.member(jsii_name="resetConditionOnValue")
    def reset_condition_on_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionOnValue", []))

    @builtins.property
    @jsii.member(jsii_name="conditionOnValue")
    def condition_on_value(
        self,
    ) -> KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValueOutputReference:
        return typing.cast(KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValueOutputReference, jsii.get(self, "conditionOnValue"))

    @builtins.property
    @jsii.member(jsii_name="conditionDocumentAttributeKeyInput")
    def condition_document_attribute_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionDocumentAttributeKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionOnValueInput")
    def condition_on_value_input(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue], jsii.get(self, "conditionOnValueInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionDocumentAttributeKey")
    def condition_document_attribute_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conditionDocumentAttributeKey"))

    @condition_document_attribute_key.setter
    def condition_document_attribute_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb450f83e0c7ce975a297989ae5d330e2e70419eb429cac6efb9013d47ee4445)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conditionDocumentAttributeKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0170941b4ac360d4868e5d98afecec06c0f65bb3febc0888ad7f59976282d40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfef27ea3dbb2909439eab5a4f941ce8cde3b1d7ccee945987fb950c8f88d594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b279041684fcc2736c07725848cf306f9add3d57db850f89224fae1447f7770a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7fd4b8b4b09358e7180c0254bb2c8e13844ed5404f01c1e94a1ed7a3c8c5219)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf794f70718cab9f6d88f13d121dd4d2d0e670121fea1982866cf72cd4fc8672)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4480b84d8ad437e96a504db8404f28a8c7e7f3be8312dc0b17c58008bf58249)
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
            type_hints = typing.get_type_hints(_typecheckingstub__654e91e10c7f6cd199cd98e662681c44a8987e6b9bd258d035d27b4d9bd7bc2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1135c4142721af293f6a1081e2bf5eb76d4d4a284c74bc7b6debbbc013ad936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4226710f899a5b786b3157973024f29d49172549fb3e915381364d96c9a1f3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        condition_document_attribute_key: builtins.str,
        operator: builtins.str,
        condition_on_value: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param condition_document_attribute_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition_document_attribute_key KendraDataSource#condition_document_attribute_key}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#operator KendraDataSource#operator}.
        :param condition_on_value: condition_on_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition_on_value KendraDataSource#condition_on_value}
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition(
            condition_document_attribute_key=condition_document_attribute_key,
            operator=operator,
            condition_on_value=condition_on_value,
        )

        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        target_document_attribute_key: typing.Optional[builtins.str] = None,
        target_document_attribute_value: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue", typing.Dict[builtins.str, typing.Any]]] = None,
        target_document_attribute_value_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param target_document_attribute_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#target_document_attribute_key KendraDataSource#target_document_attribute_key}.
        :param target_document_attribute_value: target_document_attribute_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#target_document_attribute_value KendraDataSource#target_document_attribute_value}
        :param target_document_attribute_value_deletion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#target_document_attribute_value_deletion KendraDataSource#target_document_attribute_value_deletion}.
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget(
            target_document_attribute_key=target_document_attribute_key,
            target_document_attribute_value=target_document_attribute_value,
            target_document_attribute_value_deletion=target_document_attribute_value_deletion,
        )

        return typing.cast(None, jsii.invoke(self, "putTarget", [value]))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetDocumentContentDeletion")
    def reset_document_content_deletion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentContentDeletion", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(
        self,
    ) -> KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionOutputReference:
        return typing.cast(KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionOutputReference, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(
        self,
    ) -> "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetOutputReference":
        return typing.cast("KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="documentContentDeletionInput")
    def document_content_deletion_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "documentContentDeletionInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget"]:
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="documentContentDeletion")
    def document_content_deletion(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "documentContentDeletion"))

    @document_content_deletion.setter
    def document_content_deletion(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8683de74145010db0c948939285be0245f41b79fabf8d8d78b69d2427cec4fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentContentDeletion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ece5e6be733bf20eebf65ddad3e737af1da3a7243dab8084e47b2b8a34a6b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget",
    jsii_struct_bases=[],
    name_mapping={
        "target_document_attribute_key": "targetDocumentAttributeKey",
        "target_document_attribute_value": "targetDocumentAttributeValue",
        "target_document_attribute_value_deletion": "targetDocumentAttributeValueDeletion",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget:
    def __init__(
        self,
        *,
        target_document_attribute_key: typing.Optional[builtins.str] = None,
        target_document_attribute_value: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue", typing.Dict[builtins.str, typing.Any]]] = None,
        target_document_attribute_value_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param target_document_attribute_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#target_document_attribute_key KendraDataSource#target_document_attribute_key}.
        :param target_document_attribute_value: target_document_attribute_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#target_document_attribute_value KendraDataSource#target_document_attribute_value}
        :param target_document_attribute_value_deletion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#target_document_attribute_value_deletion KendraDataSource#target_document_attribute_value_deletion}.
        '''
        if isinstance(target_document_attribute_value, dict):
            target_document_attribute_value = KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue(**target_document_attribute_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__082116a94d82277c37b7f6ab1ec2b9b3a9cd24dfa0f64360bd55ca9392972c62)
            check_type(argname="argument target_document_attribute_key", value=target_document_attribute_key, expected_type=type_hints["target_document_attribute_key"])
            check_type(argname="argument target_document_attribute_value", value=target_document_attribute_value, expected_type=type_hints["target_document_attribute_value"])
            check_type(argname="argument target_document_attribute_value_deletion", value=target_document_attribute_value_deletion, expected_type=type_hints["target_document_attribute_value_deletion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if target_document_attribute_key is not None:
            self._values["target_document_attribute_key"] = target_document_attribute_key
        if target_document_attribute_value is not None:
            self._values["target_document_attribute_value"] = target_document_attribute_value
        if target_document_attribute_value_deletion is not None:
            self._values["target_document_attribute_value_deletion"] = target_document_attribute_value_deletion

    @builtins.property
    def target_document_attribute_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#target_document_attribute_key KendraDataSource#target_document_attribute_key}.'''
        result = self._values.get("target_document_attribute_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_document_attribute_value(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue"]:
        '''target_document_attribute_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#target_document_attribute_value KendraDataSource#target_document_attribute_value}
        '''
        result = self._values.get("target_document_attribute_value")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue"], result)

    @builtins.property
    def target_document_attribute_value_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#target_document_attribute_value_deletion KendraDataSource#target_document_attribute_value_deletion}.'''
        result = self._values.get("target_document_attribute_value_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a6e9c89463262e36a83c3a8181184a4f782a8a0bc805b553ab84618a02df490)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTargetDocumentAttributeValue")
    def put_target_document_attribute_value(
        self,
        *,
        date_value: typing.Optional[builtins.str] = None,
        long_value: typing.Optional[jsii.Number] = None,
        string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.
        :param long_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.
        :param string_list_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.
        :param string_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue(
            date_value=date_value,
            long_value=long_value,
            string_list_value=string_list_value,
            string_value=string_value,
        )

        return typing.cast(None, jsii.invoke(self, "putTargetDocumentAttributeValue", [value]))

    @jsii.member(jsii_name="resetTargetDocumentAttributeKey")
    def reset_target_document_attribute_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetDocumentAttributeKey", []))

    @jsii.member(jsii_name="resetTargetDocumentAttributeValue")
    def reset_target_document_attribute_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetDocumentAttributeValue", []))

    @jsii.member(jsii_name="resetTargetDocumentAttributeValueDeletion")
    def reset_target_document_attribute_value_deletion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetDocumentAttributeValueDeletion", []))

    @builtins.property
    @jsii.member(jsii_name="targetDocumentAttributeValue")
    def target_document_attribute_value(
        self,
    ) -> "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValueOutputReference":
        return typing.cast("KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValueOutputReference", jsii.get(self, "targetDocumentAttributeValue"))

    @builtins.property
    @jsii.member(jsii_name="targetDocumentAttributeKeyInput")
    def target_document_attribute_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetDocumentAttributeKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="targetDocumentAttributeValueDeletionInput")
    def target_document_attribute_value_deletion_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "targetDocumentAttributeValueDeletionInput"))

    @builtins.property
    @jsii.member(jsii_name="targetDocumentAttributeValueInput")
    def target_document_attribute_value_input(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue"]:
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue"], jsii.get(self, "targetDocumentAttributeValueInput"))

    @builtins.property
    @jsii.member(jsii_name="targetDocumentAttributeKey")
    def target_document_attribute_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetDocumentAttributeKey"))

    @target_document_attribute_key.setter
    def target_document_attribute_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19459c12fd4037f5fc2b98fe531b1129f9b875660cb2548e6dea5a60d8008b83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetDocumentAttributeKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetDocumentAttributeValueDeletion")
    def target_document_attribute_value_deletion(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "targetDocumentAttributeValueDeletion"))

    @target_document_attribute_value_deletion.setter
    def target_document_attribute_value_deletion(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c1d85585c7a2f564eb0433874be25246529f9771bfac73ed9fc68f2c9fcc6aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetDocumentAttributeValueDeletion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c8a25197b8ca83566e5664f95d01e882cf91fec88c1da723d42e575465007c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue",
    jsii_struct_bases=[],
    name_mapping={
        "date_value": "dateValue",
        "long_value": "longValue",
        "string_list_value": "stringListValue",
        "string_value": "stringValue",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue:
    def __init__(
        self,
        *,
        date_value: typing.Optional[builtins.str] = None,
        long_value: typing.Optional[jsii.Number] = None,
        string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.
        :param long_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.
        :param string_list_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.
        :param string_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374e94fc584d9aef3583c3e5a0555b8a416de8b513050e88746df4d36c13df71)
            check_type(argname="argument date_value", value=date_value, expected_type=type_hints["date_value"])
            check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
            check_type(argname="argument string_list_value", value=string_list_value, expected_type=type_hints["string_list_value"])
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if date_value is not None:
            self._values["date_value"] = date_value
        if long_value is not None:
            self._values["long_value"] = long_value
        if string_list_value is not None:
            self._values["string_list_value"] = string_list_value
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def date_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.'''
        result = self._values.get("date_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def long_value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.'''
        result = self._values.get("long_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def string_list_value(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.'''
        result = self._values.get("string_list_value")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.'''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b5125c2337233c8190b8bc65fe6cc5b6f41e9250855660d73e7e9f4fc82c96e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDateValue")
    def reset_date_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateValue", []))

    @jsii.member(jsii_name="resetLongValue")
    def reset_long_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongValue", []))

    @jsii.member(jsii_name="resetStringListValue")
    def reset_string_list_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringListValue", []))

    @jsii.member(jsii_name="resetStringValue")
    def reset_string_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringValue", []))

    @builtins.property
    @jsii.member(jsii_name="dateValueInput")
    def date_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateValueInput"))

    @builtins.property
    @jsii.member(jsii_name="longValueInput")
    def long_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "longValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringListValueInput")
    def string_list_value_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "stringListValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringValueInput")
    def string_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stringValueInput"))

    @builtins.property
    @jsii.member(jsii_name="dateValue")
    def date_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateValue"))

    @date_value.setter
    def date_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45e5a6a0ede63f47eb11bed31f8758df7ab838b829fccc5c6d7a1c6b0ec117f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="longValue")
    def long_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "longValue"))

    @long_value.setter
    def long_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce2a2c9319e17f502b4264de0e8ebccd3205384a070e651a72b5e5711aba420d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringListValue")
    def string_list_value(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stringListValue"))

    @string_list_value.setter
    def string_list_value(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee73b5adcc91a858679a5d902c0cd955a0971dd88ad34637e40aa7d82606432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringListValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4eb360c3066babe6d8db893088b90a856a78a6662c50b27b57037048f35b081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c2fecd3bd9a9a1cb5262da1a47dada2a87cc46404e52883022ddad13a7a613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceCustomDocumentEnrichmentConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2bf319f2f7b7cc13df1b0cc3c61f1b493c3e3591e735121e6afc8f64934f512)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInlineConfigurations")
    def put_inline_configurations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716ae988460ae9be2c017c42e024a52990753b278f71f068507d6771871d86a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInlineConfigurations", [value]))

    @jsii.member(jsii_name="putPostExtractionHookConfiguration")
    def put_post_extraction_hook_configuration(
        self,
        *,
        lambda_arn: builtins.str,
        s3_bucket: builtins.str,
        invocation_condition: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param lambda_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#lambda_arn KendraDataSource#lambda_arn}.
        :param s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#s3_bucket KendraDataSource#s3_bucket}.
        :param invocation_condition: invocation_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#invocation_condition KendraDataSource#invocation_condition}
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration(
            lambda_arn=lambda_arn,
            s3_bucket=s3_bucket,
            invocation_condition=invocation_condition,
        )

        return typing.cast(None, jsii.invoke(self, "putPostExtractionHookConfiguration", [value]))

    @jsii.member(jsii_name="putPreExtractionHookConfiguration")
    def put_pre_extraction_hook_configuration(
        self,
        *,
        lambda_arn: builtins.str,
        s3_bucket: builtins.str,
        invocation_condition: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param lambda_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#lambda_arn KendraDataSource#lambda_arn}.
        :param s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#s3_bucket KendraDataSource#s3_bucket}.
        :param invocation_condition: invocation_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#invocation_condition KendraDataSource#invocation_condition}
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration(
            lambda_arn=lambda_arn,
            s3_bucket=s3_bucket,
            invocation_condition=invocation_condition,
        )

        return typing.cast(None, jsii.invoke(self, "putPreExtractionHookConfiguration", [value]))

    @jsii.member(jsii_name="resetInlineConfigurations")
    def reset_inline_configurations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInlineConfigurations", []))

    @jsii.member(jsii_name="resetPostExtractionHookConfiguration")
    def reset_post_extraction_hook_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostExtractionHookConfiguration", []))

    @jsii.member(jsii_name="resetPreExtractionHookConfiguration")
    def reset_pre_extraction_hook_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreExtractionHookConfiguration", []))

    @jsii.member(jsii_name="resetRoleArn")
    def reset_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleArn", []))

    @builtins.property
    @jsii.member(jsii_name="inlineConfigurations")
    def inline_configurations(
        self,
    ) -> KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsList:
        return typing.cast(KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsList, jsii.get(self, "inlineConfigurations"))

    @builtins.property
    @jsii.member(jsii_name="postExtractionHookConfiguration")
    def post_extraction_hook_configuration(
        self,
    ) -> "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationOutputReference":
        return typing.cast("KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationOutputReference", jsii.get(self, "postExtractionHookConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="preExtractionHookConfiguration")
    def pre_extraction_hook_configuration(
        self,
    ) -> "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationOutputReference":
        return typing.cast("KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationOutputReference", jsii.get(self, "preExtractionHookConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="inlineConfigurationsInput")
    def inline_configurations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]]], jsii.get(self, "inlineConfigurationsInput"))

    @builtins.property
    @jsii.member(jsii_name="postExtractionHookConfigurationInput")
    def post_extraction_hook_configuration_input(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration"]:
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration"], jsii.get(self, "postExtractionHookConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="preExtractionHookConfigurationInput")
    def pre_extraction_hook_configuration_input(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration"]:
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration"], jsii.get(self, "preExtractionHookConfigurationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2d095d7b477efc7117e0a0625623bbe93ac3fd9b1a3119715d703b2dd04236cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31ee0172acf7a3bc458cb54170dcef0dd36e5c01886fc6b4dae10dfc530dee20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "lambda_arn": "lambdaArn",
        "s3_bucket": "s3Bucket",
        "invocation_condition": "invocationCondition",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration:
    def __init__(
        self,
        *,
        lambda_arn: builtins.str,
        s3_bucket: builtins.str,
        invocation_condition: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param lambda_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#lambda_arn KendraDataSource#lambda_arn}.
        :param s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#s3_bucket KendraDataSource#s3_bucket}.
        :param invocation_condition: invocation_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#invocation_condition KendraDataSource#invocation_condition}
        '''
        if isinstance(invocation_condition, dict):
            invocation_condition = KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition(**invocation_condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a97940073870a7fb974efd102c7c19538e62586726bf17366eb734ab77bfcc8)
            check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            check_type(argname="argument invocation_condition", value=invocation_condition, expected_type=type_hints["invocation_condition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lambda_arn": lambda_arn,
            "s3_bucket": s3_bucket,
        }
        if invocation_condition is not None:
            self._values["invocation_condition"] = invocation_condition

    @builtins.property
    def lambda_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#lambda_arn KendraDataSource#lambda_arn}.'''
        result = self._values.get("lambda_arn")
        assert result is not None, "Required property 'lambda_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#s3_bucket KendraDataSource#s3_bucket}.'''
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def invocation_condition(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition"]:
        '''invocation_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#invocation_condition KendraDataSource#invocation_condition}
        '''
        result = self._values.get("invocation_condition")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition",
    jsii_struct_bases=[],
    name_mapping={
        "condition_document_attribute_key": "conditionDocumentAttributeKey",
        "operator": "operator",
        "condition_on_value": "conditionOnValue",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition:
    def __init__(
        self,
        *,
        condition_document_attribute_key: builtins.str,
        operator: builtins.str,
        condition_on_value: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param condition_document_attribute_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition_document_attribute_key KendraDataSource#condition_document_attribute_key}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#operator KendraDataSource#operator}.
        :param condition_on_value: condition_on_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition_on_value KendraDataSource#condition_on_value}
        '''
        if isinstance(condition_on_value, dict):
            condition_on_value = KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue(**condition_on_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e42e616d63df4c9ec32eaeb6ce9afa748c23f67a4a53ef611920089a25f25beb)
            check_type(argname="argument condition_document_attribute_key", value=condition_document_attribute_key, expected_type=type_hints["condition_document_attribute_key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument condition_on_value", value=condition_on_value, expected_type=type_hints["condition_on_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "condition_document_attribute_key": condition_document_attribute_key,
            "operator": operator,
        }
        if condition_on_value is not None:
            self._values["condition_on_value"] = condition_on_value

    @builtins.property
    def condition_document_attribute_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition_document_attribute_key KendraDataSource#condition_document_attribute_key}.'''
        result = self._values.get("condition_document_attribute_key")
        assert result is not None, "Required property 'condition_document_attribute_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#operator KendraDataSource#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition_on_value(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue"]:
        '''condition_on_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition_on_value KendraDataSource#condition_on_value}
        '''
        result = self._values.get("condition_on_value")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue",
    jsii_struct_bases=[],
    name_mapping={
        "date_value": "dateValue",
        "long_value": "longValue",
        "string_list_value": "stringListValue",
        "string_value": "stringValue",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue:
    def __init__(
        self,
        *,
        date_value: typing.Optional[builtins.str] = None,
        long_value: typing.Optional[jsii.Number] = None,
        string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.
        :param long_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.
        :param string_list_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.
        :param string_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f67dffbb04f5d7b34abb50caf364214179ade130ebda84939438558754827cd3)
            check_type(argname="argument date_value", value=date_value, expected_type=type_hints["date_value"])
            check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
            check_type(argname="argument string_list_value", value=string_list_value, expected_type=type_hints["string_list_value"])
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if date_value is not None:
            self._values["date_value"] = date_value
        if long_value is not None:
            self._values["long_value"] = long_value
        if string_list_value is not None:
            self._values["string_list_value"] = string_list_value
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def date_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.'''
        result = self._values.get("date_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def long_value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.'''
        result = self._values.get("long_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def string_list_value(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.'''
        result = self._values.get("string_list_value")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.'''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acadad16783106b2a52e1e4da86a97a7b72ca19b8cb58c7ef9c7cd32204e4c10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDateValue")
    def reset_date_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateValue", []))

    @jsii.member(jsii_name="resetLongValue")
    def reset_long_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongValue", []))

    @jsii.member(jsii_name="resetStringListValue")
    def reset_string_list_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringListValue", []))

    @jsii.member(jsii_name="resetStringValue")
    def reset_string_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringValue", []))

    @builtins.property
    @jsii.member(jsii_name="dateValueInput")
    def date_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateValueInput"))

    @builtins.property
    @jsii.member(jsii_name="longValueInput")
    def long_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "longValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringListValueInput")
    def string_list_value_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "stringListValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringValueInput")
    def string_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stringValueInput"))

    @builtins.property
    @jsii.member(jsii_name="dateValue")
    def date_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateValue"))

    @date_value.setter
    def date_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bbb0ab6cc324addc6eea6bb2c39c31ee9fc084797dd903dd4e848f948ea3fe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="longValue")
    def long_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "longValue"))

    @long_value.setter
    def long_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd1420d6ade74938cb3db297297a590459ff21a611663aa9cd9affd4aa4ade8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringListValue")
    def string_list_value(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stringListValue"))

    @string_list_value.setter
    def string_list_value(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__404a02f4462b6bd6cea2a59178af0df138ac43c119c4e969d8d9c3273a03fb26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringListValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af165b3124c88d2f0344d590e7c2fe63008f07cb610cdc2f06f8ae56545a6bc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a7de6d2e84853826998c71566f2e3ae5cc10665beb32dbe7eda6a9fa60be579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94ee628d5d09d238392be5beffe87d70d6cc6618c8fa1b736979e587a95a8d71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConditionOnValue")
    def put_condition_on_value(
        self,
        *,
        date_value: typing.Optional[builtins.str] = None,
        long_value: typing.Optional[jsii.Number] = None,
        string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.
        :param long_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.
        :param string_list_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.
        :param string_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue(
            date_value=date_value,
            long_value=long_value,
            string_list_value=string_list_value,
            string_value=string_value,
        )

        return typing.cast(None, jsii.invoke(self, "putConditionOnValue", [value]))

    @jsii.member(jsii_name="resetConditionOnValue")
    def reset_condition_on_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionOnValue", []))

    @builtins.property
    @jsii.member(jsii_name="conditionOnValue")
    def condition_on_value(
        self,
    ) -> KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference:
        return typing.cast(KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference, jsii.get(self, "conditionOnValue"))

    @builtins.property
    @jsii.member(jsii_name="conditionDocumentAttributeKeyInput")
    def condition_document_attribute_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionDocumentAttributeKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionOnValueInput")
    def condition_on_value_input(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue], jsii.get(self, "conditionOnValueInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionDocumentAttributeKey")
    def condition_document_attribute_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conditionDocumentAttributeKey"))

    @condition_document_attribute_key.setter
    def condition_document_attribute_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ff1c7fd0c6ac11f5b10b508991ffef991a03b73b4a4badbedc91cc523f0cc4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conditionDocumentAttributeKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71498d9bae0785bb868be8271a5cc3573f452fead9429307317e8f8ae338ed8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa5f00dbba79a1b41bae748280c2838aad78e0612007f86be0fafef0213ac948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e93447a983bca7d324879ad94fe6f898261c65981fcd4792130f304fb22379b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInvocationCondition")
    def put_invocation_condition(
        self,
        *,
        condition_document_attribute_key: builtins.str,
        operator: builtins.str,
        condition_on_value: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param condition_document_attribute_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition_document_attribute_key KendraDataSource#condition_document_attribute_key}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#operator KendraDataSource#operator}.
        :param condition_on_value: condition_on_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition_on_value KendraDataSource#condition_on_value}
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition(
            condition_document_attribute_key=condition_document_attribute_key,
            operator=operator,
            condition_on_value=condition_on_value,
        )

        return typing.cast(None, jsii.invoke(self, "putInvocationCondition", [value]))

    @jsii.member(jsii_name="resetInvocationCondition")
    def reset_invocation_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvocationCondition", []))

    @builtins.property
    @jsii.member(jsii_name="invocationCondition")
    def invocation_condition(
        self,
    ) -> KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionOutputReference:
        return typing.cast(KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionOutputReference, jsii.get(self, "invocationCondition"))

    @builtins.property
    @jsii.member(jsii_name="invocationConditionInput")
    def invocation_condition_input(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition], jsii.get(self, "invocationConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaArnInput")
    def lambda_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaArnInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketInput")
    def s3_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BucketInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaArn")
    def lambda_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaArn"))

    @lambda_arn.setter
    def lambda_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c4bb6ae23049e33bffad47af7567ae1cea0ea275971bb0b3248449d8a527664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Bucket"))

    @s3_bucket.setter
    def s3_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e79f634f2d81aaa5d0ba116c753f8369a1cb6eb8efc12a9f0e4c012c381e484e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd04b6b712438223c55632c32f5ea941731ad2b814083116a40be8ce355ed41c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "lambda_arn": "lambdaArn",
        "s3_bucket": "s3Bucket",
        "invocation_condition": "invocationCondition",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration:
    def __init__(
        self,
        *,
        lambda_arn: builtins.str,
        s3_bucket: builtins.str,
        invocation_condition: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param lambda_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#lambda_arn KendraDataSource#lambda_arn}.
        :param s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#s3_bucket KendraDataSource#s3_bucket}.
        :param invocation_condition: invocation_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#invocation_condition KendraDataSource#invocation_condition}
        '''
        if isinstance(invocation_condition, dict):
            invocation_condition = KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition(**invocation_condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__742e000a5448746e0b975626ca946ae280a2c8a998ac28666da38035d41c038d)
            check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            check_type(argname="argument invocation_condition", value=invocation_condition, expected_type=type_hints["invocation_condition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lambda_arn": lambda_arn,
            "s3_bucket": s3_bucket,
        }
        if invocation_condition is not None:
            self._values["invocation_condition"] = invocation_condition

    @builtins.property
    def lambda_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#lambda_arn KendraDataSource#lambda_arn}.'''
        result = self._values.get("lambda_arn")
        assert result is not None, "Required property 'lambda_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#s3_bucket KendraDataSource#s3_bucket}.'''
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def invocation_condition(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition"]:
        '''invocation_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#invocation_condition KendraDataSource#invocation_condition}
        '''
        result = self._values.get("invocation_condition")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition",
    jsii_struct_bases=[],
    name_mapping={
        "condition_document_attribute_key": "conditionDocumentAttributeKey",
        "operator": "operator",
        "condition_on_value": "conditionOnValue",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition:
    def __init__(
        self,
        *,
        condition_document_attribute_key: builtins.str,
        operator: builtins.str,
        condition_on_value: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param condition_document_attribute_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition_document_attribute_key KendraDataSource#condition_document_attribute_key}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#operator KendraDataSource#operator}.
        :param condition_on_value: condition_on_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition_on_value KendraDataSource#condition_on_value}
        '''
        if isinstance(condition_on_value, dict):
            condition_on_value = KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue(**condition_on_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05eb70b74a0e1a88c73ad47c01315ac5e0d8b0583eb79705f9ab2a81c17c9dd7)
            check_type(argname="argument condition_document_attribute_key", value=condition_document_attribute_key, expected_type=type_hints["condition_document_attribute_key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument condition_on_value", value=condition_on_value, expected_type=type_hints["condition_on_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "condition_document_attribute_key": condition_document_attribute_key,
            "operator": operator,
        }
        if condition_on_value is not None:
            self._values["condition_on_value"] = condition_on_value

    @builtins.property
    def condition_document_attribute_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition_document_attribute_key KendraDataSource#condition_document_attribute_key}.'''
        result = self._values.get("condition_document_attribute_key")
        assert result is not None, "Required property 'condition_document_attribute_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#operator KendraDataSource#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition_on_value(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue"]:
        '''condition_on_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition_on_value KendraDataSource#condition_on_value}
        '''
        result = self._values.get("condition_on_value")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue",
    jsii_struct_bases=[],
    name_mapping={
        "date_value": "dateValue",
        "long_value": "longValue",
        "string_list_value": "stringListValue",
        "string_value": "stringValue",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue:
    def __init__(
        self,
        *,
        date_value: typing.Optional[builtins.str] = None,
        long_value: typing.Optional[jsii.Number] = None,
        string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.
        :param long_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.
        :param string_list_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.
        :param string_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abb63ee831d808200d050c25dcc8fe81c0aeb1815e598be5a5ce4de15fa45335)
            check_type(argname="argument date_value", value=date_value, expected_type=type_hints["date_value"])
            check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
            check_type(argname="argument string_list_value", value=string_list_value, expected_type=type_hints["string_list_value"])
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if date_value is not None:
            self._values["date_value"] = date_value
        if long_value is not None:
            self._values["long_value"] = long_value
        if string_list_value is not None:
            self._values["string_list_value"] = string_list_value
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def date_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.'''
        result = self._values.get("date_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def long_value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.'''
        result = self._values.get("long_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def string_list_value(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.'''
        result = self._values.get("string_list_value")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.'''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__632fc5b0f356b78d713058bd9020da8963539b85914e858a90fc077e953dd310)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDateValue")
    def reset_date_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateValue", []))

    @jsii.member(jsii_name="resetLongValue")
    def reset_long_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongValue", []))

    @jsii.member(jsii_name="resetStringListValue")
    def reset_string_list_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringListValue", []))

    @jsii.member(jsii_name="resetStringValue")
    def reset_string_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringValue", []))

    @builtins.property
    @jsii.member(jsii_name="dateValueInput")
    def date_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateValueInput"))

    @builtins.property
    @jsii.member(jsii_name="longValueInput")
    def long_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "longValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringListValueInput")
    def string_list_value_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "stringListValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringValueInput")
    def string_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stringValueInput"))

    @builtins.property
    @jsii.member(jsii_name="dateValue")
    def date_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateValue"))

    @date_value.setter
    def date_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f26af1705f39b25c76c3b45f8e5c3af99299525d3aaf642ada950b6febe4c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="longValue")
    def long_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "longValue"))

    @long_value.setter
    def long_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e13215e1e0140501f45b2431b1f86b6fe73932f08869e71d165d9cc3996d3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringListValue")
    def string_list_value(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stringListValue"))

    @string_list_value.setter
    def string_list_value(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b735e74e568237fc551237f899998a4f37295695018dfe9871efbba1af3fdf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringListValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e905877fe200971011035d9e548bf7221d93bd0747265170bf04a1204fe8b5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf02e81ce8312e26e485a72052d486c4e72d7ccaaea7a2f9884fb7f0c930f044)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32d81220d3f7db2658a6dd30e95c71a184162abb3c4dca99e40e34be696a3e4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConditionOnValue")
    def put_condition_on_value(
        self,
        *,
        date_value: typing.Optional[builtins.str] = None,
        long_value: typing.Optional[jsii.Number] = None,
        string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.
        :param long_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.
        :param string_list_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.
        :param string_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue(
            date_value=date_value,
            long_value=long_value,
            string_list_value=string_list_value,
            string_value=string_value,
        )

        return typing.cast(None, jsii.invoke(self, "putConditionOnValue", [value]))

    @jsii.member(jsii_name="resetConditionOnValue")
    def reset_condition_on_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionOnValue", []))

    @builtins.property
    @jsii.member(jsii_name="conditionOnValue")
    def condition_on_value(
        self,
    ) -> KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference:
        return typing.cast(KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference, jsii.get(self, "conditionOnValue"))

    @builtins.property
    @jsii.member(jsii_name="conditionDocumentAttributeKeyInput")
    def condition_document_attribute_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionDocumentAttributeKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionOnValueInput")
    def condition_on_value_input(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue], jsii.get(self, "conditionOnValueInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionDocumentAttributeKey")
    def condition_document_attribute_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conditionDocumentAttributeKey"))

    @condition_document_attribute_key.setter
    def condition_document_attribute_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d49e39ca0c94a4683dbf19c9286a5060ee0a3cb3991c780fc33c01343e0c4576)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conditionDocumentAttributeKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9101df7986b49c0068b8bcedc789b047954bcea1372350766f7afa97b602c63f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b836388e77b86398ed5058ce87114daec76eac07ce1dfa7a51cbed3949fde35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d629dc5b6a70f75fb9f480550369d5ee70f5631c4d8548d3d5725d3bfb1c791)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInvocationCondition")
    def put_invocation_condition(
        self,
        *,
        condition_document_attribute_key: builtins.str,
        operator: builtins.str,
        condition_on_value: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param condition_document_attribute_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition_document_attribute_key KendraDataSource#condition_document_attribute_key}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#operator KendraDataSource#operator}.
        :param condition_on_value: condition_on_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#condition_on_value KendraDataSource#condition_on_value}
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition(
            condition_document_attribute_key=condition_document_attribute_key,
            operator=operator,
            condition_on_value=condition_on_value,
        )

        return typing.cast(None, jsii.invoke(self, "putInvocationCondition", [value]))

    @jsii.member(jsii_name="resetInvocationCondition")
    def reset_invocation_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvocationCondition", []))

    @builtins.property
    @jsii.member(jsii_name="invocationCondition")
    def invocation_condition(
        self,
    ) -> KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionOutputReference:
        return typing.cast(KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionOutputReference, jsii.get(self, "invocationCondition"))

    @builtins.property
    @jsii.member(jsii_name="invocationConditionInput")
    def invocation_condition_input(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition], jsii.get(self, "invocationConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaArnInput")
    def lambda_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaArnInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketInput")
    def s3_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BucketInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaArn")
    def lambda_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaArn"))

    @lambda_arn.setter
    def lambda_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ba4b0f216a91bbc7cb630fff688fc298110ce638ebaa6bdb2073b7368074b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Bucket"))

    @s3_bucket.setter
    def s3_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__291ccf5910de0cee21abf3fa63430ebbd3a78bdac56ebe33fe5cc5e3a1e33ee3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c17958b39000ab11b3700258e74eabb49bc915d8d90647674f04570e6fa6e7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class KendraDataSourceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#create KendraDataSource#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#delete KendraDataSource#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#update KendraDataSource#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051be9cb155ef5d7760000cf6342931b8b114abae360d43167df7a96f2de7497)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#create KendraDataSource#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#delete KendraDataSource#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_data_source#update KendraDataSource#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraDataSource.KendraDataSourceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58a054e2a1075f9978ab6b815d909ba98a408f3011ca35478824943b1fc76d08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88dd8e17e71cfcdd209e18fe73ce87943ef4027c0d2926719222d9632576478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a2266d779ffaa2c58bfa39fb5c0b7e34eab8c71ee3bfc031f43b22fc3afc148)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f61a24270f29c9a52f0d54032a75d67d0b8da1e11aa3acf535812037e94929f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fce650e484326e0f63bf1afd7bd73db4470408bfe318cfe69502e58d4581f26b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "KendraDataSource",
    "KendraDataSourceConfig",
    "KendraDataSourceConfiguration",
    "KendraDataSourceConfigurationOutputReference",
    "KendraDataSourceConfigurationS3Configuration",
    "KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration",
    "KendraDataSourceConfigurationS3ConfigurationAccessControlListConfigurationOutputReference",
    "KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration",
    "KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfigurationOutputReference",
    "KendraDataSourceConfigurationS3ConfigurationOutputReference",
    "KendraDataSourceConfigurationTemplateConfiguration",
    "KendraDataSourceConfigurationTemplateConfigurationOutputReference",
    "KendraDataSourceConfigurationWebCrawlerConfiguration",
    "KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration",
    "KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication",
    "KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationList",
    "KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationOutputReference",
    "KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationOutputReference",
    "KendraDataSourceConfigurationWebCrawlerConfigurationOutputReference",
    "KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration",
    "KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfigurationOutputReference",
    "KendraDataSourceConfigurationWebCrawlerConfigurationUrls",
    "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsOutputReference",
    "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration",
    "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfigurationOutputReference",
    "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration",
    "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfigurationOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfiguration",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValueOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsList",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValueOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationOutputReference",
    "KendraDataSourceTimeouts",
    "KendraDataSourceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__601295c808dbd3bcca62f66fe95ad3079963a7a1605eeecc8ce27e49e7275101(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    index_id: builtins.str,
    name: builtins.str,
    type: builtins.str,
    configuration: typing.Optional[typing.Union[KendraDataSourceConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_document_enrichment_configuration: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    language_code: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[KendraDataSourceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e963f7af95b80df7f86dc0b492776c355f162e8a878a50d24dbe76becce79694(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9414d39c9d6576175ef24b1024bef6f32dd09edb76f16c69d9ec3297f8bf425(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b96bd49078d7f4d10a29741fe638f3801b1c8a18571a79b4a755c7866b7f36e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25df564385bd9270144baba4898a615bffe610e051cb1d78c549a8b3950364c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a7ac653d97ee25f9b7d69e8ccfad0d3cdd2aeeabd6d536f876ba701c5562de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872a4912312482ca4148d844cd46e8457c767f9de6968db2b33097b933a0599f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e8c2db16e35824e6ad3b3f5f1204dc838f1e484c339a21d0a008009472583d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a09669d2ae079be243e56fb3b0601954022448bc1cae527fb3664eb34a7ee44a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ea24ca14290c7461c6d94ccf34110b34c43ab860cbc9bb65e37e0645d92f02a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4809e09f1a3a0a07815d2be74e916e5539b1bcca9c246228cb0e69b6074344bf(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3237bb9bb1bb84fc3e627bd5c3f94146a44bb6e6c9d311e4bd09692d6ac40b7c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb088e6c51691fd60276568e5643c0999be4356f9b59787a8c0160aea574774(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc7c62ed3175de52300a56dad30ffcc10d42233c9ce92d3d34ff144ce12dbec(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    index_id: builtins.str,
    name: builtins.str,
    type: builtins.str,
    configuration: typing.Optional[typing.Union[KendraDataSourceConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_document_enrichment_configuration: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    language_code: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[KendraDataSourceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33eed49f6ad43a0e4539a16e56a37e4add0430f2db747015aa1140e2a29b960d(
    *,
    s3_configuration: typing.Optional[typing.Union[KendraDataSourceConfigurationS3Configuration, typing.Dict[builtins.str, typing.Any]]] = None,
    template_configuration: typing.Optional[typing.Union[KendraDataSourceConfigurationTemplateConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    web_crawler_configuration: typing.Optional[typing.Union[KendraDataSourceConfigurationWebCrawlerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcae7d4a29d5adf2f7ed93c6062e00e741ae93a9f0fa425536e4aee08ffa5402(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82184b8184002e7cf54975e92b3ada30847c0339924ed541a5ee2e5283f0541e(
    value: typing.Optional[KendraDataSourceConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5654b469bf49c68ede20f3759380d7ddb82296c368a806f5fa5ab9cc33a33d33(
    *,
    bucket_name: builtins.str,
    access_control_list_configuration: typing.Optional[typing.Union[KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    documents_metadata_configuration: typing.Optional[typing.Union[KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ee47f4c373feeb2fb33e64b79bb9a36c6e2d2f93f1c632863030abfda18f97(
    *,
    key_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b3bd03da2f48c60dea7a9713bd62c4719e64826f76b78d171b2bd921b928ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519e093483b2182bcd056509e206c2d9edb7f9afad6e90881504d2e576f9bd6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d400c32e303c3cdf06eaad204718a0d6f9156de2f0db39826deee2883872f7(
    value: typing.Optional[KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e001b435b916cc761b681bafe11decf12fb4bbed0e488b8f4535018ead20364(
    *,
    s3_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdbe86ac294d08ae278bac22acf812dad89bca82bbcf2eac0e2fe6ba5e233492(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088cb4e2599ef8f1d90ade9435dec1abe0a0de7a8ed5b39129bfa98a5708d594(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86eb012b62a2e4423fdc38e0de0a49c458d1e83be06959084d49416e682e4322(
    value: typing.Optional[KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3caff72dccf4b5688c4ab1d9d855bc26d3aaf3f403aacbfbf7e4fb1a0ddd210b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58a44513c9920ef69f4327203b724a4a9c01b117bbcb5c8b65ffb86df6e2221b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db6481adf1f0d50b5fd5ba965cc713429914c2a5f00f4a4897857c8487bb313(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__058340ae8d0a950d65dc8a6b1e59070741a677a57a8c5367e0aa9f5d42e8a6be(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f992d3618c955055477da953edd2ea8732adcee2cb364330aa84f9291c0637(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__784da9c29762c81b7778c7b93d564fa0306c60b605462bb69fb017a3ac8ede93(
    value: typing.Optional[KendraDataSourceConfigurationS3Configuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91fa636ebc2ae6e7965d921e82cf41bd2fe37ad098ea0b47061896e587717f5c(
    *,
    template: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7284d709c85fec54bc7d29f2400dd8ceaed88dce678e577eb24499461f130c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32944546e297ba202cb4c6e9e42fd122251fa09703c504cfe3f3906caf538638(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7ab5e46d70cbc67ec458900004b4abe6f5761e5f06a718cd0d5968f762ccc1(
    value: typing.Optional[KendraDataSourceConfigurationTemplateConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d144c53335874659fb463ef4fd40424ecf52fabcea8a246e4246b3b1477f4f(
    *,
    urls: typing.Union[KendraDataSourceConfigurationWebCrawlerConfigurationUrls, typing.Dict[builtins.str, typing.Any]],
    authentication_configuration: typing.Optional[typing.Union[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    crawl_depth: typing.Optional[jsii.Number] = None,
    max_content_size_per_page_in_mega_bytes: typing.Optional[jsii.Number] = None,
    max_links_per_page: typing.Optional[jsii.Number] = None,
    max_urls_per_minute_crawl_rate: typing.Optional[jsii.Number] = None,
    proxy_configuration: typing.Optional[typing.Union[KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    url_exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    url_inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e97f4755f274ba94dd88edd04736dd486904719d36f3aad60be0fb7f363235(
    *,
    basic_authentication: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dd7091456d97da8163fa071443c814eed0e781e9c658c9321b1caa4b47b15e0(
    *,
    credentials: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8d0675a2489d557532b963438a4e7f1741f9d7bd3a4ee988bd6bf6cb6926ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef3344928d5e4a39c006d2855ea979a66b6713c99518f749fc7048789ea6e17(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2844c54df9e77c6fab64cb26397ee1846867b0507d1c7de1e690d6235ef1b086(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61be02f8426c0b3d8ae12a152b6d200ec02735098486bf892c6893f56459672b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__571e40fd4e84969ad128a64c32188b1f455348bd43be3c2455c8c49dd5361220(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac6366db632465583cf9805b93d636fab32eb73da11f63b6d8afed6182189b5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474b82d05f48a8067d93455691f788996b7b67250882f3d11f6d01bfff9a027d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c31a7b783664f009fd82a188202f2c9734eaf8bca0c8e8f5baf10fa4446a71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed15c788f9b45886942744d9b89aa7cc957575efa3dc85d44fe44f0755f04e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c89a29890fb37d66082e538322981c4c26b925ae37e9f9884452a09892ddc26(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d0b5584f6dd37e8666d8fa92b5b45d88c3b7e5ce2e1334edb2a8f2903c2fa66(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8212bcb25ffdd6ffe80c363d12b670004691c1bae617fe2871cbdfaf38d7b4f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc3335c826e986763e6d0d6f6191c3cf080accae9f3f79dd39d3011e30253c6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710933ed8c6cd0548401168f2f468825831122068a6cb617604df5d9d680ee33(
    value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__866c491357da916c17bccfc78d328120007adc4308adc1a153722f6813d03390(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e9dac34c5d57775adf4bc377e8f66b12bef422671b9c6bd9b8ad2b1f07e24f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc2f9e3c2f785444802290d916cde85ab211b3c6f031b994bf0605e106bbd9c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e058cccd6236ba019d6ab61110f97bcb63360aad4a075311fa2efb2193a4703(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94da263da28e1a73baeda5f61bccba821de2a4939efd653a64f9d4b34042d11a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1359e47f5ab59289fe97f62d8548b2271cfed31e48caabc78b1ef187debc2ff(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7240999043e9642b77d04ed87f6ff2fb5885a55e3197241f64a8066021fec2e4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6022cc606d532288d52b3147f1b9e3431f8934641d1ac5a38a71df419b6b1ad(
    value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf79b929cc438545112e015de37a4442c557fb9d160ce65459839f3427985b59(
    *,
    host: builtins.str,
    port: jsii.Number,
    credentials: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__542165a6e9b7fbe7e95e9d595dc77614d68f8fe2daf857184541d8c932c95b4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643b1cec3a3508cacba14267238ff0123666d7f1e29127367e9e507584aec044(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dfd45e47306f51796951958563e226d5daf731a1085eb3589ca59dc9ec1e3ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d09170888fcb6b9a2dffa7fae9c73ce1f4d6ba2a2dbe0dcf847363a9b34fb6a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a69b26827ffd28bd95497eee2444098b7524d8dc3e7ae54572f32555c8ed832(
    value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a5b5bd0b38657944a5a736a77dca494d87fa48392edff4fae2db1f3a49c0ab6(
    *,
    seed_url_configuration: typing.Optional[typing.Union[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    site_maps_configuration: typing.Optional[typing.Union[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdb7938a1ff5bd2a4bc30eae53be45452b2e4058c9b8bdba2763aade34e4297b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dfe8d333abe3ab104d6642d48ed467badcd419400f9a4f4f0468385cc39fd6a(
    value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrls],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54202180d4b019d797082e0eb1dede4db3daf9421f85e38432c97b2ac447c1b(
    *,
    seed_urls: typing.Sequence[builtins.str],
    web_crawler_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e24d546b778179da631a30aaebd65f91d7ad333af730909fd2dfdad605d11212(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432a22fdfa3e19ca7927d2ea470eacbb462d7ef82088371b49172bdbce42ce3f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d2507d2c4e89e4fea23cbe3b30089bdac9198dbbf5937a7e4f1bae6ad5c20a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f43932b819ca4171775a6e97788069f0da982eb36d568d10cb4c136c499800b3(
    value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa2154379922e817b228479134a214055c882b865229a734fc9c6d64804a3f7(
    *,
    site_maps: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f902f3053b43ddef1661af2d0ae9a5b87eebf1bd0dcefc51d9d2f9e828191d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73a19261abd07a13a91b3cd5e2b01271dc4873988735cbf435bce7ce30439b1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0613039a34ef5e5372107bc57a0ec3fb3e811c0f188da8efe0e634cabe07f74d(
    value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ec8fa87ec2b318982c6f4e0b5aa8badc1f8f9710bb2333b08f84cb4b6a7711(
    *,
    inline_configurations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    post_extraction_hook_configuration: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    pre_extraction_hook_configuration: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b94ddb9aa7fcd2a18c6af1b704eff87387748d47f4a51a2050668824402e17c5(
    *,
    condition: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    document_content_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    target: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a2ec1e2925630cd2dfb24467fa944dcfc0109b856dcdfe7171d9874ae8dc93(
    *,
    condition_document_attribute_key: builtins.str,
    operator: builtins.str,
    condition_on_value: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__260aff2ce28269c651bca5ec8aee18f496fffa07097cf8dcb67bc4a5d9cc601a(
    *,
    date_value: typing.Optional[builtins.str] = None,
    long_value: typing.Optional[jsii.Number] = None,
    string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1a038cf7fbdda5811f80e5f65f1a26f7e653723174cde0c18530d7eb79061ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49183218bf3ff207bd9a4ffdaf25f37ecbca97d1db0fb352fc73ff093b56db94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e24acaff46b0e5f6b2f1d158dd8ad0a6cfeae0907b1908ecd685ed60f2613d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e224790a7897b9bd09643042fea8fadd87c06cadd4053a4278ab5b934f9b8920(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f7898a7dc030a50f4a35ff01768ebd2471582250deea4fc1cac43ed16554fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6148319bc238e47971eeba6e654126a89997f44d3be6365bcadf2d086dfd405b(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75131161df10301f370f878b0d3c76ffd13d2cd099863333a1617933e75646ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb450f83e0c7ce975a297989ae5d330e2e70419eb429cac6efb9013d47ee4445(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0170941b4ac360d4868e5d98afecec06c0f65bb3febc0888ad7f59976282d40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfef27ea3dbb2909439eab5a4f941ce8cde3b1d7ccee945987fb950c8f88d594(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b279041684fcc2736c07725848cf306f9add3d57db850f89224fae1447f7770a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fd4b8b4b09358e7180c0254bb2c8e13844ed5404f01c1e94a1ed7a3c8c5219(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf794f70718cab9f6d88f13d121dd4d2d0e670121fea1982866cf72cd4fc8672(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4480b84d8ad437e96a504db8404f28a8c7e7f3be8312dc0b17c58008bf58249(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__654e91e10c7f6cd199cd98e662681c44a8987e6b9bd258d035d27b4d9bd7bc2c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1135c4142721af293f6a1081e2bf5eb76d4d4a284c74bc7b6debbbc013ad936(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4226710f899a5b786b3157973024f29d49172549fb3e915381364d96c9a1f3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8683de74145010db0c948939285be0245f41b79fabf8d8d78b69d2427cec4fd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ece5e6be733bf20eebf65ddad3e737af1da3a7243dab8084e47b2b8a34a6b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082116a94d82277c37b7f6ab1ec2b9b3a9cd24dfa0f64360bd55ca9392972c62(
    *,
    target_document_attribute_key: typing.Optional[builtins.str] = None,
    target_document_attribute_value: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue, typing.Dict[builtins.str, typing.Any]]] = None,
    target_document_attribute_value_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a6e9c89463262e36a83c3a8181184a4f782a8a0bc805b553ab84618a02df490(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19459c12fd4037f5fc2b98fe531b1129f9b875660cb2548e6dea5a60d8008b83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1d85585c7a2f564eb0433874be25246529f9771bfac73ed9fc68f2c9fcc6aa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c8a25197b8ca83566e5664f95d01e882cf91fec88c1da723d42e575465007c8(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374e94fc584d9aef3583c3e5a0555b8a416de8b513050e88746df4d36c13df71(
    *,
    date_value: typing.Optional[builtins.str] = None,
    long_value: typing.Optional[jsii.Number] = None,
    string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5125c2337233c8190b8bc65fe6cc5b6f41e9250855660d73e7e9f4fc82c96e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e5a6a0ede63f47eb11bed31f8758df7ab838b829fccc5c6d7a1c6b0ec117f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce2a2c9319e17f502b4264de0e8ebccd3205384a070e651a72b5e5711aba420d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee73b5adcc91a858679a5d902c0cd955a0971dd88ad34637e40aa7d82606432(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4eb360c3066babe6d8db893088b90a856a78a6662c50b27b57037048f35b081(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c2fecd3bd9a9a1cb5262da1a47dada2a87cc46404e52883022ddad13a7a613(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2bf319f2f7b7cc13df1b0cc3c61f1b493c3e3591e735121e6afc8f64934f512(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716ae988460ae9be2c017c42e024a52990753b278f71f068507d6771871d86a6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d095d7b477efc7117e0a0625623bbe93ac3fd9b1a3119715d703b2dd04236cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ee0172acf7a3bc458cb54170dcef0dd36e5c01886fc6b4dae10dfc530dee20(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a97940073870a7fb974efd102c7c19538e62586726bf17366eb734ab77bfcc8(
    *,
    lambda_arn: builtins.str,
    s3_bucket: builtins.str,
    invocation_condition: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42e616d63df4c9ec32eaeb6ce9afa748c23f67a4a53ef611920089a25f25beb(
    *,
    condition_document_attribute_key: builtins.str,
    operator: builtins.str,
    condition_on_value: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f67dffbb04f5d7b34abb50caf364214179ade130ebda84939438558754827cd3(
    *,
    date_value: typing.Optional[builtins.str] = None,
    long_value: typing.Optional[jsii.Number] = None,
    string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acadad16783106b2a52e1e4da86a97a7b72ca19b8cb58c7ef9c7cd32204e4c10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bbb0ab6cc324addc6eea6bb2c39c31ee9fc084797dd903dd4e848f948ea3fe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1420d6ade74938cb3db297297a590459ff21a611663aa9cd9affd4aa4ade8e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__404a02f4462b6bd6cea2a59178af0df138ac43c119c4e969d8d9c3273a03fb26(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af165b3124c88d2f0344d590e7c2fe63008f07cb610cdc2f06f8ae56545a6bc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7de6d2e84853826998c71566f2e3ae5cc10665beb32dbe7eda6a9fa60be579(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ee628d5d09d238392be5beffe87d70d6cc6618c8fa1b736979e587a95a8d71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff1c7fd0c6ac11f5b10b508991ffef991a03b73b4a4badbedc91cc523f0cc4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71498d9bae0785bb868be8271a5cc3573f452fead9429307317e8f8ae338ed8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa5f00dbba79a1b41bae748280c2838aad78e0612007f86be0fafef0213ac948(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e93447a983bca7d324879ad94fe6f898261c65981fcd4792130f304fb22379b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c4bb6ae23049e33bffad47af7567ae1cea0ea275971bb0b3248449d8a527664(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e79f634f2d81aaa5d0ba116c753f8369a1cb6eb8efc12a9f0e4c012c381e484e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd04b6b712438223c55632c32f5ea941731ad2b814083116a40be8ce355ed41c(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742e000a5448746e0b975626ca946ae280a2c8a998ac28666da38035d41c038d(
    *,
    lambda_arn: builtins.str,
    s3_bucket: builtins.str,
    invocation_condition: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05eb70b74a0e1a88c73ad47c01315ac5e0d8b0583eb79705f9ab2a81c17c9dd7(
    *,
    condition_document_attribute_key: builtins.str,
    operator: builtins.str,
    condition_on_value: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb63ee831d808200d050c25dcc8fe81c0aeb1815e598be5a5ce4de15fa45335(
    *,
    date_value: typing.Optional[builtins.str] = None,
    long_value: typing.Optional[jsii.Number] = None,
    string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__632fc5b0f356b78d713058bd9020da8963539b85914e858a90fc077e953dd310(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f26af1705f39b25c76c3b45f8e5c3af99299525d3aaf642ada950b6febe4c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e13215e1e0140501f45b2431b1f86b6fe73932f08869e71d165d9cc3996d3e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b735e74e568237fc551237f899998a4f37295695018dfe9871efbba1af3fdf8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e905877fe200971011035d9e548bf7221d93bd0747265170bf04a1204fe8b5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf02e81ce8312e26e485a72052d486c4e72d7ccaaea7a2f9884fb7f0c930f044(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d81220d3f7db2658a6dd30e95c71a184162abb3c4dca99e40e34be696a3e4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d49e39ca0c94a4683dbf19c9286a5060ee0a3cb3991c780fc33c01343e0c4576(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9101df7986b49c0068b8bcedc789b047954bcea1372350766f7afa97b602c63f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b836388e77b86398ed5058ce87114daec76eac07ce1dfa7a51cbed3949fde35(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d629dc5b6a70f75fb9f480550369d5ee70f5631c4d8548d3d5725d3bfb1c791(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba4b0f216a91bbc7cb630fff688fc298110ce638ebaa6bdb2073b7368074b39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291ccf5910de0cee21abf3fa63430ebbd3a78bdac56ebe33fe5cc5e3a1e33ee3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c17958b39000ab11b3700258e74eabb49bc915d8d90647674f04570e6fa6e7f(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051be9cb155ef5d7760000cf6342931b8b114abae360d43167df7a96f2de7497(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58a054e2a1075f9978ab6b815d909ba98a408f3011ca35478824943b1fc76d08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88dd8e17e71cfcdd209e18fe73ce87943ef4027c0d2926719222d9632576478(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a2266d779ffaa2c58bfa39fb5c0b7e34eab8c71ee3bfc031f43b22fc3afc148(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f61a24270f29c9a52f0d54032a75d67d0b8da1e11aa3acf535812037e94929f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fce650e484326e0f63bf1afd7bd73db4470408bfe318cfe69502e58d4581f26b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
