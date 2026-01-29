r'''
# `aws_sesv2_configuration_set`

Refer to the Terraform Registry for docs: [`aws_sesv2_configuration_set`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set).
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


class Sesv2ConfigurationSet(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSet.Sesv2ConfigurationSet",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set aws_sesv2_configuration_set}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        configuration_set_name: builtins.str,
        delivery_options: typing.Optional[typing.Union["Sesv2ConfigurationSetDeliveryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        reputation_options: typing.Optional[typing.Union["Sesv2ConfigurationSetReputationOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        sending_options: typing.Optional[typing.Union["Sesv2ConfigurationSetSendingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        suppression_options: typing.Optional[typing.Union["Sesv2ConfigurationSetSuppressionOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tracking_options: typing.Optional[typing.Union["Sesv2ConfigurationSetTrackingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        vdm_options: typing.Optional[typing.Union["Sesv2ConfigurationSetVdmOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set aws_sesv2_configuration_set} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param configuration_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#configuration_set_name Sesv2ConfigurationSet#configuration_set_name}.
        :param delivery_options: delivery_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#delivery_options Sesv2ConfigurationSet#delivery_options}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#id Sesv2ConfigurationSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#region Sesv2ConfigurationSet#region}
        :param reputation_options: reputation_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#reputation_options Sesv2ConfigurationSet#reputation_options}
        :param sending_options: sending_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#sending_options Sesv2ConfigurationSet#sending_options}
        :param suppression_options: suppression_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#suppression_options Sesv2ConfigurationSet#suppression_options}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#tags Sesv2ConfigurationSet#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#tags_all Sesv2ConfigurationSet#tags_all}.
        :param tracking_options: tracking_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#tracking_options Sesv2ConfigurationSet#tracking_options}
        :param vdm_options: vdm_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#vdm_options Sesv2ConfigurationSet#vdm_options}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20fbba189de34038fbb534c89b9413f229b4cd963a3460e10adc3fdcd81eeeef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = Sesv2ConfigurationSetConfig(
            configuration_set_name=configuration_set_name,
            delivery_options=delivery_options,
            id=id,
            region=region,
            reputation_options=reputation_options,
            sending_options=sending_options,
            suppression_options=suppression_options,
            tags=tags,
            tags_all=tags_all,
            tracking_options=tracking_options,
            vdm_options=vdm_options,
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
        '''Generates CDKTF code for importing a Sesv2ConfigurationSet resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Sesv2ConfigurationSet to import.
        :param import_from_id: The id of the existing Sesv2ConfigurationSet that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Sesv2ConfigurationSet to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c3499a81d1d8bc4b1005cc71a50cc531df870b39ab4598577584a58a4b6ae8c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDeliveryOptions")
    def put_delivery_options(
        self,
        *,
        max_delivery_seconds: typing.Optional[jsii.Number] = None,
        sending_pool_name: typing.Optional[builtins.str] = None,
        tls_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_delivery_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#max_delivery_seconds Sesv2ConfigurationSet#max_delivery_seconds}.
        :param sending_pool_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#sending_pool_name Sesv2ConfigurationSet#sending_pool_name}.
        :param tls_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#tls_policy Sesv2ConfigurationSet#tls_policy}.
        '''
        value = Sesv2ConfigurationSetDeliveryOptions(
            max_delivery_seconds=max_delivery_seconds,
            sending_pool_name=sending_pool_name,
            tls_policy=tls_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putDeliveryOptions", [value]))

    @jsii.member(jsii_name="putReputationOptions")
    def put_reputation_options(
        self,
        *,
        reputation_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param reputation_metrics_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#reputation_metrics_enabled Sesv2ConfigurationSet#reputation_metrics_enabled}.
        '''
        value = Sesv2ConfigurationSetReputationOptions(
            reputation_metrics_enabled=reputation_metrics_enabled
        )

        return typing.cast(None, jsii.invoke(self, "putReputationOptions", [value]))

    @jsii.member(jsii_name="putSendingOptions")
    def put_sending_options(
        self,
        *,
        sending_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param sending_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#sending_enabled Sesv2ConfigurationSet#sending_enabled}.
        '''
        value = Sesv2ConfigurationSetSendingOptions(sending_enabled=sending_enabled)

        return typing.cast(None, jsii.invoke(self, "putSendingOptions", [value]))

    @jsii.member(jsii_name="putSuppressionOptions")
    def put_suppression_options(
        self,
        *,
        suppressed_reasons: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param suppressed_reasons: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#suppressed_reasons Sesv2ConfigurationSet#suppressed_reasons}.
        '''
        value = Sesv2ConfigurationSetSuppressionOptions(
            suppressed_reasons=suppressed_reasons
        )

        return typing.cast(None, jsii.invoke(self, "putSuppressionOptions", [value]))

    @jsii.member(jsii_name="putTrackingOptions")
    def put_tracking_options(
        self,
        *,
        custom_redirect_domain: builtins.str,
        https_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_redirect_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#custom_redirect_domain Sesv2ConfigurationSet#custom_redirect_domain}.
        :param https_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#https_policy Sesv2ConfigurationSet#https_policy}.
        '''
        value = Sesv2ConfigurationSetTrackingOptions(
            custom_redirect_domain=custom_redirect_domain, https_policy=https_policy
        )

        return typing.cast(None, jsii.invoke(self, "putTrackingOptions", [value]))

    @jsii.member(jsii_name="putVdmOptions")
    def put_vdm_options(
        self,
        *,
        dashboard_options: typing.Optional[typing.Union["Sesv2ConfigurationSetVdmOptionsDashboardOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        guardian_options: typing.Optional[typing.Union["Sesv2ConfigurationSetVdmOptionsGuardianOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dashboard_options: dashboard_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#dashboard_options Sesv2ConfigurationSet#dashboard_options}
        :param guardian_options: guardian_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#guardian_options Sesv2ConfigurationSet#guardian_options}
        '''
        value = Sesv2ConfigurationSetVdmOptions(
            dashboard_options=dashboard_options, guardian_options=guardian_options
        )

        return typing.cast(None, jsii.invoke(self, "putVdmOptions", [value]))

    @jsii.member(jsii_name="resetDeliveryOptions")
    def reset_delivery_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeliveryOptions", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetReputationOptions")
    def reset_reputation_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReputationOptions", []))

    @jsii.member(jsii_name="resetSendingOptions")
    def reset_sending_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendingOptions", []))

    @jsii.member(jsii_name="resetSuppressionOptions")
    def reset_suppression_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuppressionOptions", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTrackingOptions")
    def reset_tracking_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrackingOptions", []))

    @jsii.member(jsii_name="resetVdmOptions")
    def reset_vdm_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVdmOptions", []))

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
    @jsii.member(jsii_name="deliveryOptions")
    def delivery_options(self) -> "Sesv2ConfigurationSetDeliveryOptionsOutputReference":
        return typing.cast("Sesv2ConfigurationSetDeliveryOptionsOutputReference", jsii.get(self, "deliveryOptions"))

    @builtins.property
    @jsii.member(jsii_name="reputationOptions")
    def reputation_options(
        self,
    ) -> "Sesv2ConfigurationSetReputationOptionsOutputReference":
        return typing.cast("Sesv2ConfigurationSetReputationOptionsOutputReference", jsii.get(self, "reputationOptions"))

    @builtins.property
    @jsii.member(jsii_name="sendingOptions")
    def sending_options(self) -> "Sesv2ConfigurationSetSendingOptionsOutputReference":
        return typing.cast("Sesv2ConfigurationSetSendingOptionsOutputReference", jsii.get(self, "sendingOptions"))

    @builtins.property
    @jsii.member(jsii_name="suppressionOptions")
    def suppression_options(
        self,
    ) -> "Sesv2ConfigurationSetSuppressionOptionsOutputReference":
        return typing.cast("Sesv2ConfigurationSetSuppressionOptionsOutputReference", jsii.get(self, "suppressionOptions"))

    @builtins.property
    @jsii.member(jsii_name="trackingOptions")
    def tracking_options(self) -> "Sesv2ConfigurationSetTrackingOptionsOutputReference":
        return typing.cast("Sesv2ConfigurationSetTrackingOptionsOutputReference", jsii.get(self, "trackingOptions"))

    @builtins.property
    @jsii.member(jsii_name="vdmOptions")
    def vdm_options(self) -> "Sesv2ConfigurationSetVdmOptionsOutputReference":
        return typing.cast("Sesv2ConfigurationSetVdmOptionsOutputReference", jsii.get(self, "vdmOptions"))

    @builtins.property
    @jsii.member(jsii_name="configurationSetNameInput")
    def configuration_set_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configurationSetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryOptionsInput")
    def delivery_options_input(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetDeliveryOptions"]:
        return typing.cast(typing.Optional["Sesv2ConfigurationSetDeliveryOptions"], jsii.get(self, "deliveryOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="reputationOptionsInput")
    def reputation_options_input(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetReputationOptions"]:
        return typing.cast(typing.Optional["Sesv2ConfigurationSetReputationOptions"], jsii.get(self, "reputationOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="sendingOptionsInput")
    def sending_options_input(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetSendingOptions"]:
        return typing.cast(typing.Optional["Sesv2ConfigurationSetSendingOptions"], jsii.get(self, "sendingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="suppressionOptionsInput")
    def suppression_options_input(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetSuppressionOptions"]:
        return typing.cast(typing.Optional["Sesv2ConfigurationSetSuppressionOptions"], jsii.get(self, "suppressionOptionsInput"))

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
    @jsii.member(jsii_name="trackingOptionsInput")
    def tracking_options_input(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetTrackingOptions"]:
        return typing.cast(typing.Optional["Sesv2ConfigurationSetTrackingOptions"], jsii.get(self, "trackingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="vdmOptionsInput")
    def vdm_options_input(self) -> typing.Optional["Sesv2ConfigurationSetVdmOptions"]:
        return typing.cast(typing.Optional["Sesv2ConfigurationSetVdmOptions"], jsii.get(self, "vdmOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationSetName")
    def configuration_set_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configurationSetName"))

    @configuration_set_name.setter
    def configuration_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26c48eb39f02e1e9f138e975dba0a9b89c089a4eb0bdd42f92251412bb041c92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationSetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__798b1311039f43b52d50391acafb3c3e112ebb5fc7b481cccbaa3e9028709bc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3387e1b47199ea779ab93140e9f35ce73cf127a611ade7e6c0fca24aa69c57a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e63e9e72e56c42cafb629f5223b3e7d6053b181addb6d2c2001398bccf1849)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc3e857d03540a19a314a80522d7690a8cfebc367ae367772536c0a9d3839fff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSet.Sesv2ConfigurationSetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "configuration_set_name": "configurationSetName",
        "delivery_options": "deliveryOptions",
        "id": "id",
        "region": "region",
        "reputation_options": "reputationOptions",
        "sending_options": "sendingOptions",
        "suppression_options": "suppressionOptions",
        "tags": "tags",
        "tags_all": "tagsAll",
        "tracking_options": "trackingOptions",
        "vdm_options": "vdmOptions",
    },
)
class Sesv2ConfigurationSetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        configuration_set_name: builtins.str,
        delivery_options: typing.Optional[typing.Union["Sesv2ConfigurationSetDeliveryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        reputation_options: typing.Optional[typing.Union["Sesv2ConfigurationSetReputationOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        sending_options: typing.Optional[typing.Union["Sesv2ConfigurationSetSendingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        suppression_options: typing.Optional[typing.Union["Sesv2ConfigurationSetSuppressionOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tracking_options: typing.Optional[typing.Union["Sesv2ConfigurationSetTrackingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        vdm_options: typing.Optional[typing.Union["Sesv2ConfigurationSetVdmOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param configuration_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#configuration_set_name Sesv2ConfigurationSet#configuration_set_name}.
        :param delivery_options: delivery_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#delivery_options Sesv2ConfigurationSet#delivery_options}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#id Sesv2ConfigurationSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#region Sesv2ConfigurationSet#region}
        :param reputation_options: reputation_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#reputation_options Sesv2ConfigurationSet#reputation_options}
        :param sending_options: sending_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#sending_options Sesv2ConfigurationSet#sending_options}
        :param suppression_options: suppression_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#suppression_options Sesv2ConfigurationSet#suppression_options}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#tags Sesv2ConfigurationSet#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#tags_all Sesv2ConfigurationSet#tags_all}.
        :param tracking_options: tracking_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#tracking_options Sesv2ConfigurationSet#tracking_options}
        :param vdm_options: vdm_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#vdm_options Sesv2ConfigurationSet#vdm_options}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(delivery_options, dict):
            delivery_options = Sesv2ConfigurationSetDeliveryOptions(**delivery_options)
        if isinstance(reputation_options, dict):
            reputation_options = Sesv2ConfigurationSetReputationOptions(**reputation_options)
        if isinstance(sending_options, dict):
            sending_options = Sesv2ConfigurationSetSendingOptions(**sending_options)
        if isinstance(suppression_options, dict):
            suppression_options = Sesv2ConfigurationSetSuppressionOptions(**suppression_options)
        if isinstance(tracking_options, dict):
            tracking_options = Sesv2ConfigurationSetTrackingOptions(**tracking_options)
        if isinstance(vdm_options, dict):
            vdm_options = Sesv2ConfigurationSetVdmOptions(**vdm_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01d0f20ee62a57091dca07e0dfbcda27d9f613a3ee045a1682b731319d6ba26d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument configuration_set_name", value=configuration_set_name, expected_type=type_hints["configuration_set_name"])
            check_type(argname="argument delivery_options", value=delivery_options, expected_type=type_hints["delivery_options"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument reputation_options", value=reputation_options, expected_type=type_hints["reputation_options"])
            check_type(argname="argument sending_options", value=sending_options, expected_type=type_hints["sending_options"])
            check_type(argname="argument suppression_options", value=suppression_options, expected_type=type_hints["suppression_options"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument tracking_options", value=tracking_options, expected_type=type_hints["tracking_options"])
            check_type(argname="argument vdm_options", value=vdm_options, expected_type=type_hints["vdm_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration_set_name": configuration_set_name,
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
        if delivery_options is not None:
            self._values["delivery_options"] = delivery_options
        if id is not None:
            self._values["id"] = id
        if region is not None:
            self._values["region"] = region
        if reputation_options is not None:
            self._values["reputation_options"] = reputation_options
        if sending_options is not None:
            self._values["sending_options"] = sending_options
        if suppression_options is not None:
            self._values["suppression_options"] = suppression_options
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if tracking_options is not None:
            self._values["tracking_options"] = tracking_options
        if vdm_options is not None:
            self._values["vdm_options"] = vdm_options

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
    def configuration_set_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#configuration_set_name Sesv2ConfigurationSet#configuration_set_name}.'''
        result = self._values.get("configuration_set_name")
        assert result is not None, "Required property 'configuration_set_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delivery_options(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetDeliveryOptions"]:
        '''delivery_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#delivery_options Sesv2ConfigurationSet#delivery_options}
        '''
        result = self._values.get("delivery_options")
        return typing.cast(typing.Optional["Sesv2ConfigurationSetDeliveryOptions"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#id Sesv2ConfigurationSet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#region Sesv2ConfigurationSet#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reputation_options(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetReputationOptions"]:
        '''reputation_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#reputation_options Sesv2ConfigurationSet#reputation_options}
        '''
        result = self._values.get("reputation_options")
        return typing.cast(typing.Optional["Sesv2ConfigurationSetReputationOptions"], result)

    @builtins.property
    def sending_options(self) -> typing.Optional["Sesv2ConfigurationSetSendingOptions"]:
        '''sending_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#sending_options Sesv2ConfigurationSet#sending_options}
        '''
        result = self._values.get("sending_options")
        return typing.cast(typing.Optional["Sesv2ConfigurationSetSendingOptions"], result)

    @builtins.property
    def suppression_options(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetSuppressionOptions"]:
        '''suppression_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#suppression_options Sesv2ConfigurationSet#suppression_options}
        '''
        result = self._values.get("suppression_options")
        return typing.cast(typing.Optional["Sesv2ConfigurationSetSuppressionOptions"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#tags Sesv2ConfigurationSet#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#tags_all Sesv2ConfigurationSet#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tracking_options(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetTrackingOptions"]:
        '''tracking_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#tracking_options Sesv2ConfigurationSet#tracking_options}
        '''
        result = self._values.get("tracking_options")
        return typing.cast(typing.Optional["Sesv2ConfigurationSetTrackingOptions"], result)

    @builtins.property
    def vdm_options(self) -> typing.Optional["Sesv2ConfigurationSetVdmOptions"]:
        '''vdm_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#vdm_options Sesv2ConfigurationSet#vdm_options}
        '''
        result = self._values.get("vdm_options")
        return typing.cast(typing.Optional["Sesv2ConfigurationSetVdmOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSet.Sesv2ConfigurationSetDeliveryOptions",
    jsii_struct_bases=[],
    name_mapping={
        "max_delivery_seconds": "maxDeliverySeconds",
        "sending_pool_name": "sendingPoolName",
        "tls_policy": "tlsPolicy",
    },
)
class Sesv2ConfigurationSetDeliveryOptions:
    def __init__(
        self,
        *,
        max_delivery_seconds: typing.Optional[jsii.Number] = None,
        sending_pool_name: typing.Optional[builtins.str] = None,
        tls_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_delivery_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#max_delivery_seconds Sesv2ConfigurationSet#max_delivery_seconds}.
        :param sending_pool_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#sending_pool_name Sesv2ConfigurationSet#sending_pool_name}.
        :param tls_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#tls_policy Sesv2ConfigurationSet#tls_policy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72f5c1f56b14b8c39f37db9758067f141e2783b6f61a3dd8c4a3168854553be6)
            check_type(argname="argument max_delivery_seconds", value=max_delivery_seconds, expected_type=type_hints["max_delivery_seconds"])
            check_type(argname="argument sending_pool_name", value=sending_pool_name, expected_type=type_hints["sending_pool_name"])
            check_type(argname="argument tls_policy", value=tls_policy, expected_type=type_hints["tls_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_delivery_seconds is not None:
            self._values["max_delivery_seconds"] = max_delivery_seconds
        if sending_pool_name is not None:
            self._values["sending_pool_name"] = sending_pool_name
        if tls_policy is not None:
            self._values["tls_policy"] = tls_policy

    @builtins.property
    def max_delivery_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#max_delivery_seconds Sesv2ConfigurationSet#max_delivery_seconds}.'''
        result = self._values.get("max_delivery_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sending_pool_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#sending_pool_name Sesv2ConfigurationSet#sending_pool_name}.'''
        result = self._values.get("sending_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#tls_policy Sesv2ConfigurationSet#tls_policy}.'''
        result = self._values.get("tls_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetDeliveryOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Sesv2ConfigurationSetDeliveryOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSet.Sesv2ConfigurationSetDeliveryOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1ad3c958e46379d316893208bcac5bfd8f95a2ce6fa5c07422b58ab420571f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxDeliverySeconds")
    def reset_max_delivery_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDeliverySeconds", []))

    @jsii.member(jsii_name="resetSendingPoolName")
    def reset_sending_pool_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendingPoolName", []))

    @jsii.member(jsii_name="resetTlsPolicy")
    def reset_tls_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="maxDeliverySecondsInput")
    def max_delivery_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDeliverySecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="sendingPoolNameInput")
    def sending_pool_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sendingPoolNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsPolicyInput")
    def tls_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDeliverySeconds")
    def max_delivery_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDeliverySeconds"))

    @max_delivery_seconds.setter
    def max_delivery_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fc233f6467bad5ca85b2036610d0a3df6a871eeda16c8e95b14bb56b6588593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDeliverySeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sendingPoolName")
    def sending_pool_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sendingPoolName"))

    @sending_pool_name.setter
    def sending_pool_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7eb250ce834fa30f6562c70f5b654a4f0e264d041c2d17198b21aa1a930dee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendingPoolName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsPolicy")
    def tls_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsPolicy"))

    @tls_policy.setter
    def tls_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2c520200587cf4fed9cba4af969248066189403cc2dd76118ecc55890b4d1b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Sesv2ConfigurationSetDeliveryOptions]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetDeliveryOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetDeliveryOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad213ce0fbad8a7df2f18fb03e2d8e76c58e2f0da78e9677ab113d87fa6a3945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSet.Sesv2ConfigurationSetReputationOptions",
    jsii_struct_bases=[],
    name_mapping={"reputation_metrics_enabled": "reputationMetricsEnabled"},
)
class Sesv2ConfigurationSetReputationOptions:
    def __init__(
        self,
        *,
        reputation_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param reputation_metrics_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#reputation_metrics_enabled Sesv2ConfigurationSet#reputation_metrics_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a17fb076dc3b955091fb2a4f14e23f514b77510a081e2ffa782badffe61ce45)
            check_type(argname="argument reputation_metrics_enabled", value=reputation_metrics_enabled, expected_type=type_hints["reputation_metrics_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if reputation_metrics_enabled is not None:
            self._values["reputation_metrics_enabled"] = reputation_metrics_enabled

    @builtins.property
    def reputation_metrics_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#reputation_metrics_enabled Sesv2ConfigurationSet#reputation_metrics_enabled}.'''
        result = self._values.get("reputation_metrics_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetReputationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Sesv2ConfigurationSetReputationOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSet.Sesv2ConfigurationSetReputationOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77ce1f7b809403bdfaa8c404eb88a453656bcfeadca7ae8e6f7d0d7d6121ab63)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetReputationMetricsEnabled")
    def reset_reputation_metrics_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReputationMetricsEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="lastFreshStart")
    def last_fresh_start(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastFreshStart"))

    @builtins.property
    @jsii.member(jsii_name="reputationMetricsEnabledInput")
    def reputation_metrics_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "reputationMetricsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="reputationMetricsEnabled")
    def reputation_metrics_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "reputationMetricsEnabled"))

    @reputation_metrics_enabled.setter
    def reputation_metrics_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b4441b64703ac2c06945692f51de3fb756a10ba0acd8945bd2747674f805ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reputationMetricsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Sesv2ConfigurationSetReputationOptions]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetReputationOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetReputationOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cd6d78134d5105270ff8654eee7258c4221420c1a8a19e0f971413dd90c2087)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSet.Sesv2ConfigurationSetSendingOptions",
    jsii_struct_bases=[],
    name_mapping={"sending_enabled": "sendingEnabled"},
)
class Sesv2ConfigurationSetSendingOptions:
    def __init__(
        self,
        *,
        sending_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param sending_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#sending_enabled Sesv2ConfigurationSet#sending_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d1303aa225fce095dd5cbec4e04bf34cf43ee50f45f00987aca53b50d5161b)
            check_type(argname="argument sending_enabled", value=sending_enabled, expected_type=type_hints["sending_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if sending_enabled is not None:
            self._values["sending_enabled"] = sending_enabled

    @builtins.property
    def sending_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#sending_enabled Sesv2ConfigurationSet#sending_enabled}.'''
        result = self._values.get("sending_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetSendingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Sesv2ConfigurationSetSendingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSet.Sesv2ConfigurationSetSendingOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97362f8386d7f7882ec7e95b9c9d08fd8854b5738ec3061630ba60e91d3dcc6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSendingEnabled")
    def reset_sending_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendingEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="sendingEnabledInput")
    def sending_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sendingEnabled")
    def sending_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendingEnabled"))

    @sending_enabled.setter
    def sending_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31d01e04f0c5e6c0652676718f54b46be218225bef220c3e4c1a94e126c059f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Sesv2ConfigurationSetSendingOptions]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetSendingOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetSendingOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2e11bf491100088173149abb49025e315c6c7d9e3df6f52d385f1108242f2e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSet.Sesv2ConfigurationSetSuppressionOptions",
    jsii_struct_bases=[],
    name_mapping={"suppressed_reasons": "suppressedReasons"},
)
class Sesv2ConfigurationSetSuppressionOptions:
    def __init__(
        self,
        *,
        suppressed_reasons: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param suppressed_reasons: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#suppressed_reasons Sesv2ConfigurationSet#suppressed_reasons}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8425963d36f683694a876748244d213af92289e972bf32e9239496596db0917a)
            check_type(argname="argument suppressed_reasons", value=suppressed_reasons, expected_type=type_hints["suppressed_reasons"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if suppressed_reasons is not None:
            self._values["suppressed_reasons"] = suppressed_reasons

    @builtins.property
    def suppressed_reasons(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#suppressed_reasons Sesv2ConfigurationSet#suppressed_reasons}.'''
        result = self._values.get("suppressed_reasons")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetSuppressionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Sesv2ConfigurationSetSuppressionOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSet.Sesv2ConfigurationSetSuppressionOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a8ec05724405d9ed9576cc558705999737ec8c8f7f536bc9faedc5f1bb93519)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSuppressedReasons")
    def reset_suppressed_reasons(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuppressedReasons", []))

    @builtins.property
    @jsii.member(jsii_name="suppressedReasonsInput")
    def suppressed_reasons_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "suppressedReasonsInput"))

    @builtins.property
    @jsii.member(jsii_name="suppressedReasons")
    def suppressed_reasons(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "suppressedReasons"))

    @suppressed_reasons.setter
    def suppressed_reasons(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2981e6ae4eb4f218fcdc08cc70524cca613cca0f188e96c2daace4ade4749674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suppressedReasons", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetSuppressionOptions]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetSuppressionOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetSuppressionOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__358d6322b6c6a322f5e82cbeb7f2ab4d8d364c5e5a5b4bcb17e838dc5b0db8a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSet.Sesv2ConfigurationSetTrackingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "custom_redirect_domain": "customRedirectDomain",
        "https_policy": "httpsPolicy",
    },
)
class Sesv2ConfigurationSetTrackingOptions:
    def __init__(
        self,
        *,
        custom_redirect_domain: builtins.str,
        https_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_redirect_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#custom_redirect_domain Sesv2ConfigurationSet#custom_redirect_domain}.
        :param https_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#https_policy Sesv2ConfigurationSet#https_policy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2f1eda9d6b10ff8c3d6f5e00686218bf2f3837c9776d701a91946fa1777c5ef)
            check_type(argname="argument custom_redirect_domain", value=custom_redirect_domain, expected_type=type_hints["custom_redirect_domain"])
            check_type(argname="argument https_policy", value=https_policy, expected_type=type_hints["https_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_redirect_domain": custom_redirect_domain,
        }
        if https_policy is not None:
            self._values["https_policy"] = https_policy

    @builtins.property
    def custom_redirect_domain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#custom_redirect_domain Sesv2ConfigurationSet#custom_redirect_domain}.'''
        result = self._values.get("custom_redirect_domain")
        assert result is not None, "Required property 'custom_redirect_domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def https_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#https_policy Sesv2ConfigurationSet#https_policy}.'''
        result = self._values.get("https_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetTrackingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Sesv2ConfigurationSetTrackingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSet.Sesv2ConfigurationSetTrackingOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5891c924239ba1a7721f1ee9f3a686b1546b1d7449524cc33a2f916cda9f7fc3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHttpsPolicy")
    def reset_https_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="customRedirectDomainInput")
    def custom_redirect_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customRedirectDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsPolicyInput")
    def https_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpsPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="customRedirectDomain")
    def custom_redirect_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customRedirectDomain"))

    @custom_redirect_domain.setter
    def custom_redirect_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f1b557125bb93bf70ade9346903f8c01fd68dafdf18fb0f09ea528eeea8241)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customRedirectDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsPolicy")
    def https_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsPolicy"))

    @https_policy.setter
    def https_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7da28b257f00f6b04fdd5ff93d628a52ac66badbef2c75c28a6be4b2ccd39f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Sesv2ConfigurationSetTrackingOptions]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetTrackingOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetTrackingOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36c9e273b1121b9f86fc0135285514e69944db33d4c85d85883fe5a6d05b31e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSet.Sesv2ConfigurationSetVdmOptions",
    jsii_struct_bases=[],
    name_mapping={
        "dashboard_options": "dashboardOptions",
        "guardian_options": "guardianOptions",
    },
)
class Sesv2ConfigurationSetVdmOptions:
    def __init__(
        self,
        *,
        dashboard_options: typing.Optional[typing.Union["Sesv2ConfigurationSetVdmOptionsDashboardOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        guardian_options: typing.Optional[typing.Union["Sesv2ConfigurationSetVdmOptionsGuardianOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dashboard_options: dashboard_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#dashboard_options Sesv2ConfigurationSet#dashboard_options}
        :param guardian_options: guardian_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#guardian_options Sesv2ConfigurationSet#guardian_options}
        '''
        if isinstance(dashboard_options, dict):
            dashboard_options = Sesv2ConfigurationSetVdmOptionsDashboardOptions(**dashboard_options)
        if isinstance(guardian_options, dict):
            guardian_options = Sesv2ConfigurationSetVdmOptionsGuardianOptions(**guardian_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f6bbea55f733070d17918778705dd1054fd2afaf0449cc761f3b64e3c311629)
            check_type(argname="argument dashboard_options", value=dashboard_options, expected_type=type_hints["dashboard_options"])
            check_type(argname="argument guardian_options", value=guardian_options, expected_type=type_hints["guardian_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dashboard_options is not None:
            self._values["dashboard_options"] = dashboard_options
        if guardian_options is not None:
            self._values["guardian_options"] = guardian_options

    @builtins.property
    def dashboard_options(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetVdmOptionsDashboardOptions"]:
        '''dashboard_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#dashboard_options Sesv2ConfigurationSet#dashboard_options}
        '''
        result = self._values.get("dashboard_options")
        return typing.cast(typing.Optional["Sesv2ConfigurationSetVdmOptionsDashboardOptions"], result)

    @builtins.property
    def guardian_options(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetVdmOptionsGuardianOptions"]:
        '''guardian_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#guardian_options Sesv2ConfigurationSet#guardian_options}
        '''
        result = self._values.get("guardian_options")
        return typing.cast(typing.Optional["Sesv2ConfigurationSetVdmOptionsGuardianOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetVdmOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSet.Sesv2ConfigurationSetVdmOptionsDashboardOptions",
    jsii_struct_bases=[],
    name_mapping={"engagement_metrics": "engagementMetrics"},
)
class Sesv2ConfigurationSetVdmOptionsDashboardOptions:
    def __init__(
        self,
        *,
        engagement_metrics: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param engagement_metrics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#engagement_metrics Sesv2ConfigurationSet#engagement_metrics}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__445aaae485b430360f8d2ca119b8ce7a63a244440a72a6da605103d1601f155c)
            check_type(argname="argument engagement_metrics", value=engagement_metrics, expected_type=type_hints["engagement_metrics"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if engagement_metrics is not None:
            self._values["engagement_metrics"] = engagement_metrics

    @builtins.property
    def engagement_metrics(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#engagement_metrics Sesv2ConfigurationSet#engagement_metrics}.'''
        result = self._values.get("engagement_metrics")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetVdmOptionsDashboardOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Sesv2ConfigurationSetVdmOptionsDashboardOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSet.Sesv2ConfigurationSetVdmOptionsDashboardOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__379190504eb1495d3a1b5eb604c5a92cf88e9a0d6e0fcd442ed69c16485c212f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEngagementMetrics")
    def reset_engagement_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEngagementMetrics", []))

    @builtins.property
    @jsii.member(jsii_name="engagementMetricsInput")
    def engagement_metrics_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engagementMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="engagementMetrics")
    def engagement_metrics(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engagementMetrics"))

    @engagement_metrics.setter
    def engagement_metrics(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5beea1761e3c74682d58168cc6486770a6b3af75b0ffc27a9474624a24154498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engagementMetrics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetVdmOptionsDashboardOptions]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetVdmOptionsDashboardOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetVdmOptionsDashboardOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0f06e535bf0e91e06b4e60298fb98ea368123221bc8dcbdf34bc8b56a158412)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSet.Sesv2ConfigurationSetVdmOptionsGuardianOptions",
    jsii_struct_bases=[],
    name_mapping={"optimized_shared_delivery": "optimizedSharedDelivery"},
)
class Sesv2ConfigurationSetVdmOptionsGuardianOptions:
    def __init__(
        self,
        *,
        optimized_shared_delivery: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param optimized_shared_delivery: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#optimized_shared_delivery Sesv2ConfigurationSet#optimized_shared_delivery}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef5746477c347ea8b81bdcdbac6f7e474d15c2bae4075ed076c543acbd344b9b)
            check_type(argname="argument optimized_shared_delivery", value=optimized_shared_delivery, expected_type=type_hints["optimized_shared_delivery"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if optimized_shared_delivery is not None:
            self._values["optimized_shared_delivery"] = optimized_shared_delivery

    @builtins.property
    def optimized_shared_delivery(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#optimized_shared_delivery Sesv2ConfigurationSet#optimized_shared_delivery}.'''
        result = self._values.get("optimized_shared_delivery")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetVdmOptionsGuardianOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Sesv2ConfigurationSetVdmOptionsGuardianOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSet.Sesv2ConfigurationSetVdmOptionsGuardianOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2e22d1433a1434fd5dd336e0ea9829a8e8e95f71cf61fab0bdb1677d336f328)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOptimizedSharedDelivery")
    def reset_optimized_shared_delivery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptimizedSharedDelivery", []))

    @builtins.property
    @jsii.member(jsii_name="optimizedSharedDeliveryInput")
    def optimized_shared_delivery_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "optimizedSharedDeliveryInput"))

    @builtins.property
    @jsii.member(jsii_name="optimizedSharedDelivery")
    def optimized_shared_delivery(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "optimizedSharedDelivery"))

    @optimized_shared_delivery.setter
    def optimized_shared_delivery(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d3a1be1d4a857fab4536e44ed09a335cf99cd0d2e2b71f4046c3397da894bf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optimizedSharedDelivery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetVdmOptionsGuardianOptions]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetVdmOptionsGuardianOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetVdmOptionsGuardianOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aae1cbc1d8f14417dda4d1a11f6a968dd01a0f4c6a80f476e8604b0a42ff2d71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Sesv2ConfigurationSetVdmOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sesv2ConfigurationSet.Sesv2ConfigurationSetVdmOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__626d3e9f26b9bc039e6a16b82c610a9035b000e1ba8bdc00d9ac8f10d8b0d9a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDashboardOptions")
    def put_dashboard_options(
        self,
        *,
        engagement_metrics: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param engagement_metrics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#engagement_metrics Sesv2ConfigurationSet#engagement_metrics}.
        '''
        value = Sesv2ConfigurationSetVdmOptionsDashboardOptions(
            engagement_metrics=engagement_metrics
        )

        return typing.cast(None, jsii.invoke(self, "putDashboardOptions", [value]))

    @jsii.member(jsii_name="putGuardianOptions")
    def put_guardian_options(
        self,
        *,
        optimized_shared_delivery: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param optimized_shared_delivery: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sesv2_configuration_set#optimized_shared_delivery Sesv2ConfigurationSet#optimized_shared_delivery}.
        '''
        value = Sesv2ConfigurationSetVdmOptionsGuardianOptions(
            optimized_shared_delivery=optimized_shared_delivery
        )

        return typing.cast(None, jsii.invoke(self, "putGuardianOptions", [value]))

    @jsii.member(jsii_name="resetDashboardOptions")
    def reset_dashboard_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDashboardOptions", []))

    @jsii.member(jsii_name="resetGuardianOptions")
    def reset_guardian_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuardianOptions", []))

    @builtins.property
    @jsii.member(jsii_name="dashboardOptions")
    def dashboard_options(
        self,
    ) -> Sesv2ConfigurationSetVdmOptionsDashboardOptionsOutputReference:
        return typing.cast(Sesv2ConfigurationSetVdmOptionsDashboardOptionsOutputReference, jsii.get(self, "dashboardOptions"))

    @builtins.property
    @jsii.member(jsii_name="guardianOptions")
    def guardian_options(
        self,
    ) -> Sesv2ConfigurationSetVdmOptionsGuardianOptionsOutputReference:
        return typing.cast(Sesv2ConfigurationSetVdmOptionsGuardianOptionsOutputReference, jsii.get(self, "guardianOptions"))

    @builtins.property
    @jsii.member(jsii_name="dashboardOptionsInput")
    def dashboard_options_input(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetVdmOptionsDashboardOptions]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetVdmOptionsDashboardOptions], jsii.get(self, "dashboardOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="guardianOptionsInput")
    def guardian_options_input(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetVdmOptionsGuardianOptions]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetVdmOptionsGuardianOptions], jsii.get(self, "guardianOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Sesv2ConfigurationSetVdmOptions]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetVdmOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetVdmOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfebc67645e98cfbead5eaf6cad840182e663ac2c8acab629023190b1d934351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Sesv2ConfigurationSet",
    "Sesv2ConfigurationSetConfig",
    "Sesv2ConfigurationSetDeliveryOptions",
    "Sesv2ConfigurationSetDeliveryOptionsOutputReference",
    "Sesv2ConfigurationSetReputationOptions",
    "Sesv2ConfigurationSetReputationOptionsOutputReference",
    "Sesv2ConfigurationSetSendingOptions",
    "Sesv2ConfigurationSetSendingOptionsOutputReference",
    "Sesv2ConfigurationSetSuppressionOptions",
    "Sesv2ConfigurationSetSuppressionOptionsOutputReference",
    "Sesv2ConfigurationSetTrackingOptions",
    "Sesv2ConfigurationSetTrackingOptionsOutputReference",
    "Sesv2ConfigurationSetVdmOptions",
    "Sesv2ConfigurationSetVdmOptionsDashboardOptions",
    "Sesv2ConfigurationSetVdmOptionsDashboardOptionsOutputReference",
    "Sesv2ConfigurationSetVdmOptionsGuardianOptions",
    "Sesv2ConfigurationSetVdmOptionsGuardianOptionsOutputReference",
    "Sesv2ConfigurationSetVdmOptionsOutputReference",
]

publication.publish()

def _typecheckingstub__20fbba189de34038fbb534c89b9413f229b4cd963a3460e10adc3fdcd81eeeef(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    configuration_set_name: builtins.str,
    delivery_options: typing.Optional[typing.Union[Sesv2ConfigurationSetDeliveryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    reputation_options: typing.Optional[typing.Union[Sesv2ConfigurationSetReputationOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    sending_options: typing.Optional[typing.Union[Sesv2ConfigurationSetSendingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    suppression_options: typing.Optional[typing.Union[Sesv2ConfigurationSetSuppressionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tracking_options: typing.Optional[typing.Union[Sesv2ConfigurationSetTrackingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    vdm_options: typing.Optional[typing.Union[Sesv2ConfigurationSetVdmOptions, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5c3499a81d1d8bc4b1005cc71a50cc531df870b39ab4598577584a58a4b6ae8c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c48eb39f02e1e9f138e975dba0a9b89c089a4eb0bdd42f92251412bb041c92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798b1311039f43b52d50391acafb3c3e112ebb5fc7b481cccbaa3e9028709bc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3387e1b47199ea779ab93140e9f35ce73cf127a611ade7e6c0fca24aa69c57a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e63e9e72e56c42cafb629f5223b3e7d6053b181addb6d2c2001398bccf1849(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc3e857d03540a19a314a80522d7690a8cfebc367ae367772536c0a9d3839fff(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01d0f20ee62a57091dca07e0dfbcda27d9f613a3ee045a1682b731319d6ba26d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    configuration_set_name: builtins.str,
    delivery_options: typing.Optional[typing.Union[Sesv2ConfigurationSetDeliveryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    reputation_options: typing.Optional[typing.Union[Sesv2ConfigurationSetReputationOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    sending_options: typing.Optional[typing.Union[Sesv2ConfigurationSetSendingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    suppression_options: typing.Optional[typing.Union[Sesv2ConfigurationSetSuppressionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tracking_options: typing.Optional[typing.Union[Sesv2ConfigurationSetTrackingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    vdm_options: typing.Optional[typing.Union[Sesv2ConfigurationSetVdmOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f5c1f56b14b8c39f37db9758067f141e2783b6f61a3dd8c4a3168854553be6(
    *,
    max_delivery_seconds: typing.Optional[jsii.Number] = None,
    sending_pool_name: typing.Optional[builtins.str] = None,
    tls_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ad3c958e46379d316893208bcac5bfd8f95a2ce6fa5c07422b58ab420571f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc233f6467bad5ca85b2036610d0a3df6a871eeda16c8e95b14bb56b6588593(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7eb250ce834fa30f6562c70f5b654a4f0e264d041c2d17198b21aa1a930dee5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2c520200587cf4fed9cba4af969248066189403cc2dd76118ecc55890b4d1b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad213ce0fbad8a7df2f18fb03e2d8e76c58e2f0da78e9677ab113d87fa6a3945(
    value: typing.Optional[Sesv2ConfigurationSetDeliveryOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a17fb076dc3b955091fb2a4f14e23f514b77510a081e2ffa782badffe61ce45(
    *,
    reputation_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ce1f7b809403bdfaa8c404eb88a453656bcfeadca7ae8e6f7d0d7d6121ab63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b4441b64703ac2c06945692f51de3fb756a10ba0acd8945bd2747674f805ea(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd6d78134d5105270ff8654eee7258c4221420c1a8a19e0f971413dd90c2087(
    value: typing.Optional[Sesv2ConfigurationSetReputationOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d1303aa225fce095dd5cbec4e04bf34cf43ee50f45f00987aca53b50d5161b(
    *,
    sending_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97362f8386d7f7882ec7e95b9c9d08fd8854b5738ec3061630ba60e91d3dcc6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d01e04f0c5e6c0652676718f54b46be218225bef220c3e4c1a94e126c059f1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2e11bf491100088173149abb49025e315c6c7d9e3df6f52d385f1108242f2e7(
    value: typing.Optional[Sesv2ConfigurationSetSendingOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8425963d36f683694a876748244d213af92289e972bf32e9239496596db0917a(
    *,
    suppressed_reasons: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a8ec05724405d9ed9576cc558705999737ec8c8f7f536bc9faedc5f1bb93519(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2981e6ae4eb4f218fcdc08cc70524cca613cca0f188e96c2daace4ade4749674(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358d6322b6c6a322f5e82cbeb7f2ab4d8d364c5e5a5b4bcb17e838dc5b0db8a1(
    value: typing.Optional[Sesv2ConfigurationSetSuppressionOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f1eda9d6b10ff8c3d6f5e00686218bf2f3837c9776d701a91946fa1777c5ef(
    *,
    custom_redirect_domain: builtins.str,
    https_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5891c924239ba1a7721f1ee9f3a686b1546b1d7449524cc33a2f916cda9f7fc3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f1b557125bb93bf70ade9346903f8c01fd68dafdf18fb0f09ea528eeea8241(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7da28b257f00f6b04fdd5ff93d628a52ac66badbef2c75c28a6be4b2ccd39f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c9e273b1121b9f86fc0135285514e69944db33d4c85d85883fe5a6d05b31e7(
    value: typing.Optional[Sesv2ConfigurationSetTrackingOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f6bbea55f733070d17918778705dd1054fd2afaf0449cc761f3b64e3c311629(
    *,
    dashboard_options: typing.Optional[typing.Union[Sesv2ConfigurationSetVdmOptionsDashboardOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    guardian_options: typing.Optional[typing.Union[Sesv2ConfigurationSetVdmOptionsGuardianOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__445aaae485b430360f8d2ca119b8ce7a63a244440a72a6da605103d1601f155c(
    *,
    engagement_metrics: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__379190504eb1495d3a1b5eb604c5a92cf88e9a0d6e0fcd442ed69c16485c212f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5beea1761e3c74682d58168cc6486770a6b3af75b0ffc27a9474624a24154498(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f06e535bf0e91e06b4e60298fb98ea368123221bc8dcbdf34bc8b56a158412(
    value: typing.Optional[Sesv2ConfigurationSetVdmOptionsDashboardOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5746477c347ea8b81bdcdbac6f7e474d15c2bae4075ed076c543acbd344b9b(
    *,
    optimized_shared_delivery: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2e22d1433a1434fd5dd336e0ea9829a8e8e95f71cf61fab0bdb1677d336f328(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d3a1be1d4a857fab4536e44ed09a335cf99cd0d2e2b71f4046c3397da894bf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae1cbc1d8f14417dda4d1a11f6a968dd01a0f4c6a80f476e8604b0a42ff2d71(
    value: typing.Optional[Sesv2ConfigurationSetVdmOptionsGuardianOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626d3e9f26b9bc039e6a16b82c610a9035b000e1ba8bdc00d9ac8f10d8b0d9a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfebc67645e98cfbead5eaf6cad840182e663ac2c8acab629023190b1d934351(
    value: typing.Optional[Sesv2ConfigurationSetVdmOptions],
) -> None:
    """Type checking stubs"""
    pass
