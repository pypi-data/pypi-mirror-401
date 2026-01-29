r'''
# `aws_emrcontainers_job_template`

Refer to the Terraform Registry for docs: [`aws_emrcontainers_job_template`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template).
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


class EmrcontainersJobTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template aws_emrcontainers_job_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        job_template_data: typing.Union["EmrcontainersJobTemplateJobTemplateData", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["EmrcontainersJobTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template aws_emrcontainers_job_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param job_template_data: job_template_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#job_template_data EmrcontainersJobTemplate#job_template_data}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#name EmrcontainersJobTemplate#name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#id EmrcontainersJobTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#kms_key_arn EmrcontainersJobTemplate#kms_key_arn}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#region EmrcontainersJobTemplate#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#tags EmrcontainersJobTemplate#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#tags_all EmrcontainersJobTemplate#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#timeouts EmrcontainersJobTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ce5170f32e1b9e5c6f4f5ddfc53e0cb1661fb1dcbb3c9ce387297901ea1920f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EmrcontainersJobTemplateConfig(
            job_template_data=job_template_data,
            name=name,
            id=id,
            kms_key_arn=kms_key_arn,
            region=region,
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
        '''Generates CDKTF code for importing a EmrcontainersJobTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EmrcontainersJobTemplate to import.
        :param import_from_id: The id of the existing EmrcontainersJobTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EmrcontainersJobTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edfeb6aa6a2a9269602becb9d2bc4e98aecdbdcd3254f5b64d9e4bc8fc349c13)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putJobTemplateData")
    def put_job_template_data(
        self,
        *,
        execution_role_arn: builtins.str,
        job_driver: typing.Union["EmrcontainersJobTemplateJobTemplateDataJobDriver", typing.Dict[builtins.str, typing.Any]],
        release_label: builtins.str,
        configuration_overrides: typing.Optional[typing.Union["EmrcontainersJobTemplateJobTemplateDataConfigurationOverrides", typing.Dict[builtins.str, typing.Any]]] = None,
        job_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#execution_role_arn EmrcontainersJobTemplate#execution_role_arn}.
        :param job_driver: job_driver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#job_driver EmrcontainersJobTemplate#job_driver}
        :param release_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#release_label EmrcontainersJobTemplate#release_label}.
        :param configuration_overrides: configuration_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#configuration_overrides EmrcontainersJobTemplate#configuration_overrides}
        :param job_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#job_tags EmrcontainersJobTemplate#job_tags}.
        '''
        value = EmrcontainersJobTemplateJobTemplateData(
            execution_role_arn=execution_role_arn,
            job_driver=job_driver,
            release_label=release_label,
            configuration_overrides=configuration_overrides,
            job_tags=job_tags,
        )

        return typing.cast(None, jsii.invoke(self, "putJobTemplateData", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, delete: typing.Optional[builtins.str] = None) -> None:
        '''
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#delete EmrcontainersJobTemplate#delete}.
        '''
        value = EmrcontainersJobTemplateTimeouts(delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsKeyArn")
    def reset_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyArn", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="jobTemplateData")
    def job_template_data(
        self,
    ) -> "EmrcontainersJobTemplateJobTemplateDataOutputReference":
        return typing.cast("EmrcontainersJobTemplateJobTemplateDataOutputReference", jsii.get(self, "jobTemplateData"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "EmrcontainersJobTemplateTimeoutsOutputReference":
        return typing.cast("EmrcontainersJobTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="jobTemplateDataInput")
    def job_template_data_input(
        self,
    ) -> typing.Optional["EmrcontainersJobTemplateJobTemplateData"]:
        return typing.cast(typing.Optional["EmrcontainersJobTemplateJobTemplateData"], jsii.get(self, "jobTemplateDataInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

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
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EmrcontainersJobTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EmrcontainersJobTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bd2addf4fe22cdaf16e446eeb695eb3bb662b87409a8179f1dd6b134a988133)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a8ec6fbdcf71eca9026935abe6e26b593cb766ede98702aac8ccceecf714d70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feadbc5ce32c3eba8eab78e06d3cd28ff17c12bdd7a9ff464f9492bd41d6f3ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df89225536834d816df913e5e7cf67f293472cc28eeee99ad6bc80d7702ce412)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0326106aea9705448caf48e6297f6165fdec7e1161bad394c18ed533a9896a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86113161ae54d52d671dca944162f967b396484063ceb5ac1795c565e938c0bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "job_template_data": "jobTemplateData",
        "name": "name",
        "id": "id",
        "kms_key_arn": "kmsKeyArn",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class EmrcontainersJobTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        job_template_data: typing.Union["EmrcontainersJobTemplateJobTemplateData", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["EmrcontainersJobTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param job_template_data: job_template_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#job_template_data EmrcontainersJobTemplate#job_template_data}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#name EmrcontainersJobTemplate#name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#id EmrcontainersJobTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#kms_key_arn EmrcontainersJobTemplate#kms_key_arn}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#region EmrcontainersJobTemplate#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#tags EmrcontainersJobTemplate#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#tags_all EmrcontainersJobTemplate#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#timeouts EmrcontainersJobTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(job_template_data, dict):
            job_template_data = EmrcontainersJobTemplateJobTemplateData(**job_template_data)
        if isinstance(timeouts, dict):
            timeouts = EmrcontainersJobTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__930c45fc2da31a0f824920baed5ece327eef4f03b8f8affecffa3bd2a485a192)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument job_template_data", value=job_template_data, expected_type=type_hints["job_template_data"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "job_template_data": job_template_data,
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
        if id is not None:
            self._values["id"] = id
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if region is not None:
            self._values["region"] = region
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
    def job_template_data(self) -> "EmrcontainersJobTemplateJobTemplateData":
        '''job_template_data block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#job_template_data EmrcontainersJobTemplate#job_template_data}
        '''
        result = self._values.get("job_template_data")
        assert result is not None, "Required property 'job_template_data' is missing"
        return typing.cast("EmrcontainersJobTemplateJobTemplateData", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#name EmrcontainersJobTemplate#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#id EmrcontainersJobTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#kms_key_arn EmrcontainersJobTemplate#kms_key_arn}.'''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#region EmrcontainersJobTemplate#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#tags EmrcontainersJobTemplate#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#tags_all EmrcontainersJobTemplate#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["EmrcontainersJobTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#timeouts EmrcontainersJobTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["EmrcontainersJobTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrcontainersJobTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateData",
    jsii_struct_bases=[],
    name_mapping={
        "execution_role_arn": "executionRoleArn",
        "job_driver": "jobDriver",
        "release_label": "releaseLabel",
        "configuration_overrides": "configurationOverrides",
        "job_tags": "jobTags",
    },
)
class EmrcontainersJobTemplateJobTemplateData:
    def __init__(
        self,
        *,
        execution_role_arn: builtins.str,
        job_driver: typing.Union["EmrcontainersJobTemplateJobTemplateDataJobDriver", typing.Dict[builtins.str, typing.Any]],
        release_label: builtins.str,
        configuration_overrides: typing.Optional[typing.Union["EmrcontainersJobTemplateJobTemplateDataConfigurationOverrides", typing.Dict[builtins.str, typing.Any]]] = None,
        job_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#execution_role_arn EmrcontainersJobTemplate#execution_role_arn}.
        :param job_driver: job_driver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#job_driver EmrcontainersJobTemplate#job_driver}
        :param release_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#release_label EmrcontainersJobTemplate#release_label}.
        :param configuration_overrides: configuration_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#configuration_overrides EmrcontainersJobTemplate#configuration_overrides}
        :param job_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#job_tags EmrcontainersJobTemplate#job_tags}.
        '''
        if isinstance(job_driver, dict):
            job_driver = EmrcontainersJobTemplateJobTemplateDataJobDriver(**job_driver)
        if isinstance(configuration_overrides, dict):
            configuration_overrides = EmrcontainersJobTemplateJobTemplateDataConfigurationOverrides(**configuration_overrides)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83a346369556b1c401a5587ab12af4ef743b18627db53ebeb85906753e1f3415)
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument job_driver", value=job_driver, expected_type=type_hints["job_driver"])
            check_type(argname="argument release_label", value=release_label, expected_type=type_hints["release_label"])
            check_type(argname="argument configuration_overrides", value=configuration_overrides, expected_type=type_hints["configuration_overrides"])
            check_type(argname="argument job_tags", value=job_tags, expected_type=type_hints["job_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execution_role_arn": execution_role_arn,
            "job_driver": job_driver,
            "release_label": release_label,
        }
        if configuration_overrides is not None:
            self._values["configuration_overrides"] = configuration_overrides
        if job_tags is not None:
            self._values["job_tags"] = job_tags

    @builtins.property
    def execution_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#execution_role_arn EmrcontainersJobTemplate#execution_role_arn}.'''
        result = self._values.get("execution_role_arn")
        assert result is not None, "Required property 'execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def job_driver(self) -> "EmrcontainersJobTemplateJobTemplateDataJobDriver":
        '''job_driver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#job_driver EmrcontainersJobTemplate#job_driver}
        '''
        result = self._values.get("job_driver")
        assert result is not None, "Required property 'job_driver' is missing"
        return typing.cast("EmrcontainersJobTemplateJobTemplateDataJobDriver", result)

    @builtins.property
    def release_label(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#release_label EmrcontainersJobTemplate#release_label}.'''
        result = self._values.get("release_label")
        assert result is not None, "Required property 'release_label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration_overrides(
        self,
    ) -> typing.Optional["EmrcontainersJobTemplateJobTemplateDataConfigurationOverrides"]:
        '''configuration_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#configuration_overrides EmrcontainersJobTemplate#configuration_overrides}
        '''
        result = self._values.get("configuration_overrides")
        return typing.cast(typing.Optional["EmrcontainersJobTemplateJobTemplateDataConfigurationOverrides"], result)

    @builtins.property
    def job_tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#job_tags EmrcontainersJobTemplate#job_tags}.'''
        result = self._values.get("job_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrcontainersJobTemplateJobTemplateData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataConfigurationOverrides",
    jsii_struct_bases=[],
    name_mapping={
        "application_configuration": "applicationConfiguration",
        "monitoring_configuration": "monitoringConfiguration",
    },
)
class EmrcontainersJobTemplateJobTemplateDataConfigurationOverrides:
    def __init__(
        self,
        *,
        application_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        monitoring_configuration: typing.Optional[typing.Union["EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param application_configuration: application_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#application_configuration EmrcontainersJobTemplate#application_configuration}
        :param monitoring_configuration: monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#monitoring_configuration EmrcontainersJobTemplate#monitoring_configuration}
        '''
        if isinstance(monitoring_configuration, dict):
            monitoring_configuration = EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfiguration(**monitoring_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfd41c89e82e041309825231e353d28d75eea5201aca34b311cb12d77adbd2ac)
            check_type(argname="argument application_configuration", value=application_configuration, expected_type=type_hints["application_configuration"])
            check_type(argname="argument monitoring_configuration", value=monitoring_configuration, expected_type=type_hints["monitoring_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_configuration is not None:
            self._values["application_configuration"] = application_configuration
        if monitoring_configuration is not None:
            self._values["monitoring_configuration"] = monitoring_configuration

    @builtins.property
    def application_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration"]]]:
        '''application_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#application_configuration EmrcontainersJobTemplate#application_configuration}
        '''
        result = self._values.get("application_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration"]]], result)

    @builtins.property
    def monitoring_configuration(
        self,
    ) -> typing.Optional["EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfiguration"]:
        '''monitoring_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#monitoring_configuration EmrcontainersJobTemplate#monitoring_configuration}
        '''
        result = self._values.get("monitoring_configuration")
        return typing.cast(typing.Optional["EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrcontainersJobTemplateJobTemplateDataConfigurationOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "classification": "classification",
        "configurations": "configurations",
        "properties": "properties",
    },
)
class EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration:
    def __init__(
        self,
        *,
        classification: builtins.str,
        configurations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param classification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#classification EmrcontainersJobTemplate#classification}.
        :param configurations: configurations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#configurations EmrcontainersJobTemplate#configurations}
        :param properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#properties EmrcontainersJobTemplate#properties}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c59a080635dbf8d7ba787da5e701052268f38b9cdce76a79e949057e2a6f3f87)
            check_type(argname="argument classification", value=classification, expected_type=type_hints["classification"])
            check_type(argname="argument configurations", value=configurations, expected_type=type_hints["configurations"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "classification": classification,
        }
        if configurations is not None:
            self._values["configurations"] = configurations
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def classification(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#classification EmrcontainersJobTemplate#classification}.'''
        result = self._values.get("classification")
        assert result is not None, "Required property 'classification' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configurations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations"]]]:
        '''configurations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#configurations EmrcontainersJobTemplate#configurations}
        '''
        result = self._values.get("configurations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations"]]], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#properties EmrcontainersJobTemplate#properties}.'''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations",
    jsii_struct_bases=[],
    name_mapping={"classification": "classification", "properties": "properties"},
)
class EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations:
    def __init__(
        self,
        *,
        classification: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param classification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#classification EmrcontainersJobTemplate#classification}.
        :param properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#properties EmrcontainersJobTemplate#properties}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8924b0f385b7670a2a70556b27f9e4b80575842eb3f21b326934c14c0d4dbe8d)
            check_type(argname="argument classification", value=classification, expected_type=type_hints["classification"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if classification is not None:
            self._values["classification"] = classification
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def classification(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#classification EmrcontainersJobTemplate#classification}.'''
        result = self._values.get("classification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#properties EmrcontainersJobTemplate#properties}.'''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3c2caa72563f88addb5184732375845db707e5ef89e07876264e2769c24dd62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87bbec6a0a571cdb6abfdf4a6843b486437f251eaae4164eac224e481b447a0b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af39cd85cf8b3952821450bae0f739a8f6a5eef6a6ede57e83b186f69eaa681)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b76c04ba29406db9e9531b385a7fd5ad7c4d143329813a4ce4e89b6e1c56912a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3afe3282ae52f30661e244f6a6b201bf54bdb7da8c099eb9b6a1189410c480b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12dc29a1adf419f645f8c1b74f75a3e1d144a37d73fd6f781c2245efac49db48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84d5d7dc4f2d0b734ea2fac1854f73dc15490e72905484258e5be5f0a68bb94c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetClassification")
    def reset_classification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClassification", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="classificationInput")
    def classification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "classificationInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="classification")
    def classification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "classification"))

    @classification.setter
    def classification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ff4ce76d39d12111ce84918d35407507f2ea480935b64e14aef94f49bce8c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f45170410aed80435c4f86cc6dbcc53ba1cf242ae7c1d087da294c5b2930f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c5e4eb36de4a91af3c03ff75aa4b6995842e3cf35dca6c1a7ea65a53d4c0845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c74776c0c9edc319ed294ce9eccc064b7633c68a752b1e74bef955f99bff9f8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f4853ca784243921f867687378cd5e3f46f9d86c6e8539d204e71be60da968c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a96421a04120618455d737263ed7f58d12273d5539c89b4890a4e2b2e97960b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b08588a511d3e98f1814f2b9b0fd4602b1407e3065f4c78c0fb6822ef8e9cf19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4df418596ea8cf5d88c6741fbed1334122d53a3a326725be6d16346058a5717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1acaf773064d25c0cba2b8fdf31832a8d23a879e99953f8056b67be05e6494)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b33c65d6568f1c953f8e91d00eb2fc0a3420318244a15103bd6805de9e5d6981)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putConfigurations")
    def put_configurations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631435b4eb75df9dbbca4cdb11f8752aafeac1d10cf53f2cf6367d75297dcd30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConfigurations", [value]))

    @jsii.member(jsii_name="resetConfigurations")
    def reset_configurations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigurations", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="configurations")
    def configurations(
        self,
    ) -> EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurationsList:
        return typing.cast(EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurationsList, jsii.get(self, "configurations"))

    @builtins.property
    @jsii.member(jsii_name="classificationInput")
    def classification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "classificationInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationsInput")
    def configurations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations]]], jsii.get(self, "configurationsInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="classification")
    def classification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "classification"))

    @classification.setter
    def classification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e849f897301406b7048f2bc6dea23a9fc5a707b436cbd4ce57277c463171b997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab20ba878eb4d36b70f5cc49b7228c44d7894114e835f4c1b07c126c7c42d37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f68331c1efc7be2c3673021b3bedc490da5b34785759a1b7c79c85c01563f70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_watch_monitoring_configuration": "cloudWatchMonitoringConfiguration",
        "persistent_app_ui": "persistentAppUi",
        "s3_monitoring_configuration": "s3MonitoringConfiguration",
    },
)
class EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfiguration:
    def __init__(
        self,
        *,
        cloud_watch_monitoring_configuration: typing.Optional[typing.Union["EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        persistent_app_ui: typing.Optional[builtins.str] = None,
        s3_monitoring_configuration: typing.Optional[typing.Union["EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_watch_monitoring_configuration: cloud_watch_monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#cloud_watch_monitoring_configuration EmrcontainersJobTemplate#cloud_watch_monitoring_configuration}
        :param persistent_app_ui: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#persistent_app_ui EmrcontainersJobTemplate#persistent_app_ui}.
        :param s3_monitoring_configuration: s3_monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#s3_monitoring_configuration EmrcontainersJobTemplate#s3_monitoring_configuration}
        '''
        if isinstance(cloud_watch_monitoring_configuration, dict):
            cloud_watch_monitoring_configuration = EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfiguration(**cloud_watch_monitoring_configuration)
        if isinstance(s3_monitoring_configuration, dict):
            s3_monitoring_configuration = EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfiguration(**s3_monitoring_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64c16d66ab328cf736d7f180536fbca3036d4d725adae47a3ff10bf7d6fa3dd8)
            check_type(argname="argument cloud_watch_monitoring_configuration", value=cloud_watch_monitoring_configuration, expected_type=type_hints["cloud_watch_monitoring_configuration"])
            check_type(argname="argument persistent_app_ui", value=persistent_app_ui, expected_type=type_hints["persistent_app_ui"])
            check_type(argname="argument s3_monitoring_configuration", value=s3_monitoring_configuration, expected_type=type_hints["s3_monitoring_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_watch_monitoring_configuration is not None:
            self._values["cloud_watch_monitoring_configuration"] = cloud_watch_monitoring_configuration
        if persistent_app_ui is not None:
            self._values["persistent_app_ui"] = persistent_app_ui
        if s3_monitoring_configuration is not None:
            self._values["s3_monitoring_configuration"] = s3_monitoring_configuration

    @builtins.property
    def cloud_watch_monitoring_configuration(
        self,
    ) -> typing.Optional["EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfiguration"]:
        '''cloud_watch_monitoring_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#cloud_watch_monitoring_configuration EmrcontainersJobTemplate#cloud_watch_monitoring_configuration}
        '''
        result = self._values.get("cloud_watch_monitoring_configuration")
        return typing.cast(typing.Optional["EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfiguration"], result)

    @builtins.property
    def persistent_app_ui(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#persistent_app_ui EmrcontainersJobTemplate#persistent_app_ui}.'''
        result = self._values.get("persistent_app_ui")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_monitoring_configuration(
        self,
    ) -> typing.Optional["EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfiguration"]:
        '''s3_monitoring_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#s3_monitoring_configuration EmrcontainersJobTemplate#s3_monitoring_configuration}
        '''
        result = self._values.get("s3_monitoring_configuration")
        return typing.cast(typing.Optional["EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "log_group_name": "logGroupName",
        "log_stream_name_prefix": "logStreamNamePrefix",
    },
)
class EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfiguration:
    def __init__(
        self,
        *,
        log_group_name: builtins.str,
        log_stream_name_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#log_group_name EmrcontainersJobTemplate#log_group_name}.
        :param log_stream_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#log_stream_name_prefix EmrcontainersJobTemplate#log_stream_name_prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__445a5cf7624cc0dc8a02515534eb4dd3c90a42bd2d4b110bb81f13dfd28599c4)
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_stream_name_prefix", value=log_stream_name_prefix, expected_type=type_hints["log_stream_name_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group_name": log_group_name,
        }
        if log_stream_name_prefix is not None:
            self._values["log_stream_name_prefix"] = log_stream_name_prefix

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#log_group_name EmrcontainersJobTemplate#log_group_name}.'''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_stream_name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#log_stream_name_prefix EmrcontainersJobTemplate#log_stream_name_prefix}.'''
        result = self._values.get("log_stream_name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee6e72a795567eb70199688dcd18ba0c125839fbc6156199e510c4a31be78471)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLogStreamNamePrefix")
    def reset_log_stream_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogStreamNamePrefix", []))

    @builtins.property
    @jsii.member(jsii_name="logGroupNameInput")
    def log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamNamePrefixInput")
    def log_stream_name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamNamePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e48abc7eba3c249da00917e3d61140d111fed8c293897fa5df6597f2e1de5c8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logStreamNamePrefix")
    def log_stream_name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamNamePrefix"))

    @log_stream_name_prefix.setter
    def log_stream_name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__108429c432b00be1363b31259c82d9635acaaa0b7a3d1919d31b5339ce9681ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamNamePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfiguration]:
        return typing.cast(typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81fab487b34b57fff1e6f4345769ed954af05cc6dbc6ca431a49c5ca43a296e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dffd1e7f245f29e033f3f3790bf4647bf2bb6b78c8c23a384e8a09489af8d70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudWatchMonitoringConfiguration")
    def put_cloud_watch_monitoring_configuration(
        self,
        *,
        log_group_name: builtins.str,
        log_stream_name_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#log_group_name EmrcontainersJobTemplate#log_group_name}.
        :param log_stream_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#log_stream_name_prefix EmrcontainersJobTemplate#log_stream_name_prefix}.
        '''
        value = EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfiguration(
            log_group_name=log_group_name,
            log_stream_name_prefix=log_stream_name_prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudWatchMonitoringConfiguration", [value]))

    @jsii.member(jsii_name="putS3MonitoringConfiguration")
    def put_s3_monitoring_configuration(self, *, log_uri: builtins.str) -> None:
        '''
        :param log_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#log_uri EmrcontainersJobTemplate#log_uri}.
        '''
        value = EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfiguration(
            log_uri=log_uri
        )

        return typing.cast(None, jsii.invoke(self, "putS3MonitoringConfiguration", [value]))

    @jsii.member(jsii_name="resetCloudWatchMonitoringConfiguration")
    def reset_cloud_watch_monitoring_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudWatchMonitoringConfiguration", []))

    @jsii.member(jsii_name="resetPersistentAppUi")
    def reset_persistent_app_ui(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPersistentAppUi", []))

    @jsii.member(jsii_name="resetS3MonitoringConfiguration")
    def reset_s3_monitoring_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3MonitoringConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchMonitoringConfiguration")
    def cloud_watch_monitoring_configuration(
        self,
    ) -> EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfigurationOutputReference:
        return typing.cast(EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfigurationOutputReference, jsii.get(self, "cloudWatchMonitoringConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="s3MonitoringConfiguration")
    def s3_monitoring_configuration(
        self,
    ) -> "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfigurationOutputReference":
        return typing.cast("EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfigurationOutputReference", jsii.get(self, "s3MonitoringConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchMonitoringConfigurationInput")
    def cloud_watch_monitoring_configuration_input(
        self,
    ) -> typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfiguration]:
        return typing.cast(typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfiguration], jsii.get(self, "cloudWatchMonitoringConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="persistentAppUiInput")
    def persistent_app_ui_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "persistentAppUiInput"))

    @builtins.property
    @jsii.member(jsii_name="s3MonitoringConfigurationInput")
    def s3_monitoring_configuration_input(
        self,
    ) -> typing.Optional["EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfiguration"]:
        return typing.cast(typing.Optional["EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfiguration"], jsii.get(self, "s3MonitoringConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="persistentAppUi")
    def persistent_app_ui(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "persistentAppUi"))

    @persistent_app_ui.setter
    def persistent_app_ui(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b1f604ac04153447138e8a284da776355278c5d389340977d140c062e7b716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "persistentAppUi", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfiguration]:
        return typing.cast(typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3588b50cb9117f478d3e6b7c866cb47e36b283d7274e70f6b8c82e11e47c9228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfiguration",
    jsii_struct_bases=[],
    name_mapping={"log_uri": "logUri"},
)
class EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfiguration:
    def __init__(self, *, log_uri: builtins.str) -> None:
        '''
        :param log_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#log_uri EmrcontainersJobTemplate#log_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1374be3345e2eccd4ab08db550392556161209c875abcb5ac1e1f1fb3eef6f2c)
            check_type(argname="argument log_uri", value=log_uri, expected_type=type_hints["log_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_uri": log_uri,
        }

    @builtins.property
    def log_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#log_uri EmrcontainersJobTemplate#log_uri}.'''
        result = self._values.get("log_uri")
        assert result is not None, "Required property 'log_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fc8ed79257a9e737b8c04a4b7296e121ad594a3d37234eddf4c24be95cf0852)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="logUriInput")
    def log_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logUriInput"))

    @builtins.property
    @jsii.member(jsii_name="logUri")
    def log_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logUri"))

    @log_uri.setter
    def log_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85ddaa8b739d73812ea1210bf6a0472e29eb00c5a2af42a6e82985f44c388d30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfiguration]:
        return typing.cast(typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8af775af5012269ad2928a63e62912d1a6053333c2f62c766260ed46cfbfd2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db161e5d9c5ff4b8b5c1b5dac0a6ccaa8ecb57660b55b92a4287b3c5f7e15f25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApplicationConfiguration")
    def put_application_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3b2f541e6e5d2b0e4a115add281008863a64023db5fc3bbe76163a3421be019)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putApplicationConfiguration", [value]))

    @jsii.member(jsii_name="putMonitoringConfiguration")
    def put_monitoring_configuration(
        self,
        *,
        cloud_watch_monitoring_configuration: typing.Optional[typing.Union[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        persistent_app_ui: typing.Optional[builtins.str] = None,
        s3_monitoring_configuration: typing.Optional[typing.Union[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_watch_monitoring_configuration: cloud_watch_monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#cloud_watch_monitoring_configuration EmrcontainersJobTemplate#cloud_watch_monitoring_configuration}
        :param persistent_app_ui: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#persistent_app_ui EmrcontainersJobTemplate#persistent_app_ui}.
        :param s3_monitoring_configuration: s3_monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#s3_monitoring_configuration EmrcontainersJobTemplate#s3_monitoring_configuration}
        '''
        value = EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfiguration(
            cloud_watch_monitoring_configuration=cloud_watch_monitoring_configuration,
            persistent_app_ui=persistent_app_ui,
            s3_monitoring_configuration=s3_monitoring_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putMonitoringConfiguration", [value]))

    @jsii.member(jsii_name="resetApplicationConfiguration")
    def reset_application_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationConfiguration", []))

    @jsii.member(jsii_name="resetMonitoringConfiguration")
    def reset_monitoring_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitoringConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="applicationConfiguration")
    def application_configuration(
        self,
    ) -> EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationList:
        return typing.cast(EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationList, jsii.get(self, "applicationConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="monitoringConfiguration")
    def monitoring_configuration(
        self,
    ) -> EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationOutputReference:
        return typing.cast(EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationOutputReference, jsii.get(self, "monitoringConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="applicationConfigurationInput")
    def application_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration]]], jsii.get(self, "applicationConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoringConfigurationInput")
    def monitoring_configuration_input(
        self,
    ) -> typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfiguration]:
        return typing.cast(typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfiguration], jsii.get(self, "monitoringConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverrides]:
        return typing.cast(typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverrides], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverrides],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__741c7045f78bc8f8245461147c3e1fdf454e0c581b126e94caa329f11dde10a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataJobDriver",
    jsii_struct_bases=[],
    name_mapping={
        "spark_sql_job_driver": "sparkSqlJobDriver",
        "spark_submit_job_driver": "sparkSubmitJobDriver",
    },
)
class EmrcontainersJobTemplateJobTemplateDataJobDriver:
    def __init__(
        self,
        *,
        spark_sql_job_driver: typing.Optional[typing.Union["EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriver", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_submit_job_driver: typing.Optional[typing.Union["EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriver", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param spark_sql_job_driver: spark_sql_job_driver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#spark_sql_job_driver EmrcontainersJobTemplate#spark_sql_job_driver}
        :param spark_submit_job_driver: spark_submit_job_driver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#spark_submit_job_driver EmrcontainersJobTemplate#spark_submit_job_driver}
        '''
        if isinstance(spark_sql_job_driver, dict):
            spark_sql_job_driver = EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriver(**spark_sql_job_driver)
        if isinstance(spark_submit_job_driver, dict):
            spark_submit_job_driver = EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriver(**spark_submit_job_driver)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec372ed12996679459a145cf7d11ab59439e81c321f3e451cccbad121ed8d628)
            check_type(argname="argument spark_sql_job_driver", value=spark_sql_job_driver, expected_type=type_hints["spark_sql_job_driver"])
            check_type(argname="argument spark_submit_job_driver", value=spark_submit_job_driver, expected_type=type_hints["spark_submit_job_driver"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if spark_sql_job_driver is not None:
            self._values["spark_sql_job_driver"] = spark_sql_job_driver
        if spark_submit_job_driver is not None:
            self._values["spark_submit_job_driver"] = spark_submit_job_driver

    @builtins.property
    def spark_sql_job_driver(
        self,
    ) -> typing.Optional["EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriver"]:
        '''spark_sql_job_driver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#spark_sql_job_driver EmrcontainersJobTemplate#spark_sql_job_driver}
        '''
        result = self._values.get("spark_sql_job_driver")
        return typing.cast(typing.Optional["EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriver"], result)

    @builtins.property
    def spark_submit_job_driver(
        self,
    ) -> typing.Optional["EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriver"]:
        '''spark_submit_job_driver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#spark_submit_job_driver EmrcontainersJobTemplate#spark_submit_job_driver}
        '''
        result = self._values.get("spark_submit_job_driver")
        return typing.cast(typing.Optional["EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriver"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrcontainersJobTemplateJobTemplateDataJobDriver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrcontainersJobTemplateJobTemplateDataJobDriverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataJobDriverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2299e84d55615ef9e066fb4a2174fd73577b855cbe596102660f6a8a7a671281)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSparkSqlJobDriver")
    def put_spark_sql_job_driver(
        self,
        *,
        entry_point: typing.Optional[builtins.str] = None,
        spark_sql_parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param entry_point: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#entry_point EmrcontainersJobTemplate#entry_point}.
        :param spark_sql_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#spark_sql_parameters EmrcontainersJobTemplate#spark_sql_parameters}.
        '''
        value = EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriver(
            entry_point=entry_point, spark_sql_parameters=spark_sql_parameters
        )

        return typing.cast(None, jsii.invoke(self, "putSparkSqlJobDriver", [value]))

    @jsii.member(jsii_name="putSparkSubmitJobDriver")
    def put_spark_submit_job_driver(
        self,
        *,
        entry_point: builtins.str,
        entry_point_arguments: typing.Optional[typing.Sequence[builtins.str]] = None,
        spark_submit_parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param entry_point: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#entry_point EmrcontainersJobTemplate#entry_point}.
        :param entry_point_arguments: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#entry_point_arguments EmrcontainersJobTemplate#entry_point_arguments}.
        :param spark_submit_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#spark_submit_parameters EmrcontainersJobTemplate#spark_submit_parameters}.
        '''
        value = EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriver(
            entry_point=entry_point,
            entry_point_arguments=entry_point_arguments,
            spark_submit_parameters=spark_submit_parameters,
        )

        return typing.cast(None, jsii.invoke(self, "putSparkSubmitJobDriver", [value]))

    @jsii.member(jsii_name="resetSparkSqlJobDriver")
    def reset_spark_sql_job_driver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkSqlJobDriver", []))

    @jsii.member(jsii_name="resetSparkSubmitJobDriver")
    def reset_spark_submit_job_driver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkSubmitJobDriver", []))

    @builtins.property
    @jsii.member(jsii_name="sparkSqlJobDriver")
    def spark_sql_job_driver(
        self,
    ) -> "EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriverOutputReference":
        return typing.cast("EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriverOutputReference", jsii.get(self, "sparkSqlJobDriver"))

    @builtins.property
    @jsii.member(jsii_name="sparkSubmitJobDriver")
    def spark_submit_job_driver(
        self,
    ) -> "EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriverOutputReference":
        return typing.cast("EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriverOutputReference", jsii.get(self, "sparkSubmitJobDriver"))

    @builtins.property
    @jsii.member(jsii_name="sparkSqlJobDriverInput")
    def spark_sql_job_driver_input(
        self,
    ) -> typing.Optional["EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriver"]:
        return typing.cast(typing.Optional["EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriver"], jsii.get(self, "sparkSqlJobDriverInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkSubmitJobDriverInput")
    def spark_submit_job_driver_input(
        self,
    ) -> typing.Optional["EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriver"]:
        return typing.cast(typing.Optional["EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriver"], jsii.get(self, "sparkSubmitJobDriverInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrcontainersJobTemplateJobTemplateDataJobDriver]:
        return typing.cast(typing.Optional[EmrcontainersJobTemplateJobTemplateDataJobDriver], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrcontainersJobTemplateJobTemplateDataJobDriver],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ad2ba936c7ec71b6c4e597c69cbd72c6aae075c34614a5c52c93829e98acf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriver",
    jsii_struct_bases=[],
    name_mapping={
        "entry_point": "entryPoint",
        "spark_sql_parameters": "sparkSqlParameters",
    },
)
class EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriver:
    def __init__(
        self,
        *,
        entry_point: typing.Optional[builtins.str] = None,
        spark_sql_parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param entry_point: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#entry_point EmrcontainersJobTemplate#entry_point}.
        :param spark_sql_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#spark_sql_parameters EmrcontainersJobTemplate#spark_sql_parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e861d5dbcbb0706f1d2d2272773f2012e2de5741258abe4003941b4c1c8ac279)
            check_type(argname="argument entry_point", value=entry_point, expected_type=type_hints["entry_point"])
            check_type(argname="argument spark_sql_parameters", value=spark_sql_parameters, expected_type=type_hints["spark_sql_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if entry_point is not None:
            self._values["entry_point"] = entry_point
        if spark_sql_parameters is not None:
            self._values["spark_sql_parameters"] = spark_sql_parameters

    @builtins.property
    def entry_point(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#entry_point EmrcontainersJobTemplate#entry_point}.'''
        result = self._values.get("entry_point")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark_sql_parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#spark_sql_parameters EmrcontainersJobTemplate#spark_sql_parameters}.'''
        result = self._values.get("spark_sql_parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0708d54a84eb6d8df666ab5690df1b71f9f9b4530e357de13f89de67ebcffa6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEntryPoint")
    def reset_entry_point(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntryPoint", []))

    @jsii.member(jsii_name="resetSparkSqlParameters")
    def reset_spark_sql_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkSqlParameters", []))

    @builtins.property
    @jsii.member(jsii_name="entryPointInput")
    def entry_point_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entryPointInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkSqlParametersInput")
    def spark_sql_parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sparkSqlParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="entryPoint")
    def entry_point(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entryPoint"))

    @entry_point.setter
    def entry_point(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10f8de10be6e2164f01fd09294a81dafc89db99e4c8f2d03f8e932b37074e508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entryPoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sparkSqlParameters")
    def spark_sql_parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sparkSqlParameters"))

    @spark_sql_parameters.setter
    def spark_sql_parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a29f7630b3fe26fba09afc47db9c4727e3ce9e6dce76504530faa61154d0ba53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparkSqlParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriver]:
        return typing.cast(typing.Optional[EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriver], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriver],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519ed74a8d74423e94155682f08b92f89a0b909d45dd31ea2f1c40c9fbc2e298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriver",
    jsii_struct_bases=[],
    name_mapping={
        "entry_point": "entryPoint",
        "entry_point_arguments": "entryPointArguments",
        "spark_submit_parameters": "sparkSubmitParameters",
    },
)
class EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriver:
    def __init__(
        self,
        *,
        entry_point: builtins.str,
        entry_point_arguments: typing.Optional[typing.Sequence[builtins.str]] = None,
        spark_submit_parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param entry_point: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#entry_point EmrcontainersJobTemplate#entry_point}.
        :param entry_point_arguments: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#entry_point_arguments EmrcontainersJobTemplate#entry_point_arguments}.
        :param spark_submit_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#spark_submit_parameters EmrcontainersJobTemplate#spark_submit_parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a3d619de584abbcc5f50f753dd93f3beb985117220e88b2e6864c68f4fc06f3)
            check_type(argname="argument entry_point", value=entry_point, expected_type=type_hints["entry_point"])
            check_type(argname="argument entry_point_arguments", value=entry_point_arguments, expected_type=type_hints["entry_point_arguments"])
            check_type(argname="argument spark_submit_parameters", value=spark_submit_parameters, expected_type=type_hints["spark_submit_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entry_point": entry_point,
        }
        if entry_point_arguments is not None:
            self._values["entry_point_arguments"] = entry_point_arguments
        if spark_submit_parameters is not None:
            self._values["spark_submit_parameters"] = spark_submit_parameters

    @builtins.property
    def entry_point(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#entry_point EmrcontainersJobTemplate#entry_point}.'''
        result = self._values.get("entry_point")
        assert result is not None, "Required property 'entry_point' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def entry_point_arguments(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#entry_point_arguments EmrcontainersJobTemplate#entry_point_arguments}.'''
        result = self._values.get("entry_point_arguments")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def spark_submit_parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#spark_submit_parameters EmrcontainersJobTemplate#spark_submit_parameters}.'''
        result = self._values.get("spark_submit_parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cddff962a8b45e53e84cbd989c6f751d66afa80db3efc9ed481ec59892d611a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEntryPointArguments")
    def reset_entry_point_arguments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntryPointArguments", []))

    @jsii.member(jsii_name="resetSparkSubmitParameters")
    def reset_spark_submit_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkSubmitParameters", []))

    @builtins.property
    @jsii.member(jsii_name="entryPointArgumentsInput")
    def entry_point_arguments_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "entryPointArgumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="entryPointInput")
    def entry_point_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entryPointInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkSubmitParametersInput")
    def spark_submit_parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sparkSubmitParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="entryPoint")
    def entry_point(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entryPoint"))

    @entry_point.setter
    def entry_point(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f9120eea890823cc1002094ec5562d1f3101206a458efb63c25391a0993422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entryPoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entryPointArguments")
    def entry_point_arguments(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "entryPointArguments"))

    @entry_point_arguments.setter
    def entry_point_arguments(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be3eea9eab7f6e9a002d572d1b4ec6553f563c701aa24ab5f82e308b0847637)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entryPointArguments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sparkSubmitParameters")
    def spark_submit_parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sparkSubmitParameters"))

    @spark_submit_parameters.setter
    def spark_submit_parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd7e387bd6b1f8bdaef19bc0427d23cecce939c5755b755e13b0e2aad9e07a28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparkSubmitParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriver]:
        return typing.cast(typing.Optional[EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriver], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriver],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cfc6fc56f479c2224017c8e39b1492197d876955c51950480e635a6d85ae4b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EmrcontainersJobTemplateJobTemplateDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateJobTemplateDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8060cef5b4851f88702903f17d361b8e85f8ea4a557cbf7c53294aee61b9e32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfigurationOverrides")
    def put_configuration_overrides(
        self,
        *,
        application_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
        monitoring_configuration: typing.Optional[typing.Union[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param application_configuration: application_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#application_configuration EmrcontainersJobTemplate#application_configuration}
        :param monitoring_configuration: monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#monitoring_configuration EmrcontainersJobTemplate#monitoring_configuration}
        '''
        value = EmrcontainersJobTemplateJobTemplateDataConfigurationOverrides(
            application_configuration=application_configuration,
            monitoring_configuration=monitoring_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putConfigurationOverrides", [value]))

    @jsii.member(jsii_name="putJobDriver")
    def put_job_driver(
        self,
        *,
        spark_sql_job_driver: typing.Optional[typing.Union[EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriver, typing.Dict[builtins.str, typing.Any]]] = None,
        spark_submit_job_driver: typing.Optional[typing.Union[EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriver, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param spark_sql_job_driver: spark_sql_job_driver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#spark_sql_job_driver EmrcontainersJobTemplate#spark_sql_job_driver}
        :param spark_submit_job_driver: spark_submit_job_driver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#spark_submit_job_driver EmrcontainersJobTemplate#spark_submit_job_driver}
        '''
        value = EmrcontainersJobTemplateJobTemplateDataJobDriver(
            spark_sql_job_driver=spark_sql_job_driver,
            spark_submit_job_driver=spark_submit_job_driver,
        )

        return typing.cast(None, jsii.invoke(self, "putJobDriver", [value]))

    @jsii.member(jsii_name="resetConfigurationOverrides")
    def reset_configuration_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigurationOverrides", []))

    @jsii.member(jsii_name="resetJobTags")
    def reset_job_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJobTags", []))

    @builtins.property
    @jsii.member(jsii_name="configurationOverrides")
    def configuration_overrides(
        self,
    ) -> EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesOutputReference:
        return typing.cast(EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesOutputReference, jsii.get(self, "configurationOverrides"))

    @builtins.property
    @jsii.member(jsii_name="jobDriver")
    def job_driver(
        self,
    ) -> EmrcontainersJobTemplateJobTemplateDataJobDriverOutputReference:
        return typing.cast(EmrcontainersJobTemplateJobTemplateDataJobDriverOutputReference, jsii.get(self, "jobDriver"))

    @builtins.property
    @jsii.member(jsii_name="configurationOverridesInput")
    def configuration_overrides_input(
        self,
    ) -> typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverrides]:
        return typing.cast(typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverrides], jsii.get(self, "configurationOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleArnInput")
    def execution_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="jobDriverInput")
    def job_driver_input(
        self,
    ) -> typing.Optional[EmrcontainersJobTemplateJobTemplateDataJobDriver]:
        return typing.cast(typing.Optional[EmrcontainersJobTemplateJobTemplateDataJobDriver], jsii.get(self, "jobDriverInput"))

    @builtins.property
    @jsii.member(jsii_name="jobTagsInput")
    def job_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "jobTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="releaseLabelInput")
    def release_label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "releaseLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRoleArn"))

    @execution_role_arn.setter
    def execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc76cdfda49f2df968f71b58cda47124a2a8a15937f9dd5570725186d6a8c19e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobTags")
    def job_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "jobTags"))

    @job_tags.setter
    def job_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bab11388f984ea1304615838cf3f944f45cd3f976c04935fb3564f4cf0aa3f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="releaseLabel")
    def release_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "releaseLabel"))

    @release_label.setter
    def release_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c520c5a5cf402aedd7c8f4ca77a431a62c8d89d9990dcbe9578a598c7209120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "releaseLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrcontainersJobTemplateJobTemplateData]:
        return typing.cast(typing.Optional[EmrcontainersJobTemplateJobTemplateData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrcontainersJobTemplateJobTemplateData],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3297529bbaa86761b1b932cba3ab37d8f6808353578efde1d191ab8264012001)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"delete": "delete"},
)
class EmrcontainersJobTemplateTimeouts:
    def __init__(self, *, delete: typing.Optional[builtins.str] = None) -> None:
        '''
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#delete EmrcontainersJobTemplate#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a41d252f338c791be84d170fd7470ef6a27f8b1766623fb7d955652262725a)
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/emrcontainers_job_template#delete EmrcontainersJobTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrcontainersJobTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrcontainersJobTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.emrcontainersJobTemplate.EmrcontainersJobTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__491ab0c2867a914e976bfc8266db39bd50866b84bbbcd309ca6f947747634518)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba69186155dc7094cff437c35f9b755e0b99a8c5b2356ee25f8c55c456fc313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrcontainersJobTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrcontainersJobTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrcontainersJobTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f828ee3afd1b545b34b873d9c6632d78dfc2f55bb6472adb080b92e48ca7a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EmrcontainersJobTemplate",
    "EmrcontainersJobTemplateConfig",
    "EmrcontainersJobTemplateJobTemplateData",
    "EmrcontainersJobTemplateJobTemplateDataConfigurationOverrides",
    "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration",
    "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations",
    "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurationsList",
    "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurationsOutputReference",
    "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationList",
    "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationOutputReference",
    "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfiguration",
    "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfiguration",
    "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfigurationOutputReference",
    "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationOutputReference",
    "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfiguration",
    "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfigurationOutputReference",
    "EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesOutputReference",
    "EmrcontainersJobTemplateJobTemplateDataJobDriver",
    "EmrcontainersJobTemplateJobTemplateDataJobDriverOutputReference",
    "EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriver",
    "EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriverOutputReference",
    "EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriver",
    "EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriverOutputReference",
    "EmrcontainersJobTemplateJobTemplateDataOutputReference",
    "EmrcontainersJobTemplateTimeouts",
    "EmrcontainersJobTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0ce5170f32e1b9e5c6f4f5ddfc53e0cb1661fb1dcbb3c9ce387297901ea1920f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    job_template_data: typing.Union[EmrcontainersJobTemplateJobTemplateData, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[EmrcontainersJobTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__edfeb6aa6a2a9269602becb9d2bc4e98aecdbdcd3254f5b64d9e4bc8fc349c13(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd2addf4fe22cdaf16e446eeb695eb3bb662b87409a8179f1dd6b134a988133(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a8ec6fbdcf71eca9026935abe6e26b593cb766ede98702aac8ccceecf714d70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feadbc5ce32c3eba8eab78e06d3cd28ff17c12bdd7a9ff464f9492bd41d6f3ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df89225536834d816df913e5e7cf67f293472cc28eeee99ad6bc80d7702ce412(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0326106aea9705448caf48e6297f6165fdec7e1161bad394c18ed533a9896a53(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86113161ae54d52d671dca944162f967b396484063ceb5ac1795c565e938c0bd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__930c45fc2da31a0f824920baed5ece327eef4f03b8f8affecffa3bd2a485a192(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    job_template_data: typing.Union[EmrcontainersJobTemplateJobTemplateData, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[EmrcontainersJobTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a346369556b1c401a5587ab12af4ef743b18627db53ebeb85906753e1f3415(
    *,
    execution_role_arn: builtins.str,
    job_driver: typing.Union[EmrcontainersJobTemplateJobTemplateDataJobDriver, typing.Dict[builtins.str, typing.Any]],
    release_label: builtins.str,
    configuration_overrides: typing.Optional[typing.Union[EmrcontainersJobTemplateJobTemplateDataConfigurationOverrides, typing.Dict[builtins.str, typing.Any]]] = None,
    job_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd41c89e82e041309825231e353d28d75eea5201aca34b311cb12d77adbd2ac(
    *,
    application_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    monitoring_configuration: typing.Optional[typing.Union[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c59a080635dbf8d7ba787da5e701052268f38b9cdce76a79e949057e2a6f3f87(
    *,
    classification: builtins.str,
    configurations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8924b0f385b7670a2a70556b27f9e4b80575842eb3f21b326934c14c0d4dbe8d(
    *,
    classification: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c2caa72563f88addb5184732375845db707e5ef89e07876264e2769c24dd62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87bbec6a0a571cdb6abfdf4a6843b486437f251eaae4164eac224e481b447a0b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af39cd85cf8b3952821450bae0f739a8f6a5eef6a6ede57e83b186f69eaa681(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b76c04ba29406db9e9531b385a7fd5ad7c4d143329813a4ce4e89b6e1c56912a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3afe3282ae52f30661e244f6a6b201bf54bdb7da8c099eb9b6a1189410c480b3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12dc29a1adf419f645f8c1b74f75a3e1d144a37d73fd6f781c2245efac49db48(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d5d7dc4f2d0b734ea2fac1854f73dc15490e72905484258e5be5f0a68bb94c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ff4ce76d39d12111ce84918d35407507f2ea480935b64e14aef94f49bce8c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f45170410aed80435c4f86cc6dbcc53ba1cf242ae7c1d087da294c5b2930f5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c5e4eb36de4a91af3c03ff75aa4b6995842e3cf35dca6c1a7ea65a53d4c0845(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c74776c0c9edc319ed294ce9eccc064b7633c68a752b1e74bef955f99bff9f8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4853ca784243921f867687378cd5e3f46f9d86c6e8539d204e71be60da968c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96421a04120618455d737263ed7f58d12273d5539c89b4890a4e2b2e97960b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b08588a511d3e98f1814f2b9b0fd4602b1407e3065f4c78c0fb6822ef8e9cf19(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4df418596ea8cf5d88c6741fbed1334122d53a3a326725be6d16346058a5717(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1acaf773064d25c0cba2b8fdf31832a8d23a879e99953f8056b67be05e6494(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33c65d6568f1c953f8e91d00eb2fc0a3420318244a15103bd6805de9e5d6981(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631435b4eb75df9dbbca4cdb11f8752aafeac1d10cf53f2cf6367d75297dcd30(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfigurationConfigurations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e849f897301406b7048f2bc6dea23a9fc5a707b436cbd4ce57277c463171b997(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab20ba878eb4d36b70f5cc49b7228c44d7894114e835f4c1b07c126c7c42d37(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f68331c1efc7be2c3673021b3bedc490da5b34785759a1b7c79c85c01563f70(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c16d66ab328cf736d7f180536fbca3036d4d725adae47a3ff10bf7d6fa3dd8(
    *,
    cloud_watch_monitoring_configuration: typing.Optional[typing.Union[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    persistent_app_ui: typing.Optional[builtins.str] = None,
    s3_monitoring_configuration: typing.Optional[typing.Union[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__445a5cf7624cc0dc8a02515534eb4dd3c90a42bd2d4b110bb81f13dfd28599c4(
    *,
    log_group_name: builtins.str,
    log_stream_name_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee6e72a795567eb70199688dcd18ba0c125839fbc6156199e510c4a31be78471(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48abc7eba3c249da00917e3d61140d111fed8c293897fa5df6597f2e1de5c8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108429c432b00be1363b31259c82d9635acaaa0b7a3d1919d31b5339ce9681ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81fab487b34b57fff1e6f4345769ed954af05cc6dbc6ca431a49c5ca43a296e2(
    value: typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationCloudWatchMonitoringConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dffd1e7f245f29e033f3f3790bf4647bf2bb6b78c8c23a384e8a09489af8d70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b1f604ac04153447138e8a284da776355278c5d389340977d140c062e7b716(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3588b50cb9117f478d3e6b7c866cb47e36b283d7274e70f6b8c82e11e47c9228(
    value: typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1374be3345e2eccd4ab08db550392556161209c875abcb5ac1e1f1fb3eef6f2c(
    *,
    log_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc8ed79257a9e737b8c04a4b7296e121ad594a3d37234eddf4c24be95cf0852(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ddaa8b739d73812ea1210bf6a0472e29eb00c5a2af42a6e82985f44c388d30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8af775af5012269ad2928a63e62912d1a6053333c2f62c766260ed46cfbfd2f(
    value: typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesMonitoringConfigurationS3MonitoringConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db161e5d9c5ff4b8b5c1b5dac0a6ccaa8ecb57660b55b92a4287b3c5f7e15f25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b2f541e6e5d2b0e4a115add281008863a64023db5fc3bbe76163a3421be019(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrcontainersJobTemplateJobTemplateDataConfigurationOverridesApplicationConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__741c7045f78bc8f8245461147c3e1fdf454e0c581b126e94caa329f11dde10a7(
    value: typing.Optional[EmrcontainersJobTemplateJobTemplateDataConfigurationOverrides],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec372ed12996679459a145cf7d11ab59439e81c321f3e451cccbad121ed8d628(
    *,
    spark_sql_job_driver: typing.Optional[typing.Union[EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriver, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_submit_job_driver: typing.Optional[typing.Union[EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriver, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2299e84d55615ef9e066fb4a2174fd73577b855cbe596102660f6a8a7a671281(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ad2ba936c7ec71b6c4e597c69cbd72c6aae075c34614a5c52c93829e98acf3(
    value: typing.Optional[EmrcontainersJobTemplateJobTemplateDataJobDriver],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e861d5dbcbb0706f1d2d2272773f2012e2de5741258abe4003941b4c1c8ac279(
    *,
    entry_point: typing.Optional[builtins.str] = None,
    spark_sql_parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0708d54a84eb6d8df666ab5690df1b71f9f9b4530e357de13f89de67ebcffa6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f8de10be6e2164f01fd09294a81dafc89db99e4c8f2d03f8e932b37074e508(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a29f7630b3fe26fba09afc47db9c4727e3ce9e6dce76504530faa61154d0ba53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519ed74a8d74423e94155682f08b92f89a0b909d45dd31ea2f1c40c9fbc2e298(
    value: typing.Optional[EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSqlJobDriver],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a3d619de584abbcc5f50f753dd93f3beb985117220e88b2e6864c68f4fc06f3(
    *,
    entry_point: builtins.str,
    entry_point_arguments: typing.Optional[typing.Sequence[builtins.str]] = None,
    spark_submit_parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cddff962a8b45e53e84cbd989c6f751d66afa80db3efc9ed481ec59892d611a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f9120eea890823cc1002094ec5562d1f3101206a458efb63c25391a0993422(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be3eea9eab7f6e9a002d572d1b4ec6553f563c701aa24ab5f82e308b0847637(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7e387bd6b1f8bdaef19bc0427d23cecce939c5755b755e13b0e2aad9e07a28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cfc6fc56f479c2224017c8e39b1492197d876955c51950480e635a6d85ae4b1(
    value: typing.Optional[EmrcontainersJobTemplateJobTemplateDataJobDriverSparkSubmitJobDriver],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8060cef5b4851f88702903f17d361b8e85f8ea4a557cbf7c53294aee61b9e32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc76cdfda49f2df968f71b58cda47124a2a8a15937f9dd5570725186d6a8c19e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bab11388f984ea1304615838cf3f944f45cd3f976c04935fb3564f4cf0aa3f8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c520c5a5cf402aedd7c8f4ca77a431a62c8d89d9990dcbe9578a598c7209120(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3297529bbaa86761b1b932cba3ab37d8f6808353578efde1d191ab8264012001(
    value: typing.Optional[EmrcontainersJobTemplateJobTemplateData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a41d252f338c791be84d170fd7470ef6a27f8b1766623fb7d955652262725a(
    *,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__491ab0c2867a914e976bfc8266db39bd50866b84bbbcd309ca6f947747634518(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba69186155dc7094cff437c35f9b755e0b99a8c5b2356ee25f8c55c456fc313(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f828ee3afd1b545b34b873d9c6632d78dfc2f55bb6472adb080b92e48ca7a3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrcontainersJobTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
