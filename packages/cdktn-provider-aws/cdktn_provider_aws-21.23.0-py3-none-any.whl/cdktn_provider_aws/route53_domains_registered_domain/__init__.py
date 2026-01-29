r'''
# `aws_route53domains_registered_domain`

Refer to the Terraform Registry for docs: [`aws_route53domains_registered_domain`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain).
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


class Route53DomainsRegisteredDomain(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.route53DomainsRegisteredDomain.Route53DomainsRegisteredDomain",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain aws_route53domains_registered_domain}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        domain_name: builtins.str,
        admin_contact: typing.Optional[typing.Union["Route53DomainsRegisteredDomainAdminContact", typing.Dict[builtins.str, typing.Any]]] = None,
        admin_privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_renew: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        billing_contact: typing.Optional[typing.Union["Route53DomainsRegisteredDomainBillingContact", typing.Dict[builtins.str, typing.Any]]] = None,
        billing_privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        name_server: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Route53DomainsRegisteredDomainNameServer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        registrant_contact: typing.Optional[typing.Union["Route53DomainsRegisteredDomainRegistrantContact", typing.Dict[builtins.str, typing.Any]]] = None,
        registrant_privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tech_contact: typing.Optional[typing.Union["Route53DomainsRegisteredDomainTechContact", typing.Dict[builtins.str, typing.Any]]] = None,
        tech_privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["Route53DomainsRegisteredDomainTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transfer_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain aws_route53domains_registered_domain} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#domain_name Route53DomainsRegisteredDomain#domain_name}.
        :param admin_contact: admin_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#admin_contact Route53DomainsRegisteredDomain#admin_contact}
        :param admin_privacy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#admin_privacy Route53DomainsRegisteredDomain#admin_privacy}.
        :param auto_renew: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#auto_renew Route53DomainsRegisteredDomain#auto_renew}.
        :param billing_contact: billing_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#billing_contact Route53DomainsRegisteredDomain#billing_contact}
        :param billing_privacy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#billing_privacy Route53DomainsRegisteredDomain#billing_privacy}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#id Route53DomainsRegisteredDomain#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name_server: name_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#name_server Route53DomainsRegisteredDomain#name_server}
        :param registrant_contact: registrant_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#registrant_contact Route53DomainsRegisteredDomain#registrant_contact}
        :param registrant_privacy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#registrant_privacy Route53DomainsRegisteredDomain#registrant_privacy}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#tags Route53DomainsRegisteredDomain#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#tags_all Route53DomainsRegisteredDomain#tags_all}.
        :param tech_contact: tech_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#tech_contact Route53DomainsRegisteredDomain#tech_contact}
        :param tech_privacy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#tech_privacy Route53DomainsRegisteredDomain#tech_privacy}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#timeouts Route53DomainsRegisteredDomain#timeouts}
        :param transfer_lock: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#transfer_lock Route53DomainsRegisteredDomain#transfer_lock}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__990051850705ac8a40315ac2abdf16d859b28f1f3b62e234cb6e0480f9690c4c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = Route53DomainsRegisteredDomainConfig(
            domain_name=domain_name,
            admin_contact=admin_contact,
            admin_privacy=admin_privacy,
            auto_renew=auto_renew,
            billing_contact=billing_contact,
            billing_privacy=billing_privacy,
            id=id,
            name_server=name_server,
            registrant_contact=registrant_contact,
            registrant_privacy=registrant_privacy,
            tags=tags,
            tags_all=tags_all,
            tech_contact=tech_contact,
            tech_privacy=tech_privacy,
            timeouts=timeouts,
            transfer_lock=transfer_lock,
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
        '''Generates CDKTF code for importing a Route53DomainsRegisteredDomain resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Route53DomainsRegisteredDomain to import.
        :param import_from_id: The id of the existing Route53DomainsRegisteredDomain that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Route53DomainsRegisteredDomain to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd3a2e306cd69a57c37e6bcf57563dcbd879f0dac6295d9aa284d2fa183f097)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdminContact")
    def put_admin_contact(
        self,
        *,
        address_line1: typing.Optional[builtins.str] = None,
        address_line2: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        contact_type: typing.Optional[builtins.str] = None,
        country_code: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        fax: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        organization_name: typing.Optional[builtins.str] = None,
        phone_number: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        zip_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address_line1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_1 Route53DomainsRegisteredDomain#address_line_1}.
        :param address_line2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_2 Route53DomainsRegisteredDomain#address_line_2}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#city Route53DomainsRegisteredDomain#city}.
        :param contact_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#contact_type Route53DomainsRegisteredDomain#contact_type}.
        :param country_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#country_code Route53DomainsRegisteredDomain#country_code}.
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#email Route53DomainsRegisteredDomain#email}.
        :param extra_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#extra_params Route53DomainsRegisteredDomain#extra_params}.
        :param fax: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#fax Route53DomainsRegisteredDomain#fax}.
        :param first_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#first_name Route53DomainsRegisteredDomain#first_name}.
        :param last_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#last_name Route53DomainsRegisteredDomain#last_name}.
        :param organization_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#organization_name Route53DomainsRegisteredDomain#organization_name}.
        :param phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#phone_number Route53DomainsRegisteredDomain#phone_number}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#state Route53DomainsRegisteredDomain#state}.
        :param zip_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#zip_code Route53DomainsRegisteredDomain#zip_code}.
        '''
        value = Route53DomainsRegisteredDomainAdminContact(
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            contact_type=contact_type,
            country_code=country_code,
            email=email,
            extra_params=extra_params,
            fax=fax,
            first_name=first_name,
            last_name=last_name,
            organization_name=organization_name,
            phone_number=phone_number,
            state=state,
            zip_code=zip_code,
        )

        return typing.cast(None, jsii.invoke(self, "putAdminContact", [value]))

    @jsii.member(jsii_name="putBillingContact")
    def put_billing_contact(
        self,
        *,
        address_line1: typing.Optional[builtins.str] = None,
        address_line2: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        contact_type: typing.Optional[builtins.str] = None,
        country_code: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        fax: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        organization_name: typing.Optional[builtins.str] = None,
        phone_number: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        zip_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address_line1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_1 Route53DomainsRegisteredDomain#address_line_1}.
        :param address_line2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_2 Route53DomainsRegisteredDomain#address_line_2}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#city Route53DomainsRegisteredDomain#city}.
        :param contact_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#contact_type Route53DomainsRegisteredDomain#contact_type}.
        :param country_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#country_code Route53DomainsRegisteredDomain#country_code}.
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#email Route53DomainsRegisteredDomain#email}.
        :param extra_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#extra_params Route53DomainsRegisteredDomain#extra_params}.
        :param fax: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#fax Route53DomainsRegisteredDomain#fax}.
        :param first_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#first_name Route53DomainsRegisteredDomain#first_name}.
        :param last_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#last_name Route53DomainsRegisteredDomain#last_name}.
        :param organization_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#organization_name Route53DomainsRegisteredDomain#organization_name}.
        :param phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#phone_number Route53DomainsRegisteredDomain#phone_number}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#state Route53DomainsRegisteredDomain#state}.
        :param zip_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#zip_code Route53DomainsRegisteredDomain#zip_code}.
        '''
        value = Route53DomainsRegisteredDomainBillingContact(
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            contact_type=contact_type,
            country_code=country_code,
            email=email,
            extra_params=extra_params,
            fax=fax,
            first_name=first_name,
            last_name=last_name,
            organization_name=organization_name,
            phone_number=phone_number,
            state=state,
            zip_code=zip_code,
        )

        return typing.cast(None, jsii.invoke(self, "putBillingContact", [value]))

    @jsii.member(jsii_name="putNameServer")
    def put_name_server(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Route53DomainsRegisteredDomainNameServer", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ea364002cd6ee4d39d3a13ca90d07df37c0c5af4f552a0c5be5f8283a0ea2e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNameServer", [value]))

    @jsii.member(jsii_name="putRegistrantContact")
    def put_registrant_contact(
        self,
        *,
        address_line1: typing.Optional[builtins.str] = None,
        address_line2: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        contact_type: typing.Optional[builtins.str] = None,
        country_code: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        fax: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        organization_name: typing.Optional[builtins.str] = None,
        phone_number: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        zip_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address_line1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_1 Route53DomainsRegisteredDomain#address_line_1}.
        :param address_line2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_2 Route53DomainsRegisteredDomain#address_line_2}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#city Route53DomainsRegisteredDomain#city}.
        :param contact_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#contact_type Route53DomainsRegisteredDomain#contact_type}.
        :param country_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#country_code Route53DomainsRegisteredDomain#country_code}.
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#email Route53DomainsRegisteredDomain#email}.
        :param extra_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#extra_params Route53DomainsRegisteredDomain#extra_params}.
        :param fax: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#fax Route53DomainsRegisteredDomain#fax}.
        :param first_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#first_name Route53DomainsRegisteredDomain#first_name}.
        :param last_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#last_name Route53DomainsRegisteredDomain#last_name}.
        :param organization_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#organization_name Route53DomainsRegisteredDomain#organization_name}.
        :param phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#phone_number Route53DomainsRegisteredDomain#phone_number}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#state Route53DomainsRegisteredDomain#state}.
        :param zip_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#zip_code Route53DomainsRegisteredDomain#zip_code}.
        '''
        value = Route53DomainsRegisteredDomainRegistrantContact(
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            contact_type=contact_type,
            country_code=country_code,
            email=email,
            extra_params=extra_params,
            fax=fax,
            first_name=first_name,
            last_name=last_name,
            organization_name=organization_name,
            phone_number=phone_number,
            state=state,
            zip_code=zip_code,
        )

        return typing.cast(None, jsii.invoke(self, "putRegistrantContact", [value]))

    @jsii.member(jsii_name="putTechContact")
    def put_tech_contact(
        self,
        *,
        address_line1: typing.Optional[builtins.str] = None,
        address_line2: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        contact_type: typing.Optional[builtins.str] = None,
        country_code: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        fax: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        organization_name: typing.Optional[builtins.str] = None,
        phone_number: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        zip_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address_line1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_1 Route53DomainsRegisteredDomain#address_line_1}.
        :param address_line2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_2 Route53DomainsRegisteredDomain#address_line_2}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#city Route53DomainsRegisteredDomain#city}.
        :param contact_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#contact_type Route53DomainsRegisteredDomain#contact_type}.
        :param country_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#country_code Route53DomainsRegisteredDomain#country_code}.
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#email Route53DomainsRegisteredDomain#email}.
        :param extra_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#extra_params Route53DomainsRegisteredDomain#extra_params}.
        :param fax: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#fax Route53DomainsRegisteredDomain#fax}.
        :param first_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#first_name Route53DomainsRegisteredDomain#first_name}.
        :param last_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#last_name Route53DomainsRegisteredDomain#last_name}.
        :param organization_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#organization_name Route53DomainsRegisteredDomain#organization_name}.
        :param phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#phone_number Route53DomainsRegisteredDomain#phone_number}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#state Route53DomainsRegisteredDomain#state}.
        :param zip_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#zip_code Route53DomainsRegisteredDomain#zip_code}.
        '''
        value = Route53DomainsRegisteredDomainTechContact(
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            contact_type=contact_type,
            country_code=country_code,
            email=email,
            extra_params=extra_params,
            fax=fax,
            first_name=first_name,
            last_name=last_name,
            organization_name=organization_name,
            phone_number=phone_number,
            state=state,
            zip_code=zip_code,
        )

        return typing.cast(None, jsii.invoke(self, "putTechContact", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#create Route53DomainsRegisteredDomain#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#update Route53DomainsRegisteredDomain#update}.
        '''
        value = Route53DomainsRegisteredDomainTimeouts(create=create, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdminContact")
    def reset_admin_contact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminContact", []))

    @jsii.member(jsii_name="resetAdminPrivacy")
    def reset_admin_privacy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminPrivacy", []))

    @jsii.member(jsii_name="resetAutoRenew")
    def reset_auto_renew(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoRenew", []))

    @jsii.member(jsii_name="resetBillingContact")
    def reset_billing_contact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBillingContact", []))

    @jsii.member(jsii_name="resetBillingPrivacy")
    def reset_billing_privacy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBillingPrivacy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNameServer")
    def reset_name_server(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameServer", []))

    @jsii.member(jsii_name="resetRegistrantContact")
    def reset_registrant_contact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistrantContact", []))

    @jsii.member(jsii_name="resetRegistrantPrivacy")
    def reset_registrant_privacy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistrantPrivacy", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTechContact")
    def reset_tech_contact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTechContact", []))

    @jsii.member(jsii_name="resetTechPrivacy")
    def reset_tech_privacy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTechPrivacy", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTransferLock")
    def reset_transfer_lock(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransferLock", []))

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
    @jsii.member(jsii_name="abuseContactEmail")
    def abuse_contact_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "abuseContactEmail"))

    @builtins.property
    @jsii.member(jsii_name="abuseContactPhone")
    def abuse_contact_phone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "abuseContactPhone"))

    @builtins.property
    @jsii.member(jsii_name="adminContact")
    def admin_contact(
        self,
    ) -> "Route53DomainsRegisteredDomainAdminContactOutputReference":
        return typing.cast("Route53DomainsRegisteredDomainAdminContactOutputReference", jsii.get(self, "adminContact"))

    @builtins.property
    @jsii.member(jsii_name="billingContact")
    def billing_contact(
        self,
    ) -> "Route53DomainsRegisteredDomainBillingContactOutputReference":
        return typing.cast("Route53DomainsRegisteredDomainBillingContactOutputReference", jsii.get(self, "billingContact"))

    @builtins.property
    @jsii.member(jsii_name="creationDate")
    def creation_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationDate"))

    @builtins.property
    @jsii.member(jsii_name="expirationDate")
    def expiration_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationDate"))

    @builtins.property
    @jsii.member(jsii_name="nameServer")
    def name_server(self) -> "Route53DomainsRegisteredDomainNameServerList":
        return typing.cast("Route53DomainsRegisteredDomainNameServerList", jsii.get(self, "nameServer"))

    @builtins.property
    @jsii.member(jsii_name="registrantContact")
    def registrant_contact(
        self,
    ) -> "Route53DomainsRegisteredDomainRegistrantContactOutputReference":
        return typing.cast("Route53DomainsRegisteredDomainRegistrantContactOutputReference", jsii.get(self, "registrantContact"))

    @builtins.property
    @jsii.member(jsii_name="registrarName")
    def registrar_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registrarName"))

    @builtins.property
    @jsii.member(jsii_name="registrarUrl")
    def registrar_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registrarUrl"))

    @builtins.property
    @jsii.member(jsii_name="reseller")
    def reseller(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reseller"))

    @builtins.property
    @jsii.member(jsii_name="statusList")
    def status_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "statusList"))

    @builtins.property
    @jsii.member(jsii_name="techContact")
    def tech_contact(
        self,
    ) -> "Route53DomainsRegisteredDomainTechContactOutputReference":
        return typing.cast("Route53DomainsRegisteredDomainTechContactOutputReference", jsii.get(self, "techContact"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "Route53DomainsRegisteredDomainTimeoutsOutputReference":
        return typing.cast("Route53DomainsRegisteredDomainTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updatedDate")
    def updated_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedDate"))

    @builtins.property
    @jsii.member(jsii_name="whoisServer")
    def whois_server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "whoisServer"))

    @builtins.property
    @jsii.member(jsii_name="adminContactInput")
    def admin_contact_input(
        self,
    ) -> typing.Optional["Route53DomainsRegisteredDomainAdminContact"]:
        return typing.cast(typing.Optional["Route53DomainsRegisteredDomainAdminContact"], jsii.get(self, "adminContactInput"))

    @builtins.property
    @jsii.member(jsii_name="adminPrivacyInput")
    def admin_privacy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "adminPrivacyInput"))

    @builtins.property
    @jsii.member(jsii_name="autoRenewInput")
    def auto_renew_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoRenewInput"))

    @builtins.property
    @jsii.member(jsii_name="billingContactInput")
    def billing_contact_input(
        self,
    ) -> typing.Optional["Route53DomainsRegisteredDomainBillingContact"]:
        return typing.cast(typing.Optional["Route53DomainsRegisteredDomainBillingContact"], jsii.get(self, "billingContactInput"))

    @builtins.property
    @jsii.member(jsii_name="billingPrivacyInput")
    def billing_privacy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "billingPrivacyInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameServerInput")
    def name_server_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53DomainsRegisteredDomainNameServer"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53DomainsRegisteredDomainNameServer"]]], jsii.get(self, "nameServerInput"))

    @builtins.property
    @jsii.member(jsii_name="registrantContactInput")
    def registrant_contact_input(
        self,
    ) -> typing.Optional["Route53DomainsRegisteredDomainRegistrantContact"]:
        return typing.cast(typing.Optional["Route53DomainsRegisteredDomainRegistrantContact"], jsii.get(self, "registrantContactInput"))

    @builtins.property
    @jsii.member(jsii_name="registrantPrivacyInput")
    def registrant_privacy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "registrantPrivacyInput"))

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
    @jsii.member(jsii_name="techContactInput")
    def tech_contact_input(
        self,
    ) -> typing.Optional["Route53DomainsRegisteredDomainTechContact"]:
        return typing.cast(typing.Optional["Route53DomainsRegisteredDomainTechContact"], jsii.get(self, "techContactInput"))

    @builtins.property
    @jsii.member(jsii_name="techPrivacyInput")
    def tech_privacy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "techPrivacyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "Route53DomainsRegisteredDomainTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "Route53DomainsRegisteredDomainTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="transferLockInput")
    def transfer_lock_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "transferLockInput"))

    @builtins.property
    @jsii.member(jsii_name="adminPrivacy")
    def admin_privacy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "adminPrivacy"))

    @admin_privacy.setter
    def admin_privacy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a538f31553930e89e8ecdc615cc840213bcb881cd19c076332a51ed90421b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminPrivacy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoRenew")
    def auto_renew(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoRenew"))

    @auto_renew.setter
    def auto_renew(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af380e828c67a0f50a43dac464bb8030ebb772fcb2c059eedd543893a09aa6ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoRenew", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="billingPrivacy")
    def billing_privacy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "billingPrivacy"))

    @billing_privacy.setter
    def billing_privacy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__242e625cb6f669b5c9152f8835b0e027c986fbe61d213e27018fdfb467620f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingPrivacy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbea6408212a6af509d1686437e84ded58e504416247d83402ec0e92e334d6b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9719193fd935960e274c582be531da7abb6dfee31c993f58a1cdad5e5796adb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registrantPrivacy")
    def registrant_privacy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "registrantPrivacy"))

    @registrant_privacy.setter
    def registrant_privacy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbfb979fc76a5af02daf5c17d43ea375a16eb000b157bd1236d7fe05f0f0a51f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registrantPrivacy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de5bf1462f8aee4446c7db2f00e5623805094951c100f0f9050c10519e3adaea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__830c00d1b3ceae941f3b4fac0be2bfa95734ce66eec20d01ff66daf3d07b2cd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="techPrivacy")
    def tech_privacy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "techPrivacy"))

    @tech_privacy.setter
    def tech_privacy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__390548121375afe7300a8579057520541e71441a6d15cc22b046ecff10a19450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "techPrivacy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transferLock")
    def transfer_lock(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "transferLock"))

    @transfer_lock.setter
    def transfer_lock(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb2ca3d47307b25302d9ccb7cf56652316e95f22ff959a0e004a797616442e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transferLock", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.route53DomainsRegisteredDomain.Route53DomainsRegisteredDomainAdminContact",
    jsii_struct_bases=[],
    name_mapping={
        "address_line1": "addressLine1",
        "address_line2": "addressLine2",
        "city": "city",
        "contact_type": "contactType",
        "country_code": "countryCode",
        "email": "email",
        "extra_params": "extraParams",
        "fax": "fax",
        "first_name": "firstName",
        "last_name": "lastName",
        "organization_name": "organizationName",
        "phone_number": "phoneNumber",
        "state": "state",
        "zip_code": "zipCode",
    },
)
class Route53DomainsRegisteredDomainAdminContact:
    def __init__(
        self,
        *,
        address_line1: typing.Optional[builtins.str] = None,
        address_line2: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        contact_type: typing.Optional[builtins.str] = None,
        country_code: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        fax: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        organization_name: typing.Optional[builtins.str] = None,
        phone_number: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        zip_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address_line1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_1 Route53DomainsRegisteredDomain#address_line_1}.
        :param address_line2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_2 Route53DomainsRegisteredDomain#address_line_2}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#city Route53DomainsRegisteredDomain#city}.
        :param contact_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#contact_type Route53DomainsRegisteredDomain#contact_type}.
        :param country_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#country_code Route53DomainsRegisteredDomain#country_code}.
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#email Route53DomainsRegisteredDomain#email}.
        :param extra_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#extra_params Route53DomainsRegisteredDomain#extra_params}.
        :param fax: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#fax Route53DomainsRegisteredDomain#fax}.
        :param first_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#first_name Route53DomainsRegisteredDomain#first_name}.
        :param last_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#last_name Route53DomainsRegisteredDomain#last_name}.
        :param organization_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#organization_name Route53DomainsRegisteredDomain#organization_name}.
        :param phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#phone_number Route53DomainsRegisteredDomain#phone_number}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#state Route53DomainsRegisteredDomain#state}.
        :param zip_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#zip_code Route53DomainsRegisteredDomain#zip_code}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84ad4e9066633064d6308d49f6000700b557487c5813a10fe26c7fc2aa4b4a7)
            check_type(argname="argument address_line1", value=address_line1, expected_type=type_hints["address_line1"])
            check_type(argname="argument address_line2", value=address_line2, expected_type=type_hints["address_line2"])
            check_type(argname="argument city", value=city, expected_type=type_hints["city"])
            check_type(argname="argument contact_type", value=contact_type, expected_type=type_hints["contact_type"])
            check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument extra_params", value=extra_params, expected_type=type_hints["extra_params"])
            check_type(argname="argument fax", value=fax, expected_type=type_hints["fax"])
            check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
            check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
            check_type(argname="argument organization_name", value=organization_name, expected_type=type_hints["organization_name"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument zip_code", value=zip_code, expected_type=type_hints["zip_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address_line1 is not None:
            self._values["address_line1"] = address_line1
        if address_line2 is not None:
            self._values["address_line2"] = address_line2
        if city is not None:
            self._values["city"] = city
        if contact_type is not None:
            self._values["contact_type"] = contact_type
        if country_code is not None:
            self._values["country_code"] = country_code
        if email is not None:
            self._values["email"] = email
        if extra_params is not None:
            self._values["extra_params"] = extra_params
        if fax is not None:
            self._values["fax"] = fax
        if first_name is not None:
            self._values["first_name"] = first_name
        if last_name is not None:
            self._values["last_name"] = last_name
        if organization_name is not None:
            self._values["organization_name"] = organization_name
        if phone_number is not None:
            self._values["phone_number"] = phone_number
        if state is not None:
            self._values["state"] = state
        if zip_code is not None:
            self._values["zip_code"] = zip_code

    @builtins.property
    def address_line1(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_1 Route53DomainsRegisteredDomain#address_line_1}.'''
        result = self._values.get("address_line1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address_line2(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_2 Route53DomainsRegisteredDomain#address_line_2}.'''
        result = self._values.get("address_line2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def city(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#city Route53DomainsRegisteredDomain#city}.'''
        result = self._values.get("city")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def contact_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#contact_type Route53DomainsRegisteredDomain#contact_type}.'''
        result = self._values.get("contact_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#country_code Route53DomainsRegisteredDomain#country_code}.'''
        result = self._values.get("country_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#email Route53DomainsRegisteredDomain#email}.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#extra_params Route53DomainsRegisteredDomain#extra_params}.'''
        result = self._values.get("extra_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def fax(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#fax Route53DomainsRegisteredDomain#fax}.'''
        result = self._values.get("fax")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#first_name Route53DomainsRegisteredDomain#first_name}.'''
        result = self._values.get("first_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#last_name Route53DomainsRegisteredDomain#last_name}.'''
        result = self._values.get("last_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#organization_name Route53DomainsRegisteredDomain#organization_name}.'''
        result = self._values.get("organization_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def phone_number(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#phone_number Route53DomainsRegisteredDomain#phone_number}.'''
        result = self._values.get("phone_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#state Route53DomainsRegisteredDomain#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zip_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#zip_code Route53DomainsRegisteredDomain#zip_code}.'''
        result = self._values.get("zip_code")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Route53DomainsRegisteredDomainAdminContact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Route53DomainsRegisteredDomainAdminContactOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.route53DomainsRegisteredDomain.Route53DomainsRegisteredDomainAdminContactOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0abd429f82bfe052862885276403b3771e4a7f52ea5bc55af0d3b02f141f18c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddressLine1")
    def reset_address_line1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressLine1", []))

    @jsii.member(jsii_name="resetAddressLine2")
    def reset_address_line2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressLine2", []))

    @jsii.member(jsii_name="resetCity")
    def reset_city(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCity", []))

    @jsii.member(jsii_name="resetContactType")
    def reset_contact_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContactType", []))

    @jsii.member(jsii_name="resetCountryCode")
    def reset_country_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountryCode", []))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetExtraParams")
    def reset_extra_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtraParams", []))

    @jsii.member(jsii_name="resetFax")
    def reset_fax(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFax", []))

    @jsii.member(jsii_name="resetFirstName")
    def reset_first_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstName", []))

    @jsii.member(jsii_name="resetLastName")
    def reset_last_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastName", []))

    @jsii.member(jsii_name="resetOrganizationName")
    def reset_organization_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationName", []))

    @jsii.member(jsii_name="resetPhoneNumber")
    def reset_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhoneNumber", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @jsii.member(jsii_name="resetZipCode")
    def reset_zip_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZipCode", []))

    @builtins.property
    @jsii.member(jsii_name="addressLine1Input")
    def address_line1_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressLine1Input"))

    @builtins.property
    @jsii.member(jsii_name="addressLine2Input")
    def address_line2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressLine2Input"))

    @builtins.property
    @jsii.member(jsii_name="cityInput")
    def city_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cityInput"))

    @builtins.property
    @jsii.member(jsii_name="contactTypeInput")
    def contact_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contactTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="countryCodeInput")
    def country_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="extraParamsInput")
    def extra_params_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "extraParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="faxInput")
    def fax_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "faxInput"))

    @builtins.property
    @jsii.member(jsii_name="firstNameInput")
    def first_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firstNameInput"))

    @builtins.property
    @jsii.member(jsii_name="lastNameInput")
    def last_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastNameInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationNameInput")
    def organization_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="zipCodeInput")
    def zip_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zipCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="addressLine1")
    def address_line1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addressLine1"))

    @address_line1.setter
    def address_line1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5da1663109b911cb42568dc99c46a85312bb61007bca439f39db66299483839e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressLine1", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addressLine2")
    def address_line2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addressLine2"))

    @address_line2.setter
    def address_line2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cabd9373fc0ff5f0e6138bbcfd5bdd6db7b13405f0eadf5264d436836491913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressLine2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="city")
    def city(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "city"))

    @city.setter
    def city(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d32a22518721a6ca921b110ab18d5442400bd39ebe7b52ad612dbe0fc454dc50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "city", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contactType")
    def contact_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contactType"))

    @contact_type.setter
    def contact_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7024b491c34b1176285a1b23e765e0aacf1d82761fe08c995b81c96a301243bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="countryCode")
    def country_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "countryCode"))

    @country_code.setter
    def country_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__203a93280386e44ccd9a7d501e871b593c5c960d8086c16d2ede292633769d6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "countryCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d36eba6f6ccd631ab6648569dd7d9a4a9c0d5514c7f00a55801636a35b0160a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extraParams")
    def extra_params(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "extraParams"))

    @extra_params.setter
    def extra_params(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02959121653ae3d27eda24e3e14f8bfbb61d98ba3d0d6d03d52b6c64fd24ab66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extraParams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fax")
    def fax(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fax"))

    @fax.setter
    def fax(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__418c83910233c09eff129e9797534def9c49c3f4ce01dce50da87f0438a85313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fax", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firstName")
    def first_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstName"))

    @first_name.setter
    def first_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d2e33606380a5a30be8d0332d1da8e10a0d09d741924efd4524171cf01c5d3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastName")
    def last_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastName"))

    @last_name.setter
    def last_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f8307bf5603688cf62a4896098d833a470025cc0089c213f2990ca3ebc77956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationName")
    def organization_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationName"))

    @organization_name.setter
    def organization_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2326229675e9a30e5d37f49ffd322c055cd3e959c7d2c2cf7b36e72b78999a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a4bf4b0f4a7ca8b00343f6f115e2327d46276709fcd79ae062a6286fda36bd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__512471f783be83f92a8b5d67dd235865e82ce5ea240aa32fb624fe70eb28b605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zipCode")
    def zip_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zipCode"))

    @zip_code.setter
    def zip_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11d0d8e4accdd691f07445f676570a33e9ea7d6651fd602f993d47760cf1e076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zipCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Route53DomainsRegisteredDomainAdminContact]:
        return typing.cast(typing.Optional[Route53DomainsRegisteredDomainAdminContact], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Route53DomainsRegisteredDomainAdminContact],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__098667922d789247dcd3bf69d15eca88c8a86bbc545110263e8a27399e9d5add)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.route53DomainsRegisteredDomain.Route53DomainsRegisteredDomainBillingContact",
    jsii_struct_bases=[],
    name_mapping={
        "address_line1": "addressLine1",
        "address_line2": "addressLine2",
        "city": "city",
        "contact_type": "contactType",
        "country_code": "countryCode",
        "email": "email",
        "extra_params": "extraParams",
        "fax": "fax",
        "first_name": "firstName",
        "last_name": "lastName",
        "organization_name": "organizationName",
        "phone_number": "phoneNumber",
        "state": "state",
        "zip_code": "zipCode",
    },
)
class Route53DomainsRegisteredDomainBillingContact:
    def __init__(
        self,
        *,
        address_line1: typing.Optional[builtins.str] = None,
        address_line2: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        contact_type: typing.Optional[builtins.str] = None,
        country_code: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        fax: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        organization_name: typing.Optional[builtins.str] = None,
        phone_number: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        zip_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address_line1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_1 Route53DomainsRegisteredDomain#address_line_1}.
        :param address_line2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_2 Route53DomainsRegisteredDomain#address_line_2}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#city Route53DomainsRegisteredDomain#city}.
        :param contact_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#contact_type Route53DomainsRegisteredDomain#contact_type}.
        :param country_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#country_code Route53DomainsRegisteredDomain#country_code}.
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#email Route53DomainsRegisteredDomain#email}.
        :param extra_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#extra_params Route53DomainsRegisteredDomain#extra_params}.
        :param fax: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#fax Route53DomainsRegisteredDomain#fax}.
        :param first_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#first_name Route53DomainsRegisteredDomain#first_name}.
        :param last_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#last_name Route53DomainsRegisteredDomain#last_name}.
        :param organization_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#organization_name Route53DomainsRegisteredDomain#organization_name}.
        :param phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#phone_number Route53DomainsRegisteredDomain#phone_number}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#state Route53DomainsRegisteredDomain#state}.
        :param zip_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#zip_code Route53DomainsRegisteredDomain#zip_code}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f4a156cf34e61d49efd7f426161565c4d83bccab447563ac28b5716ac617e44)
            check_type(argname="argument address_line1", value=address_line1, expected_type=type_hints["address_line1"])
            check_type(argname="argument address_line2", value=address_line2, expected_type=type_hints["address_line2"])
            check_type(argname="argument city", value=city, expected_type=type_hints["city"])
            check_type(argname="argument contact_type", value=contact_type, expected_type=type_hints["contact_type"])
            check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument extra_params", value=extra_params, expected_type=type_hints["extra_params"])
            check_type(argname="argument fax", value=fax, expected_type=type_hints["fax"])
            check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
            check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
            check_type(argname="argument organization_name", value=organization_name, expected_type=type_hints["organization_name"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument zip_code", value=zip_code, expected_type=type_hints["zip_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address_line1 is not None:
            self._values["address_line1"] = address_line1
        if address_line2 is not None:
            self._values["address_line2"] = address_line2
        if city is not None:
            self._values["city"] = city
        if contact_type is not None:
            self._values["contact_type"] = contact_type
        if country_code is not None:
            self._values["country_code"] = country_code
        if email is not None:
            self._values["email"] = email
        if extra_params is not None:
            self._values["extra_params"] = extra_params
        if fax is not None:
            self._values["fax"] = fax
        if first_name is not None:
            self._values["first_name"] = first_name
        if last_name is not None:
            self._values["last_name"] = last_name
        if organization_name is not None:
            self._values["organization_name"] = organization_name
        if phone_number is not None:
            self._values["phone_number"] = phone_number
        if state is not None:
            self._values["state"] = state
        if zip_code is not None:
            self._values["zip_code"] = zip_code

    @builtins.property
    def address_line1(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_1 Route53DomainsRegisteredDomain#address_line_1}.'''
        result = self._values.get("address_line1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address_line2(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_2 Route53DomainsRegisteredDomain#address_line_2}.'''
        result = self._values.get("address_line2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def city(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#city Route53DomainsRegisteredDomain#city}.'''
        result = self._values.get("city")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def contact_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#contact_type Route53DomainsRegisteredDomain#contact_type}.'''
        result = self._values.get("contact_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#country_code Route53DomainsRegisteredDomain#country_code}.'''
        result = self._values.get("country_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#email Route53DomainsRegisteredDomain#email}.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#extra_params Route53DomainsRegisteredDomain#extra_params}.'''
        result = self._values.get("extra_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def fax(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#fax Route53DomainsRegisteredDomain#fax}.'''
        result = self._values.get("fax")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#first_name Route53DomainsRegisteredDomain#first_name}.'''
        result = self._values.get("first_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#last_name Route53DomainsRegisteredDomain#last_name}.'''
        result = self._values.get("last_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#organization_name Route53DomainsRegisteredDomain#organization_name}.'''
        result = self._values.get("organization_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def phone_number(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#phone_number Route53DomainsRegisteredDomain#phone_number}.'''
        result = self._values.get("phone_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#state Route53DomainsRegisteredDomain#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zip_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#zip_code Route53DomainsRegisteredDomain#zip_code}.'''
        result = self._values.get("zip_code")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Route53DomainsRegisteredDomainBillingContact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Route53DomainsRegisteredDomainBillingContactOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.route53DomainsRegisteredDomain.Route53DomainsRegisteredDomainBillingContactOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfe6740fb36e304a5cc0d72cba0ae862bb19cf53a8ef7915da5babc7fcbbf4bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddressLine1")
    def reset_address_line1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressLine1", []))

    @jsii.member(jsii_name="resetAddressLine2")
    def reset_address_line2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressLine2", []))

    @jsii.member(jsii_name="resetCity")
    def reset_city(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCity", []))

    @jsii.member(jsii_name="resetContactType")
    def reset_contact_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContactType", []))

    @jsii.member(jsii_name="resetCountryCode")
    def reset_country_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountryCode", []))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetExtraParams")
    def reset_extra_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtraParams", []))

    @jsii.member(jsii_name="resetFax")
    def reset_fax(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFax", []))

    @jsii.member(jsii_name="resetFirstName")
    def reset_first_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstName", []))

    @jsii.member(jsii_name="resetLastName")
    def reset_last_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastName", []))

    @jsii.member(jsii_name="resetOrganizationName")
    def reset_organization_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationName", []))

    @jsii.member(jsii_name="resetPhoneNumber")
    def reset_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhoneNumber", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @jsii.member(jsii_name="resetZipCode")
    def reset_zip_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZipCode", []))

    @builtins.property
    @jsii.member(jsii_name="addressLine1Input")
    def address_line1_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressLine1Input"))

    @builtins.property
    @jsii.member(jsii_name="addressLine2Input")
    def address_line2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressLine2Input"))

    @builtins.property
    @jsii.member(jsii_name="cityInput")
    def city_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cityInput"))

    @builtins.property
    @jsii.member(jsii_name="contactTypeInput")
    def contact_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contactTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="countryCodeInput")
    def country_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="extraParamsInput")
    def extra_params_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "extraParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="faxInput")
    def fax_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "faxInput"))

    @builtins.property
    @jsii.member(jsii_name="firstNameInput")
    def first_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firstNameInput"))

    @builtins.property
    @jsii.member(jsii_name="lastNameInput")
    def last_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastNameInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationNameInput")
    def organization_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="zipCodeInput")
    def zip_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zipCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="addressLine1")
    def address_line1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addressLine1"))

    @address_line1.setter
    def address_line1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8040618452f6a316d3dd0a13f074d4a15f9b73637b55311719f22a028ba888b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressLine1", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addressLine2")
    def address_line2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addressLine2"))

    @address_line2.setter
    def address_line2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e29b43cb6a1470e89b4a861bd00c20d2b30e87f3d76ff720d394f540c5745a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressLine2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="city")
    def city(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "city"))

    @city.setter
    def city(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98bd194fc81e1b4468986c9ba291eee3927f111f1444a1cdb6ccf13a2d4d0c2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "city", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contactType")
    def contact_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contactType"))

    @contact_type.setter
    def contact_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a809afa52b59477bd92fe75b9482c33dbd0a85afa579453336c62f88eb6f1270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="countryCode")
    def country_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "countryCode"))

    @country_code.setter
    def country_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c4238e54d0b1df476c5977989181a3b7f460ba1221b60566f7f57d74b9597d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "countryCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba812ce8c933f766de53fe4c6ae5c4c0c48934fec03f1cb20cfc7e0eb6672807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extraParams")
    def extra_params(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "extraParams"))

    @extra_params.setter
    def extra_params(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__911a27f4d4dcbc47b0954bb5ec57ee53ee48bdea7469c00ca4742ac827208884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extraParams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fax")
    def fax(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fax"))

    @fax.setter
    def fax(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d340d1993f0feb559ade7343da26a202c758ac07f1ccf373c8f248ffe461a1f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fax", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firstName")
    def first_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstName"))

    @first_name.setter
    def first_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93e127b882a4dcabecb2706b1736c97e7fa6fad7380e2cc0447da104e53fce18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastName")
    def last_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastName"))

    @last_name.setter
    def last_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da7c559ab02cc2a93167bdc11d06d70d175f4e150626e12f687d6a104f794fc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationName")
    def organization_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationName"))

    @organization_name.setter
    def organization_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1193afd2c0846e478949eca901fc22b5b7a170dbff4d4ad664f891ad199f733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6bbe0c3c6220a97340d1b00dbbaec8f6500ab917c2f98501a5ee3b0c46a8405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c54904f74170ad3bb1fa709398d46e916f429b200a340464524581e13aa29c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zipCode")
    def zip_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zipCode"))

    @zip_code.setter
    def zip_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d01ab749e65c9de84475090b185b904b92f61e3784d7850278c11914ee3dc47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zipCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Route53DomainsRegisteredDomainBillingContact]:
        return typing.cast(typing.Optional[Route53DomainsRegisteredDomainBillingContact], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Route53DomainsRegisteredDomainBillingContact],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47f3ce35bdf9d54a9daa960c9f93cd4efb54c60f914ac9efa1280a39b1ad04fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.route53DomainsRegisteredDomain.Route53DomainsRegisteredDomainConfig",
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
        "admin_contact": "adminContact",
        "admin_privacy": "adminPrivacy",
        "auto_renew": "autoRenew",
        "billing_contact": "billingContact",
        "billing_privacy": "billingPrivacy",
        "id": "id",
        "name_server": "nameServer",
        "registrant_contact": "registrantContact",
        "registrant_privacy": "registrantPrivacy",
        "tags": "tags",
        "tags_all": "tagsAll",
        "tech_contact": "techContact",
        "tech_privacy": "techPrivacy",
        "timeouts": "timeouts",
        "transfer_lock": "transferLock",
    },
)
class Route53DomainsRegisteredDomainConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        admin_contact: typing.Optional[typing.Union[Route53DomainsRegisteredDomainAdminContact, typing.Dict[builtins.str, typing.Any]]] = None,
        admin_privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_renew: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        billing_contact: typing.Optional[typing.Union[Route53DomainsRegisteredDomainBillingContact, typing.Dict[builtins.str, typing.Any]]] = None,
        billing_privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        name_server: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Route53DomainsRegisteredDomainNameServer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        registrant_contact: typing.Optional[typing.Union["Route53DomainsRegisteredDomainRegistrantContact", typing.Dict[builtins.str, typing.Any]]] = None,
        registrant_privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tech_contact: typing.Optional[typing.Union["Route53DomainsRegisteredDomainTechContact", typing.Dict[builtins.str, typing.Any]]] = None,
        tech_privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["Route53DomainsRegisteredDomainTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transfer_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#domain_name Route53DomainsRegisteredDomain#domain_name}.
        :param admin_contact: admin_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#admin_contact Route53DomainsRegisteredDomain#admin_contact}
        :param admin_privacy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#admin_privacy Route53DomainsRegisteredDomain#admin_privacy}.
        :param auto_renew: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#auto_renew Route53DomainsRegisteredDomain#auto_renew}.
        :param billing_contact: billing_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#billing_contact Route53DomainsRegisteredDomain#billing_contact}
        :param billing_privacy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#billing_privacy Route53DomainsRegisteredDomain#billing_privacy}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#id Route53DomainsRegisteredDomain#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name_server: name_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#name_server Route53DomainsRegisteredDomain#name_server}
        :param registrant_contact: registrant_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#registrant_contact Route53DomainsRegisteredDomain#registrant_contact}
        :param registrant_privacy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#registrant_privacy Route53DomainsRegisteredDomain#registrant_privacy}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#tags Route53DomainsRegisteredDomain#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#tags_all Route53DomainsRegisteredDomain#tags_all}.
        :param tech_contact: tech_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#tech_contact Route53DomainsRegisteredDomain#tech_contact}
        :param tech_privacy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#tech_privacy Route53DomainsRegisteredDomain#tech_privacy}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#timeouts Route53DomainsRegisteredDomain#timeouts}
        :param transfer_lock: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#transfer_lock Route53DomainsRegisteredDomain#transfer_lock}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(admin_contact, dict):
            admin_contact = Route53DomainsRegisteredDomainAdminContact(**admin_contact)
        if isinstance(billing_contact, dict):
            billing_contact = Route53DomainsRegisteredDomainBillingContact(**billing_contact)
        if isinstance(registrant_contact, dict):
            registrant_contact = Route53DomainsRegisteredDomainRegistrantContact(**registrant_contact)
        if isinstance(tech_contact, dict):
            tech_contact = Route53DomainsRegisteredDomainTechContact(**tech_contact)
        if isinstance(timeouts, dict):
            timeouts = Route53DomainsRegisteredDomainTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c8eef8208c70c608628c0ea58e73055c7a1690d4e6c2f4a38501c4a1c6f7a8e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument admin_contact", value=admin_contact, expected_type=type_hints["admin_contact"])
            check_type(argname="argument admin_privacy", value=admin_privacy, expected_type=type_hints["admin_privacy"])
            check_type(argname="argument auto_renew", value=auto_renew, expected_type=type_hints["auto_renew"])
            check_type(argname="argument billing_contact", value=billing_contact, expected_type=type_hints["billing_contact"])
            check_type(argname="argument billing_privacy", value=billing_privacy, expected_type=type_hints["billing_privacy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name_server", value=name_server, expected_type=type_hints["name_server"])
            check_type(argname="argument registrant_contact", value=registrant_contact, expected_type=type_hints["registrant_contact"])
            check_type(argname="argument registrant_privacy", value=registrant_privacy, expected_type=type_hints["registrant_privacy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument tech_contact", value=tech_contact, expected_type=type_hints["tech_contact"])
            check_type(argname="argument tech_privacy", value=tech_privacy, expected_type=type_hints["tech_privacy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument transfer_lock", value=transfer_lock, expected_type=type_hints["transfer_lock"])
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
        if admin_contact is not None:
            self._values["admin_contact"] = admin_contact
        if admin_privacy is not None:
            self._values["admin_privacy"] = admin_privacy
        if auto_renew is not None:
            self._values["auto_renew"] = auto_renew
        if billing_contact is not None:
            self._values["billing_contact"] = billing_contact
        if billing_privacy is not None:
            self._values["billing_privacy"] = billing_privacy
        if id is not None:
            self._values["id"] = id
        if name_server is not None:
            self._values["name_server"] = name_server
        if registrant_contact is not None:
            self._values["registrant_contact"] = registrant_contact
        if registrant_privacy is not None:
            self._values["registrant_privacy"] = registrant_privacy
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if tech_contact is not None:
            self._values["tech_contact"] = tech_contact
        if tech_privacy is not None:
            self._values["tech_privacy"] = tech_privacy
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if transfer_lock is not None:
            self._values["transfer_lock"] = transfer_lock

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#domain_name Route53DomainsRegisteredDomain#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admin_contact(
        self,
    ) -> typing.Optional[Route53DomainsRegisteredDomainAdminContact]:
        '''admin_contact block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#admin_contact Route53DomainsRegisteredDomain#admin_contact}
        '''
        result = self._values.get("admin_contact")
        return typing.cast(typing.Optional[Route53DomainsRegisteredDomainAdminContact], result)

    @builtins.property
    def admin_privacy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#admin_privacy Route53DomainsRegisteredDomain#admin_privacy}.'''
        result = self._values.get("admin_privacy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_renew(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#auto_renew Route53DomainsRegisteredDomain#auto_renew}.'''
        result = self._values.get("auto_renew")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def billing_contact(
        self,
    ) -> typing.Optional[Route53DomainsRegisteredDomainBillingContact]:
        '''billing_contact block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#billing_contact Route53DomainsRegisteredDomain#billing_contact}
        '''
        result = self._values.get("billing_contact")
        return typing.cast(typing.Optional[Route53DomainsRegisteredDomainBillingContact], result)

    @builtins.property
    def billing_privacy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#billing_privacy Route53DomainsRegisteredDomain#billing_privacy}.'''
        result = self._values.get("billing_privacy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#id Route53DomainsRegisteredDomain#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_server(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53DomainsRegisteredDomainNameServer"]]]:
        '''name_server block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#name_server Route53DomainsRegisteredDomain#name_server}
        '''
        result = self._values.get("name_server")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Route53DomainsRegisteredDomainNameServer"]]], result)

    @builtins.property
    def registrant_contact(
        self,
    ) -> typing.Optional["Route53DomainsRegisteredDomainRegistrantContact"]:
        '''registrant_contact block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#registrant_contact Route53DomainsRegisteredDomain#registrant_contact}
        '''
        result = self._values.get("registrant_contact")
        return typing.cast(typing.Optional["Route53DomainsRegisteredDomainRegistrantContact"], result)

    @builtins.property
    def registrant_privacy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#registrant_privacy Route53DomainsRegisteredDomain#registrant_privacy}.'''
        result = self._values.get("registrant_privacy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#tags Route53DomainsRegisteredDomain#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#tags_all Route53DomainsRegisteredDomain#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tech_contact(
        self,
    ) -> typing.Optional["Route53DomainsRegisteredDomainTechContact"]:
        '''tech_contact block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#tech_contact Route53DomainsRegisteredDomain#tech_contact}
        '''
        result = self._values.get("tech_contact")
        return typing.cast(typing.Optional["Route53DomainsRegisteredDomainTechContact"], result)

    @builtins.property
    def tech_privacy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#tech_privacy Route53DomainsRegisteredDomain#tech_privacy}.'''
        result = self._values.get("tech_privacy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["Route53DomainsRegisteredDomainTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#timeouts Route53DomainsRegisteredDomain#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["Route53DomainsRegisteredDomainTimeouts"], result)

    @builtins.property
    def transfer_lock(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#transfer_lock Route53DomainsRegisteredDomain#transfer_lock}.'''
        result = self._values.get("transfer_lock")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Route53DomainsRegisteredDomainConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.route53DomainsRegisteredDomain.Route53DomainsRegisteredDomainNameServer",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "glue_ips": "glueIps"},
)
class Route53DomainsRegisteredDomainNameServer:
    def __init__(
        self,
        *,
        name: builtins.str,
        glue_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#name Route53DomainsRegisteredDomain#name}.
        :param glue_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#glue_ips Route53DomainsRegisteredDomain#glue_ips}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b017f8d6906a4dfc68a67fbcff0afdec5c094adf57de334514265886414af3e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument glue_ips", value=glue_ips, expected_type=type_hints["glue_ips"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if glue_ips is not None:
            self._values["glue_ips"] = glue_ips

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#name Route53DomainsRegisteredDomain#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def glue_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#glue_ips Route53DomainsRegisteredDomain#glue_ips}.'''
        result = self._values.get("glue_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Route53DomainsRegisteredDomainNameServer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Route53DomainsRegisteredDomainNameServerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.route53DomainsRegisteredDomain.Route53DomainsRegisteredDomainNameServerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab514636f1bf966ff4c988b430e4058441add9f7c1daaa047e390a80c1941e92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Route53DomainsRegisteredDomainNameServerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bfc69f5ea57bfe90d006bec0e202efc8bb63ae7335eb0bd7b7728adc547c673)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Route53DomainsRegisteredDomainNameServerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee2c20dc0b83759c570a9f0645ed5e51859112679797ad152b57e9df392c80f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40d18b60314ae8a4bc39085e3a472a0854f96cad1b49680a335f7835d56c6a05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__310eb6e69a0a5797a60181ad74cb03be04b5f33a507cd31889888ef21d26e571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53DomainsRegisteredDomainNameServer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53DomainsRegisteredDomainNameServer]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53DomainsRegisteredDomainNameServer]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f6641ded2726f4448beed8ea87577f5c7c581645ba0a61fc551ec0131ecb87a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Route53DomainsRegisteredDomainNameServerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.route53DomainsRegisteredDomain.Route53DomainsRegisteredDomainNameServerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b00506b80a4de51e5590e39e1dad36a4a9229659e4c66ff430cd2de7df70d2a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetGlueIps")
    def reset_glue_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlueIps", []))

    @builtins.property
    @jsii.member(jsii_name="glueIpsInput")
    def glue_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "glueIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="glueIps")
    def glue_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "glueIps"))

    @glue_ips.setter
    def glue_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ace7ee2d9c4ebf3fee65d1f00795ec430f3d0963322e8e2c0e98ae32e5397173)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "glueIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__882f1433e478da05a57f98b131264ccb33669dfe9085cf6dce2baf5063961f9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Route53DomainsRegisteredDomainNameServer]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Route53DomainsRegisteredDomainNameServer]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Route53DomainsRegisteredDomainNameServer]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c625ffabd6a91df990613121ffaf0ad917809f40ec450fce421897d03a9b22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.route53DomainsRegisteredDomain.Route53DomainsRegisteredDomainRegistrantContact",
    jsii_struct_bases=[],
    name_mapping={
        "address_line1": "addressLine1",
        "address_line2": "addressLine2",
        "city": "city",
        "contact_type": "contactType",
        "country_code": "countryCode",
        "email": "email",
        "extra_params": "extraParams",
        "fax": "fax",
        "first_name": "firstName",
        "last_name": "lastName",
        "organization_name": "organizationName",
        "phone_number": "phoneNumber",
        "state": "state",
        "zip_code": "zipCode",
    },
)
class Route53DomainsRegisteredDomainRegistrantContact:
    def __init__(
        self,
        *,
        address_line1: typing.Optional[builtins.str] = None,
        address_line2: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        contact_type: typing.Optional[builtins.str] = None,
        country_code: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        fax: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        organization_name: typing.Optional[builtins.str] = None,
        phone_number: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        zip_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address_line1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_1 Route53DomainsRegisteredDomain#address_line_1}.
        :param address_line2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_2 Route53DomainsRegisteredDomain#address_line_2}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#city Route53DomainsRegisteredDomain#city}.
        :param contact_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#contact_type Route53DomainsRegisteredDomain#contact_type}.
        :param country_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#country_code Route53DomainsRegisteredDomain#country_code}.
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#email Route53DomainsRegisteredDomain#email}.
        :param extra_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#extra_params Route53DomainsRegisteredDomain#extra_params}.
        :param fax: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#fax Route53DomainsRegisteredDomain#fax}.
        :param first_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#first_name Route53DomainsRegisteredDomain#first_name}.
        :param last_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#last_name Route53DomainsRegisteredDomain#last_name}.
        :param organization_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#organization_name Route53DomainsRegisteredDomain#organization_name}.
        :param phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#phone_number Route53DomainsRegisteredDomain#phone_number}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#state Route53DomainsRegisteredDomain#state}.
        :param zip_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#zip_code Route53DomainsRegisteredDomain#zip_code}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__539828c18da71427e2982b24d059a31647071436356e5a92b2f87a91dd92e151)
            check_type(argname="argument address_line1", value=address_line1, expected_type=type_hints["address_line1"])
            check_type(argname="argument address_line2", value=address_line2, expected_type=type_hints["address_line2"])
            check_type(argname="argument city", value=city, expected_type=type_hints["city"])
            check_type(argname="argument contact_type", value=contact_type, expected_type=type_hints["contact_type"])
            check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument extra_params", value=extra_params, expected_type=type_hints["extra_params"])
            check_type(argname="argument fax", value=fax, expected_type=type_hints["fax"])
            check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
            check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
            check_type(argname="argument organization_name", value=organization_name, expected_type=type_hints["organization_name"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument zip_code", value=zip_code, expected_type=type_hints["zip_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address_line1 is not None:
            self._values["address_line1"] = address_line1
        if address_line2 is not None:
            self._values["address_line2"] = address_line2
        if city is not None:
            self._values["city"] = city
        if contact_type is not None:
            self._values["contact_type"] = contact_type
        if country_code is not None:
            self._values["country_code"] = country_code
        if email is not None:
            self._values["email"] = email
        if extra_params is not None:
            self._values["extra_params"] = extra_params
        if fax is not None:
            self._values["fax"] = fax
        if first_name is not None:
            self._values["first_name"] = first_name
        if last_name is not None:
            self._values["last_name"] = last_name
        if organization_name is not None:
            self._values["organization_name"] = organization_name
        if phone_number is not None:
            self._values["phone_number"] = phone_number
        if state is not None:
            self._values["state"] = state
        if zip_code is not None:
            self._values["zip_code"] = zip_code

    @builtins.property
    def address_line1(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_1 Route53DomainsRegisteredDomain#address_line_1}.'''
        result = self._values.get("address_line1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address_line2(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_2 Route53DomainsRegisteredDomain#address_line_2}.'''
        result = self._values.get("address_line2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def city(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#city Route53DomainsRegisteredDomain#city}.'''
        result = self._values.get("city")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def contact_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#contact_type Route53DomainsRegisteredDomain#contact_type}.'''
        result = self._values.get("contact_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#country_code Route53DomainsRegisteredDomain#country_code}.'''
        result = self._values.get("country_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#email Route53DomainsRegisteredDomain#email}.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#extra_params Route53DomainsRegisteredDomain#extra_params}.'''
        result = self._values.get("extra_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def fax(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#fax Route53DomainsRegisteredDomain#fax}.'''
        result = self._values.get("fax")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#first_name Route53DomainsRegisteredDomain#first_name}.'''
        result = self._values.get("first_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#last_name Route53DomainsRegisteredDomain#last_name}.'''
        result = self._values.get("last_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#organization_name Route53DomainsRegisteredDomain#organization_name}.'''
        result = self._values.get("organization_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def phone_number(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#phone_number Route53DomainsRegisteredDomain#phone_number}.'''
        result = self._values.get("phone_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#state Route53DomainsRegisteredDomain#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zip_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#zip_code Route53DomainsRegisteredDomain#zip_code}.'''
        result = self._values.get("zip_code")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Route53DomainsRegisteredDomainRegistrantContact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Route53DomainsRegisteredDomainRegistrantContactOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.route53DomainsRegisteredDomain.Route53DomainsRegisteredDomainRegistrantContactOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9dd86c61758126a2b7c44cd99aa17b51845f4a8f7ba485a88e703d0cb43a2ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddressLine1")
    def reset_address_line1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressLine1", []))

    @jsii.member(jsii_name="resetAddressLine2")
    def reset_address_line2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressLine2", []))

    @jsii.member(jsii_name="resetCity")
    def reset_city(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCity", []))

    @jsii.member(jsii_name="resetContactType")
    def reset_contact_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContactType", []))

    @jsii.member(jsii_name="resetCountryCode")
    def reset_country_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountryCode", []))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetExtraParams")
    def reset_extra_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtraParams", []))

    @jsii.member(jsii_name="resetFax")
    def reset_fax(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFax", []))

    @jsii.member(jsii_name="resetFirstName")
    def reset_first_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstName", []))

    @jsii.member(jsii_name="resetLastName")
    def reset_last_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastName", []))

    @jsii.member(jsii_name="resetOrganizationName")
    def reset_organization_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationName", []))

    @jsii.member(jsii_name="resetPhoneNumber")
    def reset_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhoneNumber", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @jsii.member(jsii_name="resetZipCode")
    def reset_zip_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZipCode", []))

    @builtins.property
    @jsii.member(jsii_name="addressLine1Input")
    def address_line1_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressLine1Input"))

    @builtins.property
    @jsii.member(jsii_name="addressLine2Input")
    def address_line2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressLine2Input"))

    @builtins.property
    @jsii.member(jsii_name="cityInput")
    def city_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cityInput"))

    @builtins.property
    @jsii.member(jsii_name="contactTypeInput")
    def contact_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contactTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="countryCodeInput")
    def country_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="extraParamsInput")
    def extra_params_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "extraParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="faxInput")
    def fax_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "faxInput"))

    @builtins.property
    @jsii.member(jsii_name="firstNameInput")
    def first_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firstNameInput"))

    @builtins.property
    @jsii.member(jsii_name="lastNameInput")
    def last_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastNameInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationNameInput")
    def organization_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="zipCodeInput")
    def zip_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zipCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="addressLine1")
    def address_line1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addressLine1"))

    @address_line1.setter
    def address_line1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c10487026d7e2af9d64cbe92c54a67963508268ae30a0566246d6910562cd407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressLine1", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addressLine2")
    def address_line2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addressLine2"))

    @address_line2.setter
    def address_line2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__358b3bf53720afc889c45f6fb25657985b7abb76a8d67df65e210d1d1c67ede4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressLine2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="city")
    def city(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "city"))

    @city.setter
    def city(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dabaf2dc194b55dac46ada298b4b88944baae2922e9ee561ffa0042d1fbaf16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "city", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contactType")
    def contact_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contactType"))

    @contact_type.setter
    def contact_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f87a8496b23b2ea3a719bec4c05813ed7588af2ac838bf531a25aac9096e0871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="countryCode")
    def country_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "countryCode"))

    @country_code.setter
    def country_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb988ee378a3f1f51c3cd2e580d651cc486bd6dfbe0c790cd2c4be269080b986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "countryCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a42988decddadbe9d94e85f96b251099e0c22d4c73362910232d78cc7a53e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extraParams")
    def extra_params(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "extraParams"))

    @extra_params.setter
    def extra_params(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09dc8d6231068a0b6cca8a4c01285e70dc0d558fbb27730b4db6b3da35104967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extraParams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fax")
    def fax(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fax"))

    @fax.setter
    def fax(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd74f389b71db6562a0e674769c3125ab3e37326869f53705670d06f1b78a48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fax", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firstName")
    def first_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstName"))

    @first_name.setter
    def first_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7760211a98d3733d86eb20e11b7bc4d8b850d53453486ccf0decbb33598905ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastName")
    def last_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastName"))

    @last_name.setter
    def last_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1fa2e0ea7b037b039836b9261b515f5fa9f7162a1b89542d4f65bb2b7ff5425)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationName")
    def organization_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationName"))

    @organization_name.setter
    def organization_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__584d1ec7e5406c2531ceb7ff91a51a16f59bf07189d03b7ceedce4cf3a7df6e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e556694a155b15797ec0b8f2520d8bec4126c54761e8f21abed171a4bd06c7bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da655601bb4b1fe50b4ecc179b2efce6049a6dbcfe605089b8380329c7287b4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zipCode")
    def zip_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zipCode"))

    @zip_code.setter
    def zip_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb6f5d5e93aee6da9346adf1ae291b3a4ea14fd90cf000b541640db7e8639fc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zipCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Route53DomainsRegisteredDomainRegistrantContact]:
        return typing.cast(typing.Optional[Route53DomainsRegisteredDomainRegistrantContact], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Route53DomainsRegisteredDomainRegistrantContact],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8aec85ca3eaf76140e4dd8180cedc7cf3b845e218932897ca553221df1eedf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.route53DomainsRegisteredDomain.Route53DomainsRegisteredDomainTechContact",
    jsii_struct_bases=[],
    name_mapping={
        "address_line1": "addressLine1",
        "address_line2": "addressLine2",
        "city": "city",
        "contact_type": "contactType",
        "country_code": "countryCode",
        "email": "email",
        "extra_params": "extraParams",
        "fax": "fax",
        "first_name": "firstName",
        "last_name": "lastName",
        "organization_name": "organizationName",
        "phone_number": "phoneNumber",
        "state": "state",
        "zip_code": "zipCode",
    },
)
class Route53DomainsRegisteredDomainTechContact:
    def __init__(
        self,
        *,
        address_line1: typing.Optional[builtins.str] = None,
        address_line2: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        contact_type: typing.Optional[builtins.str] = None,
        country_code: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        fax: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        organization_name: typing.Optional[builtins.str] = None,
        phone_number: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        zip_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address_line1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_1 Route53DomainsRegisteredDomain#address_line_1}.
        :param address_line2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_2 Route53DomainsRegisteredDomain#address_line_2}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#city Route53DomainsRegisteredDomain#city}.
        :param contact_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#contact_type Route53DomainsRegisteredDomain#contact_type}.
        :param country_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#country_code Route53DomainsRegisteredDomain#country_code}.
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#email Route53DomainsRegisteredDomain#email}.
        :param extra_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#extra_params Route53DomainsRegisteredDomain#extra_params}.
        :param fax: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#fax Route53DomainsRegisteredDomain#fax}.
        :param first_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#first_name Route53DomainsRegisteredDomain#first_name}.
        :param last_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#last_name Route53DomainsRegisteredDomain#last_name}.
        :param organization_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#organization_name Route53DomainsRegisteredDomain#organization_name}.
        :param phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#phone_number Route53DomainsRegisteredDomain#phone_number}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#state Route53DomainsRegisteredDomain#state}.
        :param zip_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#zip_code Route53DomainsRegisteredDomain#zip_code}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac15abf92ca16506a573feeeb807108906192065e47e6e62e961d8673450d010)
            check_type(argname="argument address_line1", value=address_line1, expected_type=type_hints["address_line1"])
            check_type(argname="argument address_line2", value=address_line2, expected_type=type_hints["address_line2"])
            check_type(argname="argument city", value=city, expected_type=type_hints["city"])
            check_type(argname="argument contact_type", value=contact_type, expected_type=type_hints["contact_type"])
            check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument extra_params", value=extra_params, expected_type=type_hints["extra_params"])
            check_type(argname="argument fax", value=fax, expected_type=type_hints["fax"])
            check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
            check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
            check_type(argname="argument organization_name", value=organization_name, expected_type=type_hints["organization_name"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument zip_code", value=zip_code, expected_type=type_hints["zip_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address_line1 is not None:
            self._values["address_line1"] = address_line1
        if address_line2 is not None:
            self._values["address_line2"] = address_line2
        if city is not None:
            self._values["city"] = city
        if contact_type is not None:
            self._values["contact_type"] = contact_type
        if country_code is not None:
            self._values["country_code"] = country_code
        if email is not None:
            self._values["email"] = email
        if extra_params is not None:
            self._values["extra_params"] = extra_params
        if fax is not None:
            self._values["fax"] = fax
        if first_name is not None:
            self._values["first_name"] = first_name
        if last_name is not None:
            self._values["last_name"] = last_name
        if organization_name is not None:
            self._values["organization_name"] = organization_name
        if phone_number is not None:
            self._values["phone_number"] = phone_number
        if state is not None:
            self._values["state"] = state
        if zip_code is not None:
            self._values["zip_code"] = zip_code

    @builtins.property
    def address_line1(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_1 Route53DomainsRegisteredDomain#address_line_1}.'''
        result = self._values.get("address_line1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address_line2(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#address_line_2 Route53DomainsRegisteredDomain#address_line_2}.'''
        result = self._values.get("address_line2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def city(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#city Route53DomainsRegisteredDomain#city}.'''
        result = self._values.get("city")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def contact_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#contact_type Route53DomainsRegisteredDomain#contact_type}.'''
        result = self._values.get("contact_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#country_code Route53DomainsRegisteredDomain#country_code}.'''
        result = self._values.get("country_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#email Route53DomainsRegisteredDomain#email}.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#extra_params Route53DomainsRegisteredDomain#extra_params}.'''
        result = self._values.get("extra_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def fax(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#fax Route53DomainsRegisteredDomain#fax}.'''
        result = self._values.get("fax")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#first_name Route53DomainsRegisteredDomain#first_name}.'''
        result = self._values.get("first_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#last_name Route53DomainsRegisteredDomain#last_name}.'''
        result = self._values.get("last_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#organization_name Route53DomainsRegisteredDomain#organization_name}.'''
        result = self._values.get("organization_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def phone_number(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#phone_number Route53DomainsRegisteredDomain#phone_number}.'''
        result = self._values.get("phone_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#state Route53DomainsRegisteredDomain#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zip_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#zip_code Route53DomainsRegisteredDomain#zip_code}.'''
        result = self._values.get("zip_code")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Route53DomainsRegisteredDomainTechContact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Route53DomainsRegisteredDomainTechContactOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.route53DomainsRegisteredDomain.Route53DomainsRegisteredDomainTechContactOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d19a32c67b928932839db46c96b51a4f54b44508fc4c226a57230913617ef55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddressLine1")
    def reset_address_line1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressLine1", []))

    @jsii.member(jsii_name="resetAddressLine2")
    def reset_address_line2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressLine2", []))

    @jsii.member(jsii_name="resetCity")
    def reset_city(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCity", []))

    @jsii.member(jsii_name="resetContactType")
    def reset_contact_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContactType", []))

    @jsii.member(jsii_name="resetCountryCode")
    def reset_country_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountryCode", []))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetExtraParams")
    def reset_extra_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtraParams", []))

    @jsii.member(jsii_name="resetFax")
    def reset_fax(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFax", []))

    @jsii.member(jsii_name="resetFirstName")
    def reset_first_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstName", []))

    @jsii.member(jsii_name="resetLastName")
    def reset_last_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastName", []))

    @jsii.member(jsii_name="resetOrganizationName")
    def reset_organization_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationName", []))

    @jsii.member(jsii_name="resetPhoneNumber")
    def reset_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhoneNumber", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @jsii.member(jsii_name="resetZipCode")
    def reset_zip_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZipCode", []))

    @builtins.property
    @jsii.member(jsii_name="addressLine1Input")
    def address_line1_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressLine1Input"))

    @builtins.property
    @jsii.member(jsii_name="addressLine2Input")
    def address_line2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressLine2Input"))

    @builtins.property
    @jsii.member(jsii_name="cityInput")
    def city_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cityInput"))

    @builtins.property
    @jsii.member(jsii_name="contactTypeInput")
    def contact_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contactTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="countryCodeInput")
    def country_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="extraParamsInput")
    def extra_params_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "extraParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="faxInput")
    def fax_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "faxInput"))

    @builtins.property
    @jsii.member(jsii_name="firstNameInput")
    def first_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firstNameInput"))

    @builtins.property
    @jsii.member(jsii_name="lastNameInput")
    def last_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastNameInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationNameInput")
    def organization_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="zipCodeInput")
    def zip_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zipCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="addressLine1")
    def address_line1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addressLine1"))

    @address_line1.setter
    def address_line1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b571c20a2d3b903065daa3d0a5a5a90580327b9307a47a1582bd0973afe13f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressLine1", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addressLine2")
    def address_line2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addressLine2"))

    @address_line2.setter
    def address_line2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b99ae16f3d5f494da1671d937453342a25d58bd67cda408e2ca4b027b70c091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressLine2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="city")
    def city(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "city"))

    @city.setter
    def city(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c14b76708266749dbbd235c9376f5f685cb184dfdc2f86fe1724809a58dcc822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "city", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contactType")
    def contact_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contactType"))

    @contact_type.setter
    def contact_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__970dd6ae781e670e96c695c67091a365a9c514d5facdd3bbcd3583a527b22461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="countryCode")
    def country_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "countryCode"))

    @country_code.setter
    def country_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14770b16c0aa4bf4bb294382c25ed273269f9e8acd6c3e4c0e74850dc974e48f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "countryCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819eb9cf3e82ed669a758dd39e2e4efbc5b40a566228c94426a877dfac55aa7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extraParams")
    def extra_params(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "extraParams"))

    @extra_params.setter
    def extra_params(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__174bb8a49c0c8a394331a08480d84ebf27dd569805b7f9ae1ebf56ec347f0629)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extraParams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fax")
    def fax(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fax"))

    @fax.setter
    def fax(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6427e5f6111ed5151e37db503c8f53008ecf61b1dec7d4dfe2b702f832d94f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fax", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firstName")
    def first_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstName"))

    @first_name.setter
    def first_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560469859cb78f19610b6656f6b19e19f70f6de9e4e5418a8dde8ff10295c376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastName")
    def last_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastName"))

    @last_name.setter
    def last_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d44a7066bfd160444c8fe9d40d8efc74ce20b5f9687cb6ef4d7c2f40e6f2e51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationName")
    def organization_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationName"))

    @organization_name.setter
    def organization_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__404ca4c623a1a2e85e9c3eec37b60df7d67f91b7b8eaffa1bdc3b77b9d851392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8c78a7c9bc023e15b174c3f67f3605227d30b0b7b917e8029b28df239058a00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0366a1a4100d05f0b834caaf0073484a2f3585bc86be61c391e4b6758384e984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zipCode")
    def zip_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zipCode"))

    @zip_code.setter
    def zip_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25397793b3baac1a96b7b88c5369332b65d6b24587dac811e479c7e8a8d9c24c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zipCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Route53DomainsRegisteredDomainTechContact]:
        return typing.cast(typing.Optional[Route53DomainsRegisteredDomainTechContact], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Route53DomainsRegisteredDomainTechContact],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b939049113aebe8f4bc26ac65cae0aafa285468393739304bd8e86a664c0402e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.route53DomainsRegisteredDomain.Route53DomainsRegisteredDomainTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "update": "update"},
)
class Route53DomainsRegisteredDomainTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#create Route53DomainsRegisteredDomain#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#update Route53DomainsRegisteredDomain#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10db875302c90536d589cb9bfa49b134b816ff7b913106f84224c7229a298494)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#create Route53DomainsRegisteredDomain#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/route53domains_registered_domain#update Route53DomainsRegisteredDomain#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Route53DomainsRegisteredDomainTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Route53DomainsRegisteredDomainTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.route53DomainsRegisteredDomain.Route53DomainsRegisteredDomainTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5aca28ee69a96b831c07dff91bcb2f19562ada40d309710f1def17c4a56d2dcb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3a81fe083549c41cda9a4145dad298bacb15ae572804535c922bb5224b314d54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e366381a51d7e3433bd55a8a8e52d29cd52c27307d98610fcd52742a59e9321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Route53DomainsRegisteredDomainTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Route53DomainsRegisteredDomainTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Route53DomainsRegisteredDomainTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be4398a1ecc6453529490c92d8df2ce618fa2f909ba14e0e8893c950f01a0384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Route53DomainsRegisteredDomain",
    "Route53DomainsRegisteredDomainAdminContact",
    "Route53DomainsRegisteredDomainAdminContactOutputReference",
    "Route53DomainsRegisteredDomainBillingContact",
    "Route53DomainsRegisteredDomainBillingContactOutputReference",
    "Route53DomainsRegisteredDomainConfig",
    "Route53DomainsRegisteredDomainNameServer",
    "Route53DomainsRegisteredDomainNameServerList",
    "Route53DomainsRegisteredDomainNameServerOutputReference",
    "Route53DomainsRegisteredDomainRegistrantContact",
    "Route53DomainsRegisteredDomainRegistrantContactOutputReference",
    "Route53DomainsRegisteredDomainTechContact",
    "Route53DomainsRegisteredDomainTechContactOutputReference",
    "Route53DomainsRegisteredDomainTimeouts",
    "Route53DomainsRegisteredDomainTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__990051850705ac8a40315ac2abdf16d859b28f1f3b62e234cb6e0480f9690c4c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    domain_name: builtins.str,
    admin_contact: typing.Optional[typing.Union[Route53DomainsRegisteredDomainAdminContact, typing.Dict[builtins.str, typing.Any]]] = None,
    admin_privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_renew: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    billing_contact: typing.Optional[typing.Union[Route53DomainsRegisteredDomainBillingContact, typing.Dict[builtins.str, typing.Any]]] = None,
    billing_privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    name_server: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53DomainsRegisteredDomainNameServer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    registrant_contact: typing.Optional[typing.Union[Route53DomainsRegisteredDomainRegistrantContact, typing.Dict[builtins.str, typing.Any]]] = None,
    registrant_privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tech_contact: typing.Optional[typing.Union[Route53DomainsRegisteredDomainTechContact, typing.Dict[builtins.str, typing.Any]]] = None,
    tech_privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[Route53DomainsRegisteredDomainTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transfer_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__ddd3a2e306cd69a57c37e6bcf57563dcbd879f0dac6295d9aa284d2fa183f097(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ea364002cd6ee4d39d3a13ca90d07df37c0c5af4f552a0c5be5f8283a0ea2e5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53DomainsRegisteredDomainNameServer, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a538f31553930e89e8ecdc615cc840213bcb881cd19c076332a51ed90421b6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af380e828c67a0f50a43dac464bb8030ebb772fcb2c059eedd543893a09aa6ae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__242e625cb6f669b5c9152f8835b0e027c986fbe61d213e27018fdfb467620f38(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbea6408212a6af509d1686437e84ded58e504416247d83402ec0e92e334d6b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9719193fd935960e274c582be531da7abb6dfee31c993f58a1cdad5e5796adb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbfb979fc76a5af02daf5c17d43ea375a16eb000b157bd1236d7fe05f0f0a51f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de5bf1462f8aee4446c7db2f00e5623805094951c100f0f9050c10519e3adaea(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__830c00d1b3ceae941f3b4fac0be2bfa95734ce66eec20d01ff66daf3d07b2cd8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390548121375afe7300a8579057520541e71441a6d15cc22b046ecff10a19450(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb2ca3d47307b25302d9ccb7cf56652316e95f22ff959a0e004a797616442e1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84ad4e9066633064d6308d49f6000700b557487c5813a10fe26c7fc2aa4b4a7(
    *,
    address_line1: typing.Optional[builtins.str] = None,
    address_line2: typing.Optional[builtins.str] = None,
    city: typing.Optional[builtins.str] = None,
    contact_type: typing.Optional[builtins.str] = None,
    country_code: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    fax: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    organization_name: typing.Optional[builtins.str] = None,
    phone_number: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    zip_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abd429f82bfe052862885276403b3771e4a7f52ea5bc55af0d3b02f141f18c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da1663109b911cb42568dc99c46a85312bb61007bca439f39db66299483839e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cabd9373fc0ff5f0e6138bbcfd5bdd6db7b13405f0eadf5264d436836491913(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d32a22518721a6ca921b110ab18d5442400bd39ebe7b52ad612dbe0fc454dc50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7024b491c34b1176285a1b23e765e0aacf1d82761fe08c995b81c96a301243bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203a93280386e44ccd9a7d501e871b593c5c960d8086c16d2ede292633769d6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d36eba6f6ccd631ab6648569dd7d9a4a9c0d5514c7f00a55801636a35b0160a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02959121653ae3d27eda24e3e14f8bfbb61d98ba3d0d6d03d52b6c64fd24ab66(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418c83910233c09eff129e9797534def9c49c3f4ce01dce50da87f0438a85313(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2e33606380a5a30be8d0332d1da8e10a0d09d741924efd4524171cf01c5d3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f8307bf5603688cf62a4896098d833a470025cc0089c213f2990ca3ebc77956(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2326229675e9a30e5d37f49ffd322c055cd3e959c7d2c2cf7b36e72b78999a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4bf4b0f4a7ca8b00343f6f115e2327d46276709fcd79ae062a6286fda36bd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__512471f783be83f92a8b5d67dd235865e82ce5ea240aa32fb624fe70eb28b605(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d0d8e4accdd691f07445f676570a33e9ea7d6651fd602f993d47760cf1e076(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098667922d789247dcd3bf69d15eca88c8a86bbc545110263e8a27399e9d5add(
    value: typing.Optional[Route53DomainsRegisteredDomainAdminContact],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f4a156cf34e61d49efd7f426161565c4d83bccab447563ac28b5716ac617e44(
    *,
    address_line1: typing.Optional[builtins.str] = None,
    address_line2: typing.Optional[builtins.str] = None,
    city: typing.Optional[builtins.str] = None,
    contact_type: typing.Optional[builtins.str] = None,
    country_code: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    fax: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    organization_name: typing.Optional[builtins.str] = None,
    phone_number: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    zip_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe6740fb36e304a5cc0d72cba0ae862bb19cf53a8ef7915da5babc7fcbbf4bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8040618452f6a316d3dd0a13f074d4a15f9b73637b55311719f22a028ba888b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e29b43cb6a1470e89b4a861bd00c20d2b30e87f3d76ff720d394f540c5745a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98bd194fc81e1b4468986c9ba291eee3927f111f1444a1cdb6ccf13a2d4d0c2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a809afa52b59477bd92fe75b9482c33dbd0a85afa579453336c62f88eb6f1270(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c4238e54d0b1df476c5977989181a3b7f460ba1221b60566f7f57d74b9597d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba812ce8c933f766de53fe4c6ae5c4c0c48934fec03f1cb20cfc7e0eb6672807(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__911a27f4d4dcbc47b0954bb5ec57ee53ee48bdea7469c00ca4742ac827208884(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d340d1993f0feb559ade7343da26a202c758ac07f1ccf373c8f248ffe461a1f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e127b882a4dcabecb2706b1736c97e7fa6fad7380e2cc0447da104e53fce18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da7c559ab02cc2a93167bdc11d06d70d175f4e150626e12f687d6a104f794fc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1193afd2c0846e478949eca901fc22b5b7a170dbff4d4ad664f891ad199f733(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6bbe0c3c6220a97340d1b00dbbaec8f6500ab917c2f98501a5ee3b0c46a8405(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c54904f74170ad3bb1fa709398d46e916f429b200a340464524581e13aa29c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d01ab749e65c9de84475090b185b904b92f61e3784d7850278c11914ee3dc47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f3ce35bdf9d54a9daa960c9f93cd4efb54c60f914ac9efa1280a39b1ad04fe(
    value: typing.Optional[Route53DomainsRegisteredDomainBillingContact],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8eef8208c70c608628c0ea58e73055c7a1690d4e6c2f4a38501c4a1c6f7a8e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    domain_name: builtins.str,
    admin_contact: typing.Optional[typing.Union[Route53DomainsRegisteredDomainAdminContact, typing.Dict[builtins.str, typing.Any]]] = None,
    admin_privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_renew: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    billing_contact: typing.Optional[typing.Union[Route53DomainsRegisteredDomainBillingContact, typing.Dict[builtins.str, typing.Any]]] = None,
    billing_privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    name_server: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Route53DomainsRegisteredDomainNameServer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    registrant_contact: typing.Optional[typing.Union[Route53DomainsRegisteredDomainRegistrantContact, typing.Dict[builtins.str, typing.Any]]] = None,
    registrant_privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tech_contact: typing.Optional[typing.Union[Route53DomainsRegisteredDomainTechContact, typing.Dict[builtins.str, typing.Any]]] = None,
    tech_privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[Route53DomainsRegisteredDomainTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transfer_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b017f8d6906a4dfc68a67fbcff0afdec5c094adf57de334514265886414af3e(
    *,
    name: builtins.str,
    glue_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab514636f1bf966ff4c988b430e4058441add9f7c1daaa047e390a80c1941e92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bfc69f5ea57bfe90d006bec0e202efc8bb63ae7335eb0bd7b7728adc547c673(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2c20dc0b83759c570a9f0645ed5e51859112679797ad152b57e9df392c80f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d18b60314ae8a4bc39085e3a472a0854f96cad1b49680a335f7835d56c6a05(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310eb6e69a0a5797a60181ad74cb03be04b5f33a507cd31889888ef21d26e571(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f6641ded2726f4448beed8ea87577f5c7c581645ba0a61fc551ec0131ecb87a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Route53DomainsRegisteredDomainNameServer]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00506b80a4de51e5590e39e1dad36a4a9229659e4c66ff430cd2de7df70d2a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace7ee2d9c4ebf3fee65d1f00795ec430f3d0963322e8e2c0e98ae32e5397173(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882f1433e478da05a57f98b131264ccb33669dfe9085cf6dce2baf5063961f9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c625ffabd6a91df990613121ffaf0ad917809f40ec450fce421897d03a9b22(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Route53DomainsRegisteredDomainNameServer]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539828c18da71427e2982b24d059a31647071436356e5a92b2f87a91dd92e151(
    *,
    address_line1: typing.Optional[builtins.str] = None,
    address_line2: typing.Optional[builtins.str] = None,
    city: typing.Optional[builtins.str] = None,
    contact_type: typing.Optional[builtins.str] = None,
    country_code: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    fax: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    organization_name: typing.Optional[builtins.str] = None,
    phone_number: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    zip_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9dd86c61758126a2b7c44cd99aa17b51845f4a8f7ba485a88e703d0cb43a2ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c10487026d7e2af9d64cbe92c54a67963508268ae30a0566246d6910562cd407(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358b3bf53720afc889c45f6fb25657985b7abb76a8d67df65e210d1d1c67ede4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dabaf2dc194b55dac46ada298b4b88944baae2922e9ee561ffa0042d1fbaf16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f87a8496b23b2ea3a719bec4c05813ed7588af2ac838bf531a25aac9096e0871(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb988ee378a3f1f51c3cd2e580d651cc486bd6dfbe0c790cd2c4be269080b986(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a42988decddadbe9d94e85f96b251099e0c22d4c73362910232d78cc7a53e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09dc8d6231068a0b6cca8a4c01285e70dc0d558fbb27730b4db6b3da35104967(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd74f389b71db6562a0e674769c3125ab3e37326869f53705670d06f1b78a48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7760211a98d3733d86eb20e11b7bc4d8b850d53453486ccf0decbb33598905ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1fa2e0ea7b037b039836b9261b515f5fa9f7162a1b89542d4f65bb2b7ff5425(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584d1ec7e5406c2531ceb7ff91a51a16f59bf07189d03b7ceedce4cf3a7df6e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e556694a155b15797ec0b8f2520d8bec4126c54761e8f21abed171a4bd06c7bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da655601bb4b1fe50b4ecc179b2efce6049a6dbcfe605089b8380329c7287b4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6f5d5e93aee6da9346adf1ae291b3a4ea14fd90cf000b541640db7e8639fc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8aec85ca3eaf76140e4dd8180cedc7cf3b845e218932897ca553221df1eedf6(
    value: typing.Optional[Route53DomainsRegisteredDomainRegistrantContact],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac15abf92ca16506a573feeeb807108906192065e47e6e62e961d8673450d010(
    *,
    address_line1: typing.Optional[builtins.str] = None,
    address_line2: typing.Optional[builtins.str] = None,
    city: typing.Optional[builtins.str] = None,
    contact_type: typing.Optional[builtins.str] = None,
    country_code: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    fax: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    organization_name: typing.Optional[builtins.str] = None,
    phone_number: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    zip_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d19a32c67b928932839db46c96b51a4f54b44508fc4c226a57230913617ef55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b571c20a2d3b903065daa3d0a5a5a90580327b9307a47a1582bd0973afe13f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b99ae16f3d5f494da1671d937453342a25d58bd67cda408e2ca4b027b70c091(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14b76708266749dbbd235c9376f5f685cb184dfdc2f86fe1724809a58dcc822(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__970dd6ae781e670e96c695c67091a365a9c514d5facdd3bbcd3583a527b22461(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14770b16c0aa4bf4bb294382c25ed273269f9e8acd6c3e4c0e74850dc974e48f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819eb9cf3e82ed669a758dd39e2e4efbc5b40a566228c94426a877dfac55aa7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__174bb8a49c0c8a394331a08480d84ebf27dd569805b7f9ae1ebf56ec347f0629(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6427e5f6111ed5151e37db503c8f53008ecf61b1dec7d4dfe2b702f832d94f97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560469859cb78f19610b6656f6b19e19f70f6de9e4e5418a8dde8ff10295c376(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d44a7066bfd160444c8fe9d40d8efc74ce20b5f9687cb6ef4d7c2f40e6f2e51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__404ca4c623a1a2e85e9c3eec37b60df7d67f91b7b8eaffa1bdc3b77b9d851392(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8c78a7c9bc023e15b174c3f67f3605227d30b0b7b917e8029b28df239058a00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0366a1a4100d05f0b834caaf0073484a2f3585bc86be61c391e4b6758384e984(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25397793b3baac1a96b7b88c5369332b65d6b24587dac811e479c7e8a8d9c24c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b939049113aebe8f4bc26ac65cae0aafa285468393739304bd8e86a664c0402e(
    value: typing.Optional[Route53DomainsRegisteredDomainTechContact],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10db875302c90536d589cb9bfa49b134b816ff7b913106f84224c7229a298494(
    *,
    create: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aca28ee69a96b831c07dff91bcb2f19562ada40d309710f1def17c4a56d2dcb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a81fe083549c41cda9a4145dad298bacb15ae572804535c922bb5224b314d54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e366381a51d7e3433bd55a8a8e52d29cd52c27307d98610fcd52742a59e9321(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be4398a1ecc6453529490c92d8df2ce618fa2f909ba14e0e8893c950f01a0384(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Route53DomainsRegisteredDomainTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
