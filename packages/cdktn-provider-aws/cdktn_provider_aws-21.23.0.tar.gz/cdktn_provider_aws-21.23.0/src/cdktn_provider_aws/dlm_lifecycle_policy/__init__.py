r'''
# `aws_dlm_lifecycle_policy`

Refer to the Terraform Registry for docs: [`aws_dlm_lifecycle_policy`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy).
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


class DlmLifecyclePolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy aws_dlm_lifecycle_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        description: builtins.str,
        execution_role_arn: builtins.str,
        policy_details: typing.Union["DlmLifecyclePolicyPolicyDetails", typing.Dict[builtins.str, typing.Any]],
        default_policy: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy aws_dlm_lifecycle_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#description DlmLifecyclePolicy#description}.
        :param execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#execution_role_arn DlmLifecyclePolicy#execution_role_arn}.
        :param policy_details: policy_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#policy_details DlmLifecyclePolicy#policy_details}
        :param default_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#default_policy DlmLifecyclePolicy#default_policy}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#id DlmLifecyclePolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#region DlmLifecyclePolicy#region}
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#state DlmLifecyclePolicy#state}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#tags DlmLifecyclePolicy#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#tags_all DlmLifecyclePolicy#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d69f68b8aa75af137750b30d5221f328af68ac1b07e4988a3c2594b206b92fd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DlmLifecyclePolicyConfig(
            description=description,
            execution_role_arn=execution_role_arn,
            policy_details=policy_details,
            default_policy=default_policy,
            id=id,
            region=region,
            state=state,
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
        '''Generates CDKTF code for importing a DlmLifecyclePolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DlmLifecyclePolicy to import.
        :param import_from_id: The id of the existing DlmLifecyclePolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DlmLifecyclePolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38685a4e800351ca2909b4324aaa6110638b7cb4f43ea16d400dd551234189b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putPolicyDetails")
    def put_policy_details(
        self,
        *,
        action: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsAction", typing.Dict[builtins.str, typing.Any]]] = None,
        copy_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_interval: typing.Optional[jsii.Number] = None,
        event_source: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsEventSource", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusions: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsExclusions", typing.Dict[builtins.str, typing.Any]]] = None,
        extend_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        parameters: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_language: typing.Optional[builtins.str] = None,
        policy_type: typing.Optional[builtins.str] = None,
        resource_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_type: typing.Optional[builtins.str] = None,
        resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        retain_interval: typing.Optional[jsii.Number] = None,
        schedule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DlmLifecyclePolicyPolicyDetailsSchedule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#action DlmLifecyclePolicy#action}
        :param copy_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#copy_tags DlmLifecyclePolicy#copy_tags}.
        :param create_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#create_interval DlmLifecyclePolicy#create_interval}.
        :param event_source: event_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#event_source DlmLifecyclePolicy#event_source}
        :param exclusions: exclusions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#exclusions DlmLifecyclePolicy#exclusions}
        :param extend_deletion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#extend_deletion DlmLifecyclePolicy#extend_deletion}.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#parameters DlmLifecyclePolicy#parameters}
        :param policy_language: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#policy_language DlmLifecyclePolicy#policy_language}.
        :param policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#policy_type DlmLifecyclePolicy#policy_type}.
        :param resource_locations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#resource_locations DlmLifecyclePolicy#resource_locations}.
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#resource_type DlmLifecyclePolicy#resource_type}.
        :param resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#resource_types DlmLifecyclePolicy#resource_types}.
        :param retain_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#retain_interval DlmLifecyclePolicy#retain_interval}.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#schedule DlmLifecyclePolicy#schedule}
        :param target_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#target_tags DlmLifecyclePolicy#target_tags}.
        '''
        value = DlmLifecyclePolicyPolicyDetails(
            action=action,
            copy_tags=copy_tags,
            create_interval=create_interval,
            event_source=event_source,
            exclusions=exclusions,
            extend_deletion=extend_deletion,
            parameters=parameters,
            policy_language=policy_language,
            policy_type=policy_type,
            resource_locations=resource_locations,
            resource_type=resource_type,
            resource_types=resource_types,
            retain_interval=retain_interval,
            schedule=schedule,
            target_tags=target_tags,
        )

        return typing.cast(None, jsii.invoke(self, "putPolicyDetails", [value]))

    @jsii.member(jsii_name="resetDefaultPolicy")
    def reset_default_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultPolicy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

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
    @jsii.member(jsii_name="policyDetails")
    def policy_details(self) -> "DlmLifecyclePolicyPolicyDetailsOutputReference":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsOutputReference", jsii.get(self, "policyDetails"))

    @builtins.property
    @jsii.member(jsii_name="defaultPolicyInput")
    def default_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleArnInput")
    def execution_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="policyDetailsInput")
    def policy_details_input(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetails"]:
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetails"], jsii.get(self, "policyDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

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
    @jsii.member(jsii_name="defaultPolicy")
    def default_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultPolicy"))

    @default_policy.setter
    def default_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fbffc7d1c2125d8bf0d00d05b3652c91177717706d975000a1bcc9cb7209eb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bc1475b4cdafd057b5dcaf493e982d95d236c079b1bd42dce5d39eae8eddeab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRoleArn"))

    @execution_role_arn.setter
    def execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f9a927808e4d610d6a67e12f9ab9b1c394dd949506c0b5024129b67d49866f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6f2af90e344bfb2b7625bddc30430e61b850cff8b7ef786eb016a46d1341e4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183dc8677c22067bd93e98b0aeb308d865eac54a26f97bfd26313e3645c6bb6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8890f6793724f7b25b9e57a659019322b668eca6d27db32a42e0dcb6357f536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e3260b8983fa1403c04fcdaf84f15dce954d46abc45cbb89668ca357a66d7bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b024e3b90ff3c1d69c10c381ea3ea7b4d4867c1882435db717d35c571dbdf489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyConfig",
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
        "execution_role_arn": "executionRoleArn",
        "policy_details": "policyDetails",
        "default_policy": "defaultPolicy",
        "id": "id",
        "region": "region",
        "state": "state",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class DlmLifecyclePolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        execution_role_arn: builtins.str,
        policy_details: typing.Union["DlmLifecyclePolicyPolicyDetails", typing.Dict[builtins.str, typing.Any]],
        default_policy: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
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
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#description DlmLifecyclePolicy#description}.
        :param execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#execution_role_arn DlmLifecyclePolicy#execution_role_arn}.
        :param policy_details: policy_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#policy_details DlmLifecyclePolicy#policy_details}
        :param default_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#default_policy DlmLifecyclePolicy#default_policy}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#id DlmLifecyclePolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#region DlmLifecyclePolicy#region}
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#state DlmLifecyclePolicy#state}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#tags DlmLifecyclePolicy#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#tags_all DlmLifecyclePolicy#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(policy_details, dict):
            policy_details = DlmLifecyclePolicyPolicyDetails(**policy_details)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1ddb319fd3cfe27fa82e9b292ce077d8c37ffec3331e9c76521ce54d1e53b46)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument policy_details", value=policy_details, expected_type=type_hints["policy_details"])
            check_type(argname="argument default_policy", value=default_policy, expected_type=type_hints["default_policy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "execution_role_arn": execution_role_arn,
            "policy_details": policy_details,
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
        if default_policy is not None:
            self._values["default_policy"] = default_policy
        if id is not None:
            self._values["id"] = id
        if region is not None:
            self._values["region"] = region
        if state is not None:
            self._values["state"] = state
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
    def description(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#description DlmLifecyclePolicy#description}.'''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def execution_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#execution_role_arn DlmLifecyclePolicy#execution_role_arn}.'''
        result = self._values.get("execution_role_arn")
        assert result is not None, "Required property 'execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_details(self) -> "DlmLifecyclePolicyPolicyDetails":
        '''policy_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#policy_details DlmLifecyclePolicy#policy_details}
        '''
        result = self._values.get("policy_details")
        assert result is not None, "Required property 'policy_details' is missing"
        return typing.cast("DlmLifecyclePolicyPolicyDetails", result)

    @builtins.property
    def default_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#default_policy DlmLifecyclePolicy#default_policy}.'''
        result = self._values.get("default_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#id DlmLifecyclePolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#region DlmLifecyclePolicy#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#state DlmLifecyclePolicy#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#tags DlmLifecyclePolicy#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#tags_all DlmLifecyclePolicy#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetails",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "copy_tags": "copyTags",
        "create_interval": "createInterval",
        "event_source": "eventSource",
        "exclusions": "exclusions",
        "extend_deletion": "extendDeletion",
        "parameters": "parameters",
        "policy_language": "policyLanguage",
        "policy_type": "policyType",
        "resource_locations": "resourceLocations",
        "resource_type": "resourceType",
        "resource_types": "resourceTypes",
        "retain_interval": "retainInterval",
        "schedule": "schedule",
        "target_tags": "targetTags",
    },
)
class DlmLifecyclePolicyPolicyDetails:
    def __init__(
        self,
        *,
        action: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsAction", typing.Dict[builtins.str, typing.Any]]] = None,
        copy_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_interval: typing.Optional[jsii.Number] = None,
        event_source: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsEventSource", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusions: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsExclusions", typing.Dict[builtins.str, typing.Any]]] = None,
        extend_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        parameters: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_language: typing.Optional[builtins.str] = None,
        policy_type: typing.Optional[builtins.str] = None,
        resource_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_type: typing.Optional[builtins.str] = None,
        resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        retain_interval: typing.Optional[jsii.Number] = None,
        schedule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DlmLifecyclePolicyPolicyDetailsSchedule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#action DlmLifecyclePolicy#action}
        :param copy_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#copy_tags DlmLifecyclePolicy#copy_tags}.
        :param create_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#create_interval DlmLifecyclePolicy#create_interval}.
        :param event_source: event_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#event_source DlmLifecyclePolicy#event_source}
        :param exclusions: exclusions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#exclusions DlmLifecyclePolicy#exclusions}
        :param extend_deletion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#extend_deletion DlmLifecyclePolicy#extend_deletion}.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#parameters DlmLifecyclePolicy#parameters}
        :param policy_language: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#policy_language DlmLifecyclePolicy#policy_language}.
        :param policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#policy_type DlmLifecyclePolicy#policy_type}.
        :param resource_locations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#resource_locations DlmLifecyclePolicy#resource_locations}.
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#resource_type DlmLifecyclePolicy#resource_type}.
        :param resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#resource_types DlmLifecyclePolicy#resource_types}.
        :param retain_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#retain_interval DlmLifecyclePolicy#retain_interval}.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#schedule DlmLifecyclePolicy#schedule}
        :param target_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#target_tags DlmLifecyclePolicy#target_tags}.
        '''
        if isinstance(action, dict):
            action = DlmLifecyclePolicyPolicyDetailsAction(**action)
        if isinstance(event_source, dict):
            event_source = DlmLifecyclePolicyPolicyDetailsEventSource(**event_source)
        if isinstance(exclusions, dict):
            exclusions = DlmLifecyclePolicyPolicyDetailsExclusions(**exclusions)
        if isinstance(parameters, dict):
            parameters = DlmLifecyclePolicyPolicyDetailsParameters(**parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e330e7cdd1885889e82af8a2a9f5024bc6d82c73a6dba43fbd54215367c3e54)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument copy_tags", value=copy_tags, expected_type=type_hints["copy_tags"])
            check_type(argname="argument create_interval", value=create_interval, expected_type=type_hints["create_interval"])
            check_type(argname="argument event_source", value=event_source, expected_type=type_hints["event_source"])
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
            check_type(argname="argument extend_deletion", value=extend_deletion, expected_type=type_hints["extend_deletion"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument policy_language", value=policy_language, expected_type=type_hints["policy_language"])
            check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
            check_type(argname="argument resource_locations", value=resource_locations, expected_type=type_hints["resource_locations"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
            check_type(argname="argument retain_interval", value=retain_interval, expected_type=type_hints["retain_interval"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument target_tags", value=target_tags, expected_type=type_hints["target_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if copy_tags is not None:
            self._values["copy_tags"] = copy_tags
        if create_interval is not None:
            self._values["create_interval"] = create_interval
        if event_source is not None:
            self._values["event_source"] = event_source
        if exclusions is not None:
            self._values["exclusions"] = exclusions
        if extend_deletion is not None:
            self._values["extend_deletion"] = extend_deletion
        if parameters is not None:
            self._values["parameters"] = parameters
        if policy_language is not None:
            self._values["policy_language"] = policy_language
        if policy_type is not None:
            self._values["policy_type"] = policy_type
        if resource_locations is not None:
            self._values["resource_locations"] = resource_locations
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if resource_types is not None:
            self._values["resource_types"] = resource_types
        if retain_interval is not None:
            self._values["retain_interval"] = retain_interval
        if schedule is not None:
            self._values["schedule"] = schedule
        if target_tags is not None:
            self._values["target_tags"] = target_tags

    @builtins.property
    def action(self) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsAction"]:
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#action DlmLifecyclePolicy#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsAction"], result)

    @builtins.property
    def copy_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#copy_tags DlmLifecyclePolicy#copy_tags}.'''
        result = self._values.get("copy_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def create_interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#create_interval DlmLifecyclePolicy#create_interval}.'''
        result = self._values.get("create_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def event_source(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsEventSource"]:
        '''event_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#event_source DlmLifecyclePolicy#event_source}
        '''
        result = self._values.get("event_source")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsEventSource"], result)

    @builtins.property
    def exclusions(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsExclusions"]:
        '''exclusions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#exclusions DlmLifecyclePolicy#exclusions}
        '''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsExclusions"], result)

    @builtins.property
    def extend_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#extend_deletion DlmLifecyclePolicy#extend_deletion}.'''
        result = self._values.get("extend_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsParameters"]:
        '''parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#parameters DlmLifecyclePolicy#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsParameters"], result)

    @builtins.property
    def policy_language(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#policy_language DlmLifecyclePolicy#policy_language}.'''
        result = self._values.get("policy_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#policy_type DlmLifecyclePolicy#policy_type}.'''
        result = self._values.get("policy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#resource_locations DlmLifecyclePolicy#resource_locations}.'''
        result = self._values.get("resource_locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#resource_type DlmLifecyclePolicy#resource_type}.'''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#resource_types DlmLifecyclePolicy#resource_types}.'''
        result = self._values.get("resource_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def retain_interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#retain_interval DlmLifecyclePolicy#retain_interval}.'''
        result = self._values.get("retain_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DlmLifecyclePolicyPolicyDetailsSchedule"]]]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#schedule DlmLifecyclePolicy#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DlmLifecyclePolicyPolicyDetailsSchedule"]]], result)

    @builtins.property
    def target_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#target_tags DlmLifecyclePolicy#target_tags}.'''
        result = self._values.get("target_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsAction",
    jsii_struct_bases=[],
    name_mapping={"cross_region_copy": "crossRegionCopy", "name": "name"},
)
class DlmLifecyclePolicyPolicyDetailsAction:
    def __init__(
        self,
        *,
        cross_region_copy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
    ) -> None:
        '''
        :param cross_region_copy: cross_region_copy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#cross_region_copy DlmLifecyclePolicy#cross_region_copy}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#name DlmLifecyclePolicy#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__178d2ead47d60e56af30458cb553062298eb2891203c12bae99a9b00282a466c)
            check_type(argname="argument cross_region_copy", value=cross_region_copy, expected_type=type_hints["cross_region_copy"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cross_region_copy": cross_region_copy,
            "name": name,
        }

    @builtins.property
    def cross_region_copy(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy"]]:
        '''cross_region_copy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#cross_region_copy DlmLifecyclePolicy#cross_region_copy}
        '''
        result = self._values.get("cross_region_copy")
        assert result is not None, "Required property 'cross_region_copy' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#name DlmLifecyclePolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_configuration": "encryptionConfiguration",
        "target": "target",
        "retain_rule": "retainRule",
    },
)
class DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy:
    def __init__(
        self,
        *,
        encryption_configuration: typing.Union["DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]],
        target: builtins.str,
        retain_rule: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param encryption_configuration: encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#encryption_configuration DlmLifecyclePolicy#encryption_configuration}
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#target DlmLifecyclePolicy#target}.
        :param retain_rule: retain_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#retain_rule DlmLifecyclePolicy#retain_rule}
        '''
        if isinstance(encryption_configuration, dict):
            encryption_configuration = DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration(**encryption_configuration)
        if isinstance(retain_rule, dict):
            retain_rule = DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule(**retain_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4f39785a1790e58a6106b3cb8153288e0d540c9950707c650fe457572711589)
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument retain_rule", value=retain_rule, expected_type=type_hints["retain_rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "encryption_configuration": encryption_configuration,
            "target": target,
        }
        if retain_rule is not None:
            self._values["retain_rule"] = retain_rule

    @builtins.property
    def encryption_configuration(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration":
        '''encryption_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#encryption_configuration DlmLifecyclePolicy#encryption_configuration}
        '''
        result = self._values.get("encryption_configuration")
        assert result is not None, "Required property 'encryption_configuration' is missing"
        return typing.cast("DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration", result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#target DlmLifecyclePolicy#target}.'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retain_rule(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule"]:
        '''retain_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#retain_rule DlmLifecyclePolicy#retain_rule}
        '''
        result = self._values.get("retain_rule")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"cmk_arn": "cmkArn", "encrypted": "encrypted"},
)
class DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration:
    def __init__(
        self,
        *,
        cmk_arn: typing.Optional[builtins.str] = None,
        encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cmk_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#cmk_arn DlmLifecyclePolicy#cmk_arn}.
        :param encrypted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#encrypted DlmLifecyclePolicy#encrypted}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc6770e572c11f7469dbb859326afef89e28a972738906d673e7c22738f3bb6c)
            check_type(argname="argument cmk_arn", value=cmk_arn, expected_type=type_hints["cmk_arn"])
            check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cmk_arn is not None:
            self._values["cmk_arn"] = cmk_arn
        if encrypted is not None:
            self._values["encrypted"] = encrypted

    @builtins.property
    def cmk_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#cmk_arn DlmLifecyclePolicy#cmk_arn}.'''
        result = self._values.get("cmk_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#encrypted DlmLifecyclePolicy#encrypted}.'''
        result = self._values.get("encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53608064370bb39a1227e45c6b089bcde5d97d80a3c692680ce4a52ec6766ec8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCmkArn")
    def reset_cmk_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCmkArn", []))

    @jsii.member(jsii_name="resetEncrypted")
    def reset_encrypted(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncrypted", []))

    @builtins.property
    @jsii.member(jsii_name="cmkArnInput")
    def cmk_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cmkArnInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptedInput")
    def encrypted_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptedInput"))

    @builtins.property
    @jsii.member(jsii_name="cmkArn")
    def cmk_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cmkArn"))

    @cmk_arn.setter
    def cmk_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a7ef27d6dec57430a35f4468f5692594fe1a8232244dabdb202be00a624670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cmkArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encrypted")
    def encrypted(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encrypted"))

    @encrypted.setter
    def encrypted(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__311e8fb35152696cf11d19529fe48ff55415ec80efbb100896e712dc6227d55b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encrypted", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70974fcb1c1620c665c368c153c574af1c08a871207340c79b08f319ca0005c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__646e4bb20f519776c347c66fbf0e1dff0fda3bdadb42da8e9b849c3d367f76f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be020bec07783a085abf336e66c01ad9d8d47137e7ae18a5756d8fcdd182c65)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebf75f7e6881f425e9c1ee464677b965a4971d1da7f16d2576bf2d5806efa778)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0376fa006d8e22a1c3d30d293526d2be545e55450b70ac45892df01f2e2f276e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24e397e5369f01567baed64452a67ba7080f3aabe054b234b6658933a8d99e50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc591f9b5d9c6d9bb149ed13148f19ad0cf868231ad3fb543ce67bff9d9e64d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a37d05e9b03cdda86693d6a93cf5da253c2aa4e4f3c7be2b6a0c44f892cc86fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEncryptionConfiguration")
    def put_encryption_configuration(
        self,
        *,
        cmk_arn: typing.Optional[builtins.str] = None,
        encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cmk_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#cmk_arn DlmLifecyclePolicy#cmk_arn}.
        :param encrypted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#encrypted DlmLifecyclePolicy#encrypted}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration(
            cmk_arn=cmk_arn, encrypted=encrypted
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfiguration", [value]))

    @jsii.member(jsii_name="putRetainRule")
    def put_retain_rule(
        self,
        *,
        interval: jsii.Number,
        interval_unit: builtins.str,
    ) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule(
            interval=interval, interval_unit=interval_unit
        )

        return typing.cast(None, jsii.invoke(self, "putRetainRule", [value]))

    @jsii.member(jsii_name="resetRetainRule")
    def reset_retain_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetainRule", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfiguration")
    def encryption_configuration(
        self,
    ) -> DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfigurationOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfigurationOutputReference, jsii.get(self, "encryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="retainRule")
    def retain_rule(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRuleOutputReference":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRuleOutputReference", jsii.get(self, "retainRule"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigurationInput")
    def encryption_configuration_input(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration], jsii.get(self, "encryptionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="retainRuleInput")
    def retain_rule_input(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule"]:
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule"], jsii.get(self, "retainRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__959d9904d24c1225522b3db91630233518cea8327e3b03e1b71e4464f7eea468)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b86ba4cc95ec44653f97518b1e7e4ad5d9c3f980af8583bf77ead5b46e5bdc7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule",
    jsii_struct_bases=[],
    name_mapping={"interval": "interval", "interval_unit": "intervalUnit"},
)
class DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule:
    def __init__(self, *, interval: jsii.Number, interval_unit: builtins.str) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46bc3eec9d2dbcdfd4ef268c6dcc7a2264b1d12fb4b25127bd16ba9b29ce660d)
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interval": interval,
            "interval_unit": interval_unit,
        }

    @builtins.property
    def interval(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.'''
        result = self._values.get("interval")
        assert result is not None, "Required property 'interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def interval_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.'''
        result = self._values.get("interval_unit")
        assert result is not None, "Required property 'interval_unit' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6691e6a1884aa8edc3f4bf09fa951410efb894fa445286f0a1fde67a761c81b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalUnitInput")
    def interval_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d470fa773f91d52688e65112ebb43c8c3ecedef6b85248a52779ae65280f8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalUnit")
    def interval_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intervalUnit"))

    @interval_unit.setter
    def interval_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f0373d586561e3d53fef37a1a0a56b72a94d0bb014e1d61efb2afa4a7cbce0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9b8da59b9edf7d7b2e0f9c0a17b95df4d09ea47277e7c39a0a1539fd4976ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DlmLifecyclePolicyPolicyDetailsActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26cc2be8bc5401517394b6ebebfe3a98ea3a4cae1ba4d3e03bcf868521d31858)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCrossRegionCopy")
    def put_cross_region_copy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68a0adf6170cb26ed585d6802166627cb046dc8ad73dc9f744665f671b27003f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCrossRegionCopy", [value]))

    @builtins.property
    @jsii.member(jsii_name="crossRegionCopy")
    def cross_region_copy(
        self,
    ) -> DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyList:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyList, jsii.get(self, "crossRegionCopy"))

    @builtins.property
    @jsii.member(jsii_name="crossRegionCopyInput")
    def cross_region_copy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]]], jsii.get(self, "crossRegionCopyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1bbcacc3a59e50a825c3053e357819e2cb36dc9129acb64572b13d388dcdc8e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsAction]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25d6653c0d9960da52f589818f4dc2cdfdac90e0b78d48e1f8faff2b2e25c650)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsEventSource",
    jsii_struct_bases=[],
    name_mapping={"parameters": "parameters", "type": "type"},
)
class DlmLifecyclePolicyPolicyDetailsEventSource:
    def __init__(
        self,
        *,
        parameters: typing.Union["DlmLifecyclePolicyPolicyDetailsEventSourceParameters", typing.Dict[builtins.str, typing.Any]],
        type: builtins.str,
    ) -> None:
        '''
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#parameters DlmLifecyclePolicy#parameters}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#type DlmLifecyclePolicy#type}.
        '''
        if isinstance(parameters, dict):
            parameters = DlmLifecyclePolicyPolicyDetailsEventSourceParameters(**parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31eac7e36bf0ea3da6f8a49bba37c0a3a43b653cc057890fd5b22523eea586c0)
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parameters": parameters,
            "type": type,
        }

    @builtins.property
    def parameters(self) -> "DlmLifecyclePolicyPolicyDetailsEventSourceParameters":
        '''parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#parameters DlmLifecyclePolicy#parameters}
        '''
        result = self._values.get("parameters")
        assert result is not None, "Required property 'parameters' is missing"
        return typing.cast("DlmLifecyclePolicyPolicyDetailsEventSourceParameters", result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#type DlmLifecyclePolicy#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsEventSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsEventSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsEventSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4694be197b24a4dd120a338f97c722f1873635327f8e0851c0e3b13b05ee2c0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        *,
        description_regex: builtins.str,
        event_type: builtins.str,
        snapshot_owner: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param description_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#description_regex DlmLifecyclePolicy#description_regex}.
        :param event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#event_type DlmLifecyclePolicy#event_type}.
        :param snapshot_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#snapshot_owner DlmLifecyclePolicy#snapshot_owner}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsEventSourceParameters(
            description_regex=description_regex,
            event_type=event_type,
            snapshot_owner=snapshot_owner,
        )

        return typing.cast(None, jsii.invoke(self, "putParameters", [value]))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsEventSourceParametersOutputReference":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsEventSourceParametersOutputReference", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsEventSourceParameters"]:
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsEventSourceParameters"], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1757da63315f4a9b5c97dd910a77240e4f7af4e27b9d42f090433fe890754e10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSource]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__597557d0d40b0635bb675ab882a92b80aa2134985123321c1e77d35aa94391a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsEventSourceParameters",
    jsii_struct_bases=[],
    name_mapping={
        "description_regex": "descriptionRegex",
        "event_type": "eventType",
        "snapshot_owner": "snapshotOwner",
    },
)
class DlmLifecyclePolicyPolicyDetailsEventSourceParameters:
    def __init__(
        self,
        *,
        description_regex: builtins.str,
        event_type: builtins.str,
        snapshot_owner: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param description_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#description_regex DlmLifecyclePolicy#description_regex}.
        :param event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#event_type DlmLifecyclePolicy#event_type}.
        :param snapshot_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#snapshot_owner DlmLifecyclePolicy#snapshot_owner}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d9f7731e7dd60de7041643b3d42681d6c9452831207828507df5de6b696c408)
            check_type(argname="argument description_regex", value=description_regex, expected_type=type_hints["description_regex"])
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument snapshot_owner", value=snapshot_owner, expected_type=type_hints["snapshot_owner"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description_regex": description_regex,
            "event_type": event_type,
            "snapshot_owner": snapshot_owner,
        }

    @builtins.property
    def description_regex(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#description_regex DlmLifecyclePolicy#description_regex}.'''
        result = self._values.get("description_regex")
        assert result is not None, "Required property 'description_regex' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#event_type DlmLifecyclePolicy#event_type}.'''
        result = self._values.get("event_type")
        assert result is not None, "Required property 'event_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def snapshot_owner(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#snapshot_owner DlmLifecyclePolicy#snapshot_owner}.'''
        result = self._values.get("snapshot_owner")
        assert result is not None, "Required property 'snapshot_owner' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsEventSourceParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsEventSourceParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsEventSourceParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcb5136646d2ef2a4e4f6ae6a25f21b9c9d046491521fac4aff3718da40e968e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="descriptionRegexInput")
    def description_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="eventTypeInput")
    def event_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotOwnerInput")
    def snapshot_owner_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "snapshotOwnerInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionRegex")
    def description_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "descriptionRegex"))

    @description_regex.setter
    def description_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80cd553d7f2d59d98b5d246f7cb480b09020dcdd78a7fb271e1a88f47189dc5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "descriptionRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventType")
    def event_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventType"))

    @event_type.setter
    def event_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__945551cf93e0265ebc5e56e32e1239b9db4059b09db274a8d8cf74b42c11579a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotOwner")
    def snapshot_owner(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "snapshotOwner"))

    @snapshot_owner.setter
    def snapshot_owner(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__589d59a72ea9ca5e64242b5f9b7f66462e4d1720628b9155f7f5f3240f800cee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotOwner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSourceParameters]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSourceParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSourceParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82fc70b5ae17bf2aa19e932b33aa3cf4890ff1f45fa60fd19d12174f1b58b0e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsExclusions",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_boot_volumes": "excludeBootVolumes",
        "exclude_tags": "excludeTags",
        "exclude_volume_types": "excludeVolumeTypes",
    },
)
class DlmLifecyclePolicyPolicyDetailsExclusions:
    def __init__(
        self,
        *,
        exclude_boot_volumes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        exclude_volume_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param exclude_boot_volumes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#exclude_boot_volumes DlmLifecyclePolicy#exclude_boot_volumes}.
        :param exclude_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#exclude_tags DlmLifecyclePolicy#exclude_tags}.
        :param exclude_volume_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#exclude_volume_types DlmLifecyclePolicy#exclude_volume_types}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__675c3fb0c0e25d4ea7405436aa28df543db641f7796f1408469422471de99065)
            check_type(argname="argument exclude_boot_volumes", value=exclude_boot_volumes, expected_type=type_hints["exclude_boot_volumes"])
            check_type(argname="argument exclude_tags", value=exclude_tags, expected_type=type_hints["exclude_tags"])
            check_type(argname="argument exclude_volume_types", value=exclude_volume_types, expected_type=type_hints["exclude_volume_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_boot_volumes is not None:
            self._values["exclude_boot_volumes"] = exclude_boot_volumes
        if exclude_tags is not None:
            self._values["exclude_tags"] = exclude_tags
        if exclude_volume_types is not None:
            self._values["exclude_volume_types"] = exclude_volume_types

    @builtins.property
    def exclude_boot_volumes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#exclude_boot_volumes DlmLifecyclePolicy#exclude_boot_volumes}.'''
        result = self._values.get("exclude_boot_volumes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exclude_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#exclude_tags DlmLifecyclePolicy#exclude_tags}.'''
        result = self._values.get("exclude_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def exclude_volume_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#exclude_volume_types DlmLifecyclePolicy#exclude_volume_types}.'''
        result = self._values.get("exclude_volume_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsExclusions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsExclusionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsExclusionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2ae5127b182766b5619aff835805fca2ee43cf0b40425258e5fe47a795848f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludeBootVolumes")
    def reset_exclude_boot_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeBootVolumes", []))

    @jsii.member(jsii_name="resetExcludeTags")
    def reset_exclude_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeTags", []))

    @jsii.member(jsii_name="resetExcludeVolumeTypes")
    def reset_exclude_volume_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeVolumeTypes", []))

    @builtins.property
    @jsii.member(jsii_name="excludeBootVolumesInput")
    def exclude_boot_volumes_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeBootVolumesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeTagsInput")
    def exclude_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "excludeTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeVolumeTypesInput")
    def exclude_volume_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeVolumeTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeBootVolumes")
    def exclude_boot_volumes(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "excludeBootVolumes"))

    @exclude_boot_volumes.setter
    def exclude_boot_volumes(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeca3ce0d3c8b0908254f6315d626bb879239f7492e7b01e7d4926f181cdbdfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeBootVolumes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeTags")
    def exclude_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "excludeTags"))

    @exclude_tags.setter
    def exclude_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9624cfbfaaece79a91a8af54d642783068a04e8508f5cd3ad4e433dc60f81e61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeVolumeTypes")
    def exclude_volume_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeVolumeTypes"))

    @exclude_volume_types.setter
    def exclude_volume_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b46dd7bbb89c05fcf32b858b4c1472ca99135f53801fd388e81dd19c027a253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeVolumeTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsExclusions]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsExclusions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsExclusions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8effdc15f15c6f744e3dc4cb369b11bd3394f44814ecbbbd9ff74622b6f204a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DlmLifecyclePolicyPolicyDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8b5e05c26fb0752254f7ea1effdaf9307518cb38653f41ecec91777b07bd06b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        cross_region_copy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy, typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
    ) -> None:
        '''
        :param cross_region_copy: cross_region_copy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#cross_region_copy DlmLifecyclePolicy#cross_region_copy}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#name DlmLifecyclePolicy#name}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsAction(
            cross_region_copy=cross_region_copy, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putEventSource")
    def put_event_source(
        self,
        *,
        parameters: typing.Union[DlmLifecyclePolicyPolicyDetailsEventSourceParameters, typing.Dict[builtins.str, typing.Any]],
        type: builtins.str,
    ) -> None:
        '''
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#parameters DlmLifecyclePolicy#parameters}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#type DlmLifecyclePolicy#type}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsEventSource(
            parameters=parameters, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putEventSource", [value]))

    @jsii.member(jsii_name="putExclusions")
    def put_exclusions(
        self,
        *,
        exclude_boot_volumes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        exclude_volume_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param exclude_boot_volumes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#exclude_boot_volumes DlmLifecyclePolicy#exclude_boot_volumes}.
        :param exclude_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#exclude_tags DlmLifecyclePolicy#exclude_tags}.
        :param exclude_volume_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#exclude_volume_types DlmLifecyclePolicy#exclude_volume_types}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsExclusions(
            exclude_boot_volumes=exclude_boot_volumes,
            exclude_tags=exclude_tags,
            exclude_volume_types=exclude_volume_types,
        )

        return typing.cast(None, jsii.invoke(self, "putExclusions", [value]))

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        *,
        exclude_boot_volume: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        no_reboot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param exclude_boot_volume: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#exclude_boot_volume DlmLifecyclePolicy#exclude_boot_volume}.
        :param no_reboot: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#no_reboot DlmLifecyclePolicy#no_reboot}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsParameters(
            exclude_boot_volume=exclude_boot_volume, no_reboot=no_reboot
        )

        return typing.cast(None, jsii.invoke(self, "putParameters", [value]))

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DlmLifecyclePolicyPolicyDetailsSchedule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c725d1e3af4ed938d26576c1ae0ee8ae4bb60071feef981d6fbae953437e85e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetCopyTags")
    def reset_copy_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyTags", []))

    @jsii.member(jsii_name="resetCreateInterval")
    def reset_create_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateInterval", []))

    @jsii.member(jsii_name="resetEventSource")
    def reset_event_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventSource", []))

    @jsii.member(jsii_name="resetExclusions")
    def reset_exclusions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusions", []))

    @jsii.member(jsii_name="resetExtendDeletion")
    def reset_extend_deletion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtendDeletion", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetPolicyLanguage")
    def reset_policy_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyLanguage", []))

    @jsii.member(jsii_name="resetPolicyType")
    def reset_policy_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyType", []))

    @jsii.member(jsii_name="resetResourceLocations")
    def reset_resource_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceLocations", []))

    @jsii.member(jsii_name="resetResourceType")
    def reset_resource_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceType", []))

    @jsii.member(jsii_name="resetResourceTypes")
    def reset_resource_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTypes", []))

    @jsii.member(jsii_name="resetRetainInterval")
    def reset_retain_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetainInterval", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetTargetTags")
    def reset_target_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetTags", []))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> DlmLifecyclePolicyPolicyDetailsActionOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="eventSource")
    def event_source(self) -> DlmLifecyclePolicyPolicyDetailsEventSourceOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsEventSourceOutputReference, jsii.get(self, "eventSource"))

    @builtins.property
    @jsii.member(jsii_name="exclusions")
    def exclusions(self) -> DlmLifecyclePolicyPolicyDetailsExclusionsOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsExclusionsOutputReference, jsii.get(self, "exclusions"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "DlmLifecyclePolicyPolicyDetailsParametersOutputReference":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsParametersOutputReference", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> "DlmLifecyclePolicyPolicyDetailsScheduleList":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleList", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsAction]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="copyTagsInput")
    def copy_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "copyTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="createIntervalInput")
    def create_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "createIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="eventSourceInput")
    def event_source_input(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSource]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSource], jsii.get(self, "eventSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionsInput")
    def exclusions_input(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsExclusions]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsExclusions], jsii.get(self, "exclusionsInput"))

    @builtins.property
    @jsii.member(jsii_name="extendDeletionInput")
    def extend_deletion_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "extendDeletionInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsParameters"]:
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsParameters"], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="policyLanguageInput")
    def policy_language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyLanguageInput"))

    @builtins.property
    @jsii.member(jsii_name="policyTypeInput")
    def policy_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceLocationsInput")
    def resource_locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypesInput")
    def resource_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="retainIntervalInput")
    def retain_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retainIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DlmLifecyclePolicyPolicyDetailsSchedule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DlmLifecyclePolicyPolicyDetailsSchedule"]]], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="targetTagsInput")
    def target_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "targetTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="copyTags")
    def copy_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "copyTags"))

    @copy_tags.setter
    def copy_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ddbaa044bafce8cf9f39cd454fc4733edfae3d5c2b45dfa2cde838da866cc30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createInterval")
    def create_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "createInterval"))

    @create_interval.setter
    def create_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1002b3d5de4815576f01d280ebc8840ef075a7d46a2804b23ddde9573ee3f41a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extendDeletion")
    def extend_deletion(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "extendDeletion"))

    @extend_deletion.setter
    def extend_deletion(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc0332f3caf5959db9e3252c9afb02e1a5d05139200a4513d9cddbe41f60f66d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendDeletion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyLanguage")
    def policy_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyLanguage"))

    @policy_language.setter
    def policy_language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84487e7f6a6835ed94a4ee38d8c60f2de0f602d191d707cb79740709bfd3458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyLanguage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyType")
    def policy_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyType"))

    @policy_type.setter
    def policy_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cabe80f195a653e85d25029efb53ec1621cb2f7582a5358992d192a0f8a7b82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceLocations")
    def resource_locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceLocations"))

    @resource_locations.setter
    def resource_locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b63ca23ba414bd876c1ee935d3922b99b2346a09fddc02f1870ad206e8d0cd83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceLocations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b978e2568904e80e0b01a23e965620b48cc1c23c8996db11a9cd19cf6e8a89b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))

    @resource_types.setter
    def resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9afa84d5f0c70a670ca2a55f725b4239a21d7ef3afe2b976563c9abdfead385f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retainInterval")
    def retain_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retainInterval"))

    @retain_interval.setter
    def retain_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2b434f14ac4ff681428f3bce033bf87fd501e954e3515cc1e3b2d6328d50c9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retainInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetTags")
    def target_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "targetTags"))

    @target_tags.setter
    def target_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68273f21fbe7451f18708ec922154cc56bb0452530867d858400dc2f83a0b497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DlmLifecyclePolicyPolicyDetails]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c844d25800c23e6b46b1e85605f5f40afaccd2fe66191362b05d93237bc0ca14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsParameters",
    jsii_struct_bases=[],
    name_mapping={"exclude_boot_volume": "excludeBootVolume", "no_reboot": "noReboot"},
)
class DlmLifecyclePolicyPolicyDetailsParameters:
    def __init__(
        self,
        *,
        exclude_boot_volume: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        no_reboot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param exclude_boot_volume: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#exclude_boot_volume DlmLifecyclePolicy#exclude_boot_volume}.
        :param no_reboot: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#no_reboot DlmLifecyclePolicy#no_reboot}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cb40e657513d8102ad323a1b7c0ac6abbf534f8837561241f335751baa4c06c)
            check_type(argname="argument exclude_boot_volume", value=exclude_boot_volume, expected_type=type_hints["exclude_boot_volume"])
            check_type(argname="argument no_reboot", value=no_reboot, expected_type=type_hints["no_reboot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_boot_volume is not None:
            self._values["exclude_boot_volume"] = exclude_boot_volume
        if no_reboot is not None:
            self._values["no_reboot"] = no_reboot

    @builtins.property
    def exclude_boot_volume(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#exclude_boot_volume DlmLifecyclePolicy#exclude_boot_volume}.'''
        result = self._values.get("exclude_boot_volume")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def no_reboot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#no_reboot DlmLifecyclePolicy#no_reboot}.'''
        result = self._values.get("no_reboot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87ee957c5f0e79a9485c6eec40e4fe5f181bacf1322cabc25ad3c55274126e99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludeBootVolume")
    def reset_exclude_boot_volume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeBootVolume", []))

    @jsii.member(jsii_name="resetNoReboot")
    def reset_no_reboot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoReboot", []))

    @builtins.property
    @jsii.member(jsii_name="excludeBootVolumeInput")
    def exclude_boot_volume_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeBootVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="noRebootInput")
    def no_reboot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noRebootInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeBootVolume")
    def exclude_boot_volume(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "excludeBootVolume"))

    @exclude_boot_volume.setter
    def exclude_boot_volume(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a32e6a390857ed24c01bfc636a8b7a2981c81642a764e557a8c3dfcc74c6f02c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeBootVolume", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noReboot")
    def no_reboot(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noReboot"))

    @no_reboot.setter
    def no_reboot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__173ab6cc615303bf66e8b5f7e5ade1d0799dfdc5c939bfe34bd2ae35752ea329)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noReboot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsParameters]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e42b82d4c27ef8a631c7cc94aaae8ae4335c6ea968e03966a74f11841fb1fc36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "create_rule": "createRule",
        "name": "name",
        "retain_rule": "retainRule",
        "archive_rule": "archiveRule",
        "copy_tags": "copyTags",
        "cross_region_copy_rule": "crossRegionCopyRule",
        "deprecate_rule": "deprecateRule",
        "fast_restore_rule": "fastRestoreRule",
        "share_rule": "shareRule",
        "tags_to_add": "tagsToAdd",
        "variable_tags": "variableTags",
    },
)
class DlmLifecyclePolicyPolicyDetailsSchedule:
    def __init__(
        self,
        *,
        create_rule: typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleCreateRule", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        retain_rule: typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleRetainRule", typing.Dict[builtins.str, typing.Any]],
        archive_rule: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule", typing.Dict[builtins.str, typing.Any]]] = None,
        copy_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cross_region_copy_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        deprecate_rule: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule", typing.Dict[builtins.str, typing.Any]]] = None,
        fast_restore_rule: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule", typing.Dict[builtins.str, typing.Any]]] = None,
        share_rule: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleShareRule", typing.Dict[builtins.str, typing.Any]]] = None,
        tags_to_add: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        variable_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param create_rule: create_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#create_rule DlmLifecyclePolicy#create_rule}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#name DlmLifecyclePolicy#name}.
        :param retain_rule: retain_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#retain_rule DlmLifecyclePolicy#retain_rule}
        :param archive_rule: archive_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#archive_rule DlmLifecyclePolicy#archive_rule}
        :param copy_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#copy_tags DlmLifecyclePolicy#copy_tags}.
        :param cross_region_copy_rule: cross_region_copy_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#cross_region_copy_rule DlmLifecyclePolicy#cross_region_copy_rule}
        :param deprecate_rule: deprecate_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#deprecate_rule DlmLifecyclePolicy#deprecate_rule}
        :param fast_restore_rule: fast_restore_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#fast_restore_rule DlmLifecyclePolicy#fast_restore_rule}
        :param share_rule: share_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#share_rule DlmLifecyclePolicy#share_rule}
        :param tags_to_add: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#tags_to_add DlmLifecyclePolicy#tags_to_add}.
        :param variable_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#variable_tags DlmLifecyclePolicy#variable_tags}.
        '''
        if isinstance(create_rule, dict):
            create_rule = DlmLifecyclePolicyPolicyDetailsScheduleCreateRule(**create_rule)
        if isinstance(retain_rule, dict):
            retain_rule = DlmLifecyclePolicyPolicyDetailsScheduleRetainRule(**retain_rule)
        if isinstance(archive_rule, dict):
            archive_rule = DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule(**archive_rule)
        if isinstance(deprecate_rule, dict):
            deprecate_rule = DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule(**deprecate_rule)
        if isinstance(fast_restore_rule, dict):
            fast_restore_rule = DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule(**fast_restore_rule)
        if isinstance(share_rule, dict):
            share_rule = DlmLifecyclePolicyPolicyDetailsScheduleShareRule(**share_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd2abeb5e6e0befa5173a64322545acb6b0cfe1d7bef2ad07a02f120e948e2c9)
            check_type(argname="argument create_rule", value=create_rule, expected_type=type_hints["create_rule"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument retain_rule", value=retain_rule, expected_type=type_hints["retain_rule"])
            check_type(argname="argument archive_rule", value=archive_rule, expected_type=type_hints["archive_rule"])
            check_type(argname="argument copy_tags", value=copy_tags, expected_type=type_hints["copy_tags"])
            check_type(argname="argument cross_region_copy_rule", value=cross_region_copy_rule, expected_type=type_hints["cross_region_copy_rule"])
            check_type(argname="argument deprecate_rule", value=deprecate_rule, expected_type=type_hints["deprecate_rule"])
            check_type(argname="argument fast_restore_rule", value=fast_restore_rule, expected_type=type_hints["fast_restore_rule"])
            check_type(argname="argument share_rule", value=share_rule, expected_type=type_hints["share_rule"])
            check_type(argname="argument tags_to_add", value=tags_to_add, expected_type=type_hints["tags_to_add"])
            check_type(argname="argument variable_tags", value=variable_tags, expected_type=type_hints["variable_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "create_rule": create_rule,
            "name": name,
            "retain_rule": retain_rule,
        }
        if archive_rule is not None:
            self._values["archive_rule"] = archive_rule
        if copy_tags is not None:
            self._values["copy_tags"] = copy_tags
        if cross_region_copy_rule is not None:
            self._values["cross_region_copy_rule"] = cross_region_copy_rule
        if deprecate_rule is not None:
            self._values["deprecate_rule"] = deprecate_rule
        if fast_restore_rule is not None:
            self._values["fast_restore_rule"] = fast_restore_rule
        if share_rule is not None:
            self._values["share_rule"] = share_rule
        if tags_to_add is not None:
            self._values["tags_to_add"] = tags_to_add
        if variable_tags is not None:
            self._values["variable_tags"] = variable_tags

    @builtins.property
    def create_rule(self) -> "DlmLifecyclePolicyPolicyDetailsScheduleCreateRule":
        '''create_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#create_rule DlmLifecyclePolicy#create_rule}
        '''
        result = self._values.get("create_rule")
        assert result is not None, "Required property 'create_rule' is missing"
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleCreateRule", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#name DlmLifecyclePolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retain_rule(self) -> "DlmLifecyclePolicyPolicyDetailsScheduleRetainRule":
        '''retain_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#retain_rule DlmLifecyclePolicy#retain_rule}
        '''
        result = self._values.get("retain_rule")
        assert result is not None, "Required property 'retain_rule' is missing"
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleRetainRule", result)

    @builtins.property
    def archive_rule(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule"]:
        '''archive_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#archive_rule DlmLifecyclePolicy#archive_rule}
        '''
        result = self._values.get("archive_rule")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule"], result)

    @builtins.property
    def copy_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#copy_tags DlmLifecyclePolicy#copy_tags}.'''
        result = self._values.get("copy_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cross_region_copy_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule"]]]:
        '''cross_region_copy_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#cross_region_copy_rule DlmLifecyclePolicy#cross_region_copy_rule}
        '''
        result = self._values.get("cross_region_copy_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule"]]], result)

    @builtins.property
    def deprecate_rule(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule"]:
        '''deprecate_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#deprecate_rule DlmLifecyclePolicy#deprecate_rule}
        '''
        result = self._values.get("deprecate_rule")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule"], result)

    @builtins.property
    def fast_restore_rule(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule"]:
        '''fast_restore_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#fast_restore_rule DlmLifecyclePolicy#fast_restore_rule}
        '''
        result = self._values.get("fast_restore_rule")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule"], result)

    @builtins.property
    def share_rule(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleShareRule"]:
        '''share_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#share_rule DlmLifecyclePolicy#share_rule}
        '''
        result = self._values.get("share_rule")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleShareRule"], result)

    @builtins.property
    def tags_to_add(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#tags_to_add DlmLifecyclePolicy#tags_to_add}.'''
        result = self._values.get("tags_to_add")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def variable_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#variable_tags DlmLifecyclePolicy#variable_tags}.'''
        result = self._values.get("variable_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule",
    jsii_struct_bases=[],
    name_mapping={"archive_retain_rule": "archiveRetainRule"},
)
class DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule:
    def __init__(
        self,
        *,
        archive_retain_rule: typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param archive_retain_rule: archive_retain_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#archive_retain_rule DlmLifecyclePolicy#archive_retain_rule}
        '''
        if isinstance(archive_retain_rule, dict):
            archive_retain_rule = DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule(**archive_retain_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2afe8342a00c89e2240f847bb9ac5521470f61af7d39687e43e449c0ea793a69)
            check_type(argname="argument archive_retain_rule", value=archive_retain_rule, expected_type=type_hints["archive_retain_rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "archive_retain_rule": archive_retain_rule,
        }

    @builtins.property
    def archive_retain_rule(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule":
        '''archive_retain_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#archive_retain_rule DlmLifecyclePolicy#archive_retain_rule}
        '''
        result = self._values.get("archive_retain_rule")
        assert result is not None, "Required property 'archive_retain_rule' is missing"
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule",
    jsii_struct_bases=[],
    name_mapping={"retention_archive_tier": "retentionArchiveTier"},
)
class DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule:
    def __init__(
        self,
        *,
        retention_archive_tier: typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param retention_archive_tier: retention_archive_tier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#retention_archive_tier DlmLifecyclePolicy#retention_archive_tier}
        '''
        if isinstance(retention_archive_tier, dict):
            retention_archive_tier = DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier(**retention_archive_tier)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90097b0c628fa7399618c6408ccef97facc03e9f066a5bd21b1163a780cb4383)
            check_type(argname="argument retention_archive_tier", value=retention_archive_tier, expected_type=type_hints["retention_archive_tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "retention_archive_tier": retention_archive_tier,
        }

    @builtins.property
    def retention_archive_tier(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier":
        '''retention_archive_tier block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#retention_archive_tier DlmLifecyclePolicy#retention_archive_tier}
        '''
        result = self._values.get("retention_archive_tier")
        assert result is not None, "Required property 'retention_archive_tier' is missing"
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6334dbca8c00f93d77d7a08f7ccfd8db4a3891d1ab272c3633441e35184ee56d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRetentionArchiveTier")
    def put_retention_archive_tier(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier(
            count=count, interval=interval, interval_unit=interval_unit
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionArchiveTier", [value]))

    @builtins.property
    @jsii.member(jsii_name="retentionArchiveTier")
    def retention_archive_tier(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTierOutputReference":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTierOutputReference", jsii.get(self, "retentionArchiveTier"))

    @builtins.property
    @jsii.member(jsii_name="retentionArchiveTierInput")
    def retention_archive_tier_input(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier"]:
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier"], jsii.get(self, "retentionArchiveTierInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c809cdf2f984796d8fda7d51636df8480f5a5af893f9ac690fc6285960e4f549)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "interval": "interval",
        "interval_unit": "intervalUnit",
    },
)
class DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e56253935adb255723a0524d88cebf3c1200534208240f1917e62b4776a9bc82)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if interval is not None:
            self._values["interval"] = interval
        if interval_unit is not None:
            self._values["interval_unit"] = interval_unit

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.'''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.'''
        result = self._values.get("interval_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTierOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTierOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b84d974c3bbd3681ac745660d64784be0aab98cac92a0e745a54050b8fe2dd9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetIntervalUnit")
    def reset_interval_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalUnit", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalUnitInput")
    def interval_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7aebde98b2d5f0caf3dc47e9cbe5cec5fd60adaea9724049b09dee8df7626fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59cc55275d5fed8a5813030345b492b9b22ca42bd6ff7f8572cb7b40d5d346d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalUnit")
    def interval_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intervalUnit"))

    @interval_unit.setter
    def interval_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf315935c06dc3bd9043ca0349e58a2a0641a89825b357d7c6f72461cda56376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe02d5425bd6b8e472e5f51c04df3cba36f1ea391d0b2ab439189f166e72984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a82350f3fcb1613112b97ee4938785dc9a4a8ec9e25b60479c43cf9e727619c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putArchiveRetainRule")
    def put_archive_retain_rule(
        self,
        *,
        retention_archive_tier: typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param retention_archive_tier: retention_archive_tier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#retention_archive_tier DlmLifecyclePolicy#retention_archive_tier}
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule(
            retention_archive_tier=retention_archive_tier
        )

        return typing.cast(None, jsii.invoke(self, "putArchiveRetainRule", [value]))

    @builtins.property
    @jsii.member(jsii_name="archiveRetainRule")
    def archive_retain_rule(
        self,
    ) -> DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleOutputReference, jsii.get(self, "archiveRetainRule"))

    @builtins.property
    @jsii.member(jsii_name="archiveRetainRuleInput")
    def archive_retain_rule_input(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule], jsii.get(self, "archiveRetainRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d15d044404f4b5b59fe58afa0d2e60d27be9110cd6f25685b2328f9a29cf3751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCreateRule",
    jsii_struct_bases=[],
    name_mapping={
        "cron_expression": "cronExpression",
        "interval": "interval",
        "interval_unit": "intervalUnit",
        "location": "location",
        "scripts": "scripts",
        "times": "times",
    },
)
class DlmLifecyclePolicyPolicyDetailsScheduleCreateRule:
    def __init__(
        self,
        *,
        cron_expression: typing.Optional[builtins.str] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        scripts: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts", typing.Dict[builtins.str, typing.Any]]] = None,
        times: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cron_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#cron_expression DlmLifecyclePolicy#cron_expression}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#location DlmLifecyclePolicy#location}.
        :param scripts: scripts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#scripts DlmLifecyclePolicy#scripts}
        :param times: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#times DlmLifecyclePolicy#times}.
        '''
        if isinstance(scripts, dict):
            scripts = DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts(**scripts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29646122068fd6436132ab85b0f0194bfefa9ccc572a23a11b4a1f6e99781428)
            check_type(argname="argument cron_expression", value=cron_expression, expected_type=type_hints["cron_expression"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
            check_type(argname="argument times", value=times, expected_type=type_hints["times"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cron_expression is not None:
            self._values["cron_expression"] = cron_expression
        if interval is not None:
            self._values["interval"] = interval
        if interval_unit is not None:
            self._values["interval_unit"] = interval_unit
        if location is not None:
            self._values["location"] = location
        if scripts is not None:
            self._values["scripts"] = scripts
        if times is not None:
            self._values["times"] = times

    @builtins.property
    def cron_expression(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#cron_expression DlmLifecyclePolicy#cron_expression}.'''
        result = self._values.get("cron_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.'''
        result = self._values.get("interval_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#location DlmLifecyclePolicy#location}.'''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scripts(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts"]:
        '''scripts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#scripts DlmLifecyclePolicy#scripts}
        '''
        result = self._values.get("scripts")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts"], result)

    @builtins.property
    def times(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#times DlmLifecyclePolicy#times}.'''
        result = self._values.get("times")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleCreateRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00663b822ba754432609693e450b1d73c3b619b4c48e276f3230cb4aea2fb30e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScripts")
    def put_scripts(
        self,
        *,
        execution_handler: builtins.str,
        execute_operation_on_script_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        execution_handler_service: typing.Optional[builtins.str] = None,
        execution_timeout: typing.Optional[jsii.Number] = None,
        maximum_retry_count: typing.Optional[jsii.Number] = None,
        stages: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param execution_handler: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#execution_handler DlmLifecyclePolicy#execution_handler}.
        :param execute_operation_on_script_failure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#execute_operation_on_script_failure DlmLifecyclePolicy#execute_operation_on_script_failure}.
        :param execution_handler_service: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#execution_handler_service DlmLifecyclePolicy#execution_handler_service}.
        :param execution_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#execution_timeout DlmLifecyclePolicy#execution_timeout}.
        :param maximum_retry_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#maximum_retry_count DlmLifecyclePolicy#maximum_retry_count}.
        :param stages: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#stages DlmLifecyclePolicy#stages}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts(
            execution_handler=execution_handler,
            execute_operation_on_script_failure=execute_operation_on_script_failure,
            execution_handler_service=execution_handler_service,
            execution_timeout=execution_timeout,
            maximum_retry_count=maximum_retry_count,
            stages=stages,
        )

        return typing.cast(None, jsii.invoke(self, "putScripts", [value]))

    @jsii.member(jsii_name="resetCronExpression")
    def reset_cron_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCronExpression", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetIntervalUnit")
    def reset_interval_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalUnit", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetScripts")
    def reset_scripts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScripts", []))

    @jsii.member(jsii_name="resetTimes")
    def reset_times(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimes", []))

    @builtins.property
    @jsii.member(jsii_name="scripts")
    def scripts(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScriptsOutputReference":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScriptsOutputReference", jsii.get(self, "scripts"))

    @builtins.property
    @jsii.member(jsii_name="cronExpressionInput")
    def cron_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cronExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalUnitInput")
    def interval_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptsInput")
    def scripts_input(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts"]:
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts"], jsii.get(self, "scriptsInput"))

    @builtins.property
    @jsii.member(jsii_name="timesInput")
    def times_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "timesInput"))

    @builtins.property
    @jsii.member(jsii_name="cronExpression")
    def cron_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cronExpression"))

    @cron_expression.setter
    def cron_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1612ecd610e246fb011d339cf67c5544782d5a0c1c891608bdf11d044c2ead3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cronExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e003c6ca50b22bb962fc7bcebee6611543c4861240e41710bc7d6e3bef2563c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalUnit")
    def interval_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intervalUnit"))

    @interval_unit.setter
    def interval_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61728cd297bb67766970abf9a38dffb0dc1ba5dec098bc20bcdd23e0dddfe504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b4e1ee1d78ce3c699893f85e309d859c05e9e8faeb83daacacda750ce310290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="times")
    def times(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "times"))

    @times.setter
    def times(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6469f867a1ef48d9bdbf16eb0fdf5397faad84309562aa89e7d73db13d6f8fba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "times", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed617d402b6f264357439c59d557b3181cb38f946d2d7f1c7e65c12dd6565996)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts",
    jsii_struct_bases=[],
    name_mapping={
        "execution_handler": "executionHandler",
        "execute_operation_on_script_failure": "executeOperationOnScriptFailure",
        "execution_handler_service": "executionHandlerService",
        "execution_timeout": "executionTimeout",
        "maximum_retry_count": "maximumRetryCount",
        "stages": "stages",
    },
)
class DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts:
    def __init__(
        self,
        *,
        execution_handler: builtins.str,
        execute_operation_on_script_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        execution_handler_service: typing.Optional[builtins.str] = None,
        execution_timeout: typing.Optional[jsii.Number] = None,
        maximum_retry_count: typing.Optional[jsii.Number] = None,
        stages: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param execution_handler: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#execution_handler DlmLifecyclePolicy#execution_handler}.
        :param execute_operation_on_script_failure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#execute_operation_on_script_failure DlmLifecyclePolicy#execute_operation_on_script_failure}.
        :param execution_handler_service: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#execution_handler_service DlmLifecyclePolicy#execution_handler_service}.
        :param execution_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#execution_timeout DlmLifecyclePolicy#execution_timeout}.
        :param maximum_retry_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#maximum_retry_count DlmLifecyclePolicy#maximum_retry_count}.
        :param stages: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#stages DlmLifecyclePolicy#stages}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__200d2f20e562b31cf22ae7d8f9e428a5fc46bb3ecb01e498954bcd3e2c8a1162)
            check_type(argname="argument execution_handler", value=execution_handler, expected_type=type_hints["execution_handler"])
            check_type(argname="argument execute_operation_on_script_failure", value=execute_operation_on_script_failure, expected_type=type_hints["execute_operation_on_script_failure"])
            check_type(argname="argument execution_handler_service", value=execution_handler_service, expected_type=type_hints["execution_handler_service"])
            check_type(argname="argument execution_timeout", value=execution_timeout, expected_type=type_hints["execution_timeout"])
            check_type(argname="argument maximum_retry_count", value=maximum_retry_count, expected_type=type_hints["maximum_retry_count"])
            check_type(argname="argument stages", value=stages, expected_type=type_hints["stages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execution_handler": execution_handler,
        }
        if execute_operation_on_script_failure is not None:
            self._values["execute_operation_on_script_failure"] = execute_operation_on_script_failure
        if execution_handler_service is not None:
            self._values["execution_handler_service"] = execution_handler_service
        if execution_timeout is not None:
            self._values["execution_timeout"] = execution_timeout
        if maximum_retry_count is not None:
            self._values["maximum_retry_count"] = maximum_retry_count
        if stages is not None:
            self._values["stages"] = stages

    @builtins.property
    def execution_handler(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#execution_handler DlmLifecyclePolicy#execution_handler}.'''
        result = self._values.get("execution_handler")
        assert result is not None, "Required property 'execution_handler' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def execute_operation_on_script_failure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#execute_operation_on_script_failure DlmLifecyclePolicy#execute_operation_on_script_failure}.'''
        result = self._values.get("execute_operation_on_script_failure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def execution_handler_service(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#execution_handler_service DlmLifecyclePolicy#execution_handler_service}.'''
        result = self._values.get("execution_handler_service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#execution_timeout DlmLifecyclePolicy#execution_timeout}.'''
        result = self._values.get("execution_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_retry_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#maximum_retry_count DlmLifecyclePolicy#maximum_retry_count}.'''
        result = self._values.get("maximum_retry_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#stages DlmLifecyclePolicy#stages}.'''
        result = self._values.get("stages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScriptsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScriptsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a78dc264b2c3e3d0643411cdfe602a46d82d7c5973c7968fe45268a843d5a678)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExecuteOperationOnScriptFailure")
    def reset_execute_operation_on_script_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecuteOperationOnScriptFailure", []))

    @jsii.member(jsii_name="resetExecutionHandlerService")
    def reset_execution_handler_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionHandlerService", []))

    @jsii.member(jsii_name="resetExecutionTimeout")
    def reset_execution_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionTimeout", []))

    @jsii.member(jsii_name="resetMaximumRetryCount")
    def reset_maximum_retry_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRetryCount", []))

    @jsii.member(jsii_name="resetStages")
    def reset_stages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStages", []))

    @builtins.property
    @jsii.member(jsii_name="executeOperationOnScriptFailureInput")
    def execute_operation_on_script_failure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "executeOperationOnScriptFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="executionHandlerInput")
    def execution_handler_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionHandlerInput"))

    @builtins.property
    @jsii.member(jsii_name="executionHandlerServiceInput")
    def execution_handler_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionHandlerServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="executionTimeoutInput")
    def execution_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "executionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumRetryCountInput")
    def maximum_retry_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumRetryCountInput"))

    @builtins.property
    @jsii.member(jsii_name="stagesInput")
    def stages_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "stagesInput"))

    @builtins.property
    @jsii.member(jsii_name="executeOperationOnScriptFailure")
    def execute_operation_on_script_failure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "executeOperationOnScriptFailure"))

    @execute_operation_on_script_failure.setter
    def execute_operation_on_script_failure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c181d5338ac2533976cdb75269f16af80a6a6662052025eab28a219415bce43e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executeOperationOnScriptFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionHandler")
    def execution_handler(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionHandler"))

    @execution_handler.setter
    def execution_handler(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5169aafcd513cae0a1e3e5d16e2290e512a3a81477dc834765cfa891be658c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionHandler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionHandlerService")
    def execution_handler_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionHandlerService"))

    @execution_handler_service.setter
    def execution_handler_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b60b3c94e8745eb1e0c02c40e0fa3ff8e72b9efe9f60550c44642199523d41b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionHandlerService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionTimeout")
    def execution_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "executionTimeout"))

    @execution_timeout.setter
    def execution_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17bf9f923aebe47ee682284837c0f3af923235f3a39a2be5886f87a2dcfe0125)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumRetryCount")
    def maximum_retry_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRetryCount"))

    @maximum_retry_count.setter
    def maximum_retry_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9790d6cc67b29369f6b8c3087603babca975de874e9c7333b7a9b94d31623377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRetryCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stages")
    def stages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stages"))

    @stages.setter
    def stages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6818506cdac07bcc60cb190c937a4eb2bce086a1522b9f5e3650d95d1b54f3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d509caa3eefbd7d66164303c1ead31c28fe36ff372a753374b77c613c1ce736a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule",
    jsii_struct_bases=[],
    name_mapping={
        "encrypted": "encrypted",
        "cmk_arn": "cmkArn",
        "copy_tags": "copyTags",
        "deprecate_rule": "deprecateRule",
        "retain_rule": "retainRule",
        "target": "target",
        "target_region": "targetRegion",
    },
)
class DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule:
    def __init__(
        self,
        *,
        encrypted: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        cmk_arn: typing.Optional[builtins.str] = None,
        copy_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deprecate_rule: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule", typing.Dict[builtins.str, typing.Any]]] = None,
        retain_rule: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule", typing.Dict[builtins.str, typing.Any]]] = None,
        target: typing.Optional[builtins.str] = None,
        target_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encrypted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#encrypted DlmLifecyclePolicy#encrypted}.
        :param cmk_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#cmk_arn DlmLifecyclePolicy#cmk_arn}.
        :param copy_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#copy_tags DlmLifecyclePolicy#copy_tags}.
        :param deprecate_rule: deprecate_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#deprecate_rule DlmLifecyclePolicy#deprecate_rule}
        :param retain_rule: retain_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#retain_rule DlmLifecyclePolicy#retain_rule}
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#target DlmLifecyclePolicy#target}.
        :param target_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#target_region DlmLifecyclePolicy#target_region}.
        '''
        if isinstance(deprecate_rule, dict):
            deprecate_rule = DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule(**deprecate_rule)
        if isinstance(retain_rule, dict):
            retain_rule = DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule(**retain_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8970e6173d98abbfe5d0ded5297854793937febd74c33e41588334ff1b59852)
            check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
            check_type(argname="argument cmk_arn", value=cmk_arn, expected_type=type_hints["cmk_arn"])
            check_type(argname="argument copy_tags", value=copy_tags, expected_type=type_hints["copy_tags"])
            check_type(argname="argument deprecate_rule", value=deprecate_rule, expected_type=type_hints["deprecate_rule"])
            check_type(argname="argument retain_rule", value=retain_rule, expected_type=type_hints["retain_rule"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument target_region", value=target_region, expected_type=type_hints["target_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "encrypted": encrypted,
        }
        if cmk_arn is not None:
            self._values["cmk_arn"] = cmk_arn
        if copy_tags is not None:
            self._values["copy_tags"] = copy_tags
        if deprecate_rule is not None:
            self._values["deprecate_rule"] = deprecate_rule
        if retain_rule is not None:
            self._values["retain_rule"] = retain_rule
        if target is not None:
            self._values["target"] = target
        if target_region is not None:
            self._values["target_region"] = target_region

    @builtins.property
    def encrypted(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#encrypted DlmLifecyclePolicy#encrypted}.'''
        result = self._values.get("encrypted")
        assert result is not None, "Required property 'encrypted' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def cmk_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#cmk_arn DlmLifecyclePolicy#cmk_arn}.'''
        result = self._values.get("cmk_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copy_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#copy_tags DlmLifecyclePolicy#copy_tags}.'''
        result = self._values.get("copy_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def deprecate_rule(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule"]:
        '''deprecate_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#deprecate_rule DlmLifecyclePolicy#deprecate_rule}
        '''
        result = self._values.get("deprecate_rule")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule"], result)

    @builtins.property
    def retain_rule(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule"]:
        '''retain_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#retain_rule DlmLifecyclePolicy#retain_rule}
        '''
        result = self._values.get("retain_rule")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule"], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#target DlmLifecyclePolicy#target}.'''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#target_region DlmLifecyclePolicy#target_region}.'''
        result = self._values.get("target_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule",
    jsii_struct_bases=[],
    name_mapping={"interval": "interval", "interval_unit": "intervalUnit"},
)
class DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule:
    def __init__(self, *, interval: jsii.Number, interval_unit: builtins.str) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe4b7f65ddf09ad869a3d872a65323f1f02886d677deebc258091370c1d33c56)
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interval": interval,
            "interval_unit": interval_unit,
        }

    @builtins.property
    def interval(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.'''
        result = self._values.get("interval")
        assert result is not None, "Required property 'interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def interval_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.'''
        result = self._values.get("interval_unit")
        assert result is not None, "Required property 'interval_unit' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cf545e2c016fe1df044ddcfd051ec62fdc4291ebb0d6cdd2c53c217ceec795f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalUnitInput")
    def interval_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc2ad3295856779507cb3c8a0340162038f2fc7753fbddd570d77ef977600e31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalUnit")
    def interval_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intervalUnit"))

    @interval_unit.setter
    def interval_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb3d058f7f93d0b29a1de97ea2fd001a6a9d6c294cbc19f0c28efcf5bbb588fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5211d4ebfa2186fab2502f8c4d396371ae1d8a527d1e9fbfb5cb290ba4f0079d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6374b0924206eb61157cc1c7d67e24504c0950e37f416da98f490f0f1f78386)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3001ef503b1435d0cc398fea273d1095162e8a97c28058132887ca0207fdb72b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487b7896fe34ad3bc793aff1ccf61f251891620f19bc7e2019d890613a54aa88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__665aa08b61889d062fbd48b2b92cab857a69d6964eb3c2e402f3f43ef32adf3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68ab49cdf7d86c54cdcacc138458e9f7be7068607ee0c8231181311890a35d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7570faf210cba50a544f968cea8256f4712eb6913ea158651dbc4067eb49a5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0885292d869a85fd049f34c2dc0874eb7545b2ef42851c28916f7c754d4948c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDeprecateRule")
    def put_deprecate_rule(
        self,
        *,
        interval: jsii.Number,
        interval_unit: builtins.str,
    ) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule(
            interval=interval, interval_unit=interval_unit
        )

        return typing.cast(None, jsii.invoke(self, "putDeprecateRule", [value]))

    @jsii.member(jsii_name="putRetainRule")
    def put_retain_rule(
        self,
        *,
        interval: jsii.Number,
        interval_unit: builtins.str,
    ) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule(
            interval=interval, interval_unit=interval_unit
        )

        return typing.cast(None, jsii.invoke(self, "putRetainRule", [value]))

    @jsii.member(jsii_name="resetCmkArn")
    def reset_cmk_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCmkArn", []))

    @jsii.member(jsii_name="resetCopyTags")
    def reset_copy_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyTags", []))

    @jsii.member(jsii_name="resetDeprecateRule")
    def reset_deprecate_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeprecateRule", []))

    @jsii.member(jsii_name="resetRetainRule")
    def reset_retain_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetainRule", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @jsii.member(jsii_name="resetTargetRegion")
    def reset_target_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="deprecateRule")
    def deprecate_rule(
        self,
    ) -> DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRuleOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRuleOutputReference, jsii.get(self, "deprecateRule"))

    @builtins.property
    @jsii.member(jsii_name="retainRule")
    def retain_rule(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRuleOutputReference":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRuleOutputReference", jsii.get(self, "retainRule"))

    @builtins.property
    @jsii.member(jsii_name="cmkArnInput")
    def cmk_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cmkArnInput"))

    @builtins.property
    @jsii.member(jsii_name="copyTagsInput")
    def copy_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "copyTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="deprecateRuleInput")
    def deprecate_rule_input(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule], jsii.get(self, "deprecateRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptedInput")
    def encrypted_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptedInput"))

    @builtins.property
    @jsii.member(jsii_name="retainRuleInput")
    def retain_rule_input(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule"]:
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule"], jsii.get(self, "retainRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="targetRegionInput")
    def target_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="cmkArn")
    def cmk_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cmkArn"))

    @cmk_arn.setter
    def cmk_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325e276f988f98ab8217629edb3e1bb553ff8f21a5495e16eeacff1b882b8ca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cmkArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="copyTags")
    def copy_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "copyTags"))

    @copy_tags.setter
    def copy_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62120b951be3559046c42c7641bff19beb8d787c124a0df6ac97d097009450e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encrypted")
    def encrypted(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encrypted"))

    @encrypted.setter
    def encrypted(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5a1f263bfb6bf3371fce27cbda9e77cf65873ee6d3ef05f5c9d3d87c836fbfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encrypted", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ece47337370ae832d6cb401c8636216062bc6fc8df4df1e716ec208721265c56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetRegion")
    def target_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetRegion"))

    @target_region.setter
    def target_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec4aee510c2d1934b2cc36a6a978b6c9da3400592d62f4b6260962acfb19221)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea0c6b885b2e9a05d66bc58f1a9551a77fafe7743d68d961659da7c4e52cf54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule",
    jsii_struct_bases=[],
    name_mapping={"interval": "interval", "interval_unit": "intervalUnit"},
)
class DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule:
    def __init__(self, *, interval: jsii.Number, interval_unit: builtins.str) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73399a56d282e97de3f55816b35011bb8bea89e95fee6641b041c3c03eda3459)
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interval": interval,
            "interval_unit": interval_unit,
        }

    @builtins.property
    def interval(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.'''
        result = self._values.get("interval")
        assert result is not None, "Required property 'interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def interval_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.'''
        result = self._values.get("interval_unit")
        assert result is not None, "Required property 'interval_unit' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__725dfe082fde14dfb9857ceb92cea3cad15509ca515f971ff91a0714e0cda023)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalUnitInput")
    def interval_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31a9cadf9377b5a154c79e62f8bcb2686c3a71f55ae6b1fd6b419730b684133)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalUnit")
    def interval_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intervalUnit"))

    @interval_unit.setter
    def interval_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16ce76333fc72975d2126febd5df3412ad900471896d1424d137d665fe171a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce4d145d7b1c4370ed2087e99eb0e5e84ba052937bfe5e01dcf45d6a95f36e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "interval": "interval",
        "interval_unit": "intervalUnit",
    },
)
class DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b8b5d500dba036f67ef467e6d8f5c801ce365520db9235b942f1b83075610cf)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if interval is not None:
            self._values["interval"] = interval
        if interval_unit is not None:
            self._values["interval_unit"] = interval_unit

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.'''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.'''
        result = self._values.get("interval_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__851fd8bd01bb36088cfc9b9cbf117420dd58fd3617140bfb8c890af2646657af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetIntervalUnit")
    def reset_interval_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalUnit", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalUnitInput")
    def interval_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d749acd24d7e267cef86a8707198914e3caf4464c96fb99d11c6ec57cebf6dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a32149f59e612b367f483724d06f85734c9d09ac166b76f3aa9502e96d2615f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalUnit")
    def interval_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intervalUnit"))

    @interval_unit.setter
    def interval_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b778cd9c430df289b2f6c2ec4571b2e232dbfa273f7d82731a01364f8b1a699f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23eea193861826ba0b60d346b281b0220f5470cc7c368881d96d885f42b30a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zones": "availabilityZones",
        "count": "count",
        "interval": "interval",
        "interval_unit": "intervalUnit",
    },
)
class DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule:
    def __init__(
        self,
        *,
        availability_zones: typing.Sequence[builtins.str],
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#availability_zones DlmLifecyclePolicy#availability_zones}.
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff9c85dc3fc85490e77a4b7e8c4cbaaacfe07988ba491a67517d8e9e3d29db71)
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zones": availability_zones,
        }
        if count is not None:
            self._values["count"] = count
        if interval is not None:
            self._values["interval"] = interval
        if interval_unit is not None:
            self._values["interval_unit"] = interval_unit

    @builtins.property
    def availability_zones(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#availability_zones DlmLifecyclePolicy#availability_zones}.'''
        result = self._values.get("availability_zones")
        assert result is not None, "Required property 'availability_zones' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.'''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.'''
        result = self._values.get("interval_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__097f5dd289b2790bf3f07b1f86d321b6efa83b1c4ada79e7824b535048f72b20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetIntervalUnit")
    def reset_interval_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalUnit", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityZonesInput")
    def availability_zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availabilityZonesInput"))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalUnitInput")
    def interval_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZones"))

    @availability_zones.setter
    def availability_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ea84d85f89fef367020acb4ddb2edfa5e65ef38c21e6cb21165fb363978bdc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9ac3b173faefbf5310a9a5dab2bf7dc934d2631aeab31a90e4ed16097ba9d69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39f0ca7bf65a63b643bcfb8ff55c675adc645bd06268117081e68ef5e2e977af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalUnit")
    def interval_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intervalUnit"))

    @interval_unit.setter
    def interval_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1dcb79f975c426742bb8a94ebe82d110197dd73825a5ac5c80480dcbc159de3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76922bfbffc6af75ef57f3084a81c8681d7b8743d679d447f539da74abe773e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DlmLifecyclePolicyPolicyDetailsScheduleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d83d295dd6c58e5eddd5571fde69574d7584c406fdb158b106bd52dbccac1e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DlmLifecyclePolicyPolicyDetailsScheduleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff25695396c4277fbd90ae3e922b8f03b76c1904e458953b98fd1f09f197ac6a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8466f1a3defe0fad7a3a64a8088b1d1f35bfce1112b8610e4d3d3c93a74594d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c1e03fefe07baf9a4f2fd59aed06bd1d2838c99559b4bbebb6d700a450bac23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a1b1e093b18daf6b482d6acea6988e6bd537fb095e1a59b7f950ddb39623311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsSchedule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsSchedule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsSchedule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6183e0096132132bd64ec28525b719c48c9a148d9ff2cc8920292996bee6dd80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DlmLifecyclePolicyPolicyDetailsScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd285e74d1ac8ec4e65c4c46935aeb2a42ec4337f16792f3fe4d9f9b51c10f5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putArchiveRule")
    def put_archive_rule(
        self,
        *,
        archive_retain_rule: typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param archive_retain_rule: archive_retain_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#archive_retain_rule DlmLifecyclePolicy#archive_retain_rule}
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule(
            archive_retain_rule=archive_retain_rule
        )

        return typing.cast(None, jsii.invoke(self, "putArchiveRule", [value]))

    @jsii.member(jsii_name="putCreateRule")
    def put_create_rule(
        self,
        *,
        cron_expression: typing.Optional[builtins.str] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        scripts: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts, typing.Dict[builtins.str, typing.Any]]] = None,
        times: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cron_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#cron_expression DlmLifecyclePolicy#cron_expression}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#location DlmLifecyclePolicy#location}.
        :param scripts: scripts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#scripts DlmLifecyclePolicy#scripts}
        :param times: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#times DlmLifecyclePolicy#times}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleCreateRule(
            cron_expression=cron_expression,
            interval=interval,
            interval_unit=interval_unit,
            location=location,
            scripts=scripts,
            times=times,
        )

        return typing.cast(None, jsii.invoke(self, "putCreateRule", [value]))

    @jsii.member(jsii_name="putCrossRegionCopyRule")
    def put_cross_region_copy_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd84ad164d6cbf41e77c77a883883b7caa92db2619e2ba0cc5721f3c6e3f7acb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCrossRegionCopyRule", [value]))

    @jsii.member(jsii_name="putDeprecateRule")
    def put_deprecate_rule(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule(
            count=count, interval=interval, interval_unit=interval_unit
        )

        return typing.cast(None, jsii.invoke(self, "putDeprecateRule", [value]))

    @jsii.member(jsii_name="putFastRestoreRule")
    def put_fast_restore_rule(
        self,
        *,
        availability_zones: typing.Sequence[builtins.str],
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#availability_zones DlmLifecyclePolicy#availability_zones}.
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule(
            availability_zones=availability_zones,
            count=count,
            interval=interval,
            interval_unit=interval_unit,
        )

        return typing.cast(None, jsii.invoke(self, "putFastRestoreRule", [value]))

    @jsii.member(jsii_name="putRetainRule")
    def put_retain_rule(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleRetainRule(
            count=count, interval=interval, interval_unit=interval_unit
        )

        return typing.cast(None, jsii.invoke(self, "putRetainRule", [value]))

    @jsii.member(jsii_name="putShareRule")
    def put_share_rule(
        self,
        *,
        target_accounts: typing.Sequence[builtins.str],
        unshare_interval: typing.Optional[jsii.Number] = None,
        unshare_interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_accounts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#target_accounts DlmLifecyclePolicy#target_accounts}.
        :param unshare_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#unshare_interval DlmLifecyclePolicy#unshare_interval}.
        :param unshare_interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#unshare_interval_unit DlmLifecyclePolicy#unshare_interval_unit}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleShareRule(
            target_accounts=target_accounts,
            unshare_interval=unshare_interval,
            unshare_interval_unit=unshare_interval_unit,
        )

        return typing.cast(None, jsii.invoke(self, "putShareRule", [value]))

    @jsii.member(jsii_name="resetArchiveRule")
    def reset_archive_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchiveRule", []))

    @jsii.member(jsii_name="resetCopyTags")
    def reset_copy_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyTags", []))

    @jsii.member(jsii_name="resetCrossRegionCopyRule")
    def reset_cross_region_copy_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossRegionCopyRule", []))

    @jsii.member(jsii_name="resetDeprecateRule")
    def reset_deprecate_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeprecateRule", []))

    @jsii.member(jsii_name="resetFastRestoreRule")
    def reset_fast_restore_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFastRestoreRule", []))

    @jsii.member(jsii_name="resetShareRule")
    def reset_share_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShareRule", []))

    @jsii.member(jsii_name="resetTagsToAdd")
    def reset_tags_to_add(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsToAdd", []))

    @jsii.member(jsii_name="resetVariableTags")
    def reset_variable_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariableTags", []))

    @builtins.property
    @jsii.member(jsii_name="archiveRule")
    def archive_rule(
        self,
    ) -> DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleOutputReference, jsii.get(self, "archiveRule"))

    @builtins.property
    @jsii.member(jsii_name="createRule")
    def create_rule(
        self,
    ) -> DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleOutputReference, jsii.get(self, "createRule"))

    @builtins.property
    @jsii.member(jsii_name="crossRegionCopyRule")
    def cross_region_copy_rule(
        self,
    ) -> DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleList:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleList, jsii.get(self, "crossRegionCopyRule"))

    @builtins.property
    @jsii.member(jsii_name="deprecateRule")
    def deprecate_rule(
        self,
    ) -> DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRuleOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRuleOutputReference, jsii.get(self, "deprecateRule"))

    @builtins.property
    @jsii.member(jsii_name="fastRestoreRule")
    def fast_restore_rule(
        self,
    ) -> DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRuleOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRuleOutputReference, jsii.get(self, "fastRestoreRule"))

    @builtins.property
    @jsii.member(jsii_name="retainRule")
    def retain_rule(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsScheduleRetainRuleOutputReference":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleRetainRuleOutputReference", jsii.get(self, "retainRule"))

    @builtins.property
    @jsii.member(jsii_name="shareRule")
    def share_rule(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsScheduleShareRuleOutputReference":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleShareRuleOutputReference", jsii.get(self, "shareRule"))

    @builtins.property
    @jsii.member(jsii_name="archiveRuleInput")
    def archive_rule_input(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule], jsii.get(self, "archiveRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="copyTagsInput")
    def copy_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "copyTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="createRuleInput")
    def create_rule_input(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRule], jsii.get(self, "createRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="crossRegionCopyRuleInput")
    def cross_region_copy_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]]], jsii.get(self, "crossRegionCopyRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="deprecateRuleInput")
    def deprecate_rule_input(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule], jsii.get(self, "deprecateRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="fastRestoreRuleInput")
    def fast_restore_rule_input(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule], jsii.get(self, "fastRestoreRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="retainRuleInput")
    def retain_rule_input(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleRetainRule"]:
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleRetainRule"], jsii.get(self, "retainRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="shareRuleInput")
    def share_rule_input(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleShareRule"]:
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleShareRule"], jsii.get(self, "shareRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsToAddInput")
    def tags_to_add_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsToAddInput"))

    @builtins.property
    @jsii.member(jsii_name="variableTagsInput")
    def variable_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "variableTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="copyTags")
    def copy_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "copyTags"))

    @copy_tags.setter
    def copy_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6a59945949062caa16860f62ead5611bd0a63f10954588e068b27cc0e13be8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e3bd371a178d939e8e33b30f181d34912fde367a595cee6fdb4c1d7ec806c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsToAdd")
    def tags_to_add(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsToAdd"))

    @tags_to_add.setter
    def tags_to_add(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb19b5a4863e9824cc293cccee2eacbc6d46f321a4311967f067b9891926b8f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsToAdd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="variableTags")
    def variable_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "variableTags"))

    @variable_tags.setter
    def variable_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a6e957943efdd835e9660254bfa19273d5f5a155577c33cb38d9734c54b50dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variableTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsSchedule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsSchedule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsSchedule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5b4f7fd437f15f94215ad5d8fb7272db71ab652aeb885c367acab24fef3991f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleRetainRule",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "interval": "interval",
        "interval_unit": "intervalUnit",
    },
)
class DlmLifecyclePolicyPolicyDetailsScheduleRetainRule:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff008472d933ce5b02ef6718abdcec211979bc56941d13684eb3c8af0a3a5386)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if interval is not None:
            self._values["interval"] = interval
        if interval_unit is not None:
            self._values["interval_unit"] = interval_unit

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.'''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.'''
        result = self._values.get("interval_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleRetainRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleRetainRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleRetainRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20c82ba153deb4e42412278c5ff4c3978e353856373421bcebe05e87666c19ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetIntervalUnit")
    def reset_interval_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalUnit", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalUnitInput")
    def interval_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7f58445a3517777c68d37f23d039e2de05a89a6b4ebcba5f0e1de1dce01b1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b49e48cdaac1fc4deb63760d9dcc33a01319cee9f3e1b1d22b401c254203753)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalUnit")
    def interval_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intervalUnit"))

    @interval_unit.setter
    def interval_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7897c3ab58312739c892efe5565588c16b6733ba268a18d0ccdc8471d7a4f171)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleRetainRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleRetainRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleRetainRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f184fb773115c959fe99d97aa05809a71c77f11640c0b6475835e246f7f4f26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleShareRule",
    jsii_struct_bases=[],
    name_mapping={
        "target_accounts": "targetAccounts",
        "unshare_interval": "unshareInterval",
        "unshare_interval_unit": "unshareIntervalUnit",
    },
)
class DlmLifecyclePolicyPolicyDetailsScheduleShareRule:
    def __init__(
        self,
        *,
        target_accounts: typing.Sequence[builtins.str],
        unshare_interval: typing.Optional[jsii.Number] = None,
        unshare_interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_accounts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#target_accounts DlmLifecyclePolicy#target_accounts}.
        :param unshare_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#unshare_interval DlmLifecyclePolicy#unshare_interval}.
        :param unshare_interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#unshare_interval_unit DlmLifecyclePolicy#unshare_interval_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c11fcdd2f559b49a8ada3dacd4c9062022bca6fd14f206407b0775b73e5cac75)
            check_type(argname="argument target_accounts", value=target_accounts, expected_type=type_hints["target_accounts"])
            check_type(argname="argument unshare_interval", value=unshare_interval, expected_type=type_hints["unshare_interval"])
            check_type(argname="argument unshare_interval_unit", value=unshare_interval_unit, expected_type=type_hints["unshare_interval_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_accounts": target_accounts,
        }
        if unshare_interval is not None:
            self._values["unshare_interval"] = unshare_interval
        if unshare_interval_unit is not None:
            self._values["unshare_interval_unit"] = unshare_interval_unit

    @builtins.property
    def target_accounts(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#target_accounts DlmLifecyclePolicy#target_accounts}.'''
        result = self._values.get("target_accounts")
        assert result is not None, "Required property 'target_accounts' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def unshare_interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#unshare_interval DlmLifecyclePolicy#unshare_interval}.'''
        result = self._values.get("unshare_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unshare_interval_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dlm_lifecycle_policy#unshare_interval_unit DlmLifecyclePolicy#unshare_interval_unit}.'''
        result = self._values.get("unshare_interval_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleShareRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleShareRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleShareRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efd125f9c4c3dad6262e5fa4f1e2c498cd4f522b82a0ddd85e15e835b9142c96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUnshareInterval")
    def reset_unshare_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnshareInterval", []))

    @jsii.member(jsii_name="resetUnshareIntervalUnit")
    def reset_unshare_interval_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnshareIntervalUnit", []))

    @builtins.property
    @jsii.member(jsii_name="targetAccountsInput")
    def target_accounts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetAccountsInput"))

    @builtins.property
    @jsii.member(jsii_name="unshareIntervalInput")
    def unshare_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "unshareIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="unshareIntervalUnitInput")
    def unshare_interval_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unshareIntervalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="targetAccounts")
    def target_accounts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetAccounts"))

    @target_accounts.setter
    def target_accounts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42573d3e43c36c321ad6b5902dcc6018edd7f16715dcb3312583bbc6f45a1cb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetAccounts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unshareInterval")
    def unshare_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unshareInterval"))

    @unshare_interval.setter
    def unshare_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b7a106fa85c83827424cd6c8eea4b690153d1140e4729939e92905ce725f30a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unshareInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unshareIntervalUnit")
    def unshare_interval_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unshareIntervalUnit"))

    @unshare_interval_unit.setter
    def unshare_interval_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef1fc058f58edd7ddab42d238974708ff91804ebd7adab6795a3238345974a68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unshareIntervalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleShareRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleShareRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleShareRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a989cec4c83bafd39edf6ac278c1c6fc558c7915f6d412899c709d9f834e72f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DlmLifecyclePolicy",
    "DlmLifecyclePolicyConfig",
    "DlmLifecyclePolicyPolicyDetails",
    "DlmLifecyclePolicyPolicyDetailsAction",
    "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy",
    "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration",
    "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfigurationOutputReference",
    "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyList",
    "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyOutputReference",
    "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule",
    "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsActionOutputReference",
    "DlmLifecyclePolicyPolicyDetailsEventSource",
    "DlmLifecyclePolicyPolicyDetailsEventSourceOutputReference",
    "DlmLifecyclePolicyPolicyDetailsEventSourceParameters",
    "DlmLifecyclePolicyPolicyDetailsEventSourceParametersOutputReference",
    "DlmLifecyclePolicyPolicyDetailsExclusions",
    "DlmLifecyclePolicyPolicyDetailsExclusionsOutputReference",
    "DlmLifecyclePolicyPolicyDetailsOutputReference",
    "DlmLifecyclePolicyPolicyDetailsParameters",
    "DlmLifecyclePolicyPolicyDetailsParametersOutputReference",
    "DlmLifecyclePolicyPolicyDetailsSchedule",
    "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier",
    "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTierOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleCreateRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts",
    "DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScriptsOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleList",
    "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleList",
    "DlmLifecyclePolicyPolicyDetailsScheduleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleRetainRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleRetainRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleShareRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleShareRuleOutputReference",
]

publication.publish()

def _typecheckingstub__5d69f68b8aa75af137750b30d5221f328af68ac1b07e4988a3c2594b206b92fd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    description: builtins.str,
    execution_role_arn: builtins.str,
    policy_details: typing.Union[DlmLifecyclePolicyPolicyDetails, typing.Dict[builtins.str, typing.Any]],
    default_policy: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__38685a4e800351ca2909b4324aaa6110638b7cb4f43ea16d400dd551234189b8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fbffc7d1c2125d8bf0d00d05b3652c91177717706d975000a1bcc9cb7209eb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc1475b4cdafd057b5dcaf493e982d95d236c079b1bd42dce5d39eae8eddeab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f9a927808e4d610d6a67e12f9ab9b1c394dd949506c0b5024129b67d49866f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6f2af90e344bfb2b7625bddc30430e61b850cff8b7ef786eb016a46d1341e4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183dc8677c22067bd93e98b0aeb308d865eac54a26f97bfd26313e3645c6bb6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8890f6793724f7b25b9e57a659019322b668eca6d27db32a42e0dcb6357f536(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3260b8983fa1403c04fcdaf84f15dce954d46abc45cbb89668ca357a66d7bd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b024e3b90ff3c1d69c10c381ea3ea7b4d4867c1882435db717d35c571dbdf489(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ddb319fd3cfe27fa82e9b292ce077d8c37ffec3331e9c76521ce54d1e53b46(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: builtins.str,
    execution_role_arn: builtins.str,
    policy_details: typing.Union[DlmLifecyclePolicyPolicyDetails, typing.Dict[builtins.str, typing.Any]],
    default_policy: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e330e7cdd1885889e82af8a2a9f5024bc6d82c73a6dba43fbd54215367c3e54(
    *,
    action: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsAction, typing.Dict[builtins.str, typing.Any]]] = None,
    copy_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    create_interval: typing.Optional[jsii.Number] = None,
    event_source: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsEventSource, typing.Dict[builtins.str, typing.Any]]] = None,
    exclusions: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsExclusions, typing.Dict[builtins.str, typing.Any]]] = None,
    extend_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    parameters: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    policy_language: typing.Optional[builtins.str] = None,
    policy_type: typing.Optional[builtins.str] = None,
    resource_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_type: typing.Optional[builtins.str] = None,
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    retain_interval: typing.Optional[jsii.Number] = None,
    schedule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DlmLifecyclePolicyPolicyDetailsSchedule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178d2ead47d60e56af30458cb553062298eb2891203c12bae99a9b00282a466c(
    *,
    cross_region_copy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f39785a1790e58a6106b3cb8153288e0d540c9950707c650fe457572711589(
    *,
    encryption_configuration: typing.Union[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]],
    target: builtins.str,
    retain_rule: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6770e572c11f7469dbb859326afef89e28a972738906d673e7c22738f3bb6c(
    *,
    cmk_arn: typing.Optional[builtins.str] = None,
    encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53608064370bb39a1227e45c6b089bcde5d97d80a3c692680ce4a52ec6766ec8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a7ef27d6dec57430a35f4468f5692594fe1a8232244dabdb202be00a624670(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311e8fb35152696cf11d19529fe48ff55415ec80efbb100896e712dc6227d55b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70974fcb1c1620c665c368c153c574af1c08a871207340c79b08f319ca0005c7(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__646e4bb20f519776c347c66fbf0e1dff0fda3bdadb42da8e9b849c3d367f76f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be020bec07783a085abf336e66c01ad9d8d47137e7ae18a5756d8fcdd182c65(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf75f7e6881f425e9c1ee464677b965a4971d1da7f16d2576bf2d5806efa778(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0376fa006d8e22a1c3d30d293526d2be545e55450b70ac45892df01f2e2f276e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e397e5369f01567baed64452a67ba7080f3aabe054b234b6658933a8d99e50(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc591f9b5d9c6d9bb149ed13148f19ad0cf868231ad3fb543ce67bff9d9e64d3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a37d05e9b03cdda86693d6a93cf5da253c2aa4e4f3c7be2b6a0c44f892cc86fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__959d9904d24c1225522b3db91630233518cea8327e3b03e1b71e4464f7eea468(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86ba4cc95ec44653f97518b1e7e4ad5d9c3f980af8583bf77ead5b46e5bdc7e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46bc3eec9d2dbcdfd4ef268c6dcc7a2264b1d12fb4b25127bd16ba9b29ce660d(
    *,
    interval: jsii.Number,
    interval_unit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6691e6a1884aa8edc3f4bf09fa951410efb894fa445286f0a1fde67a761c81b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d470fa773f91d52688e65112ebb43c8c3ecedef6b85248a52779ae65280f8a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f0373d586561e3d53fef37a1a0a56b72a94d0bb014e1d61efb2afa4a7cbce0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9b8da59b9edf7d7b2e0f9c0a17b95df4d09ea47277e7c39a0a1539fd4976ed(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26cc2be8bc5401517394b6ebebfe3a98ea3a4cae1ba4d3e03bcf868521d31858(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a0adf6170cb26ed585d6802166627cb046dc8ad73dc9f744665f671b27003f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bbcacc3a59e50a825c3053e357819e2cb36dc9129acb64572b13d388dcdc8e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d6653c0d9960da52f589818f4dc2cdfdac90e0b78d48e1f8faff2b2e25c650(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31eac7e36bf0ea3da6f8a49bba37c0a3a43b653cc057890fd5b22523eea586c0(
    *,
    parameters: typing.Union[DlmLifecyclePolicyPolicyDetailsEventSourceParameters, typing.Dict[builtins.str, typing.Any]],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4694be197b24a4dd120a338f97c722f1873635327f8e0851c0e3b13b05ee2c0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1757da63315f4a9b5c97dd910a77240e4f7af4e27b9d42f090433fe890754e10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__597557d0d40b0635bb675ab882a92b80aa2134985123321c1e77d35aa94391a1(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d9f7731e7dd60de7041643b3d42681d6c9452831207828507df5de6b696c408(
    *,
    description_regex: builtins.str,
    event_type: builtins.str,
    snapshot_owner: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb5136646d2ef2a4e4f6ae6a25f21b9c9d046491521fac4aff3718da40e968e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80cd553d7f2d59d98b5d246f7cb480b09020dcdd78a7fb271e1a88f47189dc5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__945551cf93e0265ebc5e56e32e1239b9db4059b09db274a8d8cf74b42c11579a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__589d59a72ea9ca5e64242b5f9b7f66462e4d1720628b9155f7f5f3240f800cee(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82fc70b5ae17bf2aa19e932b33aa3cf4890ff1f45fa60fd19d12174f1b58b0e7(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSourceParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675c3fb0c0e25d4ea7405436aa28df543db641f7796f1408469422471de99065(
    *,
    exclude_boot_volumes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclude_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    exclude_volume_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ae5127b182766b5619aff835805fca2ee43cf0b40425258e5fe47a795848f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeca3ce0d3c8b0908254f6315d626bb879239f7492e7b01e7d4926f181cdbdfd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9624cfbfaaece79a91a8af54d642783068a04e8508f5cd3ad4e433dc60f81e61(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b46dd7bbb89c05fcf32b858b4c1472ca99135f53801fd388e81dd19c027a253(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8effdc15f15c6f744e3dc4cb369b11bd3394f44814ecbbbd9ff74622b6f204a5(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsExclusions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b5e05c26fb0752254f7ea1effdaf9307518cb38653f41ecec91777b07bd06b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c725d1e3af4ed938d26576c1ae0ee8ae4bb60071feef981d6fbae953437e85e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DlmLifecyclePolicyPolicyDetailsSchedule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ddbaa044bafce8cf9f39cd454fc4733edfae3d5c2b45dfa2cde838da866cc30(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1002b3d5de4815576f01d280ebc8840ef075a7d46a2804b23ddde9573ee3f41a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc0332f3caf5959db9e3252c9afb02e1a5d05139200a4513d9cddbe41f60f66d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84487e7f6a6835ed94a4ee38d8c60f2de0f602d191d707cb79740709bfd3458(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cabe80f195a653e85d25029efb53ec1621cb2f7582a5358992d192a0f8a7b82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b63ca23ba414bd876c1ee935d3922b99b2346a09fddc02f1870ad206e8d0cd83(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b978e2568904e80e0b01a23e965620b48cc1c23c8996db11a9cd19cf6e8a89b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9afa84d5f0c70a670ca2a55f725b4239a21d7ef3afe2b976563c9abdfead385f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b434f14ac4ff681428f3bce033bf87fd501e954e3515cc1e3b2d6328d50c9c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68273f21fbe7451f18708ec922154cc56bb0452530867d858400dc2f83a0b497(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c844d25800c23e6b46b1e85605f5f40afaccd2fe66191362b05d93237bc0ca14(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb40e657513d8102ad323a1b7c0ac6abbf534f8837561241f335751baa4c06c(
    *,
    exclude_boot_volume: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    no_reboot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ee957c5f0e79a9485c6eec40e4fe5f181bacf1322cabc25ad3c55274126e99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32e6a390857ed24c01bfc636a8b7a2981c81642a764e557a8c3dfcc74c6f02c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173ab6cc615303bf66e8b5f7e5ade1d0799dfdc5c939bfe34bd2ae35752ea329(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42b82d4c27ef8a631c7cc94aaae8ae4335c6ea968e03966a74f11841fb1fc36(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd2abeb5e6e0befa5173a64322545acb6b0cfe1d7bef2ad07a02f120e948e2c9(
    *,
    create_rule: typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleCreateRule, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    retain_rule: typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleRetainRule, typing.Dict[builtins.str, typing.Any]],
    archive_rule: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule, typing.Dict[builtins.str, typing.Any]]] = None,
    copy_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cross_region_copy_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    deprecate_rule: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule, typing.Dict[builtins.str, typing.Any]]] = None,
    fast_restore_rule: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule, typing.Dict[builtins.str, typing.Any]]] = None,
    share_rule: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleShareRule, typing.Dict[builtins.str, typing.Any]]] = None,
    tags_to_add: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    variable_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2afe8342a00c89e2240f847bb9ac5521470f61af7d39687e43e449c0ea793a69(
    *,
    archive_retain_rule: typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90097b0c628fa7399618c6408ccef97facc03e9f066a5bd21b1163a780cb4383(
    *,
    retention_archive_tier: typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6334dbca8c00f93d77d7a08f7ccfd8db4a3891d1ab272c3633441e35184ee56d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c809cdf2f984796d8fda7d51636df8480f5a5af893f9ac690fc6285960e4f549(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e56253935adb255723a0524d88cebf3c1200534208240f1917e62b4776a9bc82(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b84d974c3bbd3681ac745660d64784be0aab98cac92a0e745a54050b8fe2dd9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7aebde98b2d5f0caf3dc47e9cbe5cec5fd60adaea9724049b09dee8df7626fe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59cc55275d5fed8a5813030345b492b9b22ca42bd6ff7f8572cb7b40d5d346d8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf315935c06dc3bd9043ca0349e58a2a0641a89825b357d7c6f72461cda56376(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe02d5425bd6b8e472e5f51c04df3cba36f1ea391d0b2ab439189f166e72984(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a82350f3fcb1613112b97ee4938785dc9a4a8ec9e25b60479c43cf9e727619c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d15d044404f4b5b59fe58afa0d2e60d27be9110cd6f25685b2328f9a29cf3751(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29646122068fd6436132ab85b0f0194bfefa9ccc572a23a11b4a1f6e99781428(
    *,
    cron_expression: typing.Optional[builtins.str] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    scripts: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts, typing.Dict[builtins.str, typing.Any]]] = None,
    times: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00663b822ba754432609693e450b1d73c3b619b4c48e276f3230cb4aea2fb30e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1612ecd610e246fb011d339cf67c5544782d5a0c1c891608bdf11d044c2ead3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e003c6ca50b22bb962fc7bcebee6611543c4861240e41710bc7d6e3bef2563c3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61728cd297bb67766970abf9a38dffb0dc1ba5dec098bc20bcdd23e0dddfe504(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4e1ee1d78ce3c699893f85e309d859c05e9e8faeb83daacacda750ce310290(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6469f867a1ef48d9bdbf16eb0fdf5397faad84309562aa89e7d73db13d6f8fba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed617d402b6f264357439c59d557b3181cb38f946d2d7f1c7e65c12dd6565996(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__200d2f20e562b31cf22ae7d8f9e428a5fc46bb3ecb01e498954bcd3e2c8a1162(
    *,
    execution_handler: builtins.str,
    execute_operation_on_script_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    execution_handler_service: typing.Optional[builtins.str] = None,
    execution_timeout: typing.Optional[jsii.Number] = None,
    maximum_retry_count: typing.Optional[jsii.Number] = None,
    stages: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a78dc264b2c3e3d0643411cdfe602a46d82d7c5973c7968fe45268a843d5a678(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c181d5338ac2533976cdb75269f16af80a6a6662052025eab28a219415bce43e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5169aafcd513cae0a1e3e5d16e2290e512a3a81477dc834765cfa891be658c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b60b3c94e8745eb1e0c02c40e0fa3ff8e72b9efe9f60550c44642199523d41b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17bf9f923aebe47ee682284837c0f3af923235f3a39a2be5886f87a2dcfe0125(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9790d6cc67b29369f6b8c3087603babca975de874e9c7333b7a9b94d31623377(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6818506cdac07bcc60cb190c937a4eb2bce086a1522b9f5e3650d95d1b54f3e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d509caa3eefbd7d66164303c1ead31c28fe36ff372a753374b77c613c1ce736a(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8970e6173d98abbfe5d0ded5297854793937febd74c33e41588334ff1b59852(
    *,
    encrypted: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    cmk_arn: typing.Optional[builtins.str] = None,
    copy_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deprecate_rule: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule, typing.Dict[builtins.str, typing.Any]]] = None,
    retain_rule: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule, typing.Dict[builtins.str, typing.Any]]] = None,
    target: typing.Optional[builtins.str] = None,
    target_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4b7f65ddf09ad869a3d872a65323f1f02886d677deebc258091370c1d33c56(
    *,
    interval: jsii.Number,
    interval_unit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf545e2c016fe1df044ddcfd051ec62fdc4291ebb0d6cdd2c53c217ceec795f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2ad3295856779507cb3c8a0340162038f2fc7753fbddd570d77ef977600e31(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb3d058f7f93d0b29a1de97ea2fd001a6a9d6c294cbc19f0c28efcf5bbb588fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5211d4ebfa2186fab2502f8c4d396371ae1d8a527d1e9fbfb5cb290ba4f0079d(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6374b0924206eb61157cc1c7d67e24504c0950e37f416da98f490f0f1f78386(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3001ef503b1435d0cc398fea273d1095162e8a97c28058132887ca0207fdb72b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487b7896fe34ad3bc793aff1ccf61f251891620f19bc7e2019d890613a54aa88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665aa08b61889d062fbd48b2b92cab857a69d6964eb3c2e402f3f43ef32adf3a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ab49cdf7d86c54cdcacc138458e9f7be7068607ee0c8231181311890a35d5e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7570faf210cba50a544f968cea8256f4712eb6913ea158651dbc4067eb49a5f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0885292d869a85fd049f34c2dc0874eb7545b2ef42851c28916f7c754d4948c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325e276f988f98ab8217629edb3e1bb553ff8f21a5495e16eeacff1b882b8ca3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62120b951be3559046c42c7641bff19beb8d787c124a0df6ac97d097009450e1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a1f263bfb6bf3371fce27cbda9e77cf65873ee6d3ef05f5c9d3d87c836fbfb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece47337370ae832d6cb401c8636216062bc6fc8df4df1e716ec208721265c56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec4aee510c2d1934b2cc36a6a978b6c9da3400592d62f4b6260962acfb19221(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea0c6b885b2e9a05d66bc58f1a9551a77fafe7743d68d961659da7c4e52cf54(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73399a56d282e97de3f55816b35011bb8bea89e95fee6641b041c3c03eda3459(
    *,
    interval: jsii.Number,
    interval_unit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__725dfe082fde14dfb9857ceb92cea3cad15509ca515f971ff91a0714e0cda023(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31a9cadf9377b5a154c79e62f8bcb2686c3a71f55ae6b1fd6b419730b684133(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16ce76333fc72975d2126febd5df3412ad900471896d1424d137d665fe171a6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce4d145d7b1c4370ed2087e99eb0e5e84ba052937bfe5e01dcf45d6a95f36e1(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8b5d500dba036f67ef467e6d8f5c801ce365520db9235b942f1b83075610cf(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__851fd8bd01bb36088cfc9b9cbf117420dd58fd3617140bfb8c890af2646657af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d749acd24d7e267cef86a8707198914e3caf4464c96fb99d11c6ec57cebf6dd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a32149f59e612b367f483724d06f85734c9d09ac166b76f3aa9502e96d2615f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b778cd9c430df289b2f6c2ec4571b2e232dbfa273f7d82731a01364f8b1a699f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23eea193861826ba0b60d346b281b0220f5470cc7c368881d96d885f42b30a10(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff9c85dc3fc85490e77a4b7e8c4cbaaacfe07988ba491a67517d8e9e3d29db71(
    *,
    availability_zones: typing.Sequence[builtins.str],
    count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097f5dd289b2790bf3f07b1f86d321b6efa83b1c4ada79e7824b535048f72b20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ea84d85f89fef367020acb4ddb2edfa5e65ef38c21e6cb21165fb363978bdc0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9ac3b173faefbf5310a9a5dab2bf7dc934d2631aeab31a90e4ed16097ba9d69(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f0ca7bf65a63b643bcfb8ff55c675adc645bd06268117081e68ef5e2e977af(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1dcb79f975c426742bb8a94ebe82d110197dd73825a5ac5c80480dcbc159de3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76922bfbffc6af75ef57f3084a81c8681d7b8743d679d447f539da74abe773e4(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d83d295dd6c58e5eddd5571fde69574d7584c406fdb158b106bd52dbccac1e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff25695396c4277fbd90ae3e922b8f03b76c1904e458953b98fd1f09f197ac6a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8466f1a3defe0fad7a3a64a8088b1d1f35bfce1112b8610e4d3d3c93a74594d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1e03fefe07baf9a4f2fd59aed06bd1d2838c99559b4bbebb6d700a450bac23(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1b1e093b18daf6b482d6acea6988e6bd537fb095e1a59b7f950ddb39623311(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6183e0096132132bd64ec28525b719c48c9a148d9ff2cc8920292996bee6dd80(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsSchedule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd285e74d1ac8ec4e65c4c46935aeb2a42ec4337f16792f3fe4d9f9b51c10f5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd84ad164d6cbf41e77c77a883883b7caa92db2619e2ba0cc5721f3c6e3f7acb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6a59945949062caa16860f62ead5611bd0a63f10954588e068b27cc0e13be8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e3bd371a178d939e8e33b30f181d34912fde367a595cee6fdb4c1d7ec806c09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb19b5a4863e9824cc293cccee2eacbc6d46f321a4311967f067b9891926b8f0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6e957943efdd835e9660254bfa19273d5f5a155577c33cb38d9734c54b50dd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b4f7fd437f15f94215ad5d8fb7272db71ab652aeb885c367acab24fef3991f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsSchedule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff008472d933ce5b02ef6718abdcec211979bc56941d13684eb3c8af0a3a5386(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c82ba153deb4e42412278c5ff4c3978e353856373421bcebe05e87666c19ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7f58445a3517777c68d37f23d039e2de05a89a6b4ebcba5f0e1de1dce01b1d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b49e48cdaac1fc4deb63760d9dcc33a01319cee9f3e1b1d22b401c254203753(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7897c3ab58312739c892efe5565588c16b6733ba268a18d0ccdc8471d7a4f171(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f184fb773115c959fe99d97aa05809a71c77f11640c0b6475835e246f7f4f26(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleRetainRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11fcdd2f559b49a8ada3dacd4c9062022bca6fd14f206407b0775b73e5cac75(
    *,
    target_accounts: typing.Sequence[builtins.str],
    unshare_interval: typing.Optional[jsii.Number] = None,
    unshare_interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd125f9c4c3dad6262e5fa4f1e2c498cd4f522b82a0ddd85e15e835b9142c96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42573d3e43c36c321ad6b5902dcc6018edd7f16715dcb3312583bbc6f45a1cb8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7a106fa85c83827424cd6c8eea4b690153d1140e4729939e92905ce725f30a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1fc058f58edd7ddab42d238974708ff91804ebd7adab6795a3238345974a68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a989cec4c83bafd39edf6ac278c1c6fc558c7915f6d412899c709d9f834e72f2(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleShareRule],
) -> None:
    """Type checking stubs"""
    pass
