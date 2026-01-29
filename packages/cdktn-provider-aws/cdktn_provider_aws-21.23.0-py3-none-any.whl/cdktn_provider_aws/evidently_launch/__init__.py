r'''
# `aws_evidently_launch`

Refer to the Terraform Registry for docs: [`aws_evidently_launch`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch).
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


class EvidentlyLaunch(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunch",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch aws_evidently_launch}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EvidentlyLaunchGroups", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        project: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        metric_monitors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EvidentlyLaunchMetricMonitors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        randomization_salt: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scheduled_splits_config: typing.Optional[typing.Union["EvidentlyLaunchScheduledSplitsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["EvidentlyLaunchTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch aws_evidently_launch} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param groups: groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#groups EvidentlyLaunch#groups}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#name EvidentlyLaunch#name}.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#project EvidentlyLaunch#project}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#description EvidentlyLaunch#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#id EvidentlyLaunch#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metric_monitors: metric_monitors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#metric_monitors EvidentlyLaunch#metric_monitors}
        :param randomization_salt: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#randomization_salt EvidentlyLaunch#randomization_salt}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#region EvidentlyLaunch#region}
        :param scheduled_splits_config: scheduled_splits_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#scheduled_splits_config EvidentlyLaunch#scheduled_splits_config}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#tags EvidentlyLaunch#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#tags_all EvidentlyLaunch#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#timeouts EvidentlyLaunch#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7585259ec71ac752032bb97374f37c091cdad4ac6e760c1aafb8249e441fb5d4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EvidentlyLaunchConfig(
            groups=groups,
            name=name,
            project=project,
            description=description,
            id=id,
            metric_monitors=metric_monitors,
            randomization_salt=randomization_salt,
            region=region,
            scheduled_splits_config=scheduled_splits_config,
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
        '''Generates CDKTF code for importing a EvidentlyLaunch resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EvidentlyLaunch to import.
        :param import_from_id: The id of the existing EvidentlyLaunch that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EvidentlyLaunch to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23d71251d3702e8749892b711b09202dee4838001e49a3df0dde4c4a9bc6f162)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putGroups")
    def put_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EvidentlyLaunchGroups", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__360b457c2009c3e93059cba904a028607964d5d14f9c169f413c281b3e15cd9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGroups", [value]))

    @jsii.member(jsii_name="putMetricMonitors")
    def put_metric_monitors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EvidentlyLaunchMetricMonitors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a28c4c90034c7916080604cc7e24205c0fe6d68c7b56afc9b676d05a2aef34e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetricMonitors", [value]))

    @jsii.member(jsii_name="putScheduledSplitsConfig")
    def put_scheduled_splits_config(
        self,
        *,
        steps: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EvidentlyLaunchScheduledSplitsConfigSteps", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param steps: steps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#steps EvidentlyLaunch#steps}
        '''
        value = EvidentlyLaunchScheduledSplitsConfig(steps=steps)

        return typing.cast(None, jsii.invoke(self, "putScheduledSplitsConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#create EvidentlyLaunch#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#delete EvidentlyLaunch#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#update EvidentlyLaunch#update}.
        '''
        value = EvidentlyLaunchTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMetricMonitors")
    def reset_metric_monitors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricMonitors", []))

    @jsii.member(jsii_name="resetRandomizationSalt")
    def reset_randomization_salt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRandomizationSalt", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetScheduledSplitsConfig")
    def reset_scheduled_splits_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduledSplitsConfig", []))

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
    @jsii.member(jsii_name="createdTime")
    def created_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdTime"))

    @builtins.property
    @jsii.member(jsii_name="execution")
    def execution(self) -> "EvidentlyLaunchExecutionList":
        return typing.cast("EvidentlyLaunchExecutionList", jsii.get(self, "execution"))

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> "EvidentlyLaunchGroupsList":
        return typing.cast("EvidentlyLaunchGroupsList", jsii.get(self, "groups"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdatedTime")
    def last_updated_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdatedTime"))

    @builtins.property
    @jsii.member(jsii_name="metricMonitors")
    def metric_monitors(self) -> "EvidentlyLaunchMetricMonitorsList":
        return typing.cast("EvidentlyLaunchMetricMonitorsList", jsii.get(self, "metricMonitors"))

    @builtins.property
    @jsii.member(jsii_name="scheduledSplitsConfig")
    def scheduled_splits_config(
        self,
    ) -> "EvidentlyLaunchScheduledSplitsConfigOutputReference":
        return typing.cast("EvidentlyLaunchScheduledSplitsConfigOutputReference", jsii.get(self, "scheduledSplitsConfig"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="statusReason")
    def status_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusReason"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "EvidentlyLaunchTimeoutsOutputReference":
        return typing.cast("EvidentlyLaunchTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsInput")
    def groups_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EvidentlyLaunchGroups"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EvidentlyLaunchGroups"]]], jsii.get(self, "groupsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="metricMonitorsInput")
    def metric_monitors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EvidentlyLaunchMetricMonitors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EvidentlyLaunchMetricMonitors"]]], jsii.get(self, "metricMonitorsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="randomizationSaltInput")
    def randomization_salt_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "randomizationSaltInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduledSplitsConfigInput")
    def scheduled_splits_config_input(
        self,
    ) -> typing.Optional["EvidentlyLaunchScheduledSplitsConfig"]:
        return typing.cast(typing.Optional["EvidentlyLaunchScheduledSplitsConfig"], jsii.get(self, "scheduledSplitsConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EvidentlyLaunchTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EvidentlyLaunchTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f455e164ca605858bc7e053913b5a91e7cad51aad6ab29e4a82c3f3da9fe082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__665c81134efa2b0579aaf9df084fb740c73d9dc5290a59d5ea78ead790589bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56ea910a5f1c9dec5aef93747ce5e3b9224c04973a33e954c043ba53f886f2bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__370bd23b304152093b16fb5b809805f04187a8557ec6bfc3798183274957ebdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="randomizationSalt")
    def randomization_salt(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "randomizationSalt"))

    @randomization_salt.setter
    def randomization_salt(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b352ccaad0ab2b8494352d4dd475108e82c496c8fbd9285de24ae04f1f6d90a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "randomizationSalt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37f66606608aa00a10ec602a900d8e81a24437342f0ab7d2ab86d2451489a66f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574e5157b7b490043490779e30234a983e9de44252fd26b29c2b9636851779f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d43d428e7e7823c6801e1b09e15742377ebdee477c4fc84a5c80c04f86ac52f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "groups": "groups",
        "name": "name",
        "project": "project",
        "description": "description",
        "id": "id",
        "metric_monitors": "metricMonitors",
        "randomization_salt": "randomizationSalt",
        "region": "region",
        "scheduled_splits_config": "scheduledSplitsConfig",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class EvidentlyLaunchConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EvidentlyLaunchGroups", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        project: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        metric_monitors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EvidentlyLaunchMetricMonitors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        randomization_salt: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scheduled_splits_config: typing.Optional[typing.Union["EvidentlyLaunchScheduledSplitsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["EvidentlyLaunchTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param groups: groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#groups EvidentlyLaunch#groups}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#name EvidentlyLaunch#name}.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#project EvidentlyLaunch#project}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#description EvidentlyLaunch#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#id EvidentlyLaunch#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metric_monitors: metric_monitors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#metric_monitors EvidentlyLaunch#metric_monitors}
        :param randomization_salt: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#randomization_salt EvidentlyLaunch#randomization_salt}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#region EvidentlyLaunch#region}
        :param scheduled_splits_config: scheduled_splits_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#scheduled_splits_config EvidentlyLaunch#scheduled_splits_config}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#tags EvidentlyLaunch#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#tags_all EvidentlyLaunch#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#timeouts EvidentlyLaunch#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(scheduled_splits_config, dict):
            scheduled_splits_config = EvidentlyLaunchScheduledSplitsConfig(**scheduled_splits_config)
        if isinstance(timeouts, dict):
            timeouts = EvidentlyLaunchTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f7bd0424c475b1783bf96f94f9003591dd7bd1bf78c55cd170c314b6edbc504)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument metric_monitors", value=metric_monitors, expected_type=type_hints["metric_monitors"])
            check_type(argname="argument randomization_salt", value=randomization_salt, expected_type=type_hints["randomization_salt"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument scheduled_splits_config", value=scheduled_splits_config, expected_type=type_hints["scheduled_splits_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "groups": groups,
            "name": name,
            "project": project,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if metric_monitors is not None:
            self._values["metric_monitors"] = metric_monitors
        if randomization_salt is not None:
            self._values["randomization_salt"] = randomization_salt
        if region is not None:
            self._values["region"] = region
        if scheduled_splits_config is not None:
            self._values["scheduled_splits_config"] = scheduled_splits_config
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
    def groups(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EvidentlyLaunchGroups"]]:
        '''groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#groups EvidentlyLaunch#groups}
        '''
        result = self._values.get("groups")
        assert result is not None, "Required property 'groups' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EvidentlyLaunchGroups"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#name EvidentlyLaunch#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#project EvidentlyLaunch#project}.'''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#description EvidentlyLaunch#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#id EvidentlyLaunch#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_monitors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EvidentlyLaunchMetricMonitors"]]]:
        '''metric_monitors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#metric_monitors EvidentlyLaunch#metric_monitors}
        '''
        result = self._values.get("metric_monitors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EvidentlyLaunchMetricMonitors"]]], result)

    @builtins.property
    def randomization_salt(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#randomization_salt EvidentlyLaunch#randomization_salt}.'''
        result = self._values.get("randomization_salt")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#region EvidentlyLaunch#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduled_splits_config(
        self,
    ) -> typing.Optional["EvidentlyLaunchScheduledSplitsConfig"]:
        '''scheduled_splits_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#scheduled_splits_config EvidentlyLaunch#scheduled_splits_config}
        '''
        result = self._values.get("scheduled_splits_config")
        return typing.cast(typing.Optional["EvidentlyLaunchScheduledSplitsConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#tags EvidentlyLaunch#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#tags_all EvidentlyLaunch#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["EvidentlyLaunchTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#timeouts EvidentlyLaunch#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["EvidentlyLaunchTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EvidentlyLaunchConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchExecution",
    jsii_struct_bases=[],
    name_mapping={},
)
class EvidentlyLaunchExecution:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EvidentlyLaunchExecution(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EvidentlyLaunchExecutionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchExecutionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b27868861ded82d53865da0f8744d4fd9fdc2a7c4547c0c4c4a95fbe497d9d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EvidentlyLaunchExecutionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76238fc8d3b68ac85a189a838fc1541541dca1b58c0e770543d99c1ae0697f86)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EvidentlyLaunchExecutionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__109c58ecbf8a5dd0eea5c5b48d3a5be7642de2173c7c453af4fd3ba64ae16a9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__797d47c53aed7ccdf46dec0ad1830ea732bd2f33b78f22b3a37d69739a03c755)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4242991cc2c1bb9e87ed24848ca0b4987b11fa639be43fbf7a19d24e3a49b5ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class EvidentlyLaunchExecutionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchExecutionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b5e038f57424f47b05e358a50320daa3a5f86d5083a09716908bf5b46446d07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endedTime")
    def ended_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endedTime"))

    @builtins.property
    @jsii.member(jsii_name="startedTime")
    def started_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startedTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EvidentlyLaunchExecution]:
        return typing.cast(typing.Optional[EvidentlyLaunchExecution], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EvidentlyLaunchExecution]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74dec3bc2f27cace88b5bacad1ecf98292eb2742f5489c72a7d9a454ab1823b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchGroups",
    jsii_struct_bases=[],
    name_mapping={
        "feature": "feature",
        "name": "name",
        "variation": "variation",
        "description": "description",
    },
)
class EvidentlyLaunchGroups:
    def __init__(
        self,
        *,
        feature: builtins.str,
        name: builtins.str,
        variation: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param feature: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#feature EvidentlyLaunch#feature}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#name EvidentlyLaunch#name}.
        :param variation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#variation EvidentlyLaunch#variation}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#description EvidentlyLaunch#description}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d0e86df276f47a2ff2cb5ade5bb6888214c3bb2e6219bad1852254080f9f8bd)
            check_type(argname="argument feature", value=feature, expected_type=type_hints["feature"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument variation", value=variation, expected_type=type_hints["variation"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "feature": feature,
            "name": name,
            "variation": variation,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def feature(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#feature EvidentlyLaunch#feature}.'''
        result = self._values.get("feature")
        assert result is not None, "Required property 'feature' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#name EvidentlyLaunch#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def variation(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#variation EvidentlyLaunch#variation}.'''
        result = self._values.get("variation")
        assert result is not None, "Required property 'variation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#description EvidentlyLaunch#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EvidentlyLaunchGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EvidentlyLaunchGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a169b8da5f5a6da4f81eb62618b3d7ecbd559a26505a62cbe7692ee9ce0c150)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EvidentlyLaunchGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c023cce2ea7e7129d18444ba4c25aa7e2fa7ac7c97890bbd8ec7b1d45e8dace9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EvidentlyLaunchGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7667a975fa0651a68255b8ce78d00f0441b7157247c6c06041a5322c2760124f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__476c718288df79c494bc8422490c28ac64de5e168fe1a0d78605cf20686b7f20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3c1831231397757e5ff7ddf26b9d5c3aaa930be3ae23de19cb58829d7d00988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EvidentlyLaunchGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EvidentlyLaunchGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EvidentlyLaunchGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e18e60c9129d28acedc984372627bd3ab64e0481fd109b070e2494077212370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EvidentlyLaunchGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7821b2f1c2af44f02b03a435aee18b85f8fcdce901b1c201d224625458f596f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="featureInput")
    def feature_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featureInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="variationInput")
    def variation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "variationInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e0cfc3cff17e521f764c4aab63aaf9488c597767f73ca4af00ae2f85a74b380)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="feature")
    def feature(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "feature"))

    @feature.setter
    def feature(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e892c86508cf04bdc8ca7916f5978319cc9246071ef8112d5a3de24753d75b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "feature", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e9bcf31ec221aedcd86c84d5e0561aa3fcfbe5a7cf3bf48ffea7d8a6235e4b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="variation")
    def variation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "variation"))

    @variation.setter
    def variation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f47556d3a59ada9e254c098b4ac2fec90c91749b93d9bbeb02faefa61e24242e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6592dd5cbb9cb647018c6862aecc14112fda361eebf308d2399aaf750f94f6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchMetricMonitors",
    jsii_struct_bases=[],
    name_mapping={"metric_definition": "metricDefinition"},
)
class EvidentlyLaunchMetricMonitors:
    def __init__(
        self,
        *,
        metric_definition: typing.Union["EvidentlyLaunchMetricMonitorsMetricDefinition", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param metric_definition: metric_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#metric_definition EvidentlyLaunch#metric_definition}
        '''
        if isinstance(metric_definition, dict):
            metric_definition = EvidentlyLaunchMetricMonitorsMetricDefinition(**metric_definition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3345eaab8f2f8451093bc2e20c44590d444ed3759b79274bca57eb064659f82a)
            check_type(argname="argument metric_definition", value=metric_definition, expected_type=type_hints["metric_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_definition": metric_definition,
        }

    @builtins.property
    def metric_definition(self) -> "EvidentlyLaunchMetricMonitorsMetricDefinition":
        '''metric_definition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#metric_definition EvidentlyLaunch#metric_definition}
        '''
        result = self._values.get("metric_definition")
        assert result is not None, "Required property 'metric_definition' is missing"
        return typing.cast("EvidentlyLaunchMetricMonitorsMetricDefinition", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EvidentlyLaunchMetricMonitors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EvidentlyLaunchMetricMonitorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchMetricMonitorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43570485a573d6d536bd18c588d2e458f4cad9db98658566a8b263699544d990)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EvidentlyLaunchMetricMonitorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c33b35ddee0b87982ef356cc4fb1a4d80d9162a2ed28512d62f273c0f630dd8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EvidentlyLaunchMetricMonitorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b1f866db5eadb976dfe08569932c194f2bb25cf904d0bfa49f74b1079bdd6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__275da59ee00c6d5cc79aa058c1fe0acd691e0af4ca02fed9605e21901d9e6683)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9246f94de3a7f1afa58d6d4f7ea72e19781b9ede88907919b3553d9331a53cd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EvidentlyLaunchMetricMonitors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EvidentlyLaunchMetricMonitors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EvidentlyLaunchMetricMonitors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d29135c5152466a3798491ab728a4834fd88be36172bd6c3c4a9324c0a0c58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchMetricMonitorsMetricDefinition",
    jsii_struct_bases=[],
    name_mapping={
        "entity_id_key": "entityIdKey",
        "name": "name",
        "value_key": "valueKey",
        "event_pattern": "eventPattern",
        "unit_label": "unitLabel",
    },
)
class EvidentlyLaunchMetricMonitorsMetricDefinition:
    def __init__(
        self,
        *,
        entity_id_key: builtins.str,
        name: builtins.str,
        value_key: builtins.str,
        event_pattern: typing.Optional[builtins.str] = None,
        unit_label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param entity_id_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#entity_id_key EvidentlyLaunch#entity_id_key}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#name EvidentlyLaunch#name}.
        :param value_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#value_key EvidentlyLaunch#value_key}.
        :param event_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#event_pattern EvidentlyLaunch#event_pattern}.
        :param unit_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#unit_label EvidentlyLaunch#unit_label}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69fd1b96a13d89f63a7d3087789b171dea71f2683c6c3f6a0c40d6249a3c1560)
            check_type(argname="argument entity_id_key", value=entity_id_key, expected_type=type_hints["entity_id_key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value_key", value=value_key, expected_type=type_hints["value_key"])
            check_type(argname="argument event_pattern", value=event_pattern, expected_type=type_hints["event_pattern"])
            check_type(argname="argument unit_label", value=unit_label, expected_type=type_hints["unit_label"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entity_id_key": entity_id_key,
            "name": name,
            "value_key": value_key,
        }
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if unit_label is not None:
            self._values["unit_label"] = unit_label

    @builtins.property
    def entity_id_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#entity_id_key EvidentlyLaunch#entity_id_key}.'''
        result = self._values.get("entity_id_key")
        assert result is not None, "Required property 'entity_id_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#name EvidentlyLaunch#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#value_key EvidentlyLaunch#value_key}.'''
        result = self._values.get("value_key")
        assert result is not None, "Required property 'value_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_pattern(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#event_pattern EvidentlyLaunch#event_pattern}.'''
        result = self._values.get("event_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unit_label(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#unit_label EvidentlyLaunch#unit_label}.'''
        result = self._values.get("unit_label")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EvidentlyLaunchMetricMonitorsMetricDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EvidentlyLaunchMetricMonitorsMetricDefinitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchMetricMonitorsMetricDefinitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bed9b7eb10a692c3cdda1bbb8684ed849639ec4f4a33fe571ca541d61bdd266)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEventPattern")
    def reset_event_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventPattern", []))

    @jsii.member(jsii_name="resetUnitLabel")
    def reset_unit_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnitLabel", []))

    @builtins.property
    @jsii.member(jsii_name="entityIdKeyInput")
    def entity_id_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entityIdKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="eventPatternInput")
    def event_pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventPatternInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="unitLabelInput")
    def unit_label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="valueKeyInput")
    def value_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="entityIdKey")
    def entity_id_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entityIdKey"))

    @entity_id_key.setter
    def entity_id_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d967e18f36ba6128aa80533f2f812a2037d463dcf11b19bdc475cc57cac95ec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityIdKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventPattern")
    def event_pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventPattern"))

    @event_pattern.setter
    def event_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e613abb008b5d1b33f7220e9ee512b68169ce8ce700ae65a3528dc01c79f8239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventPattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__902b8e6a1f9c037939afc31e662932828e7afe578ddcff42ec06a23eb28f7229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unitLabel")
    def unit_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unitLabel"))

    @unit_label.setter
    def unit_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530ed7d26de31d78681206654d685d8752eaeb2c01fac264dec22016a9a92784)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unitLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueKey")
    def value_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueKey"))

    @value_key.setter
    def value_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__941ed15958c1230bac537fc46dfbfdbe7ef204638d2c81017ac1eb01b82284b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EvidentlyLaunchMetricMonitorsMetricDefinition]:
        return typing.cast(typing.Optional[EvidentlyLaunchMetricMonitorsMetricDefinition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EvidentlyLaunchMetricMonitorsMetricDefinition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0e5682b590e8f1fb4c0a9a7e88b333f2d6901334fa337566c26872b84e4cad0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EvidentlyLaunchMetricMonitorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchMetricMonitorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d90abbfcb0f2e3b91af5aa1b6e17e33f280ee0b5ca01b0b5de50a28902c5dff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMetricDefinition")
    def put_metric_definition(
        self,
        *,
        entity_id_key: builtins.str,
        name: builtins.str,
        value_key: builtins.str,
        event_pattern: typing.Optional[builtins.str] = None,
        unit_label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param entity_id_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#entity_id_key EvidentlyLaunch#entity_id_key}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#name EvidentlyLaunch#name}.
        :param value_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#value_key EvidentlyLaunch#value_key}.
        :param event_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#event_pattern EvidentlyLaunch#event_pattern}.
        :param unit_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#unit_label EvidentlyLaunch#unit_label}.
        '''
        value = EvidentlyLaunchMetricMonitorsMetricDefinition(
            entity_id_key=entity_id_key,
            name=name,
            value_key=value_key,
            event_pattern=event_pattern,
            unit_label=unit_label,
        )

        return typing.cast(None, jsii.invoke(self, "putMetricDefinition", [value]))

    @builtins.property
    @jsii.member(jsii_name="metricDefinition")
    def metric_definition(
        self,
    ) -> EvidentlyLaunchMetricMonitorsMetricDefinitionOutputReference:
        return typing.cast(EvidentlyLaunchMetricMonitorsMetricDefinitionOutputReference, jsii.get(self, "metricDefinition"))

    @builtins.property
    @jsii.member(jsii_name="metricDefinitionInput")
    def metric_definition_input(
        self,
    ) -> typing.Optional[EvidentlyLaunchMetricMonitorsMetricDefinition]:
        return typing.cast(typing.Optional[EvidentlyLaunchMetricMonitorsMetricDefinition], jsii.get(self, "metricDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchMetricMonitors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchMetricMonitors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchMetricMonitors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f6daa23a8fd096ce945e62719616b265ffa3a69d3cea18a3dcdf56a472a06b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchScheduledSplitsConfig",
    jsii_struct_bases=[],
    name_mapping={"steps": "steps"},
)
class EvidentlyLaunchScheduledSplitsConfig:
    def __init__(
        self,
        *,
        steps: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EvidentlyLaunchScheduledSplitsConfigSteps", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param steps: steps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#steps EvidentlyLaunch#steps}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ea367d15190bf6d0df9ac61ff000c6b774a352f6e68dfac52192d935f98d57)
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "steps": steps,
        }

    @builtins.property
    def steps(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EvidentlyLaunchScheduledSplitsConfigSteps"]]:
        '''steps block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#steps EvidentlyLaunch#steps}
        '''
        result = self._values.get("steps")
        assert result is not None, "Required property 'steps' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EvidentlyLaunchScheduledSplitsConfigSteps"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EvidentlyLaunchScheduledSplitsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EvidentlyLaunchScheduledSplitsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchScheduledSplitsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91775c0488d6a84f1598a01f0d8a4918db5e57e0cc08f9c1361dc4653ee3d152)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSteps")
    def put_steps(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EvidentlyLaunchScheduledSplitsConfigSteps", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7783b15b73e2dad77b47f90b79e290f4960a615b006077af1baa2c5c74f91f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSteps", [value]))

    @builtins.property
    @jsii.member(jsii_name="steps")
    def steps(self) -> "EvidentlyLaunchScheduledSplitsConfigStepsList":
        return typing.cast("EvidentlyLaunchScheduledSplitsConfigStepsList", jsii.get(self, "steps"))

    @builtins.property
    @jsii.member(jsii_name="stepsInput")
    def steps_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EvidentlyLaunchScheduledSplitsConfigSteps"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EvidentlyLaunchScheduledSplitsConfigSteps"]]], jsii.get(self, "stepsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EvidentlyLaunchScheduledSplitsConfig]:
        return typing.cast(typing.Optional[EvidentlyLaunchScheduledSplitsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EvidentlyLaunchScheduledSplitsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec3d8e7b2906e305ef60ab616a6ce15cdabeff51c2e0611f9de86565e76b7b5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchScheduledSplitsConfigSteps",
    jsii_struct_bases=[],
    name_mapping={
        "group_weights": "groupWeights",
        "start_time": "startTime",
        "segment_overrides": "segmentOverrides",
    },
)
class EvidentlyLaunchScheduledSplitsConfigSteps:
    def __init__(
        self,
        *,
        group_weights: typing.Mapping[builtins.str, jsii.Number],
        start_time: builtins.str,
        segment_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param group_weights: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#group_weights EvidentlyLaunch#group_weights}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#start_time EvidentlyLaunch#start_time}.
        :param segment_overrides: segment_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#segment_overrides EvidentlyLaunch#segment_overrides}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1d802cfabaf16e03e38bfe35b09f5d64af19a7a24154f5ccd144a0f5419f76)
            check_type(argname="argument group_weights", value=group_weights, expected_type=type_hints["group_weights"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument segment_overrides", value=segment_overrides, expected_type=type_hints["segment_overrides"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_weights": group_weights,
            "start_time": start_time,
        }
        if segment_overrides is not None:
            self._values["segment_overrides"] = segment_overrides

    @builtins.property
    def group_weights(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#group_weights EvidentlyLaunch#group_weights}.'''
        result = self._values.get("group_weights")
        assert result is not None, "Required property 'group_weights' is missing"
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#start_time EvidentlyLaunch#start_time}.'''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def segment_overrides(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides"]]]:
        '''segment_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#segment_overrides EvidentlyLaunch#segment_overrides}
        '''
        result = self._values.get("segment_overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EvidentlyLaunchScheduledSplitsConfigSteps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EvidentlyLaunchScheduledSplitsConfigStepsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchScheduledSplitsConfigStepsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6487a87809d6eb9dd5816ae8a5e16e147bfb1667216cd0341b819e0c2969815e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EvidentlyLaunchScheduledSplitsConfigStepsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d816d83fd7a840f5b13b563a9dd505503514c56023d0ffa00bb47cb89656d46)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EvidentlyLaunchScheduledSplitsConfigStepsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b8de3a593307da377fb6b394561d9847400ab3df903949b60816cfcf625609a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea904bc77e35560b28411afce03daaa5f88d4ab6d342bd60850a4f9e14ee098d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f579af253d936715652f6f48f87218cc9a474928b9f9dc733419bd16eb139d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EvidentlyLaunchScheduledSplitsConfigSteps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EvidentlyLaunchScheduledSplitsConfigSteps]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EvidentlyLaunchScheduledSplitsConfigSteps]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f17b384e102cec59df404fa9dd0289002531879a8cbff9d19b3057e481bf42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EvidentlyLaunchScheduledSplitsConfigStepsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchScheduledSplitsConfigStepsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c04e073fec16b956f7cee18c2ba51a911d1d56cf80de67d8b8106217a29bb96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSegmentOverrides")
    def put_segment_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdefc864cda3c818b04175d54ed8caf0991cbe9a8ad6926cccb53d1f993a55f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSegmentOverrides", [value]))

    @jsii.member(jsii_name="resetSegmentOverrides")
    def reset_segment_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSegmentOverrides", []))

    @builtins.property
    @jsii.member(jsii_name="segmentOverrides")
    def segment_overrides(
        self,
    ) -> "EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverridesList":
        return typing.cast("EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverridesList", jsii.get(self, "segmentOverrides"))

    @builtins.property
    @jsii.member(jsii_name="groupWeightsInput")
    def group_weights_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, jsii.Number]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, jsii.Number]], jsii.get(self, "groupWeightsInput"))

    @builtins.property
    @jsii.member(jsii_name="segmentOverridesInput")
    def segment_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides"]]], jsii.get(self, "segmentOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="groupWeights")
    def group_weights(self) -> typing.Mapping[builtins.str, jsii.Number]:
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.get(self, "groupWeights"))

    @group_weights.setter
    def group_weights(self, value: typing.Mapping[builtins.str, jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d314a31fa3b54674c45be9f4472cdfa94e8d166d8e76efaea2e98cba5fa946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupWeights", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95996523889e632ec4681365e577c79be020ed1234882ff101c91becea5dec17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchScheduledSplitsConfigSteps]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchScheduledSplitsConfigSteps]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchScheduledSplitsConfigSteps]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d17c036692176bd266170f5cd94a3bd1f0d48d5fa0d5f71d4ccaa693a0f94e19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides",
    jsii_struct_bases=[],
    name_mapping={
        "evaluation_order": "evaluationOrder",
        "segment": "segment",
        "weights": "weights",
    },
)
class EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides:
    def __init__(
        self,
        *,
        evaluation_order: jsii.Number,
        segment: builtins.str,
        weights: typing.Mapping[builtins.str, jsii.Number],
    ) -> None:
        '''
        :param evaluation_order: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#evaluation_order EvidentlyLaunch#evaluation_order}.
        :param segment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#segment EvidentlyLaunch#segment}.
        :param weights: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#weights EvidentlyLaunch#weights}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f230fe7290f86f3597f8e24f220b7fbd16d6042bc8cc6edefa707166fd4b94b5)
            check_type(argname="argument evaluation_order", value=evaluation_order, expected_type=type_hints["evaluation_order"])
            check_type(argname="argument segment", value=segment, expected_type=type_hints["segment"])
            check_type(argname="argument weights", value=weights, expected_type=type_hints["weights"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "evaluation_order": evaluation_order,
            "segment": segment,
            "weights": weights,
        }

    @builtins.property
    def evaluation_order(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#evaluation_order EvidentlyLaunch#evaluation_order}.'''
        result = self._values.get("evaluation_order")
        assert result is not None, "Required property 'evaluation_order' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def segment(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#segment EvidentlyLaunch#segment}.'''
        result = self._values.get("segment")
        assert result is not None, "Required property 'segment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def weights(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#weights EvidentlyLaunch#weights}.'''
        result = self._values.get("weights")
        assert result is not None, "Required property 'weights' is missing"
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7fa2748993de5371a1b282c727b20cc31d5576ac4bb2887f292dc6c19225a16)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f06767f2aa54bb57fe1299183e6da42bae22e5f5edbf093544fea4c8f1315a1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42452fcbb5834f9ab0307d7a7affad16e33961e3182f1f69ae8148fad83f78f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__529b21ec49e5eea3f711bdccb2a52b4fce3ef59957f4f2b2bbc3d2885a3cb12c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccf63cd87460481e8010b9e4144a1ddf5350e8371f7618da60ffbb315872e9df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf9306dab7275b461ccad604615990b83d7da1aa73eeaed29a41a85cec97653)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7042c1b3bfce266150000d82558f023588a296beb3f16b5d83dbb1325d498225)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="evaluationOrderInput")
    def evaluation_order_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "evaluationOrderInput"))

    @builtins.property
    @jsii.member(jsii_name="segmentInput")
    def segment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "segmentInput"))

    @builtins.property
    @jsii.member(jsii_name="weightsInput")
    def weights_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, jsii.Number]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, jsii.Number]], jsii.get(self, "weightsInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluationOrder")
    def evaluation_order(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "evaluationOrder"))

    @evaluation_order.setter
    def evaluation_order(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e6e0218aa107188730e9f944a244f8d9251ff2aec421b622bf7b38570dec253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationOrder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="segment")
    def segment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "segment"))

    @segment.setter
    def segment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1078e7cd4bb60cdcfa4c453e484efc97dccfeb2d476cf0bd89149a6067a717a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weights")
    def weights(self) -> typing.Mapping[builtins.str, jsii.Number]:
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.get(self, "weights"))

    @weights.setter
    def weights(self, value: typing.Mapping[builtins.str, jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1cfd08bab8870b2ac0bafd546ad5e1a14ffad32bdcbace63024de7656ef5569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weights", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ae3b7cc0cda2831728b5ecb1921defda4c5ad01a546678fbaa84d610504b954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class EvidentlyLaunchTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#create EvidentlyLaunch#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#delete EvidentlyLaunch#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#update EvidentlyLaunch#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8781e1ea9b2783f4d252ccb5f9146620bca1f2d862ca594394a650a9a5fc3277)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#create EvidentlyLaunch#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#delete EvidentlyLaunch#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/evidently_launch#update EvidentlyLaunch#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EvidentlyLaunchTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EvidentlyLaunchTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.evidentlyLaunch.EvidentlyLaunchTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d19bc504f28de385e0f2c8f3217443b42fbd92689c4fc766a680ad4a2b5834e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c41bc871eca3b515faabcd33c3d4ee0a43615931ea61ae5703a5c6ae107d672a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06c0cd98b3a13e6c9699e66f235fe8d89ce51c830e5028410e160ee5d2b46c61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b05e47ece7001b4a4a0df71d3ab70c8a16db063388673761a36692ca33c5814f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af086c84d67e24834226ff05c538b784bf82f449fa04030cb221df25600b540f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EvidentlyLaunch",
    "EvidentlyLaunchConfig",
    "EvidentlyLaunchExecution",
    "EvidentlyLaunchExecutionList",
    "EvidentlyLaunchExecutionOutputReference",
    "EvidentlyLaunchGroups",
    "EvidentlyLaunchGroupsList",
    "EvidentlyLaunchGroupsOutputReference",
    "EvidentlyLaunchMetricMonitors",
    "EvidentlyLaunchMetricMonitorsList",
    "EvidentlyLaunchMetricMonitorsMetricDefinition",
    "EvidentlyLaunchMetricMonitorsMetricDefinitionOutputReference",
    "EvidentlyLaunchMetricMonitorsOutputReference",
    "EvidentlyLaunchScheduledSplitsConfig",
    "EvidentlyLaunchScheduledSplitsConfigOutputReference",
    "EvidentlyLaunchScheduledSplitsConfigSteps",
    "EvidentlyLaunchScheduledSplitsConfigStepsList",
    "EvidentlyLaunchScheduledSplitsConfigStepsOutputReference",
    "EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides",
    "EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverridesList",
    "EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverridesOutputReference",
    "EvidentlyLaunchTimeouts",
    "EvidentlyLaunchTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7585259ec71ac752032bb97374f37c091cdad4ac6e760c1aafb8249e441fb5d4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EvidentlyLaunchGroups, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    project: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    metric_monitors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EvidentlyLaunchMetricMonitors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    randomization_salt: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    scheduled_splits_config: typing.Optional[typing.Union[EvidentlyLaunchScheduledSplitsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[EvidentlyLaunchTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__23d71251d3702e8749892b711b09202dee4838001e49a3df0dde4c4a9bc6f162(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360b457c2009c3e93059cba904a028607964d5d14f9c169f413c281b3e15cd9f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EvidentlyLaunchGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a28c4c90034c7916080604cc7e24205c0fe6d68c7b56afc9b676d05a2aef34e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EvidentlyLaunchMetricMonitors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f455e164ca605858bc7e053913b5a91e7cad51aad6ab29e4a82c3f3da9fe082(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665c81134efa2b0579aaf9df084fb740c73d9dc5290a59d5ea78ead790589bac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56ea910a5f1c9dec5aef93747ce5e3b9224c04973a33e954c043ba53f886f2bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__370bd23b304152093b16fb5b809805f04187a8557ec6bfc3798183274957ebdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b352ccaad0ab2b8494352d4dd475108e82c496c8fbd9285de24ae04f1f6d90a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f66606608aa00a10ec602a900d8e81a24437342f0ab7d2ab86d2451489a66f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574e5157b7b490043490779e30234a983e9de44252fd26b29c2b9636851779f7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43d428e7e7823c6801e1b09e15742377ebdee477c4fc84a5c80c04f86ac52f6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7bd0424c475b1783bf96f94f9003591dd7bd1bf78c55cd170c314b6edbc504(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EvidentlyLaunchGroups, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    project: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    metric_monitors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EvidentlyLaunchMetricMonitors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    randomization_salt: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    scheduled_splits_config: typing.Optional[typing.Union[EvidentlyLaunchScheduledSplitsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[EvidentlyLaunchTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b27868861ded82d53865da0f8744d4fd9fdc2a7c4547c0c4c4a95fbe497d9d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76238fc8d3b68ac85a189a838fc1541541dca1b58c0e770543d99c1ae0697f86(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109c58ecbf8a5dd0eea5c5b48d3a5be7642de2173c7c453af4fd3ba64ae16a9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797d47c53aed7ccdf46dec0ad1830ea732bd2f33b78f22b3a37d69739a03c755(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4242991cc2c1bb9e87ed24848ca0b4987b11fa639be43fbf7a19d24e3a49b5ac(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5e038f57424f47b05e358a50320daa3a5f86d5083a09716908bf5b46446d07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74dec3bc2f27cace88b5bacad1ecf98292eb2742f5489c72a7d9a454ab1823b1(
    value: typing.Optional[EvidentlyLaunchExecution],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d0e86df276f47a2ff2cb5ade5bb6888214c3bb2e6219bad1852254080f9f8bd(
    *,
    feature: builtins.str,
    name: builtins.str,
    variation: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a169b8da5f5a6da4f81eb62618b3d7ecbd559a26505a62cbe7692ee9ce0c150(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c023cce2ea7e7129d18444ba4c25aa7e2fa7ac7c97890bbd8ec7b1d45e8dace9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7667a975fa0651a68255b8ce78d00f0441b7157247c6c06041a5322c2760124f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__476c718288df79c494bc8422490c28ac64de5e168fe1a0d78605cf20686b7f20(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c1831231397757e5ff7ddf26b9d5c3aaa930be3ae23de19cb58829d7d00988(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e18e60c9129d28acedc984372627bd3ab64e0481fd109b070e2494077212370(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EvidentlyLaunchGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7821b2f1c2af44f02b03a435aee18b85f8fcdce901b1c201d224625458f596f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0cfc3cff17e521f764c4aab63aaf9488c597767f73ca4af00ae2f85a74b380(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e892c86508cf04bdc8ca7916f5978319cc9246071ef8112d5a3de24753d75b90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9bcf31ec221aedcd86c84d5e0561aa3fcfbe5a7cf3bf48ffea7d8a6235e4b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f47556d3a59ada9e254c098b4ac2fec90c91749b93d9bbeb02faefa61e24242e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6592dd5cbb9cb647018c6862aecc14112fda361eebf308d2399aaf750f94f6a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3345eaab8f2f8451093bc2e20c44590d444ed3759b79274bca57eb064659f82a(
    *,
    metric_definition: typing.Union[EvidentlyLaunchMetricMonitorsMetricDefinition, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43570485a573d6d536bd18c588d2e458f4cad9db98658566a8b263699544d990(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c33b35ddee0b87982ef356cc4fb1a4d80d9162a2ed28512d62f273c0f630dd8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b1f866db5eadb976dfe08569932c194f2bb25cf904d0bfa49f74b1079bdd6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__275da59ee00c6d5cc79aa058c1fe0acd691e0af4ca02fed9605e21901d9e6683(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9246f94de3a7f1afa58d6d4f7ea72e19781b9ede88907919b3553d9331a53cd2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d29135c5152466a3798491ab728a4834fd88be36172bd6c3c4a9324c0a0c58(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EvidentlyLaunchMetricMonitors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69fd1b96a13d89f63a7d3087789b171dea71f2683c6c3f6a0c40d6249a3c1560(
    *,
    entity_id_key: builtins.str,
    name: builtins.str,
    value_key: builtins.str,
    event_pattern: typing.Optional[builtins.str] = None,
    unit_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bed9b7eb10a692c3cdda1bbb8684ed849639ec4f4a33fe571ca541d61bdd266(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d967e18f36ba6128aa80533f2f812a2037d463dcf11b19bdc475cc57cac95ec9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e613abb008b5d1b33f7220e9ee512b68169ce8ce700ae65a3528dc01c79f8239(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__902b8e6a1f9c037939afc31e662932828e7afe578ddcff42ec06a23eb28f7229(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530ed7d26de31d78681206654d685d8752eaeb2c01fac264dec22016a9a92784(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941ed15958c1230bac537fc46dfbfdbe7ef204638d2c81017ac1eb01b82284b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e5682b590e8f1fb4c0a9a7e88b333f2d6901334fa337566c26872b84e4cad0(
    value: typing.Optional[EvidentlyLaunchMetricMonitorsMetricDefinition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d90abbfcb0f2e3b91af5aa1b6e17e33f280ee0b5ca01b0b5de50a28902c5dff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6daa23a8fd096ce945e62719616b265ffa3a69d3cea18a3dcdf56a472a06b0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchMetricMonitors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ea367d15190bf6d0df9ac61ff000c6b774a352f6e68dfac52192d935f98d57(
    *,
    steps: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EvidentlyLaunchScheduledSplitsConfigSteps, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91775c0488d6a84f1598a01f0d8a4918db5e57e0cc08f9c1361dc4653ee3d152(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7783b15b73e2dad77b47f90b79e290f4960a615b006077af1baa2c5c74f91f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EvidentlyLaunchScheduledSplitsConfigSteps, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec3d8e7b2906e305ef60ab616a6ce15cdabeff51c2e0611f9de86565e76b7b5e(
    value: typing.Optional[EvidentlyLaunchScheduledSplitsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1d802cfabaf16e03e38bfe35b09f5d64af19a7a24154f5ccd144a0f5419f76(
    *,
    group_weights: typing.Mapping[builtins.str, jsii.Number],
    start_time: builtins.str,
    segment_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6487a87809d6eb9dd5816ae8a5e16e147bfb1667216cd0341b819e0c2969815e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d816d83fd7a840f5b13b563a9dd505503514c56023d0ffa00bb47cb89656d46(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b8de3a593307da377fb6b394561d9847400ab3df903949b60816cfcf625609a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea904bc77e35560b28411afce03daaa5f88d4ab6d342bd60850a4f9e14ee098d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f579af253d936715652f6f48f87218cc9a474928b9f9dc733419bd16eb139d8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f17b384e102cec59df404fa9dd0289002531879a8cbff9d19b3057e481bf42(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EvidentlyLaunchScheduledSplitsConfigSteps]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c04e073fec16b956f7cee18c2ba51a911d1d56cf80de67d8b8106217a29bb96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdefc864cda3c818b04175d54ed8caf0991cbe9a8ad6926cccb53d1f993a55f6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d314a31fa3b54674c45be9f4472cdfa94e8d166d8e76efaea2e98cba5fa946(
    value: typing.Mapping[builtins.str, jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95996523889e632ec4681365e577c79be020ed1234882ff101c91becea5dec17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17c036692176bd266170f5cd94a3bd1f0d48d5fa0d5f71d4ccaa693a0f94e19(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchScheduledSplitsConfigSteps]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f230fe7290f86f3597f8e24f220b7fbd16d6042bc8cc6edefa707166fd4b94b5(
    *,
    evaluation_order: jsii.Number,
    segment: builtins.str,
    weights: typing.Mapping[builtins.str, jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7fa2748993de5371a1b282c727b20cc31d5576ac4bb2887f292dc6c19225a16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f06767f2aa54bb57fe1299183e6da42bae22e5f5edbf093544fea4c8f1315a1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42452fcbb5834f9ab0307d7a7affad16e33961e3182f1f69ae8148fad83f78f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__529b21ec49e5eea3f711bdccb2a52b4fce3ef59957f4f2b2bbc3d2885a3cb12c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf63cd87460481e8010b9e4144a1ddf5350e8371f7618da60ffbb315872e9df(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf9306dab7275b461ccad604615990b83d7da1aa73eeaed29a41a85cec97653(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7042c1b3bfce266150000d82558f023588a296beb3f16b5d83dbb1325d498225(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e6e0218aa107188730e9f944a244f8d9251ff2aec421b622bf7b38570dec253(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1078e7cd4bb60cdcfa4c453e484efc97dccfeb2d476cf0bd89149a6067a717a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1cfd08bab8870b2ac0bafd546ad5e1a14ffad32bdcbace63024de7656ef5569(
    value: typing.Mapping[builtins.str, jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae3b7cc0cda2831728b5ecb1921defda4c5ad01a546678fbaa84d610504b954(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchScheduledSplitsConfigStepsSegmentOverrides]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8781e1ea9b2783f4d252ccb5f9146620bca1f2d862ca594394a650a9a5fc3277(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19bc504f28de385e0f2c8f3217443b42fbd92689c4fc766a680ad4a2b5834e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c41bc871eca3b515faabcd33c3d4ee0a43615931ea61ae5703a5c6ae107d672a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06c0cd98b3a13e6c9699e66f235fe8d89ce51c830e5028410e160ee5d2b46c61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b05e47ece7001b4a4a0df71d3ab70c8a16db063388673761a36692ca33c5814f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af086c84d67e24834226ff05c538b784bf82f449fa04030cb221df25600b540f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EvidentlyLaunchTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
