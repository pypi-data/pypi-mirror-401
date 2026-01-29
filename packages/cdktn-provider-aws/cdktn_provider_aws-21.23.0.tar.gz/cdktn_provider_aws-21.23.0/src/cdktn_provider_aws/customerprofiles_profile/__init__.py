r'''
# `aws_customerprofiles_profile`

Refer to the Terraform Registry for docs: [`aws_customerprofiles_profile`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile).
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


class CustomerprofilesProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.customerprofilesProfile.CustomerprofilesProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile aws_customerprofiles_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        domain_name: builtins.str,
        account_number: typing.Optional[builtins.str] = None,
        additional_information: typing.Optional[builtins.str] = None,
        address: typing.Optional[typing.Union["CustomerprofilesProfileAddress", typing.Dict[builtins.str, typing.Any]]] = None,
        attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        billing_address: typing.Optional[typing.Union["CustomerprofilesProfileBillingAddress", typing.Dict[builtins.str, typing.Any]]] = None,
        birth_date: typing.Optional[builtins.str] = None,
        business_email_address: typing.Optional[builtins.str] = None,
        business_name: typing.Optional[builtins.str] = None,
        business_phone_number: typing.Optional[builtins.str] = None,
        email_address: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        gender_string: typing.Optional[builtins.str] = None,
        home_phone_number: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        mailing_address: typing.Optional[typing.Union["CustomerprofilesProfileMailingAddress", typing.Dict[builtins.str, typing.Any]]] = None,
        middle_name: typing.Optional[builtins.str] = None,
        mobile_phone_number: typing.Optional[builtins.str] = None,
        party_type_string: typing.Optional[builtins.str] = None,
        personal_email_address: typing.Optional[builtins.str] = None,
        phone_number: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        shipping_address: typing.Optional[typing.Union["CustomerprofilesProfileShippingAddress", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile aws_customerprofiles_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#domain_name CustomerprofilesProfile#domain_name}.
        :param account_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#account_number CustomerprofilesProfile#account_number}.
        :param additional_information: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#additional_information CustomerprofilesProfile#additional_information}.
        :param address: address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address CustomerprofilesProfile#address}
        :param attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#attributes CustomerprofilesProfile#attributes}.
        :param billing_address: billing_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#billing_address CustomerprofilesProfile#billing_address}
        :param birth_date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#birth_date CustomerprofilesProfile#birth_date}.
        :param business_email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#business_email_address CustomerprofilesProfile#business_email_address}.
        :param business_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#business_name CustomerprofilesProfile#business_name}.
        :param business_phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#business_phone_number CustomerprofilesProfile#business_phone_number}.
        :param email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#email_address CustomerprofilesProfile#email_address}.
        :param first_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#first_name CustomerprofilesProfile#first_name}.
        :param gender_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#gender_string CustomerprofilesProfile#gender_string}.
        :param home_phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#home_phone_number CustomerprofilesProfile#home_phone_number}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#id CustomerprofilesProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param last_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#last_name CustomerprofilesProfile#last_name}.
        :param mailing_address: mailing_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#mailing_address CustomerprofilesProfile#mailing_address}
        :param middle_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#middle_name CustomerprofilesProfile#middle_name}.
        :param mobile_phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#mobile_phone_number CustomerprofilesProfile#mobile_phone_number}.
        :param party_type_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#party_type_string CustomerprofilesProfile#party_type_string}.
        :param personal_email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#personal_email_address CustomerprofilesProfile#personal_email_address}.
        :param phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#phone_number CustomerprofilesProfile#phone_number}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#region CustomerprofilesProfile#region}
        :param shipping_address: shipping_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#shipping_address CustomerprofilesProfile#shipping_address}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286a735a194bb21b26056a13c76cc590af724c27d8f746d69ff414956240ad7e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CustomerprofilesProfileConfig(
            domain_name=domain_name,
            account_number=account_number,
            additional_information=additional_information,
            address=address,
            attributes=attributes,
            billing_address=billing_address,
            birth_date=birth_date,
            business_email_address=business_email_address,
            business_name=business_name,
            business_phone_number=business_phone_number,
            email_address=email_address,
            first_name=first_name,
            gender_string=gender_string,
            home_phone_number=home_phone_number,
            id=id,
            last_name=last_name,
            mailing_address=mailing_address,
            middle_name=middle_name,
            mobile_phone_number=mobile_phone_number,
            party_type_string=party_type_string,
            personal_email_address=personal_email_address,
            phone_number=phone_number,
            region=region,
            shipping_address=shipping_address,
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
        '''Generates CDKTF code for importing a CustomerprofilesProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CustomerprofilesProfile to import.
        :param import_from_id: The id of the existing CustomerprofilesProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CustomerprofilesProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d508db9dbc4129efb481bdf78910624adcb79d2036069cff97fab0a2337a8e93)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAddress")
    def put_address(
        self,
        *,
        address1: typing.Optional[builtins.str] = None,
        address2: typing.Optional[builtins.str] = None,
        address3: typing.Optional[builtins.str] = None,
        address4: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        county: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.
        :param address2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.
        :param address3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.
        :param address4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.
        :param country: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.
        :param county: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.
        :param postal_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.
        :param province: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.
        '''
        value = CustomerprofilesProfileAddress(
            address1=address1,
            address2=address2,
            address3=address3,
            address4=address4,
            city=city,
            country=country,
            county=county,
            postal_code=postal_code,
            province=province,
            state=state,
        )

        return typing.cast(None, jsii.invoke(self, "putAddress", [value]))

    @jsii.member(jsii_name="putBillingAddress")
    def put_billing_address(
        self,
        *,
        address1: typing.Optional[builtins.str] = None,
        address2: typing.Optional[builtins.str] = None,
        address3: typing.Optional[builtins.str] = None,
        address4: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        county: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.
        :param address2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.
        :param address3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.
        :param address4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.
        :param country: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.
        :param county: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.
        :param postal_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.
        :param province: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.
        '''
        value = CustomerprofilesProfileBillingAddress(
            address1=address1,
            address2=address2,
            address3=address3,
            address4=address4,
            city=city,
            country=country,
            county=county,
            postal_code=postal_code,
            province=province,
            state=state,
        )

        return typing.cast(None, jsii.invoke(self, "putBillingAddress", [value]))

    @jsii.member(jsii_name="putMailingAddress")
    def put_mailing_address(
        self,
        *,
        address1: typing.Optional[builtins.str] = None,
        address2: typing.Optional[builtins.str] = None,
        address3: typing.Optional[builtins.str] = None,
        address4: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        county: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.
        :param address2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.
        :param address3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.
        :param address4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.
        :param country: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.
        :param county: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.
        :param postal_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.
        :param province: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.
        '''
        value = CustomerprofilesProfileMailingAddress(
            address1=address1,
            address2=address2,
            address3=address3,
            address4=address4,
            city=city,
            country=country,
            county=county,
            postal_code=postal_code,
            province=province,
            state=state,
        )

        return typing.cast(None, jsii.invoke(self, "putMailingAddress", [value]))

    @jsii.member(jsii_name="putShippingAddress")
    def put_shipping_address(
        self,
        *,
        address1: typing.Optional[builtins.str] = None,
        address2: typing.Optional[builtins.str] = None,
        address3: typing.Optional[builtins.str] = None,
        address4: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        county: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.
        :param address2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.
        :param address3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.
        :param address4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.
        :param country: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.
        :param county: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.
        :param postal_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.
        :param province: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.
        '''
        value = CustomerprofilesProfileShippingAddress(
            address1=address1,
            address2=address2,
            address3=address3,
            address4=address4,
            city=city,
            country=country,
            county=county,
            postal_code=postal_code,
            province=province,
            state=state,
        )

        return typing.cast(None, jsii.invoke(self, "putShippingAddress", [value]))

    @jsii.member(jsii_name="resetAccountNumber")
    def reset_account_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountNumber", []))

    @jsii.member(jsii_name="resetAdditionalInformation")
    def reset_additional_information(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalInformation", []))

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetAttributes")
    def reset_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributes", []))

    @jsii.member(jsii_name="resetBillingAddress")
    def reset_billing_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBillingAddress", []))

    @jsii.member(jsii_name="resetBirthDate")
    def reset_birth_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBirthDate", []))

    @jsii.member(jsii_name="resetBusinessEmailAddress")
    def reset_business_email_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBusinessEmailAddress", []))

    @jsii.member(jsii_name="resetBusinessName")
    def reset_business_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBusinessName", []))

    @jsii.member(jsii_name="resetBusinessPhoneNumber")
    def reset_business_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBusinessPhoneNumber", []))

    @jsii.member(jsii_name="resetEmailAddress")
    def reset_email_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailAddress", []))

    @jsii.member(jsii_name="resetFirstName")
    def reset_first_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstName", []))

    @jsii.member(jsii_name="resetGenderString")
    def reset_gender_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenderString", []))

    @jsii.member(jsii_name="resetHomePhoneNumber")
    def reset_home_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHomePhoneNumber", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLastName")
    def reset_last_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastName", []))

    @jsii.member(jsii_name="resetMailingAddress")
    def reset_mailing_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMailingAddress", []))

    @jsii.member(jsii_name="resetMiddleName")
    def reset_middle_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMiddleName", []))

    @jsii.member(jsii_name="resetMobilePhoneNumber")
    def reset_mobile_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMobilePhoneNumber", []))

    @jsii.member(jsii_name="resetPartyTypeString")
    def reset_party_type_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartyTypeString", []))

    @jsii.member(jsii_name="resetPersonalEmailAddress")
    def reset_personal_email_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPersonalEmailAddress", []))

    @jsii.member(jsii_name="resetPhoneNumber")
    def reset_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhoneNumber", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetShippingAddress")
    def reset_shipping_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShippingAddress", []))

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
    @jsii.member(jsii_name="address")
    def address(self) -> "CustomerprofilesProfileAddressOutputReference":
        return typing.cast("CustomerprofilesProfileAddressOutputReference", jsii.get(self, "address"))

    @builtins.property
    @jsii.member(jsii_name="billingAddress")
    def billing_address(self) -> "CustomerprofilesProfileBillingAddressOutputReference":
        return typing.cast("CustomerprofilesProfileBillingAddressOutputReference", jsii.get(self, "billingAddress"))

    @builtins.property
    @jsii.member(jsii_name="mailingAddress")
    def mailing_address(self) -> "CustomerprofilesProfileMailingAddressOutputReference":
        return typing.cast("CustomerprofilesProfileMailingAddressOutputReference", jsii.get(self, "mailingAddress"))

    @builtins.property
    @jsii.member(jsii_name="shippingAddress")
    def shipping_address(
        self,
    ) -> "CustomerprofilesProfileShippingAddressOutputReference":
        return typing.cast("CustomerprofilesProfileShippingAddressOutputReference", jsii.get(self, "shippingAddress"))

    @builtins.property
    @jsii.member(jsii_name="accountNumberInput")
    def account_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalInformationInput")
    def additional_information_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "additionalInformationInput"))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional["CustomerprofilesProfileAddress"]:
        return typing.cast(typing.Optional["CustomerprofilesProfileAddress"], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="attributesInput")
    def attributes_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "attributesInput"))

    @builtins.property
    @jsii.member(jsii_name="billingAddressInput")
    def billing_address_input(
        self,
    ) -> typing.Optional["CustomerprofilesProfileBillingAddress"]:
        return typing.cast(typing.Optional["CustomerprofilesProfileBillingAddress"], jsii.get(self, "billingAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="birthDateInput")
    def birth_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "birthDateInput"))

    @builtins.property
    @jsii.member(jsii_name="businessEmailAddressInput")
    def business_email_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "businessEmailAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="businessNameInput")
    def business_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "businessNameInput"))

    @builtins.property
    @jsii.member(jsii_name="businessPhoneNumberInput")
    def business_phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "businessPhoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAddressInput")
    def email_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="firstNameInput")
    def first_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firstNameInput"))

    @builtins.property
    @jsii.member(jsii_name="genderStringInput")
    def gender_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "genderStringInput"))

    @builtins.property
    @jsii.member(jsii_name="homePhoneNumberInput")
    def home_phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "homePhoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lastNameInput")
    def last_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastNameInput"))

    @builtins.property
    @jsii.member(jsii_name="mailingAddressInput")
    def mailing_address_input(
        self,
    ) -> typing.Optional["CustomerprofilesProfileMailingAddress"]:
        return typing.cast(typing.Optional["CustomerprofilesProfileMailingAddress"], jsii.get(self, "mailingAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="middleNameInput")
    def middle_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "middleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="mobilePhoneNumberInput")
    def mobile_phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mobilePhoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="partyTypeStringInput")
    def party_type_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partyTypeStringInput"))

    @builtins.property
    @jsii.member(jsii_name="personalEmailAddressInput")
    def personal_email_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "personalEmailAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="shippingAddressInput")
    def shipping_address_input(
        self,
    ) -> typing.Optional["CustomerprofilesProfileShippingAddress"]:
        return typing.cast(typing.Optional["CustomerprofilesProfileShippingAddress"], jsii.get(self, "shippingAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="accountNumber")
    def account_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountNumber"))

    @account_number.setter
    def account_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c6b14f644c7c000e9a45ca183acf72b73d1ddc10c94345ce8e3a033dddd4ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="additionalInformation")
    def additional_information(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "additionalInformation"))

    @additional_information.setter
    def additional_information(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6de069a5e433e4edc537ba9c167a4f4461c0e7f1f31ad936296ff7b1e4d60e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalInformation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "attributes"))

    @attributes.setter
    def attributes(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80055f9502869ef978414346747c1257e6ad4637dd2e97def99f94d5dbb70069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="birthDate")
    def birth_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "birthDate"))

    @birth_date.setter
    def birth_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca7f594314aa15e9abc2e5731479efe24f0fed671d622a0a8f76e9c577f2665f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "birthDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="businessEmailAddress")
    def business_email_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "businessEmailAddress"))

    @business_email_address.setter
    def business_email_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388b9c0957c7288c7984e4f079581df2ca050fdf6d4f1104e8e9e8788b9572ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "businessEmailAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="businessName")
    def business_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "businessName"))

    @business_name.setter
    def business_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c77572190bbacbb807cc22c148f41702201df8fcdc67e0e2789d84830071125)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "businessName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="businessPhoneNumber")
    def business_phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "businessPhoneNumber"))

    @business_phone_number.setter
    def business_phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4b8fdfbea4b2bd3940861930791ce194cbf5f789bd0163c58919a3da0fc4cab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "businessPhoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8a1526f03990e057fd0f35e5c4615959f8e3ec00b90fd6f6ea5f90220e5f107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailAddress")
    def email_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailAddress"))

    @email_address.setter
    def email_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b4479b5764a552595b253285bc3c870e7f816b959c91cf080b3fddde5ab7bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firstName")
    def first_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstName"))

    @first_name.setter
    def first_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__735272019693e0a3526302499fb4b21fa159c1a13068261ab60791dda38606fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="genderString")
    def gender_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "genderString"))

    @gender_string.setter
    def gender_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83034a8ed4fb23c154fb57696d4b4c2ba8caa986b103638a8c7a0f4e4f44bf53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "genderString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="homePhoneNumber")
    def home_phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "homePhoneNumber"))

    @home_phone_number.setter
    def home_phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80671af65429a08156fe1822663377a70b0984ddc85226f90089c34b90b979e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "homePhoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd82711e5c57c193f6a3355e946e7dd71788fae6067a5801f7dc7d19511933f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastName")
    def last_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastName"))

    @last_name.setter
    def last_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b453dd61bb551d462baa2e2472eb66ae3eaf4302625aae5e0483710c630d1e90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="middleName")
    def middle_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "middleName"))

    @middle_name.setter
    def middle_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1add9cb1673673e470f0f2d227e035923cec47d2d334fc6f8f87ce39e0901e7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "middleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mobilePhoneNumber")
    def mobile_phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mobilePhoneNumber"))

    @mobile_phone_number.setter
    def mobile_phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac709921df4316822d9b0fdf31c3b08e9647a67e67339862c3574f0ea8464034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mobilePhoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partyTypeString")
    def party_type_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partyTypeString"))

    @party_type_string.setter
    def party_type_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a795081f5f8463dcada0707888a38876b1693ff3ad44141209dda510ec27275)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partyTypeString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="personalEmailAddress")
    def personal_email_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "personalEmailAddress"))

    @personal_email_address.setter
    def personal_email_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbe61b2de783e36ca8b23b2d8bbf1ad6961aa34256f97ab01eb5cd8686cd77bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "personalEmailAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b361ebe50002c159495450d072137387e2fb88c48ae81be9fe42cf2566443fcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dac2c4364c27ac65c3c79a19b08528bc8137ff5d2a264a2ba65cfe6007b048e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.customerprofilesProfile.CustomerprofilesProfileAddress",
    jsii_struct_bases=[],
    name_mapping={
        "address1": "address1",
        "address2": "address2",
        "address3": "address3",
        "address4": "address4",
        "city": "city",
        "country": "country",
        "county": "county",
        "postal_code": "postalCode",
        "province": "province",
        "state": "state",
    },
)
class CustomerprofilesProfileAddress:
    def __init__(
        self,
        *,
        address1: typing.Optional[builtins.str] = None,
        address2: typing.Optional[builtins.str] = None,
        address3: typing.Optional[builtins.str] = None,
        address4: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        county: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.
        :param address2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.
        :param address3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.
        :param address4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.
        :param country: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.
        :param county: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.
        :param postal_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.
        :param province: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f27f606049198b66fdda91d2d036679390e1bd18e1b859f80639cc3c3014bb55)
            check_type(argname="argument address1", value=address1, expected_type=type_hints["address1"])
            check_type(argname="argument address2", value=address2, expected_type=type_hints["address2"])
            check_type(argname="argument address3", value=address3, expected_type=type_hints["address3"])
            check_type(argname="argument address4", value=address4, expected_type=type_hints["address4"])
            check_type(argname="argument city", value=city, expected_type=type_hints["city"])
            check_type(argname="argument country", value=country, expected_type=type_hints["country"])
            check_type(argname="argument county", value=county, expected_type=type_hints["county"])
            check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
            check_type(argname="argument province", value=province, expected_type=type_hints["province"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address1 is not None:
            self._values["address1"] = address1
        if address2 is not None:
            self._values["address2"] = address2
        if address3 is not None:
            self._values["address3"] = address3
        if address4 is not None:
            self._values["address4"] = address4
        if city is not None:
            self._values["city"] = city
        if country is not None:
            self._values["country"] = country
        if county is not None:
            self._values["county"] = county
        if postal_code is not None:
            self._values["postal_code"] = postal_code
        if province is not None:
            self._values["province"] = province
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def address1(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.'''
        result = self._values.get("address1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address2(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.'''
        result = self._values.get("address2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address3(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.'''
        result = self._values.get("address3")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address4(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.'''
        result = self._values.get("address4")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def city(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.'''
        result = self._values.get("city")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.'''
        result = self._values.get("country")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def county(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.'''
        result = self._values.get("county")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.'''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def province(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.'''
        result = self._values.get("province")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesProfileAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomerprofilesProfileAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.customerprofilesProfile.CustomerprofilesProfileAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91f506043be9ccdfbc6dc45f6a21d10995c8255f76e62bd335b9701e54b37864)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddress1")
    def reset_address1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress1", []))

    @jsii.member(jsii_name="resetAddress2")
    def reset_address2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress2", []))

    @jsii.member(jsii_name="resetAddress3")
    def reset_address3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress3", []))

    @jsii.member(jsii_name="resetAddress4")
    def reset_address4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress4", []))

    @jsii.member(jsii_name="resetCity")
    def reset_city(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCity", []))

    @jsii.member(jsii_name="resetCountry")
    def reset_country(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountry", []))

    @jsii.member(jsii_name="resetCounty")
    def reset_county(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCounty", []))

    @jsii.member(jsii_name="resetPostalCode")
    def reset_postal_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostalCode", []))

    @jsii.member(jsii_name="resetProvince")
    def reset_province(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvince", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @builtins.property
    @jsii.member(jsii_name="address1Input")
    def address1_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address1Input"))

    @builtins.property
    @jsii.member(jsii_name="address2Input")
    def address2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address2Input"))

    @builtins.property
    @jsii.member(jsii_name="address3Input")
    def address3_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address3Input"))

    @builtins.property
    @jsii.member(jsii_name="address4Input")
    def address4_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address4Input"))

    @builtins.property
    @jsii.member(jsii_name="cityInput")
    def city_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cityInput"))

    @builtins.property
    @jsii.member(jsii_name="countryInput")
    def country_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryInput"))

    @builtins.property
    @jsii.member(jsii_name="countyInput")
    def county_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countyInput"))

    @builtins.property
    @jsii.member(jsii_name="postalCodeInput")
    def postal_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postalCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="provinceInput")
    def province_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provinceInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="address1")
    def address1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address1"))

    @address1.setter
    def address1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e9bc70b3bc7b034e8a29528ebb75e84a49c4f4e16966ef14e45691ada3684dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address1", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address2")
    def address2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address2"))

    @address2.setter
    def address2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e53f50d4939794018df36521fe9be452bb3a0820e0c16b56ebad5ee07b4afb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address3")
    def address3(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address3"))

    @address3.setter
    def address3(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7168376cfc381c99c22bd36831a87457baf27ef404a68f1c420c2be1e42f9800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address3", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address4")
    def address4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address4"))

    @address4.setter
    def address4(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa92bbfb19b1915ac7e34da5377091820a187dd86392a0ae97d9fde65265735e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="city")
    def city(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "city"))

    @city.setter
    def city(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6255056e84799dab564e0c8a472a3e30cd036100bf8f99bd01326da4c4994e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "city", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="country")
    def country(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "country"))

    @country.setter
    def country(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c5e70f7739213f967819a4d104c57eec7e9a19c54f94c6cf9eed4c76781e76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "country", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="county")
    def county(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "county"))

    @county.setter
    def county(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__006e15ff70a276e2f5b77cea7fa9a3a01b46038b45bbc6f5cbb36b3a25f4ca85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "county", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db50af56bf85fb22ac26b74b6c04e865951a1656abea2ba7b24ba1d1b7d67903)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="province")
    def province(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "province"))

    @province.setter
    def province(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6cea153e77c7538c96d21d06c167dbfc4c6b16caa15b404cf5b894820278c9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "province", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f57ca773af0cc46d0e6355cc6d8f6327c94dbd940a14e8047eaa06b664ef4fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CustomerprofilesProfileAddress]:
        return typing.cast(typing.Optional[CustomerprofilesProfileAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesProfileAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2b851e442224c8219513cf7b92a2d00725644dfa9622937202755585a98b074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.customerprofilesProfile.CustomerprofilesProfileBillingAddress",
    jsii_struct_bases=[],
    name_mapping={
        "address1": "address1",
        "address2": "address2",
        "address3": "address3",
        "address4": "address4",
        "city": "city",
        "country": "country",
        "county": "county",
        "postal_code": "postalCode",
        "province": "province",
        "state": "state",
    },
)
class CustomerprofilesProfileBillingAddress:
    def __init__(
        self,
        *,
        address1: typing.Optional[builtins.str] = None,
        address2: typing.Optional[builtins.str] = None,
        address3: typing.Optional[builtins.str] = None,
        address4: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        county: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.
        :param address2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.
        :param address3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.
        :param address4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.
        :param country: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.
        :param county: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.
        :param postal_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.
        :param province: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce9591fc3889db608c96b5127fdfb17830e62e28b17421d5aef5e593011ff54)
            check_type(argname="argument address1", value=address1, expected_type=type_hints["address1"])
            check_type(argname="argument address2", value=address2, expected_type=type_hints["address2"])
            check_type(argname="argument address3", value=address3, expected_type=type_hints["address3"])
            check_type(argname="argument address4", value=address4, expected_type=type_hints["address4"])
            check_type(argname="argument city", value=city, expected_type=type_hints["city"])
            check_type(argname="argument country", value=country, expected_type=type_hints["country"])
            check_type(argname="argument county", value=county, expected_type=type_hints["county"])
            check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
            check_type(argname="argument province", value=province, expected_type=type_hints["province"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address1 is not None:
            self._values["address1"] = address1
        if address2 is not None:
            self._values["address2"] = address2
        if address3 is not None:
            self._values["address3"] = address3
        if address4 is not None:
            self._values["address4"] = address4
        if city is not None:
            self._values["city"] = city
        if country is not None:
            self._values["country"] = country
        if county is not None:
            self._values["county"] = county
        if postal_code is not None:
            self._values["postal_code"] = postal_code
        if province is not None:
            self._values["province"] = province
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def address1(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.'''
        result = self._values.get("address1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address2(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.'''
        result = self._values.get("address2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address3(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.'''
        result = self._values.get("address3")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address4(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.'''
        result = self._values.get("address4")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def city(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.'''
        result = self._values.get("city")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.'''
        result = self._values.get("country")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def county(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.'''
        result = self._values.get("county")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.'''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def province(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.'''
        result = self._values.get("province")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesProfileBillingAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomerprofilesProfileBillingAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.customerprofilesProfile.CustomerprofilesProfileBillingAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dac9070e6be00a7b73c5a30797e6e4b121ae435b5e6281bb80a7d02ec9599096)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddress1")
    def reset_address1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress1", []))

    @jsii.member(jsii_name="resetAddress2")
    def reset_address2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress2", []))

    @jsii.member(jsii_name="resetAddress3")
    def reset_address3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress3", []))

    @jsii.member(jsii_name="resetAddress4")
    def reset_address4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress4", []))

    @jsii.member(jsii_name="resetCity")
    def reset_city(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCity", []))

    @jsii.member(jsii_name="resetCountry")
    def reset_country(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountry", []))

    @jsii.member(jsii_name="resetCounty")
    def reset_county(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCounty", []))

    @jsii.member(jsii_name="resetPostalCode")
    def reset_postal_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostalCode", []))

    @jsii.member(jsii_name="resetProvince")
    def reset_province(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvince", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @builtins.property
    @jsii.member(jsii_name="address1Input")
    def address1_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address1Input"))

    @builtins.property
    @jsii.member(jsii_name="address2Input")
    def address2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address2Input"))

    @builtins.property
    @jsii.member(jsii_name="address3Input")
    def address3_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address3Input"))

    @builtins.property
    @jsii.member(jsii_name="address4Input")
    def address4_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address4Input"))

    @builtins.property
    @jsii.member(jsii_name="cityInput")
    def city_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cityInput"))

    @builtins.property
    @jsii.member(jsii_name="countryInput")
    def country_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryInput"))

    @builtins.property
    @jsii.member(jsii_name="countyInput")
    def county_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countyInput"))

    @builtins.property
    @jsii.member(jsii_name="postalCodeInput")
    def postal_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postalCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="provinceInput")
    def province_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provinceInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="address1")
    def address1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address1"))

    @address1.setter
    def address1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3312ea67b7084ffeec545f8b194c294b1696717c9f5fbee727fb908e76a5fc23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address1", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address2")
    def address2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address2"))

    @address2.setter
    def address2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5323a69af51dadaba55bce047450b5fad5d2e6955275c388bae456e217084319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address3")
    def address3(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address3"))

    @address3.setter
    def address3(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31f3f0f86b55dd7ea959a8d10cf55be38f7b77a2f1e622b1cac10e6298c9c84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address3", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address4")
    def address4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address4"))

    @address4.setter
    def address4(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b459846b793e87f045fb5e4a73fa333be4090131c1fb10d83a46d5bb32fccfa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="city")
    def city(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "city"))

    @city.setter
    def city(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__500a7ee939b37821d63785f94e4279378e42d8e914c098927e72ad0459741de2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "city", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="country")
    def country(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "country"))

    @country.setter
    def country(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f52c4cc3c683f88b38fac4a107753d12bb911e44355f3563a48e316e9f56bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "country", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="county")
    def county(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "county"))

    @county.setter
    def county(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71dad32f651d721fdddeeb1fd52d76a76242f52425b5659f243c68f15105085d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "county", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574ab219f012061c8de81b7eee3a8aa51621036a0fc331ff175c915d531e8f9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="province")
    def province(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "province"))

    @province.setter
    def province(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc8b8abeb44df844c191afeb6c8c5970d9db2b58a972289939e794f4e8e6b4b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "province", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86f791af2a97bb7b12d19cc3f1122bc0e2c59b9e1e47f0e0cdc8f150155cdfa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CustomerprofilesProfileBillingAddress]:
        return typing.cast(typing.Optional[CustomerprofilesProfileBillingAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesProfileBillingAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d277e0ff42ad7562a61861b261825f1781c713a4c19b43ec7188cb7c13097eda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.customerprofilesProfile.CustomerprofilesProfileConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "domain_name": "domainName",
        "account_number": "accountNumber",
        "additional_information": "additionalInformation",
        "address": "address",
        "attributes": "attributes",
        "billing_address": "billingAddress",
        "birth_date": "birthDate",
        "business_email_address": "businessEmailAddress",
        "business_name": "businessName",
        "business_phone_number": "businessPhoneNumber",
        "email_address": "emailAddress",
        "first_name": "firstName",
        "gender_string": "genderString",
        "home_phone_number": "homePhoneNumber",
        "id": "id",
        "last_name": "lastName",
        "mailing_address": "mailingAddress",
        "middle_name": "middleName",
        "mobile_phone_number": "mobilePhoneNumber",
        "party_type_string": "partyTypeString",
        "personal_email_address": "personalEmailAddress",
        "phone_number": "phoneNumber",
        "region": "region",
        "shipping_address": "shippingAddress",
    },
)
class CustomerprofilesProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        domain_name: builtins.str,
        account_number: typing.Optional[builtins.str] = None,
        additional_information: typing.Optional[builtins.str] = None,
        address: typing.Optional[typing.Union[CustomerprofilesProfileAddress, typing.Dict[builtins.str, typing.Any]]] = None,
        attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        billing_address: typing.Optional[typing.Union[CustomerprofilesProfileBillingAddress, typing.Dict[builtins.str, typing.Any]]] = None,
        birth_date: typing.Optional[builtins.str] = None,
        business_email_address: typing.Optional[builtins.str] = None,
        business_name: typing.Optional[builtins.str] = None,
        business_phone_number: typing.Optional[builtins.str] = None,
        email_address: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        gender_string: typing.Optional[builtins.str] = None,
        home_phone_number: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        mailing_address: typing.Optional[typing.Union["CustomerprofilesProfileMailingAddress", typing.Dict[builtins.str, typing.Any]]] = None,
        middle_name: typing.Optional[builtins.str] = None,
        mobile_phone_number: typing.Optional[builtins.str] = None,
        party_type_string: typing.Optional[builtins.str] = None,
        personal_email_address: typing.Optional[builtins.str] = None,
        phone_number: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        shipping_address: typing.Optional[typing.Union["CustomerprofilesProfileShippingAddress", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#domain_name CustomerprofilesProfile#domain_name}.
        :param account_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#account_number CustomerprofilesProfile#account_number}.
        :param additional_information: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#additional_information CustomerprofilesProfile#additional_information}.
        :param address: address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address CustomerprofilesProfile#address}
        :param attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#attributes CustomerprofilesProfile#attributes}.
        :param billing_address: billing_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#billing_address CustomerprofilesProfile#billing_address}
        :param birth_date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#birth_date CustomerprofilesProfile#birth_date}.
        :param business_email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#business_email_address CustomerprofilesProfile#business_email_address}.
        :param business_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#business_name CustomerprofilesProfile#business_name}.
        :param business_phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#business_phone_number CustomerprofilesProfile#business_phone_number}.
        :param email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#email_address CustomerprofilesProfile#email_address}.
        :param first_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#first_name CustomerprofilesProfile#first_name}.
        :param gender_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#gender_string CustomerprofilesProfile#gender_string}.
        :param home_phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#home_phone_number CustomerprofilesProfile#home_phone_number}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#id CustomerprofilesProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param last_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#last_name CustomerprofilesProfile#last_name}.
        :param mailing_address: mailing_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#mailing_address CustomerprofilesProfile#mailing_address}
        :param middle_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#middle_name CustomerprofilesProfile#middle_name}.
        :param mobile_phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#mobile_phone_number CustomerprofilesProfile#mobile_phone_number}.
        :param party_type_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#party_type_string CustomerprofilesProfile#party_type_string}.
        :param personal_email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#personal_email_address CustomerprofilesProfile#personal_email_address}.
        :param phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#phone_number CustomerprofilesProfile#phone_number}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#region CustomerprofilesProfile#region}
        :param shipping_address: shipping_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#shipping_address CustomerprofilesProfile#shipping_address}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(address, dict):
            address = CustomerprofilesProfileAddress(**address)
        if isinstance(billing_address, dict):
            billing_address = CustomerprofilesProfileBillingAddress(**billing_address)
        if isinstance(mailing_address, dict):
            mailing_address = CustomerprofilesProfileMailingAddress(**mailing_address)
        if isinstance(shipping_address, dict):
            shipping_address = CustomerprofilesProfileShippingAddress(**shipping_address)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03b3e865c5d72c17cdd3d04087e92e8518c5b3f193180c1435185321da77d50)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument account_number", value=account_number, expected_type=type_hints["account_number"])
            check_type(argname="argument additional_information", value=additional_information, expected_type=type_hints["additional_information"])
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument billing_address", value=billing_address, expected_type=type_hints["billing_address"])
            check_type(argname="argument birth_date", value=birth_date, expected_type=type_hints["birth_date"])
            check_type(argname="argument business_email_address", value=business_email_address, expected_type=type_hints["business_email_address"])
            check_type(argname="argument business_name", value=business_name, expected_type=type_hints["business_name"])
            check_type(argname="argument business_phone_number", value=business_phone_number, expected_type=type_hints["business_phone_number"])
            check_type(argname="argument email_address", value=email_address, expected_type=type_hints["email_address"])
            check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
            check_type(argname="argument gender_string", value=gender_string, expected_type=type_hints["gender_string"])
            check_type(argname="argument home_phone_number", value=home_phone_number, expected_type=type_hints["home_phone_number"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
            check_type(argname="argument mailing_address", value=mailing_address, expected_type=type_hints["mailing_address"])
            check_type(argname="argument middle_name", value=middle_name, expected_type=type_hints["middle_name"])
            check_type(argname="argument mobile_phone_number", value=mobile_phone_number, expected_type=type_hints["mobile_phone_number"])
            check_type(argname="argument party_type_string", value=party_type_string, expected_type=type_hints["party_type_string"])
            check_type(argname="argument personal_email_address", value=personal_email_address, expected_type=type_hints["personal_email_address"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument shipping_address", value=shipping_address, expected_type=type_hints["shipping_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
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
        if account_number is not None:
            self._values["account_number"] = account_number
        if additional_information is not None:
            self._values["additional_information"] = additional_information
        if address is not None:
            self._values["address"] = address
        if attributes is not None:
            self._values["attributes"] = attributes
        if billing_address is not None:
            self._values["billing_address"] = billing_address
        if birth_date is not None:
            self._values["birth_date"] = birth_date
        if business_email_address is not None:
            self._values["business_email_address"] = business_email_address
        if business_name is not None:
            self._values["business_name"] = business_name
        if business_phone_number is not None:
            self._values["business_phone_number"] = business_phone_number
        if email_address is not None:
            self._values["email_address"] = email_address
        if first_name is not None:
            self._values["first_name"] = first_name
        if gender_string is not None:
            self._values["gender_string"] = gender_string
        if home_phone_number is not None:
            self._values["home_phone_number"] = home_phone_number
        if id is not None:
            self._values["id"] = id
        if last_name is not None:
            self._values["last_name"] = last_name
        if mailing_address is not None:
            self._values["mailing_address"] = mailing_address
        if middle_name is not None:
            self._values["middle_name"] = middle_name
        if mobile_phone_number is not None:
            self._values["mobile_phone_number"] = mobile_phone_number
        if party_type_string is not None:
            self._values["party_type_string"] = party_type_string
        if personal_email_address is not None:
            self._values["personal_email_address"] = personal_email_address
        if phone_number is not None:
            self._values["phone_number"] = phone_number
        if region is not None:
            self._values["region"] = region
        if shipping_address is not None:
            self._values["shipping_address"] = shipping_address

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
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#domain_name CustomerprofilesProfile#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_number(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#account_number CustomerprofilesProfile#account_number}.'''
        result = self._values.get("account_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def additional_information(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#additional_information CustomerprofilesProfile#additional_information}.'''
        result = self._values.get("additional_information")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address(self) -> typing.Optional[CustomerprofilesProfileAddress]:
        '''address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address CustomerprofilesProfile#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[CustomerprofilesProfileAddress], result)

    @builtins.property
    def attributes(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#attributes CustomerprofilesProfile#attributes}.'''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def billing_address(self) -> typing.Optional[CustomerprofilesProfileBillingAddress]:
        '''billing_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#billing_address CustomerprofilesProfile#billing_address}
        '''
        result = self._values.get("billing_address")
        return typing.cast(typing.Optional[CustomerprofilesProfileBillingAddress], result)

    @builtins.property
    def birth_date(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#birth_date CustomerprofilesProfile#birth_date}.'''
        result = self._values.get("birth_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def business_email_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#business_email_address CustomerprofilesProfile#business_email_address}.'''
        result = self._values.get("business_email_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def business_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#business_name CustomerprofilesProfile#business_name}.'''
        result = self._values.get("business_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def business_phone_number(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#business_phone_number CustomerprofilesProfile#business_phone_number}.'''
        result = self._values.get("business_phone_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#email_address CustomerprofilesProfile#email_address}.'''
        result = self._values.get("email_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#first_name CustomerprofilesProfile#first_name}.'''
        result = self._values.get("first_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gender_string(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#gender_string CustomerprofilesProfile#gender_string}.'''
        result = self._values.get("gender_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def home_phone_number(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#home_phone_number CustomerprofilesProfile#home_phone_number}.'''
        result = self._values.get("home_phone_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#id CustomerprofilesProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#last_name CustomerprofilesProfile#last_name}.'''
        result = self._values.get("last_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mailing_address(
        self,
    ) -> typing.Optional["CustomerprofilesProfileMailingAddress"]:
        '''mailing_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#mailing_address CustomerprofilesProfile#mailing_address}
        '''
        result = self._values.get("mailing_address")
        return typing.cast(typing.Optional["CustomerprofilesProfileMailingAddress"], result)

    @builtins.property
    def middle_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#middle_name CustomerprofilesProfile#middle_name}.'''
        result = self._values.get("middle_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mobile_phone_number(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#mobile_phone_number CustomerprofilesProfile#mobile_phone_number}.'''
        result = self._values.get("mobile_phone_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def party_type_string(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#party_type_string CustomerprofilesProfile#party_type_string}.'''
        result = self._values.get("party_type_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def personal_email_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#personal_email_address CustomerprofilesProfile#personal_email_address}.'''
        result = self._values.get("personal_email_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def phone_number(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#phone_number CustomerprofilesProfile#phone_number}.'''
        result = self._values.get("phone_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#region CustomerprofilesProfile#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shipping_address(
        self,
    ) -> typing.Optional["CustomerprofilesProfileShippingAddress"]:
        '''shipping_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#shipping_address CustomerprofilesProfile#shipping_address}
        '''
        result = self._values.get("shipping_address")
        return typing.cast(typing.Optional["CustomerprofilesProfileShippingAddress"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.customerprofilesProfile.CustomerprofilesProfileMailingAddress",
    jsii_struct_bases=[],
    name_mapping={
        "address1": "address1",
        "address2": "address2",
        "address3": "address3",
        "address4": "address4",
        "city": "city",
        "country": "country",
        "county": "county",
        "postal_code": "postalCode",
        "province": "province",
        "state": "state",
    },
)
class CustomerprofilesProfileMailingAddress:
    def __init__(
        self,
        *,
        address1: typing.Optional[builtins.str] = None,
        address2: typing.Optional[builtins.str] = None,
        address3: typing.Optional[builtins.str] = None,
        address4: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        county: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.
        :param address2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.
        :param address3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.
        :param address4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.
        :param country: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.
        :param county: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.
        :param postal_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.
        :param province: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0448cbab4f3475de4f05c49b221d101316d6db98d4d325ead3b1c61c4bc3ce17)
            check_type(argname="argument address1", value=address1, expected_type=type_hints["address1"])
            check_type(argname="argument address2", value=address2, expected_type=type_hints["address2"])
            check_type(argname="argument address3", value=address3, expected_type=type_hints["address3"])
            check_type(argname="argument address4", value=address4, expected_type=type_hints["address4"])
            check_type(argname="argument city", value=city, expected_type=type_hints["city"])
            check_type(argname="argument country", value=country, expected_type=type_hints["country"])
            check_type(argname="argument county", value=county, expected_type=type_hints["county"])
            check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
            check_type(argname="argument province", value=province, expected_type=type_hints["province"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address1 is not None:
            self._values["address1"] = address1
        if address2 is not None:
            self._values["address2"] = address2
        if address3 is not None:
            self._values["address3"] = address3
        if address4 is not None:
            self._values["address4"] = address4
        if city is not None:
            self._values["city"] = city
        if country is not None:
            self._values["country"] = country
        if county is not None:
            self._values["county"] = county
        if postal_code is not None:
            self._values["postal_code"] = postal_code
        if province is not None:
            self._values["province"] = province
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def address1(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.'''
        result = self._values.get("address1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address2(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.'''
        result = self._values.get("address2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address3(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.'''
        result = self._values.get("address3")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address4(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.'''
        result = self._values.get("address4")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def city(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.'''
        result = self._values.get("city")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.'''
        result = self._values.get("country")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def county(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.'''
        result = self._values.get("county")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.'''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def province(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.'''
        result = self._values.get("province")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesProfileMailingAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomerprofilesProfileMailingAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.customerprofilesProfile.CustomerprofilesProfileMailingAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f35edbcb9c0cf751d6b8a6c21d5948b289bc2121b7fb9b4de7d692cec0039b04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddress1")
    def reset_address1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress1", []))

    @jsii.member(jsii_name="resetAddress2")
    def reset_address2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress2", []))

    @jsii.member(jsii_name="resetAddress3")
    def reset_address3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress3", []))

    @jsii.member(jsii_name="resetAddress4")
    def reset_address4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress4", []))

    @jsii.member(jsii_name="resetCity")
    def reset_city(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCity", []))

    @jsii.member(jsii_name="resetCountry")
    def reset_country(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountry", []))

    @jsii.member(jsii_name="resetCounty")
    def reset_county(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCounty", []))

    @jsii.member(jsii_name="resetPostalCode")
    def reset_postal_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostalCode", []))

    @jsii.member(jsii_name="resetProvince")
    def reset_province(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvince", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @builtins.property
    @jsii.member(jsii_name="address1Input")
    def address1_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address1Input"))

    @builtins.property
    @jsii.member(jsii_name="address2Input")
    def address2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address2Input"))

    @builtins.property
    @jsii.member(jsii_name="address3Input")
    def address3_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address3Input"))

    @builtins.property
    @jsii.member(jsii_name="address4Input")
    def address4_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address4Input"))

    @builtins.property
    @jsii.member(jsii_name="cityInput")
    def city_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cityInput"))

    @builtins.property
    @jsii.member(jsii_name="countryInput")
    def country_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryInput"))

    @builtins.property
    @jsii.member(jsii_name="countyInput")
    def county_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countyInput"))

    @builtins.property
    @jsii.member(jsii_name="postalCodeInput")
    def postal_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postalCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="provinceInput")
    def province_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provinceInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="address1")
    def address1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address1"))

    @address1.setter
    def address1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b35078931b577c335f1f5235f8e6b19a75e917e44b680d42a36d63c8568969a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address1", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address2")
    def address2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address2"))

    @address2.setter
    def address2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__418a9d0d5dc929f77d869940b69dde94f2b7d7cf30dc42610242f00cb5356abe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address3")
    def address3(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address3"))

    @address3.setter
    def address3(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0dbeb184caaaad3132c902d09a7e70396cb592306d345482984f7eb13d53e52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address3", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address4")
    def address4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address4"))

    @address4.setter
    def address4(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__580ed4571996c741366336c402fa216db6b40499af95c1584bed0f6fa83020ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="city")
    def city(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "city"))

    @city.setter
    def city(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74828a63d0a69a81d68f875b6ec473f1cb48b46b221e283b4a26c86e38d6d794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "city", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="country")
    def country(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "country"))

    @country.setter
    def country(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4287ee45a92ab20219724ace12273b77edafe2395956bff5b79f4536bfc58d5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "country", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="county")
    def county(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "county"))

    @county.setter
    def county(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__470e66e10c8b4e8596349028f6dd518b3cf7ad1a4824ff62476793c0386efe87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "county", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fedecea716df58399f80386046cc743197e19b543ad293c6e53b21598a32ad47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="province")
    def province(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "province"))

    @province.setter
    def province(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3c4efa8d4071fcfa38f7d87114622f85c507a45c58bdd8772a24e308eadb2f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "province", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea6ee148207fdb29bddbbed819b29235ec525ce1f219f5f7d8688568e0e0b29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CustomerprofilesProfileMailingAddress]:
        return typing.cast(typing.Optional[CustomerprofilesProfileMailingAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesProfileMailingAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__170b4402de559dd3a251de61d78e1738ff9e652ccb372940b6a4804b7fd6e697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.customerprofilesProfile.CustomerprofilesProfileShippingAddress",
    jsii_struct_bases=[],
    name_mapping={
        "address1": "address1",
        "address2": "address2",
        "address3": "address3",
        "address4": "address4",
        "city": "city",
        "country": "country",
        "county": "county",
        "postal_code": "postalCode",
        "province": "province",
        "state": "state",
    },
)
class CustomerprofilesProfileShippingAddress:
    def __init__(
        self,
        *,
        address1: typing.Optional[builtins.str] = None,
        address2: typing.Optional[builtins.str] = None,
        address3: typing.Optional[builtins.str] = None,
        address4: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        county: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.
        :param address2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.
        :param address3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.
        :param address4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.
        :param country: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.
        :param county: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.
        :param postal_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.
        :param province: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__520b893d2f541bee73272d3715ce3c3d4463e96e5cc9cbc4a0028b19e6fb7143)
            check_type(argname="argument address1", value=address1, expected_type=type_hints["address1"])
            check_type(argname="argument address2", value=address2, expected_type=type_hints["address2"])
            check_type(argname="argument address3", value=address3, expected_type=type_hints["address3"])
            check_type(argname="argument address4", value=address4, expected_type=type_hints["address4"])
            check_type(argname="argument city", value=city, expected_type=type_hints["city"])
            check_type(argname="argument country", value=country, expected_type=type_hints["country"])
            check_type(argname="argument county", value=county, expected_type=type_hints["county"])
            check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
            check_type(argname="argument province", value=province, expected_type=type_hints["province"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address1 is not None:
            self._values["address1"] = address1
        if address2 is not None:
            self._values["address2"] = address2
        if address3 is not None:
            self._values["address3"] = address3
        if address4 is not None:
            self._values["address4"] = address4
        if city is not None:
            self._values["city"] = city
        if country is not None:
            self._values["country"] = country
        if county is not None:
            self._values["county"] = county
        if postal_code is not None:
            self._values["postal_code"] = postal_code
        if province is not None:
            self._values["province"] = province
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def address1(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.'''
        result = self._values.get("address1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address2(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.'''
        result = self._values.get("address2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address3(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.'''
        result = self._values.get("address3")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address4(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.'''
        result = self._values.get("address4")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def city(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.'''
        result = self._values.get("city")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.'''
        result = self._values.get("country")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def county(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.'''
        result = self._values.get("county")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.'''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def province(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.'''
        result = self._values.get("province")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesProfileShippingAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomerprofilesProfileShippingAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.customerprofilesProfile.CustomerprofilesProfileShippingAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__575242622bda97619850ea48f4a77fec7460c5f89d8a01aac28b6b3b84970be6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddress1")
    def reset_address1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress1", []))

    @jsii.member(jsii_name="resetAddress2")
    def reset_address2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress2", []))

    @jsii.member(jsii_name="resetAddress3")
    def reset_address3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress3", []))

    @jsii.member(jsii_name="resetAddress4")
    def reset_address4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress4", []))

    @jsii.member(jsii_name="resetCity")
    def reset_city(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCity", []))

    @jsii.member(jsii_name="resetCountry")
    def reset_country(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountry", []))

    @jsii.member(jsii_name="resetCounty")
    def reset_county(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCounty", []))

    @jsii.member(jsii_name="resetPostalCode")
    def reset_postal_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostalCode", []))

    @jsii.member(jsii_name="resetProvince")
    def reset_province(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvince", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @builtins.property
    @jsii.member(jsii_name="address1Input")
    def address1_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address1Input"))

    @builtins.property
    @jsii.member(jsii_name="address2Input")
    def address2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address2Input"))

    @builtins.property
    @jsii.member(jsii_name="address3Input")
    def address3_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address3Input"))

    @builtins.property
    @jsii.member(jsii_name="address4Input")
    def address4_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address4Input"))

    @builtins.property
    @jsii.member(jsii_name="cityInput")
    def city_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cityInput"))

    @builtins.property
    @jsii.member(jsii_name="countryInput")
    def country_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryInput"))

    @builtins.property
    @jsii.member(jsii_name="countyInput")
    def county_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countyInput"))

    @builtins.property
    @jsii.member(jsii_name="postalCodeInput")
    def postal_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postalCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="provinceInput")
    def province_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provinceInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="address1")
    def address1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address1"))

    @address1.setter
    def address1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a75cf48d9b2ffb5ebc019371b0096926ac30cd0aa635fb2992939debe829e5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address1", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address2")
    def address2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address2"))

    @address2.setter
    def address2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aa0205ec5a0b7229a3dca7070a98f77feda9cedf2c091fead88ad2fd18843de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address3")
    def address3(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address3"))

    @address3.setter
    def address3(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec86340b355e78ca535f45716c5d4ffdd319321ab99aebb0d85a980d6af6d48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address3", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address4")
    def address4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address4"))

    @address4.setter
    def address4(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3a329d95e91b2e0c57340b8fa8d1b399f2ce52004f203e53d9bc7a53ea12edc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="city")
    def city(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "city"))

    @city.setter
    def city(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84282ef7e5fbd33f88442768a3d20119fa37b289a81a780398a32232a61dc3a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "city", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="country")
    def country(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "country"))

    @country.setter
    def country(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a48bf3383a736ac4407258816bc983eaf76312c13598f09eb6b36a3805667708)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "country", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="county")
    def county(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "county"))

    @county.setter
    def county(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce66f6f07138cc1e277b258591c0edec361d8a215c3bb5ef28cfb0f6d2a4039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "county", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9be65ae4b11f94053c1b7e621a01438fbe4f7109f19922ca19e681e2c64d4747)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="province")
    def province(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "province"))

    @province.setter
    def province(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea7b9ad40b5eb2e63b30da1f1d4bd573fa60273c0e12f099e6207d62b3f91af5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "province", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__546e3ac7fde09d2afd276eef20e51a5bf8731441521e707f4c3ba9c3edc3fd92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CustomerprofilesProfileShippingAddress]:
        return typing.cast(typing.Optional[CustomerprofilesProfileShippingAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesProfileShippingAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec03ae91041a01413b84c558632ef12f39bc7f8bda0d9702c2516ef10abb24f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CustomerprofilesProfile",
    "CustomerprofilesProfileAddress",
    "CustomerprofilesProfileAddressOutputReference",
    "CustomerprofilesProfileBillingAddress",
    "CustomerprofilesProfileBillingAddressOutputReference",
    "CustomerprofilesProfileConfig",
    "CustomerprofilesProfileMailingAddress",
    "CustomerprofilesProfileMailingAddressOutputReference",
    "CustomerprofilesProfileShippingAddress",
    "CustomerprofilesProfileShippingAddressOutputReference",
]

publication.publish()

def _typecheckingstub__286a735a194bb21b26056a13c76cc590af724c27d8f746d69ff414956240ad7e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    domain_name: builtins.str,
    account_number: typing.Optional[builtins.str] = None,
    additional_information: typing.Optional[builtins.str] = None,
    address: typing.Optional[typing.Union[CustomerprofilesProfileAddress, typing.Dict[builtins.str, typing.Any]]] = None,
    attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    billing_address: typing.Optional[typing.Union[CustomerprofilesProfileBillingAddress, typing.Dict[builtins.str, typing.Any]]] = None,
    birth_date: typing.Optional[builtins.str] = None,
    business_email_address: typing.Optional[builtins.str] = None,
    business_name: typing.Optional[builtins.str] = None,
    business_phone_number: typing.Optional[builtins.str] = None,
    email_address: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    gender_string: typing.Optional[builtins.str] = None,
    home_phone_number: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    mailing_address: typing.Optional[typing.Union[CustomerprofilesProfileMailingAddress, typing.Dict[builtins.str, typing.Any]]] = None,
    middle_name: typing.Optional[builtins.str] = None,
    mobile_phone_number: typing.Optional[builtins.str] = None,
    party_type_string: typing.Optional[builtins.str] = None,
    personal_email_address: typing.Optional[builtins.str] = None,
    phone_number: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    shipping_address: typing.Optional[typing.Union[CustomerprofilesProfileShippingAddress, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d508db9dbc4129efb481bdf78910624adcb79d2036069cff97fab0a2337a8e93(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c6b14f644c7c000e9a45ca183acf72b73d1ddc10c94345ce8e3a033dddd4ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6de069a5e433e4edc537ba9c167a4f4461c0e7f1f31ad936296ff7b1e4d60e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80055f9502869ef978414346747c1257e6ad4637dd2e97def99f94d5dbb70069(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca7f594314aa15e9abc2e5731479efe24f0fed671d622a0a8f76e9c577f2665f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388b9c0957c7288c7984e4f079581df2ca050fdf6d4f1104e8e9e8788b9572ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c77572190bbacbb807cc22c148f41702201df8fcdc67e0e2789d84830071125(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b8fdfbea4b2bd3940861930791ce194cbf5f789bd0163c58919a3da0fc4cab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a1526f03990e057fd0f35e5c4615959f8e3ec00b90fd6f6ea5f90220e5f107(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b4479b5764a552595b253285bc3c870e7f816b959c91cf080b3fddde5ab7bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735272019693e0a3526302499fb4b21fa159c1a13068261ab60791dda38606fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83034a8ed4fb23c154fb57696d4b4c2ba8caa986b103638a8c7a0f4e4f44bf53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80671af65429a08156fe1822663377a70b0984ddc85226f90089c34b90b979e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd82711e5c57c193f6a3355e946e7dd71788fae6067a5801f7dc7d19511933f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b453dd61bb551d462baa2e2472eb66ae3eaf4302625aae5e0483710c630d1e90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1add9cb1673673e470f0f2d227e035923cec47d2d334fc6f8f87ce39e0901e7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac709921df4316822d9b0fdf31c3b08e9647a67e67339862c3574f0ea8464034(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a795081f5f8463dcada0707888a38876b1693ff3ad44141209dda510ec27275(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe61b2de783e36ca8b23b2d8bbf1ad6961aa34256f97ab01eb5cd8686cd77bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b361ebe50002c159495450d072137387e2fb88c48ae81be9fe42cf2566443fcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dac2c4364c27ac65c3c79a19b08528bc8137ff5d2a264a2ba65cfe6007b048e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27f606049198b66fdda91d2d036679390e1bd18e1b859f80639cc3c3014bb55(
    *,
    address1: typing.Optional[builtins.str] = None,
    address2: typing.Optional[builtins.str] = None,
    address3: typing.Optional[builtins.str] = None,
    address4: typing.Optional[builtins.str] = None,
    city: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    county: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    province: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f506043be9ccdfbc6dc45f6a21d10995c8255f76e62bd335b9701e54b37864(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9bc70b3bc7b034e8a29528ebb75e84a49c4f4e16966ef14e45691ada3684dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e53f50d4939794018df36521fe9be452bb3a0820e0c16b56ebad5ee07b4afb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7168376cfc381c99c22bd36831a87457baf27ef404a68f1c420c2be1e42f9800(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa92bbfb19b1915ac7e34da5377091820a187dd86392a0ae97d9fde65265735e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6255056e84799dab564e0c8a472a3e30cd036100bf8f99bd01326da4c4994e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c5e70f7739213f967819a4d104c57eec7e9a19c54f94c6cf9eed4c76781e76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006e15ff70a276e2f5b77cea7fa9a3a01b46038b45bbc6f5cbb36b3a25f4ca85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db50af56bf85fb22ac26b74b6c04e865951a1656abea2ba7b24ba1d1b7d67903(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6cea153e77c7538c96d21d06c167dbfc4c6b16caa15b404cf5b894820278c9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f57ca773af0cc46d0e6355cc6d8f6327c94dbd940a14e8047eaa06b664ef4fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b851e442224c8219513cf7b92a2d00725644dfa9622937202755585a98b074(
    value: typing.Optional[CustomerprofilesProfileAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce9591fc3889db608c96b5127fdfb17830e62e28b17421d5aef5e593011ff54(
    *,
    address1: typing.Optional[builtins.str] = None,
    address2: typing.Optional[builtins.str] = None,
    address3: typing.Optional[builtins.str] = None,
    address4: typing.Optional[builtins.str] = None,
    city: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    county: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    province: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dac9070e6be00a7b73c5a30797e6e4b121ae435b5e6281bb80a7d02ec9599096(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3312ea67b7084ffeec545f8b194c294b1696717c9f5fbee727fb908e76a5fc23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5323a69af51dadaba55bce047450b5fad5d2e6955275c388bae456e217084319(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31f3f0f86b55dd7ea959a8d10cf55be38f7b77a2f1e622b1cac10e6298c9c84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b459846b793e87f045fb5e4a73fa333be4090131c1fb10d83a46d5bb32fccfa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500a7ee939b37821d63785f94e4279378e42d8e914c098927e72ad0459741de2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f52c4cc3c683f88b38fac4a107753d12bb911e44355f3563a48e316e9f56bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71dad32f651d721fdddeeb1fd52d76a76242f52425b5659f243c68f15105085d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574ab219f012061c8de81b7eee3a8aa51621036a0fc331ff175c915d531e8f9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8b8abeb44df844c191afeb6c8c5970d9db2b58a972289939e794f4e8e6b4b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f791af2a97bb7b12d19cc3f1122bc0e2c59b9e1e47f0e0cdc8f150155cdfa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d277e0ff42ad7562a61861b261825f1781c713a4c19b43ec7188cb7c13097eda(
    value: typing.Optional[CustomerprofilesProfileBillingAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03b3e865c5d72c17cdd3d04087e92e8518c5b3f193180c1435185321da77d50(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    domain_name: builtins.str,
    account_number: typing.Optional[builtins.str] = None,
    additional_information: typing.Optional[builtins.str] = None,
    address: typing.Optional[typing.Union[CustomerprofilesProfileAddress, typing.Dict[builtins.str, typing.Any]]] = None,
    attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    billing_address: typing.Optional[typing.Union[CustomerprofilesProfileBillingAddress, typing.Dict[builtins.str, typing.Any]]] = None,
    birth_date: typing.Optional[builtins.str] = None,
    business_email_address: typing.Optional[builtins.str] = None,
    business_name: typing.Optional[builtins.str] = None,
    business_phone_number: typing.Optional[builtins.str] = None,
    email_address: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    gender_string: typing.Optional[builtins.str] = None,
    home_phone_number: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    mailing_address: typing.Optional[typing.Union[CustomerprofilesProfileMailingAddress, typing.Dict[builtins.str, typing.Any]]] = None,
    middle_name: typing.Optional[builtins.str] = None,
    mobile_phone_number: typing.Optional[builtins.str] = None,
    party_type_string: typing.Optional[builtins.str] = None,
    personal_email_address: typing.Optional[builtins.str] = None,
    phone_number: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    shipping_address: typing.Optional[typing.Union[CustomerprofilesProfileShippingAddress, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0448cbab4f3475de4f05c49b221d101316d6db98d4d325ead3b1c61c4bc3ce17(
    *,
    address1: typing.Optional[builtins.str] = None,
    address2: typing.Optional[builtins.str] = None,
    address3: typing.Optional[builtins.str] = None,
    address4: typing.Optional[builtins.str] = None,
    city: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    county: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    province: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f35edbcb9c0cf751d6b8a6c21d5948b289bc2121b7fb9b4de7d692cec0039b04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b35078931b577c335f1f5235f8e6b19a75e917e44b680d42a36d63c8568969a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418a9d0d5dc929f77d869940b69dde94f2b7d7cf30dc42610242f00cb5356abe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0dbeb184caaaad3132c902d09a7e70396cb592306d345482984f7eb13d53e52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580ed4571996c741366336c402fa216db6b40499af95c1584bed0f6fa83020ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74828a63d0a69a81d68f875b6ec473f1cb48b46b221e283b4a26c86e38d6d794(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4287ee45a92ab20219724ace12273b77edafe2395956bff5b79f4536bfc58d5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470e66e10c8b4e8596349028f6dd518b3cf7ad1a4824ff62476793c0386efe87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fedecea716df58399f80386046cc743197e19b543ad293c6e53b21598a32ad47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3c4efa8d4071fcfa38f7d87114622f85c507a45c58bdd8772a24e308eadb2f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea6ee148207fdb29bddbbed819b29235ec525ce1f219f5f7d8688568e0e0b29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__170b4402de559dd3a251de61d78e1738ff9e652ccb372940b6a4804b7fd6e697(
    value: typing.Optional[CustomerprofilesProfileMailingAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520b893d2f541bee73272d3715ce3c3d4463e96e5cc9cbc4a0028b19e6fb7143(
    *,
    address1: typing.Optional[builtins.str] = None,
    address2: typing.Optional[builtins.str] = None,
    address3: typing.Optional[builtins.str] = None,
    address4: typing.Optional[builtins.str] = None,
    city: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    county: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    province: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575242622bda97619850ea48f4a77fec7460c5f89d8a01aac28b6b3b84970be6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a75cf48d9b2ffb5ebc019371b0096926ac30cd0aa635fb2992939debe829e5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa0205ec5a0b7229a3dca7070a98f77feda9cedf2c091fead88ad2fd18843de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec86340b355e78ca535f45716c5d4ffdd319321ab99aebb0d85a980d6af6d48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a329d95e91b2e0c57340b8fa8d1b399f2ce52004f203e53d9bc7a53ea12edc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84282ef7e5fbd33f88442768a3d20119fa37b289a81a780398a32232a61dc3a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a48bf3383a736ac4407258816bc983eaf76312c13598f09eb6b36a3805667708(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce66f6f07138cc1e277b258591c0edec361d8a215c3bb5ef28cfb0f6d2a4039(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9be65ae4b11f94053c1b7e621a01438fbe4f7109f19922ca19e681e2c64d4747(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7b9ad40b5eb2e63b30da1f1d4bd573fa60273c0e12f099e6207d62b3f91af5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__546e3ac7fde09d2afd276eef20e51a5bf8731441521e707f4c3ba9c3edc3fd92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec03ae91041a01413b84c558632ef12f39bc7f8bda0d9702c2516ef10abb24f(
    value: typing.Optional[CustomerprofilesProfileShippingAddress],
) -> None:
    """Type checking stubs"""
    pass
