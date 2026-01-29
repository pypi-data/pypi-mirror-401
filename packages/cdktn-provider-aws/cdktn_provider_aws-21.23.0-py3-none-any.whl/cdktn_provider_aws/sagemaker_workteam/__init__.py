r'''
# `aws_sagemaker_workteam`

Refer to the Terraform Registry for docs: [`aws_sagemaker_workteam`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam).
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


class SagemakerWorkteam(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerWorkteam.SagemakerWorkteam",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam aws_sagemaker_workteam}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        description: builtins.str,
        member_definition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerWorkteamMemberDefinition", typing.Dict[builtins.str, typing.Any]]]],
        workteam_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        notification_configuration: typing.Optional[typing.Union["SagemakerWorkteamNotificationConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        worker_access_configuration: typing.Optional[typing.Union["SagemakerWorkteamWorkerAccessConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        workforce_name: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam aws_sagemaker_workteam} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#description SagemakerWorkteam#description}.
        :param member_definition: member_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#member_definition SagemakerWorkteam#member_definition}
        :param workteam_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#workteam_name SagemakerWorkteam#workteam_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#id SagemakerWorkteam#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notification_configuration: notification_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#notification_configuration SagemakerWorkteam#notification_configuration}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#region SagemakerWorkteam#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#tags SagemakerWorkteam#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#tags_all SagemakerWorkteam#tags_all}.
        :param worker_access_configuration: worker_access_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#worker_access_configuration SagemakerWorkteam#worker_access_configuration}
        :param workforce_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#workforce_name SagemakerWorkteam#workforce_name}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61182a7f7a8c9b80e8fc65f15d2ebe44a7fdfd9e422e92478001ec9212c954c8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SagemakerWorkteamConfig(
            description=description,
            member_definition=member_definition,
            workteam_name=workteam_name,
            id=id,
            notification_configuration=notification_configuration,
            region=region,
            tags=tags,
            tags_all=tags_all,
            worker_access_configuration=worker_access_configuration,
            workforce_name=workforce_name,
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
        '''Generates CDKTF code for importing a SagemakerWorkteam resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SagemakerWorkteam to import.
        :param import_from_id: The id of the existing SagemakerWorkteam that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SagemakerWorkteam to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ca4261e3280eccc6a2d60b532c297870eb3add0694fbc6d2946ddaf2266d502)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMemberDefinition")
    def put_member_definition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerWorkteamMemberDefinition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__399477def7d0cd56e9a8af3307b32471949f81d10a9cb4c4f290b07e1fba188f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMemberDefinition", [value]))

    @jsii.member(jsii_name="putNotificationConfiguration")
    def put_notification_configuration(
        self,
        *,
        notification_topic_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param notification_topic_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#notification_topic_arn SagemakerWorkteam#notification_topic_arn}.
        '''
        value = SagemakerWorkteamNotificationConfiguration(
            notification_topic_arn=notification_topic_arn
        )

        return typing.cast(None, jsii.invoke(self, "putNotificationConfiguration", [value]))

    @jsii.member(jsii_name="putWorkerAccessConfiguration")
    def put_worker_access_configuration(
        self,
        *,
        s3_presign: typing.Optional[typing.Union["SagemakerWorkteamWorkerAccessConfigurationS3Presign", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param s3_presign: s3_presign block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#s3_presign SagemakerWorkteam#s3_presign}
        '''
        value = SagemakerWorkteamWorkerAccessConfiguration(s3_presign=s3_presign)

        return typing.cast(None, jsii.invoke(self, "putWorkerAccessConfiguration", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNotificationConfiguration")
    def reset_notification_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationConfiguration", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetWorkerAccessConfiguration")
    def reset_worker_access_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerAccessConfiguration", []))

    @jsii.member(jsii_name="resetWorkforceName")
    def reset_workforce_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkforceName", []))

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
    @jsii.member(jsii_name="memberDefinition")
    def member_definition(self) -> "SagemakerWorkteamMemberDefinitionList":
        return typing.cast("SagemakerWorkteamMemberDefinitionList", jsii.get(self, "memberDefinition"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfiguration")
    def notification_configuration(
        self,
    ) -> "SagemakerWorkteamNotificationConfigurationOutputReference":
        return typing.cast("SagemakerWorkteamNotificationConfigurationOutputReference", jsii.get(self, "notificationConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="subdomain")
    def subdomain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subdomain"))

    @builtins.property
    @jsii.member(jsii_name="workerAccessConfiguration")
    def worker_access_configuration(
        self,
    ) -> "SagemakerWorkteamWorkerAccessConfigurationOutputReference":
        return typing.cast("SagemakerWorkteamWorkerAccessConfigurationOutputReference", jsii.get(self, "workerAccessConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="memberDefinitionInput")
    def member_definition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerWorkteamMemberDefinition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerWorkteamMemberDefinition"]]], jsii.get(self, "memberDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfigurationInput")
    def notification_configuration_input(
        self,
    ) -> typing.Optional["SagemakerWorkteamNotificationConfiguration"]:
        return typing.cast(typing.Optional["SagemakerWorkteamNotificationConfiguration"], jsii.get(self, "notificationConfigurationInput"))

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
    @jsii.member(jsii_name="workerAccessConfigurationInput")
    def worker_access_configuration_input(
        self,
    ) -> typing.Optional["SagemakerWorkteamWorkerAccessConfiguration"]:
        return typing.cast(typing.Optional["SagemakerWorkteamWorkerAccessConfiguration"], jsii.get(self, "workerAccessConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="workforceNameInput")
    def workforce_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workforceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="workteamNameInput")
    def workteam_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workteamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2902d8aa9c03c3b31424678deccde9b4de5848a04be276db07d9034ffd2cbb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17c581cd990eef46f9483226a7f3761c0e24563ad6792bdb12cd1d95f54f15af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9df337d0b7cfe8d81593354b6647f45ac506201cf147c3d4b5b16088e06fd0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a1f0ba0fd7d8b8c892a4da468ba5cae517487c1756ac0997757bfa9798323c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b34429ce15bbc06ca6adbe9f349ae45c3eefc9996a85947db2d72b7f63fb95e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workforceName")
    def workforce_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workforceName"))

    @workforce_name.setter
    def workforce_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9ff16d87e0d45fe09ba0b8b4accb062ede88b872434aa61c252098b58583fd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workforceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workteamName")
    def workteam_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workteamName"))

    @workteam_name.setter
    def workteam_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12f80b9924b811aeba7014bc8972a1acd4d99297f423b032bc96ff3a175c64d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workteamName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerWorkteam.SagemakerWorkteamConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "description": "description",
        "member_definition": "memberDefinition",
        "workteam_name": "workteamName",
        "id": "id",
        "notification_configuration": "notificationConfiguration",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
        "worker_access_configuration": "workerAccessConfiguration",
        "workforce_name": "workforceName",
    },
)
class SagemakerWorkteamConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        description: builtins.str,
        member_definition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerWorkteamMemberDefinition", typing.Dict[builtins.str, typing.Any]]]],
        workteam_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        notification_configuration: typing.Optional[typing.Union["SagemakerWorkteamNotificationConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        worker_access_configuration: typing.Optional[typing.Union["SagemakerWorkteamWorkerAccessConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        workforce_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#description SagemakerWorkteam#description}.
        :param member_definition: member_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#member_definition SagemakerWorkteam#member_definition}
        :param workteam_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#workteam_name SagemakerWorkteam#workteam_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#id SagemakerWorkteam#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notification_configuration: notification_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#notification_configuration SagemakerWorkteam#notification_configuration}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#region SagemakerWorkteam#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#tags SagemakerWorkteam#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#tags_all SagemakerWorkteam#tags_all}.
        :param worker_access_configuration: worker_access_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#worker_access_configuration SagemakerWorkteam#worker_access_configuration}
        :param workforce_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#workforce_name SagemakerWorkteam#workforce_name}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(notification_configuration, dict):
            notification_configuration = SagemakerWorkteamNotificationConfiguration(**notification_configuration)
        if isinstance(worker_access_configuration, dict):
            worker_access_configuration = SagemakerWorkteamWorkerAccessConfiguration(**worker_access_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c910d7d3230cf7e74716e8921164dfadcea8e81be0222dd6b3cd806c4e6cf884)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument member_definition", value=member_definition, expected_type=type_hints["member_definition"])
            check_type(argname="argument workteam_name", value=workteam_name, expected_type=type_hints["workteam_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notification_configuration", value=notification_configuration, expected_type=type_hints["notification_configuration"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument worker_access_configuration", value=worker_access_configuration, expected_type=type_hints["worker_access_configuration"])
            check_type(argname="argument workforce_name", value=workforce_name, expected_type=type_hints["workforce_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "member_definition": member_definition,
            "workteam_name": workteam_name,
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
        if notification_configuration is not None:
            self._values["notification_configuration"] = notification_configuration
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if worker_access_configuration is not None:
            self._values["worker_access_configuration"] = worker_access_configuration
        if workforce_name is not None:
            self._values["workforce_name"] = workforce_name

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
    def description(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#description SagemakerWorkteam#description}.'''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def member_definition(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerWorkteamMemberDefinition"]]:
        '''member_definition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#member_definition SagemakerWorkteam#member_definition}
        '''
        result = self._values.get("member_definition")
        assert result is not None, "Required property 'member_definition' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerWorkteamMemberDefinition"]], result)

    @builtins.property
    def workteam_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#workteam_name SagemakerWorkteam#workteam_name}.'''
        result = self._values.get("workteam_name")
        assert result is not None, "Required property 'workteam_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#id SagemakerWorkteam#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_configuration(
        self,
    ) -> typing.Optional["SagemakerWorkteamNotificationConfiguration"]:
        '''notification_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#notification_configuration SagemakerWorkteam#notification_configuration}
        '''
        result = self._values.get("notification_configuration")
        return typing.cast(typing.Optional["SagemakerWorkteamNotificationConfiguration"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#region SagemakerWorkteam#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#tags SagemakerWorkteam#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#tags_all SagemakerWorkteam#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def worker_access_configuration(
        self,
    ) -> typing.Optional["SagemakerWorkteamWorkerAccessConfiguration"]:
        '''worker_access_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#worker_access_configuration SagemakerWorkteam#worker_access_configuration}
        '''
        result = self._values.get("worker_access_configuration")
        return typing.cast(typing.Optional["SagemakerWorkteamWorkerAccessConfiguration"], result)

    @builtins.property
    def workforce_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#workforce_name SagemakerWorkteam#workforce_name}.'''
        result = self._values.get("workforce_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerWorkteamConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerWorkteam.SagemakerWorkteamMemberDefinition",
    jsii_struct_bases=[],
    name_mapping={
        "cognito_member_definition": "cognitoMemberDefinition",
        "oidc_member_definition": "oidcMemberDefinition",
    },
)
class SagemakerWorkteamMemberDefinition:
    def __init__(
        self,
        *,
        cognito_member_definition: typing.Optional[typing.Union["SagemakerWorkteamMemberDefinitionCognitoMemberDefinition", typing.Dict[builtins.str, typing.Any]]] = None,
        oidc_member_definition: typing.Optional[typing.Union["SagemakerWorkteamMemberDefinitionOidcMemberDefinition", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cognito_member_definition: cognito_member_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#cognito_member_definition SagemakerWorkteam#cognito_member_definition}
        :param oidc_member_definition: oidc_member_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#oidc_member_definition SagemakerWorkteam#oidc_member_definition}
        '''
        if isinstance(cognito_member_definition, dict):
            cognito_member_definition = SagemakerWorkteamMemberDefinitionCognitoMemberDefinition(**cognito_member_definition)
        if isinstance(oidc_member_definition, dict):
            oidc_member_definition = SagemakerWorkteamMemberDefinitionOidcMemberDefinition(**oidc_member_definition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ec1f46097cd8e139b9f276e90e90ba35360426877ec444c0aee7e854557dc0c)
            check_type(argname="argument cognito_member_definition", value=cognito_member_definition, expected_type=type_hints["cognito_member_definition"])
            check_type(argname="argument oidc_member_definition", value=oidc_member_definition, expected_type=type_hints["oidc_member_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cognito_member_definition is not None:
            self._values["cognito_member_definition"] = cognito_member_definition
        if oidc_member_definition is not None:
            self._values["oidc_member_definition"] = oidc_member_definition

    @builtins.property
    def cognito_member_definition(
        self,
    ) -> typing.Optional["SagemakerWorkteamMemberDefinitionCognitoMemberDefinition"]:
        '''cognito_member_definition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#cognito_member_definition SagemakerWorkteam#cognito_member_definition}
        '''
        result = self._values.get("cognito_member_definition")
        return typing.cast(typing.Optional["SagemakerWorkteamMemberDefinitionCognitoMemberDefinition"], result)

    @builtins.property
    def oidc_member_definition(
        self,
    ) -> typing.Optional["SagemakerWorkteamMemberDefinitionOidcMemberDefinition"]:
        '''oidc_member_definition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#oidc_member_definition SagemakerWorkteam#oidc_member_definition}
        '''
        result = self._values.get("oidc_member_definition")
        return typing.cast(typing.Optional["SagemakerWorkteamMemberDefinitionOidcMemberDefinition"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerWorkteamMemberDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerWorkteam.SagemakerWorkteamMemberDefinitionCognitoMemberDefinition",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "user_group": "userGroup",
        "user_pool": "userPool",
    },
)
class SagemakerWorkteamMemberDefinitionCognitoMemberDefinition:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        user_group: builtins.str,
        user_pool: builtins.str,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#client_id SagemakerWorkteam#client_id}.
        :param user_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#user_group SagemakerWorkteam#user_group}.
        :param user_pool: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#user_pool SagemakerWorkteam#user_pool}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4259d08b00e73e9a08d481689225f083a849accabcc3cbcffce7ccdd874f6d90)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument user_group", value=user_group, expected_type=type_hints["user_group"])
            check_type(argname="argument user_pool", value=user_pool, expected_type=type_hints["user_pool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "user_group": user_group,
            "user_pool": user_pool,
        }

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#client_id SagemakerWorkteam#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_group(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#user_group SagemakerWorkteam#user_group}.'''
        result = self._values.get("user_group")
        assert result is not None, "Required property 'user_group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_pool(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#user_pool SagemakerWorkteam#user_pool}.'''
        result = self._values.get("user_pool")
        assert result is not None, "Required property 'user_pool' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerWorkteamMemberDefinitionCognitoMemberDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerWorkteamMemberDefinitionCognitoMemberDefinitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerWorkteam.SagemakerWorkteamMemberDefinitionCognitoMemberDefinitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8faba07020798b8733a47562f3905cb437242cd2478c08876230f6d0e27feef4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userGroupInput")
    def user_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="userPoolInput")
    def user_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb9abc9a4b5902148cb4b2dd1b5be77da8caa9ef8f8e1dc9bb0ccd906fbd7b2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userGroup")
    def user_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userGroup"))

    @user_group.setter
    def user_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fdfa3d905f5938a797779ecd19dda8a3b9c69f3d775edf5bf6af46bdd975caa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPool")
    def user_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPool"))

    @user_pool.setter
    def user_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64fb07ec4190fb86008f7ff0a7b681015878c237bcbe9a6049be176153583857)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerWorkteamMemberDefinitionCognitoMemberDefinition]:
        return typing.cast(typing.Optional[SagemakerWorkteamMemberDefinitionCognitoMemberDefinition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerWorkteamMemberDefinitionCognitoMemberDefinition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__122cf41577872df8c64efa43059019c9080ea0c518e1e2f2beb05b357dd87750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerWorkteamMemberDefinitionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerWorkteam.SagemakerWorkteamMemberDefinitionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e14c3816c0212519e8bf1533f6f88219c15fa29d3e1dcb60de417592bfd1f72c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerWorkteamMemberDefinitionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b247c76f2cd39e3aba315dc2a8a2bc80fd8441a9c533a440fe5599dfb26e8b8c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerWorkteamMemberDefinitionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea7a42239181987c78c909e36777a8c1e5758940730345b28890dc86d6c2d008)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ece7957b87483c35103e003f9308f002ad668c92f5077d71d63468b5c817700)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2e69095cf81591c072a441d179ea79d47aea4429f5d57355610cf40b10b1263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerWorkteamMemberDefinition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerWorkteamMemberDefinition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerWorkteamMemberDefinition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce3b84479409b9cdaa9777f2bfb222fc4cae30f54e559bf712d6cd24fbf3a046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerWorkteam.SagemakerWorkteamMemberDefinitionOidcMemberDefinition",
    jsii_struct_bases=[],
    name_mapping={"groups": "groups"},
)
class SagemakerWorkteamMemberDefinitionOidcMemberDefinition:
    def __init__(self, *, groups: typing.Sequence[builtins.str]) -> None:
        '''
        :param groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#groups SagemakerWorkteam#groups}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a3f10b47933d93d68c5933dd3c7daad6d3496352a45ab1d842db09e698b084)
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "groups": groups,
        }

    @builtins.property
    def groups(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#groups SagemakerWorkteam#groups}.'''
        result = self._values.get("groups")
        assert result is not None, "Required property 'groups' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerWorkteamMemberDefinitionOidcMemberDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerWorkteamMemberDefinitionOidcMemberDefinitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerWorkteam.SagemakerWorkteamMemberDefinitionOidcMemberDefinitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf41e2aa12965e76bb57a942fa7e2a1f650192df0fa25648056dc48bd2497fde)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="groupsInput")
    def groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupsInput"))

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7c7e26ab9941476e6a763965c4d940cdbec9abaff3aa3bf1c51f95777ad6237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerWorkteamMemberDefinitionOidcMemberDefinition]:
        return typing.cast(typing.Optional[SagemakerWorkteamMemberDefinitionOidcMemberDefinition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerWorkteamMemberDefinitionOidcMemberDefinition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dfac0beba56fb8943d55a3a0a608a802e4e46e3966ea4f9a092a6123cbf1118)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerWorkteamMemberDefinitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerWorkteam.SagemakerWorkteamMemberDefinitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e52f43a05a7a7b808d56ef32ae6790e725c6490ba2e884f63a6d3e3003379f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCognitoMemberDefinition")
    def put_cognito_member_definition(
        self,
        *,
        client_id: builtins.str,
        user_group: builtins.str,
        user_pool: builtins.str,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#client_id SagemakerWorkteam#client_id}.
        :param user_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#user_group SagemakerWorkteam#user_group}.
        :param user_pool: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#user_pool SagemakerWorkteam#user_pool}.
        '''
        value = SagemakerWorkteamMemberDefinitionCognitoMemberDefinition(
            client_id=client_id, user_group=user_group, user_pool=user_pool
        )

        return typing.cast(None, jsii.invoke(self, "putCognitoMemberDefinition", [value]))

    @jsii.member(jsii_name="putOidcMemberDefinition")
    def put_oidc_member_definition(
        self,
        *,
        groups: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#groups SagemakerWorkteam#groups}.
        '''
        value = SagemakerWorkteamMemberDefinitionOidcMemberDefinition(groups=groups)

        return typing.cast(None, jsii.invoke(self, "putOidcMemberDefinition", [value]))

    @jsii.member(jsii_name="resetCognitoMemberDefinition")
    def reset_cognito_member_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCognitoMemberDefinition", []))

    @jsii.member(jsii_name="resetOidcMemberDefinition")
    def reset_oidc_member_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOidcMemberDefinition", []))

    @builtins.property
    @jsii.member(jsii_name="cognitoMemberDefinition")
    def cognito_member_definition(
        self,
    ) -> SagemakerWorkteamMemberDefinitionCognitoMemberDefinitionOutputReference:
        return typing.cast(SagemakerWorkteamMemberDefinitionCognitoMemberDefinitionOutputReference, jsii.get(self, "cognitoMemberDefinition"))

    @builtins.property
    @jsii.member(jsii_name="oidcMemberDefinition")
    def oidc_member_definition(
        self,
    ) -> SagemakerWorkteamMemberDefinitionOidcMemberDefinitionOutputReference:
        return typing.cast(SagemakerWorkteamMemberDefinitionOidcMemberDefinitionOutputReference, jsii.get(self, "oidcMemberDefinition"))

    @builtins.property
    @jsii.member(jsii_name="cognitoMemberDefinitionInput")
    def cognito_member_definition_input(
        self,
    ) -> typing.Optional[SagemakerWorkteamMemberDefinitionCognitoMemberDefinition]:
        return typing.cast(typing.Optional[SagemakerWorkteamMemberDefinitionCognitoMemberDefinition], jsii.get(self, "cognitoMemberDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcMemberDefinitionInput")
    def oidc_member_definition_input(
        self,
    ) -> typing.Optional[SagemakerWorkteamMemberDefinitionOidcMemberDefinition]:
        return typing.cast(typing.Optional[SagemakerWorkteamMemberDefinitionOidcMemberDefinition], jsii.get(self, "oidcMemberDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerWorkteamMemberDefinition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerWorkteamMemberDefinition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerWorkteamMemberDefinition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e10bf959cea5469e142a5324f0ad83acded9fbe0f4caf463d31fa45f87d2144f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerWorkteam.SagemakerWorkteamNotificationConfiguration",
    jsii_struct_bases=[],
    name_mapping={"notification_topic_arn": "notificationTopicArn"},
)
class SagemakerWorkteamNotificationConfiguration:
    def __init__(
        self,
        *,
        notification_topic_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param notification_topic_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#notification_topic_arn SagemakerWorkteam#notification_topic_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__411960949d6f61249995df19a838c3fc1697ed16a5fe7eb64a243fa6cc2dc608)
            check_type(argname="argument notification_topic_arn", value=notification_topic_arn, expected_type=type_hints["notification_topic_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if notification_topic_arn is not None:
            self._values["notification_topic_arn"] = notification_topic_arn

    @builtins.property
    def notification_topic_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#notification_topic_arn SagemakerWorkteam#notification_topic_arn}.'''
        result = self._values.get("notification_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerWorkteamNotificationConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerWorkteamNotificationConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerWorkteam.SagemakerWorkteamNotificationConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdb0ebfd9c7c5fd3522a90b85b7821835b1eea9677293ef926f979221ea2c613)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNotificationTopicArn")
    def reset_notification_topic_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationTopicArn", []))

    @builtins.property
    @jsii.member(jsii_name="notificationTopicArnInput")
    def notification_topic_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationTopicArnInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationTopicArn")
    def notification_topic_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationTopicArn"))

    @notification_topic_arn.setter
    def notification_topic_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bcbc236bf264a7a1f6e01b1377fbcef4517de4b2aeb397d18b45c43ccb87e58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationTopicArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerWorkteamNotificationConfiguration]:
        return typing.cast(typing.Optional[SagemakerWorkteamNotificationConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerWorkteamNotificationConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e542892aab3049955aeceaa936f493270e08956f7986e862f786deabaaeb8681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerWorkteam.SagemakerWorkteamWorkerAccessConfiguration",
    jsii_struct_bases=[],
    name_mapping={"s3_presign": "s3Presign"},
)
class SagemakerWorkteamWorkerAccessConfiguration:
    def __init__(
        self,
        *,
        s3_presign: typing.Optional[typing.Union["SagemakerWorkteamWorkerAccessConfigurationS3Presign", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param s3_presign: s3_presign block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#s3_presign SagemakerWorkteam#s3_presign}
        '''
        if isinstance(s3_presign, dict):
            s3_presign = SagemakerWorkteamWorkerAccessConfigurationS3Presign(**s3_presign)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d2e4fbc8d6306e304c405ca540dfede49c5aa2ef31cff4437a98e33dd30a48)
            check_type(argname="argument s3_presign", value=s3_presign, expected_type=type_hints["s3_presign"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3_presign is not None:
            self._values["s3_presign"] = s3_presign

    @builtins.property
    def s3_presign(
        self,
    ) -> typing.Optional["SagemakerWorkteamWorkerAccessConfigurationS3Presign"]:
        '''s3_presign block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#s3_presign SagemakerWorkteam#s3_presign}
        '''
        result = self._values.get("s3_presign")
        return typing.cast(typing.Optional["SagemakerWorkteamWorkerAccessConfigurationS3Presign"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerWorkteamWorkerAccessConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerWorkteamWorkerAccessConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerWorkteam.SagemakerWorkteamWorkerAccessConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7545e72ee5b2bf5a4785c2131bd9141f6064043e984de0f4eab1635517084d86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putS3Presign")
    def put_s3_presign(
        self,
        *,
        iam_policy_constraints: typing.Optional[typing.Union["SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param iam_policy_constraints: iam_policy_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#iam_policy_constraints SagemakerWorkteam#iam_policy_constraints}
        '''
        value = SagemakerWorkteamWorkerAccessConfigurationS3Presign(
            iam_policy_constraints=iam_policy_constraints
        )

        return typing.cast(None, jsii.invoke(self, "putS3Presign", [value]))

    @jsii.member(jsii_name="resetS3Presign")
    def reset_s3_presign(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Presign", []))

    @builtins.property
    @jsii.member(jsii_name="s3Presign")
    def s3_presign(
        self,
    ) -> "SagemakerWorkteamWorkerAccessConfigurationS3PresignOutputReference":
        return typing.cast("SagemakerWorkteamWorkerAccessConfigurationS3PresignOutputReference", jsii.get(self, "s3Presign"))

    @builtins.property
    @jsii.member(jsii_name="s3PresignInput")
    def s3_presign_input(
        self,
    ) -> typing.Optional["SagemakerWorkteamWorkerAccessConfigurationS3Presign"]:
        return typing.cast(typing.Optional["SagemakerWorkteamWorkerAccessConfigurationS3Presign"], jsii.get(self, "s3PresignInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerWorkteamWorkerAccessConfiguration]:
        return typing.cast(typing.Optional[SagemakerWorkteamWorkerAccessConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerWorkteamWorkerAccessConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c788d42d1004534b4d87f198750c4f6f2a3d3038f05a52602e09366f626f45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerWorkteam.SagemakerWorkteamWorkerAccessConfigurationS3Presign",
    jsii_struct_bases=[],
    name_mapping={"iam_policy_constraints": "iamPolicyConstraints"},
)
class SagemakerWorkteamWorkerAccessConfigurationS3Presign:
    def __init__(
        self,
        *,
        iam_policy_constraints: typing.Optional[typing.Union["SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param iam_policy_constraints: iam_policy_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#iam_policy_constraints SagemakerWorkteam#iam_policy_constraints}
        '''
        if isinstance(iam_policy_constraints, dict):
            iam_policy_constraints = SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraints(**iam_policy_constraints)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__901bee5d5be4f6c7292b93b9ed04a18f4f99f64afb5e9df4be10ecc420af0e0b)
            check_type(argname="argument iam_policy_constraints", value=iam_policy_constraints, expected_type=type_hints["iam_policy_constraints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if iam_policy_constraints is not None:
            self._values["iam_policy_constraints"] = iam_policy_constraints

    @builtins.property
    def iam_policy_constraints(
        self,
    ) -> typing.Optional["SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraints"]:
        '''iam_policy_constraints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#iam_policy_constraints SagemakerWorkteam#iam_policy_constraints}
        '''
        result = self._values.get("iam_policy_constraints")
        return typing.cast(typing.Optional["SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraints"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerWorkteamWorkerAccessConfigurationS3Presign(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerWorkteam.SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraints",
    jsii_struct_bases=[],
    name_mapping={"source_ip": "sourceIp", "vpc_source_ip": "vpcSourceIp"},
)
class SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraints:
    def __init__(
        self,
        *,
        source_ip: typing.Optional[builtins.str] = None,
        vpc_source_ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#source_ip SagemakerWorkteam#source_ip}.
        :param vpc_source_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#vpc_source_ip SagemakerWorkteam#vpc_source_ip}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2202bc6e7f1f9cbfa59d4e89a3657e178eead1d1ec8a94de17074302b11f698a)
            check_type(argname="argument source_ip", value=source_ip, expected_type=type_hints["source_ip"])
            check_type(argname="argument vpc_source_ip", value=vpc_source_ip, expected_type=type_hints["vpc_source_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if source_ip is not None:
            self._values["source_ip"] = source_ip
        if vpc_source_ip is not None:
            self._values["vpc_source_ip"] = vpc_source_ip

    @builtins.property
    def source_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#source_ip SagemakerWorkteam#source_ip}.'''
        result = self._values.get("source_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_source_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#vpc_source_ip SagemakerWorkteam#vpc_source_ip}.'''
        result = self._values.get("vpc_source_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerWorkteam.SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cd9c65cad15af4362d22d4b8838ac3315877a37c5389e4538931b12ae17f666)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSourceIp")
    def reset_source_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceIp", []))

    @jsii.member(jsii_name="resetVpcSourceIp")
    def reset_vpc_source_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcSourceIp", []))

    @builtins.property
    @jsii.member(jsii_name="sourceIpInput")
    def source_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceIpInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcSourceIpInput")
    def vpc_source_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcSourceIpInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceIp")
    def source_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceIp"))

    @source_ip.setter
    def source_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc19a59e0a625c62d1da4989f58c06b8bd235c9eb82aa61d8db55d51c939531)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcSourceIp")
    def vpc_source_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcSourceIp"))

    @vpc_source_ip.setter
    def vpc_source_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5fb08d738e183eee3b4363a3fed843924f9bd4179c76a5b0f2b19d185802376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcSourceIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraints]:
        return typing.cast(typing.Optional[SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__899d648ae04f01e95546475a5665a593657e6f7adc4810fd940c4d8e0a83c9e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerWorkteamWorkerAccessConfigurationS3PresignOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerWorkteam.SagemakerWorkteamWorkerAccessConfigurationS3PresignOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e491c49b12cb980eb04ba716dfb786b69789201b33ccecf676d7a98e2f5f5311)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIamPolicyConstraints")
    def put_iam_policy_constraints(
        self,
        *,
        source_ip: typing.Optional[builtins.str] = None,
        vpc_source_ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#source_ip SagemakerWorkteam#source_ip}.
        :param vpc_source_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_workteam#vpc_source_ip SagemakerWorkteam#vpc_source_ip}.
        '''
        value = SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraints(
            source_ip=source_ip, vpc_source_ip=vpc_source_ip
        )

        return typing.cast(None, jsii.invoke(self, "putIamPolicyConstraints", [value]))

    @jsii.member(jsii_name="resetIamPolicyConstraints")
    def reset_iam_policy_constraints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIamPolicyConstraints", []))

    @builtins.property
    @jsii.member(jsii_name="iamPolicyConstraints")
    def iam_policy_constraints(
        self,
    ) -> SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraintsOutputReference:
        return typing.cast(SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraintsOutputReference, jsii.get(self, "iamPolicyConstraints"))

    @builtins.property
    @jsii.member(jsii_name="iamPolicyConstraintsInput")
    def iam_policy_constraints_input(
        self,
    ) -> typing.Optional[SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraints]:
        return typing.cast(typing.Optional[SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraints], jsii.get(self, "iamPolicyConstraintsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerWorkteamWorkerAccessConfigurationS3Presign]:
        return typing.cast(typing.Optional[SagemakerWorkteamWorkerAccessConfigurationS3Presign], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerWorkteamWorkerAccessConfigurationS3Presign],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f4f8c26454219edce9c3d6a33e892d9814f1a794f4f52188897fea2cd4aae42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SagemakerWorkteam",
    "SagemakerWorkteamConfig",
    "SagemakerWorkteamMemberDefinition",
    "SagemakerWorkteamMemberDefinitionCognitoMemberDefinition",
    "SagemakerWorkteamMemberDefinitionCognitoMemberDefinitionOutputReference",
    "SagemakerWorkteamMemberDefinitionList",
    "SagemakerWorkteamMemberDefinitionOidcMemberDefinition",
    "SagemakerWorkteamMemberDefinitionOidcMemberDefinitionOutputReference",
    "SagemakerWorkteamMemberDefinitionOutputReference",
    "SagemakerWorkteamNotificationConfiguration",
    "SagemakerWorkteamNotificationConfigurationOutputReference",
    "SagemakerWorkteamWorkerAccessConfiguration",
    "SagemakerWorkteamWorkerAccessConfigurationOutputReference",
    "SagemakerWorkteamWorkerAccessConfigurationS3Presign",
    "SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraints",
    "SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraintsOutputReference",
    "SagemakerWorkteamWorkerAccessConfigurationS3PresignOutputReference",
]

publication.publish()

def _typecheckingstub__61182a7f7a8c9b80e8fc65f15d2ebe44a7fdfd9e422e92478001ec9212c954c8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    description: builtins.str,
    member_definition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerWorkteamMemberDefinition, typing.Dict[builtins.str, typing.Any]]]],
    workteam_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    notification_configuration: typing.Optional[typing.Union[SagemakerWorkteamNotificationConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    worker_access_configuration: typing.Optional[typing.Union[SagemakerWorkteamWorkerAccessConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    workforce_name: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__9ca4261e3280eccc6a2d60b532c297870eb3add0694fbc6d2946ddaf2266d502(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__399477def7d0cd56e9a8af3307b32471949f81d10a9cb4c4f290b07e1fba188f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerWorkteamMemberDefinition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2902d8aa9c03c3b31424678deccde9b4de5848a04be276db07d9034ffd2cbb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c581cd990eef46f9483226a7f3761c0e24563ad6792bdb12cd1d95f54f15af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9df337d0b7cfe8d81593354b6647f45ac506201cf147c3d4b5b16088e06fd0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a1f0ba0fd7d8b8c892a4da468ba5cae517487c1756ac0997757bfa9798323c8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b34429ce15bbc06ca6adbe9f349ae45c3eefc9996a85947db2d72b7f63fb95e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ff16d87e0d45fe09ba0b8b4accb062ede88b872434aa61c252098b58583fd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f80b9924b811aeba7014bc8972a1acd4d99297f423b032bc96ff3a175c64d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c910d7d3230cf7e74716e8921164dfadcea8e81be0222dd6b3cd806c4e6cf884(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: builtins.str,
    member_definition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerWorkteamMemberDefinition, typing.Dict[builtins.str, typing.Any]]]],
    workteam_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    notification_configuration: typing.Optional[typing.Union[SagemakerWorkteamNotificationConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    worker_access_configuration: typing.Optional[typing.Union[SagemakerWorkteamWorkerAccessConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    workforce_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ec1f46097cd8e139b9f276e90e90ba35360426877ec444c0aee7e854557dc0c(
    *,
    cognito_member_definition: typing.Optional[typing.Union[SagemakerWorkteamMemberDefinitionCognitoMemberDefinition, typing.Dict[builtins.str, typing.Any]]] = None,
    oidc_member_definition: typing.Optional[typing.Union[SagemakerWorkteamMemberDefinitionOidcMemberDefinition, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4259d08b00e73e9a08d481689225f083a849accabcc3cbcffce7ccdd874f6d90(
    *,
    client_id: builtins.str,
    user_group: builtins.str,
    user_pool: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8faba07020798b8733a47562f3905cb437242cd2478c08876230f6d0e27feef4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9abc9a4b5902148cb4b2dd1b5be77da8caa9ef8f8e1dc9bb0ccd906fbd7b2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fdfa3d905f5938a797779ecd19dda8a3b9c69f3d775edf5bf6af46bdd975caa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64fb07ec4190fb86008f7ff0a7b681015878c237bcbe9a6049be176153583857(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__122cf41577872df8c64efa43059019c9080ea0c518e1e2f2beb05b357dd87750(
    value: typing.Optional[SagemakerWorkteamMemberDefinitionCognitoMemberDefinition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14c3816c0212519e8bf1533f6f88219c15fa29d3e1dcb60de417592bfd1f72c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b247c76f2cd39e3aba315dc2a8a2bc80fd8441a9c533a440fe5599dfb26e8b8c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7a42239181987c78c909e36777a8c1e5758940730345b28890dc86d6c2d008(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ece7957b87483c35103e003f9308f002ad668c92f5077d71d63468b5c817700(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e69095cf81591c072a441d179ea79d47aea4429f5d57355610cf40b10b1263(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3b84479409b9cdaa9777f2bfb222fc4cae30f54e559bf712d6cd24fbf3a046(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerWorkteamMemberDefinition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a3f10b47933d93d68c5933dd3c7daad6d3496352a45ab1d842db09e698b084(
    *,
    groups: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf41e2aa12965e76bb57a942fa7e2a1f650192df0fa25648056dc48bd2497fde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7c7e26ab9941476e6a763965c4d940cdbec9abaff3aa3bf1c51f95777ad6237(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dfac0beba56fb8943d55a3a0a608a802e4e46e3966ea4f9a092a6123cbf1118(
    value: typing.Optional[SagemakerWorkteamMemberDefinitionOidcMemberDefinition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e52f43a05a7a7b808d56ef32ae6790e725c6490ba2e884f63a6d3e3003379f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10bf959cea5469e142a5324f0ad83acded9fbe0f4caf463d31fa45f87d2144f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerWorkteamMemberDefinition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__411960949d6f61249995df19a838c3fc1697ed16a5fe7eb64a243fa6cc2dc608(
    *,
    notification_topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdb0ebfd9c7c5fd3522a90b85b7821835b1eea9677293ef926f979221ea2c613(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bcbc236bf264a7a1f6e01b1377fbcef4517de4b2aeb397d18b45c43ccb87e58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e542892aab3049955aeceaa936f493270e08956f7986e862f786deabaaeb8681(
    value: typing.Optional[SagemakerWorkteamNotificationConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d2e4fbc8d6306e304c405ca540dfede49c5aa2ef31cff4437a98e33dd30a48(
    *,
    s3_presign: typing.Optional[typing.Union[SagemakerWorkteamWorkerAccessConfigurationS3Presign, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7545e72ee5b2bf5a4785c2131bd9141f6064043e984de0f4eab1635517084d86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c788d42d1004534b4d87f198750c4f6f2a3d3038f05a52602e09366f626f45(
    value: typing.Optional[SagemakerWorkteamWorkerAccessConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901bee5d5be4f6c7292b93b9ed04a18f4f99f64afb5e9df4be10ecc420af0e0b(
    *,
    iam_policy_constraints: typing.Optional[typing.Union[SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraints, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2202bc6e7f1f9cbfa59d4e89a3657e178eead1d1ec8a94de17074302b11f698a(
    *,
    source_ip: typing.Optional[builtins.str] = None,
    vpc_source_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd9c65cad15af4362d22d4b8838ac3315877a37c5389e4538931b12ae17f666(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc19a59e0a625c62d1da4989f58c06b8bd235c9eb82aa61d8db55d51c939531(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5fb08d738e183eee3b4363a3fed843924f9bd4179c76a5b0f2b19d185802376(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899d648ae04f01e95546475a5665a593657e6f7adc4810fd940c4d8e0a83c9e6(
    value: typing.Optional[SagemakerWorkteamWorkerAccessConfigurationS3PresignIamPolicyConstraints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e491c49b12cb980eb04ba716dfb786b69789201b33ccecf676d7a98e2f5f5311(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f4f8c26454219edce9c3d6a33e892d9814f1a794f4f52188897fea2cd4aae42(
    value: typing.Optional[SagemakerWorkteamWorkerAccessConfigurationS3Presign],
) -> None:
    """Type checking stubs"""
    pass
