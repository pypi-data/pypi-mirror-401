r'''
# `aws_transfer_server`

Refer to the Terraform Registry for docs: [`aws_transfer_server`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server).
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


class TransferServer(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferServer.TransferServer",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server aws_transfer_server}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        certificate: typing.Optional[builtins.str] = None,
        directory_id: typing.Optional[builtins.str] = None,
        domain: typing.Optional[builtins.str] = None,
        endpoint_details: typing.Optional[typing.Union["TransferServerEndpointDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        function: typing.Optional[builtins.str] = None,
        host_key: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity_provider_type: typing.Optional[builtins.str] = None,
        invocation_role: typing.Optional[builtins.str] = None,
        logging_role: typing.Optional[builtins.str] = None,
        post_authentication_login_banner: typing.Optional[builtins.str] = None,
        pre_authentication_login_banner: typing.Optional[builtins.str] = None,
        protocol_details: typing.Optional[typing.Union["TransferServerProtocolDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        s3_storage_options: typing.Optional[typing.Union["TransferServerS3StorageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        security_policy_name: typing.Optional[builtins.str] = None,
        sftp_authentication_methods: typing.Optional[builtins.str] = None,
        structured_log_destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        url: typing.Optional[builtins.str] = None,
        workflow_details: typing.Optional[typing.Union["TransferServerWorkflowDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server aws_transfer_server} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#certificate TransferServer#certificate}.
        :param directory_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#directory_id TransferServer#directory_id}.
        :param domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#domain TransferServer#domain}.
        :param endpoint_details: endpoint_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#endpoint_details TransferServer#endpoint_details}
        :param endpoint_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#endpoint_type TransferServer#endpoint_type}.
        :param force_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#force_destroy TransferServer#force_destroy}.
        :param function: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#function TransferServer#function}.
        :param host_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#host_key TransferServer#host_key}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#id TransferServer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity_provider_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#identity_provider_type TransferServer#identity_provider_type}.
        :param invocation_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#invocation_role TransferServer#invocation_role}.
        :param logging_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#logging_role TransferServer#logging_role}.
        :param post_authentication_login_banner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#post_authentication_login_banner TransferServer#post_authentication_login_banner}.
        :param pre_authentication_login_banner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#pre_authentication_login_banner TransferServer#pre_authentication_login_banner}.
        :param protocol_details: protocol_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#protocol_details TransferServer#protocol_details}
        :param protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#protocols TransferServer#protocols}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#region TransferServer#region}
        :param s3_storage_options: s3_storage_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#s3_storage_options TransferServer#s3_storage_options}
        :param security_policy_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#security_policy_name TransferServer#security_policy_name}.
        :param sftp_authentication_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#sftp_authentication_methods TransferServer#sftp_authentication_methods}.
        :param structured_log_destinations: This is a set of arns of destinations that will receive structured logs from the transfer server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#structured_log_destinations TransferServer#structured_log_destinations}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#tags TransferServer#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#tags_all TransferServer#tags_all}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#url TransferServer#url}.
        :param workflow_details: workflow_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#workflow_details TransferServer#workflow_details}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b07ce2b8386429f1f291351751b79399b69e0014027c3c572d7121a9d5118013)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = TransferServerConfig(
            certificate=certificate,
            directory_id=directory_id,
            domain=domain,
            endpoint_details=endpoint_details,
            endpoint_type=endpoint_type,
            force_destroy=force_destroy,
            function=function,
            host_key=host_key,
            id=id,
            identity_provider_type=identity_provider_type,
            invocation_role=invocation_role,
            logging_role=logging_role,
            post_authentication_login_banner=post_authentication_login_banner,
            pre_authentication_login_banner=pre_authentication_login_banner,
            protocol_details=protocol_details,
            protocols=protocols,
            region=region,
            s3_storage_options=s3_storage_options,
            security_policy_name=security_policy_name,
            sftp_authentication_methods=sftp_authentication_methods,
            structured_log_destinations=structured_log_destinations,
            tags=tags,
            tags_all=tags_all,
            url=url,
            workflow_details=workflow_details,
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
        '''Generates CDKTF code for importing a TransferServer resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the TransferServer to import.
        :param import_from_id: The id of the existing TransferServer that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the TransferServer to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17bd59aed27bc4e14848794c431d4187e85487f95d72a07786a6a19e574e151c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEndpointDetails")
    def put_endpoint_details(
        self,
        *,
        address_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_endpoint_id: typing.Optional[builtins.str] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address_allocation_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#address_allocation_ids TransferServer#address_allocation_ids}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#security_group_ids TransferServer#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#subnet_ids TransferServer#subnet_ids}.
        :param vpc_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#vpc_endpoint_id TransferServer#vpc_endpoint_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#vpc_id TransferServer#vpc_id}.
        '''
        value = TransferServerEndpointDetails(
            address_allocation_ids=address_allocation_ids,
            security_group_ids=security_group_ids,
            subnet_ids=subnet_ids,
            vpc_endpoint_id=vpc_endpoint_id,
            vpc_id=vpc_id,
        )

        return typing.cast(None, jsii.invoke(self, "putEndpointDetails", [value]))

    @jsii.member(jsii_name="putProtocolDetails")
    def put_protocol_details(
        self,
        *,
        as2_transports: typing.Optional[typing.Sequence[builtins.str]] = None,
        passive_ip: typing.Optional[builtins.str] = None,
        set_stat_option: typing.Optional[builtins.str] = None,
        tls_session_resumption_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param as2_transports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#as2_transports TransferServer#as2_transports}.
        :param passive_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#passive_ip TransferServer#passive_ip}.
        :param set_stat_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#set_stat_option TransferServer#set_stat_option}.
        :param tls_session_resumption_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#tls_session_resumption_mode TransferServer#tls_session_resumption_mode}.
        '''
        value = TransferServerProtocolDetails(
            as2_transports=as2_transports,
            passive_ip=passive_ip,
            set_stat_option=set_stat_option,
            tls_session_resumption_mode=tls_session_resumption_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putProtocolDetails", [value]))

    @jsii.member(jsii_name="putS3StorageOptions")
    def put_s3_storage_options(
        self,
        *,
        directory_listing_optimization: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param directory_listing_optimization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#directory_listing_optimization TransferServer#directory_listing_optimization}.
        '''
        value = TransferServerS3StorageOptions(
            directory_listing_optimization=directory_listing_optimization
        )

        return typing.cast(None, jsii.invoke(self, "putS3StorageOptions", [value]))

    @jsii.member(jsii_name="putWorkflowDetails")
    def put_workflow_details(
        self,
        *,
        on_partial_upload: typing.Optional[typing.Union["TransferServerWorkflowDetailsOnPartialUpload", typing.Dict[builtins.str, typing.Any]]] = None,
        on_upload: typing.Optional[typing.Union["TransferServerWorkflowDetailsOnUpload", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param on_partial_upload: on_partial_upload block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#on_partial_upload TransferServer#on_partial_upload}
        :param on_upload: on_upload block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#on_upload TransferServer#on_upload}
        '''
        value = TransferServerWorkflowDetails(
            on_partial_upload=on_partial_upload, on_upload=on_upload
        )

        return typing.cast(None, jsii.invoke(self, "putWorkflowDetails", [value]))

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetDirectoryId")
    def reset_directory_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirectoryId", []))

    @jsii.member(jsii_name="resetDomain")
    def reset_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomain", []))

    @jsii.member(jsii_name="resetEndpointDetails")
    def reset_endpoint_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointDetails", []))

    @jsii.member(jsii_name="resetEndpointType")
    def reset_endpoint_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointType", []))

    @jsii.member(jsii_name="resetForceDestroy")
    def reset_force_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceDestroy", []))

    @jsii.member(jsii_name="resetFunction")
    def reset_function(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunction", []))

    @jsii.member(jsii_name="resetHostKey")
    def reset_host_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostKey", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentityProviderType")
    def reset_identity_provider_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProviderType", []))

    @jsii.member(jsii_name="resetInvocationRole")
    def reset_invocation_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvocationRole", []))

    @jsii.member(jsii_name="resetLoggingRole")
    def reset_logging_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingRole", []))

    @jsii.member(jsii_name="resetPostAuthenticationLoginBanner")
    def reset_post_authentication_login_banner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostAuthenticationLoginBanner", []))

    @jsii.member(jsii_name="resetPreAuthenticationLoginBanner")
    def reset_pre_authentication_login_banner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreAuthenticationLoginBanner", []))

    @jsii.member(jsii_name="resetProtocolDetails")
    def reset_protocol_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocolDetails", []))

    @jsii.member(jsii_name="resetProtocols")
    def reset_protocols(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocols", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetS3StorageOptions")
    def reset_s3_storage_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3StorageOptions", []))

    @jsii.member(jsii_name="resetSecurityPolicyName")
    def reset_security_policy_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityPolicyName", []))

    @jsii.member(jsii_name="resetSftpAuthenticationMethods")
    def reset_sftp_authentication_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSftpAuthenticationMethods", []))

    @jsii.member(jsii_name="resetStructuredLogDestinations")
    def reset_structured_log_destinations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStructuredLogDestinations", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @jsii.member(jsii_name="resetWorkflowDetails")
    def reset_workflow_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkflowDetails", []))

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
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="endpointDetails")
    def endpoint_details(self) -> "TransferServerEndpointDetailsOutputReference":
        return typing.cast("TransferServerEndpointDetailsOutputReference", jsii.get(self, "endpointDetails"))

    @builtins.property
    @jsii.member(jsii_name="hostKeyFingerprint")
    def host_key_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostKeyFingerprint"))

    @builtins.property
    @jsii.member(jsii_name="protocolDetails")
    def protocol_details(self) -> "TransferServerProtocolDetailsOutputReference":
        return typing.cast("TransferServerProtocolDetailsOutputReference", jsii.get(self, "protocolDetails"))

    @builtins.property
    @jsii.member(jsii_name="s3StorageOptions")
    def s3_storage_options(self) -> "TransferServerS3StorageOptionsOutputReference":
        return typing.cast("TransferServerS3StorageOptionsOutputReference", jsii.get(self, "s3StorageOptions"))

    @builtins.property
    @jsii.member(jsii_name="workflowDetails")
    def workflow_details(self) -> "TransferServerWorkflowDetailsOutputReference":
        return typing.cast("TransferServerWorkflowDetailsOutputReference", jsii.get(self, "workflowDetails"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="directoryIdInput")
    def directory_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directoryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointDetailsInput")
    def endpoint_details_input(
        self,
    ) -> typing.Optional["TransferServerEndpointDetails"]:
        return typing.cast(typing.Optional["TransferServerEndpointDetails"], jsii.get(self, "endpointDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointTypeInput")
    def endpoint_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDestroyInput")
    def force_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="functionInput")
    def function_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionInput"))

    @builtins.property
    @jsii.member(jsii_name="hostKeyInput")
    def host_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="identityProviderTypeInput")
    def identity_provider_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityProviderTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="invocationRoleInput")
    def invocation_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "invocationRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingRoleInput")
    def logging_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loggingRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="postAuthenticationLoginBannerInput")
    def post_authentication_login_banner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postAuthenticationLoginBannerInput"))

    @builtins.property
    @jsii.member(jsii_name="preAuthenticationLoginBannerInput")
    def pre_authentication_login_banner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preAuthenticationLoginBannerInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolDetailsInput")
    def protocol_details_input(
        self,
    ) -> typing.Optional["TransferServerProtocolDetails"]:
        return typing.cast(typing.Optional["TransferServerProtocolDetails"], jsii.get(self, "protocolDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolsInput")
    def protocols_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "protocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="s3StorageOptionsInput")
    def s3_storage_options_input(
        self,
    ) -> typing.Optional["TransferServerS3StorageOptions"]:
        return typing.cast(typing.Optional["TransferServerS3StorageOptions"], jsii.get(self, "s3StorageOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityPolicyNameInput")
    def security_policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityPolicyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sftpAuthenticationMethodsInput")
    def sftp_authentication_methods_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sftpAuthenticationMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="structuredLogDestinationsInput")
    def structured_log_destinations_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "structuredLogDestinationsInput"))

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
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="workflowDetailsInput")
    def workflow_details_input(
        self,
    ) -> typing.Optional["TransferServerWorkflowDetails"]:
        return typing.cast(typing.Optional["TransferServerWorkflowDetails"], jsii.get(self, "workflowDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e908c29a7d52a107a3030f0768d3d2e91ef31ec2f849a714413f16beb1a963)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="directoryId")
    def directory_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "directoryId"))

    @directory_id.setter
    def directory_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1909e168849216d8b93017c775bece2feb45bc415fd249a7a0183dafdc698a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directoryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a8db6038c5c805e737434bfe98f7f9d7bc6f1d635164a85d8204857afdfc09a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointType")
    def endpoint_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointType"))

    @endpoint_type.setter
    def endpoint_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf586fdf69308c31a5fdffa68f4015543c4cdf1c9052bf522c315b09c7b123ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceDestroy")
    def force_destroy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceDestroy"))

    @force_destroy.setter
    def force_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dc3e90d779bf029e795581bf70c76fa2eb133aa43e80d413e37b32f55ef6863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "function"))

    @function.setter
    def function(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0a045101cb2941820b7b544809344635073039583bb38600a663920e8f0b9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "function", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostKey")
    def host_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostKey"))

    @host_key.setter
    def host_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d98e9dde5c4cfcf270a5fbbf88a685da1e4c6f03096c360ce17d481701fa198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d49ae8e144d91d535d8a210cd36c7a73683cac9fec7e9c48c3fda0459124f2b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityProviderType")
    def identity_provider_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProviderType"))

    @identity_provider_type.setter
    def identity_provider_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3788ea02f16031b8bdd8d7dd9d0dde1fc4666062b890cf89ad4b7978c33a7a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="invocationRole")
    def invocation_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "invocationRole"))

    @invocation_role.setter
    def invocation_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ba09b80d64edeac368484a9f6064bd6371b53406d7609251fa6df718a04b3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invocationRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loggingRole")
    def logging_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loggingRole"))

    @logging_role.setter
    def logging_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a80a38a1bfacd42fb61475219472eb6a08f3f09a26904753dc41bb1690c303)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postAuthenticationLoginBanner")
    def post_authentication_login_banner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postAuthenticationLoginBanner"))

    @post_authentication_login_banner.setter
    def post_authentication_login_banner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab652dfe080cbbd8b8c953e58d3df102b339302f79f2cca6fee8667967b3908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postAuthenticationLoginBanner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preAuthenticationLoginBanner")
    def pre_authentication_login_banner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preAuthenticationLoginBanner"))

    @pre_authentication_login_banner.setter
    def pre_authentication_login_banner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9705036070d2d3699c542995cac649ea35c6d031ab02031bb1e297c64b3a0a35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preAuthenticationLoginBanner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocols")
    def protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "protocols"))

    @protocols.setter
    def protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7849fc2bf268dc16784b881c694014faa36d72fcf0b5fbaf139b80ec7b69e791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__863ae668fa8f6bbdc17eb41247adfdccc4c9e3fd68fc41ac8d4dca74f0a36aee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityPolicyName")
    def security_policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityPolicyName"))

    @security_policy_name.setter
    def security_policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5117c3c19a6ae1eef21d5fd7cede4469b81fe057b6d490bdd78236e27c0498af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityPolicyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sftpAuthenticationMethods")
    def sftp_authentication_methods(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sftpAuthenticationMethods"))

    @sftp_authentication_methods.setter
    def sftp_authentication_methods(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be5cc4862cd276276b8cf11b8ca739ec04974edc7865c43202349047b7e9989f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sftpAuthenticationMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="structuredLogDestinations")
    def structured_log_destinations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "structuredLogDestinations"))

    @structured_log_destinations.setter
    def structured_log_destinations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10dc2590e7058e13f0eee27abbb9483ac196c7353fb2de68c9379f65f680648b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "structuredLogDestinations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9533cc00b00828d31bcb958197bd4cdf51597ca5a978fc57705e942a6e24e48f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0be0dce44937110e96c7ff1b72ae2dba92ccdd60fa022d20898bbc036796e56f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73b542f162f7942149431b38d270c4ccbf5c64acf69ac89db689b08426f56b33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferServer.TransferServerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "certificate": "certificate",
        "directory_id": "directoryId",
        "domain": "domain",
        "endpoint_details": "endpointDetails",
        "endpoint_type": "endpointType",
        "force_destroy": "forceDestroy",
        "function": "function",
        "host_key": "hostKey",
        "id": "id",
        "identity_provider_type": "identityProviderType",
        "invocation_role": "invocationRole",
        "logging_role": "loggingRole",
        "post_authentication_login_banner": "postAuthenticationLoginBanner",
        "pre_authentication_login_banner": "preAuthenticationLoginBanner",
        "protocol_details": "protocolDetails",
        "protocols": "protocols",
        "region": "region",
        "s3_storage_options": "s3StorageOptions",
        "security_policy_name": "securityPolicyName",
        "sftp_authentication_methods": "sftpAuthenticationMethods",
        "structured_log_destinations": "structuredLogDestinations",
        "tags": "tags",
        "tags_all": "tagsAll",
        "url": "url",
        "workflow_details": "workflowDetails",
    },
)
class TransferServerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        certificate: typing.Optional[builtins.str] = None,
        directory_id: typing.Optional[builtins.str] = None,
        domain: typing.Optional[builtins.str] = None,
        endpoint_details: typing.Optional[typing.Union["TransferServerEndpointDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        function: typing.Optional[builtins.str] = None,
        host_key: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity_provider_type: typing.Optional[builtins.str] = None,
        invocation_role: typing.Optional[builtins.str] = None,
        logging_role: typing.Optional[builtins.str] = None,
        post_authentication_login_banner: typing.Optional[builtins.str] = None,
        pre_authentication_login_banner: typing.Optional[builtins.str] = None,
        protocol_details: typing.Optional[typing.Union["TransferServerProtocolDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        s3_storage_options: typing.Optional[typing.Union["TransferServerS3StorageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        security_policy_name: typing.Optional[builtins.str] = None,
        sftp_authentication_methods: typing.Optional[builtins.str] = None,
        structured_log_destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        url: typing.Optional[builtins.str] = None,
        workflow_details: typing.Optional[typing.Union["TransferServerWorkflowDetails", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#certificate TransferServer#certificate}.
        :param directory_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#directory_id TransferServer#directory_id}.
        :param domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#domain TransferServer#domain}.
        :param endpoint_details: endpoint_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#endpoint_details TransferServer#endpoint_details}
        :param endpoint_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#endpoint_type TransferServer#endpoint_type}.
        :param force_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#force_destroy TransferServer#force_destroy}.
        :param function: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#function TransferServer#function}.
        :param host_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#host_key TransferServer#host_key}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#id TransferServer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity_provider_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#identity_provider_type TransferServer#identity_provider_type}.
        :param invocation_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#invocation_role TransferServer#invocation_role}.
        :param logging_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#logging_role TransferServer#logging_role}.
        :param post_authentication_login_banner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#post_authentication_login_banner TransferServer#post_authentication_login_banner}.
        :param pre_authentication_login_banner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#pre_authentication_login_banner TransferServer#pre_authentication_login_banner}.
        :param protocol_details: protocol_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#protocol_details TransferServer#protocol_details}
        :param protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#protocols TransferServer#protocols}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#region TransferServer#region}
        :param s3_storage_options: s3_storage_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#s3_storage_options TransferServer#s3_storage_options}
        :param security_policy_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#security_policy_name TransferServer#security_policy_name}.
        :param sftp_authentication_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#sftp_authentication_methods TransferServer#sftp_authentication_methods}.
        :param structured_log_destinations: This is a set of arns of destinations that will receive structured logs from the transfer server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#structured_log_destinations TransferServer#structured_log_destinations}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#tags TransferServer#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#tags_all TransferServer#tags_all}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#url TransferServer#url}.
        :param workflow_details: workflow_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#workflow_details TransferServer#workflow_details}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(endpoint_details, dict):
            endpoint_details = TransferServerEndpointDetails(**endpoint_details)
        if isinstance(protocol_details, dict):
            protocol_details = TransferServerProtocolDetails(**protocol_details)
        if isinstance(s3_storage_options, dict):
            s3_storage_options = TransferServerS3StorageOptions(**s3_storage_options)
        if isinstance(workflow_details, dict):
            workflow_details = TransferServerWorkflowDetails(**workflow_details)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd011d1fa7c25e69d821066b7109b8d0c43f0df64afa2085944f8410427680e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument directory_id", value=directory_id, expected_type=type_hints["directory_id"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument endpoint_details", value=endpoint_details, expected_type=type_hints["endpoint_details"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument force_destroy", value=force_destroy, expected_type=type_hints["force_destroy"])
            check_type(argname="argument function", value=function, expected_type=type_hints["function"])
            check_type(argname="argument host_key", value=host_key, expected_type=type_hints["host_key"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity_provider_type", value=identity_provider_type, expected_type=type_hints["identity_provider_type"])
            check_type(argname="argument invocation_role", value=invocation_role, expected_type=type_hints["invocation_role"])
            check_type(argname="argument logging_role", value=logging_role, expected_type=type_hints["logging_role"])
            check_type(argname="argument post_authentication_login_banner", value=post_authentication_login_banner, expected_type=type_hints["post_authentication_login_banner"])
            check_type(argname="argument pre_authentication_login_banner", value=pre_authentication_login_banner, expected_type=type_hints["pre_authentication_login_banner"])
            check_type(argname="argument protocol_details", value=protocol_details, expected_type=type_hints["protocol_details"])
            check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument s3_storage_options", value=s3_storage_options, expected_type=type_hints["s3_storage_options"])
            check_type(argname="argument security_policy_name", value=security_policy_name, expected_type=type_hints["security_policy_name"])
            check_type(argname="argument sftp_authentication_methods", value=sftp_authentication_methods, expected_type=type_hints["sftp_authentication_methods"])
            check_type(argname="argument structured_log_destinations", value=structured_log_destinations, expected_type=type_hints["structured_log_destinations"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument workflow_details", value=workflow_details, expected_type=type_hints["workflow_details"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if certificate is not None:
            self._values["certificate"] = certificate
        if directory_id is not None:
            self._values["directory_id"] = directory_id
        if domain is not None:
            self._values["domain"] = domain
        if endpoint_details is not None:
            self._values["endpoint_details"] = endpoint_details
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type
        if force_destroy is not None:
            self._values["force_destroy"] = force_destroy
        if function is not None:
            self._values["function"] = function
        if host_key is not None:
            self._values["host_key"] = host_key
        if id is not None:
            self._values["id"] = id
        if identity_provider_type is not None:
            self._values["identity_provider_type"] = identity_provider_type
        if invocation_role is not None:
            self._values["invocation_role"] = invocation_role
        if logging_role is not None:
            self._values["logging_role"] = logging_role
        if post_authentication_login_banner is not None:
            self._values["post_authentication_login_banner"] = post_authentication_login_banner
        if pre_authentication_login_banner is not None:
            self._values["pre_authentication_login_banner"] = pre_authentication_login_banner
        if protocol_details is not None:
            self._values["protocol_details"] = protocol_details
        if protocols is not None:
            self._values["protocols"] = protocols
        if region is not None:
            self._values["region"] = region
        if s3_storage_options is not None:
            self._values["s3_storage_options"] = s3_storage_options
        if security_policy_name is not None:
            self._values["security_policy_name"] = security_policy_name
        if sftp_authentication_methods is not None:
            self._values["sftp_authentication_methods"] = sftp_authentication_methods
        if structured_log_destinations is not None:
            self._values["structured_log_destinations"] = structured_log_destinations
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if url is not None:
            self._values["url"] = url
        if workflow_details is not None:
            self._values["workflow_details"] = workflow_details

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
    def certificate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#certificate TransferServer#certificate}.'''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def directory_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#directory_id TransferServer#directory_id}.'''
        result = self._values.get("directory_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#domain TransferServer#domain}.'''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_details(self) -> typing.Optional["TransferServerEndpointDetails"]:
        '''endpoint_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#endpoint_details TransferServer#endpoint_details}
        '''
        result = self._values.get("endpoint_details")
        return typing.cast(typing.Optional["TransferServerEndpointDetails"], result)

    @builtins.property
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#endpoint_type TransferServer#endpoint_type}.'''
        result = self._values.get("endpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#force_destroy TransferServer#force_destroy}.'''
        result = self._values.get("force_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def function(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#function TransferServer#function}.'''
        result = self._values.get("function")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#host_key TransferServer#host_key}.'''
        result = self._values.get("host_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#id TransferServer#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_provider_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#identity_provider_type TransferServer#identity_provider_type}.'''
        result = self._values.get("identity_provider_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invocation_role(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#invocation_role TransferServer#invocation_role}.'''
        result = self._values.get("invocation_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_role(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#logging_role TransferServer#logging_role}.'''
        result = self._values.get("logging_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_authentication_login_banner(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#post_authentication_login_banner TransferServer#post_authentication_login_banner}.'''
        result = self._values.get("post_authentication_login_banner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pre_authentication_login_banner(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#pre_authentication_login_banner TransferServer#pre_authentication_login_banner}.'''
        result = self._values.get("pre_authentication_login_banner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol_details(self) -> typing.Optional["TransferServerProtocolDetails"]:
        '''protocol_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#protocol_details TransferServer#protocol_details}
        '''
        result = self._values.get("protocol_details")
        return typing.cast(typing.Optional["TransferServerProtocolDetails"], result)

    @builtins.property
    def protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#protocols TransferServer#protocols}.'''
        result = self._values.get("protocols")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#region TransferServer#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_storage_options(self) -> typing.Optional["TransferServerS3StorageOptions"]:
        '''s3_storage_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#s3_storage_options TransferServer#s3_storage_options}
        '''
        result = self._values.get("s3_storage_options")
        return typing.cast(typing.Optional["TransferServerS3StorageOptions"], result)

    @builtins.property
    def security_policy_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#security_policy_name TransferServer#security_policy_name}.'''
        result = self._values.get("security_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sftp_authentication_methods(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#sftp_authentication_methods TransferServer#sftp_authentication_methods}.'''
        result = self._values.get("sftp_authentication_methods")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def structured_log_destinations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''This is a set of arns of destinations that will receive structured logs from the transfer server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#structured_log_destinations TransferServer#structured_log_destinations}
        '''
        result = self._values.get("structured_log_destinations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#tags TransferServer#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#tags_all TransferServer#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#url TransferServer#url}.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_details(self) -> typing.Optional["TransferServerWorkflowDetails"]:
        '''workflow_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#workflow_details TransferServer#workflow_details}
        '''
        result = self._values.get("workflow_details")
        return typing.cast(typing.Optional["TransferServerWorkflowDetails"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferServerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferServer.TransferServerEndpointDetails",
    jsii_struct_bases=[],
    name_mapping={
        "address_allocation_ids": "addressAllocationIds",
        "security_group_ids": "securityGroupIds",
        "subnet_ids": "subnetIds",
        "vpc_endpoint_id": "vpcEndpointId",
        "vpc_id": "vpcId",
    },
)
class TransferServerEndpointDetails:
    def __init__(
        self,
        *,
        address_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_endpoint_id: typing.Optional[builtins.str] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address_allocation_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#address_allocation_ids TransferServer#address_allocation_ids}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#security_group_ids TransferServer#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#subnet_ids TransferServer#subnet_ids}.
        :param vpc_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#vpc_endpoint_id TransferServer#vpc_endpoint_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#vpc_id TransferServer#vpc_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b895c234d48390c17a011cc05d71587f3c0d1074ca5768692cd34bf830f2aa)
            check_type(argname="argument address_allocation_ids", value=address_allocation_ids, expected_type=type_hints["address_allocation_ids"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument vpc_endpoint_id", value=vpc_endpoint_id, expected_type=type_hints["vpc_endpoint_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address_allocation_ids is not None:
            self._values["address_allocation_ids"] = address_allocation_ids
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if vpc_endpoint_id is not None:
            self._values["vpc_endpoint_id"] = vpc_endpoint_id
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def address_allocation_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#address_allocation_ids TransferServer#address_allocation_ids}.'''
        result = self._values.get("address_allocation_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#security_group_ids TransferServer#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#subnet_ids TransferServer#subnet_ids}.'''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#vpc_endpoint_id TransferServer#vpc_endpoint_id}.'''
        result = self._values.get("vpc_endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#vpc_id TransferServer#vpc_id}.'''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferServerEndpointDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferServerEndpointDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferServer.TransferServerEndpointDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec974208dc5ff7ae391a974fd6c089cbb5a7163e39498ce912313707b09c3ab2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddressAllocationIds")
    def reset_address_allocation_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressAllocationIds", []))

    @jsii.member(jsii_name="resetSecurityGroupIds")
    def reset_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupIds", []))

    @jsii.member(jsii_name="resetSubnetIds")
    def reset_subnet_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetIds", []))

    @jsii.member(jsii_name="resetVpcEndpointId")
    def reset_vpc_endpoint_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcEndpointId", []))

    @jsii.member(jsii_name="resetVpcId")
    def reset_vpc_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcId", []))

    @builtins.property
    @jsii.member(jsii_name="addressAllocationIdsInput")
    def address_allocation_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "addressAllocationIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdsInput")
    def subnet_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcEndpointIdInput")
    def vpc_endpoint_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcEndpointIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="addressAllocationIds")
    def address_allocation_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "addressAllocationIds"))

    @address_allocation_ids.setter
    def address_allocation_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1b99a6c4c023258199fd55a1ac29fb4acbbf0cf380fd5f8cd48dbd47bc7cea3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressAllocationIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c495914791016e02f502ab73e9ccc33e72355ace914cab17e4bfddabb4ff773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e46671076ff4b86bb9104fefc7e871d44337059908dfaafd2f624f85a85dd14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcEndpointId")
    def vpc_endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcEndpointId"))

    @vpc_endpoint_id.setter
    def vpc_endpoint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7202a768803e2d9907a2ae9b4c69b6f2ad82d77ed6f984cf0ae98b4cc53680b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcEndpointId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692e842178056a71ddde6862b4fa13fb6c0009a55cd42416f0ee81273f6edcb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TransferServerEndpointDetails]:
        return typing.cast(typing.Optional[TransferServerEndpointDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferServerEndpointDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2333673614215d8c687d7b12ec474eecda65b7301f33f040de8fe11745654cac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferServer.TransferServerProtocolDetails",
    jsii_struct_bases=[],
    name_mapping={
        "as2_transports": "as2Transports",
        "passive_ip": "passiveIp",
        "set_stat_option": "setStatOption",
        "tls_session_resumption_mode": "tlsSessionResumptionMode",
    },
)
class TransferServerProtocolDetails:
    def __init__(
        self,
        *,
        as2_transports: typing.Optional[typing.Sequence[builtins.str]] = None,
        passive_ip: typing.Optional[builtins.str] = None,
        set_stat_option: typing.Optional[builtins.str] = None,
        tls_session_resumption_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param as2_transports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#as2_transports TransferServer#as2_transports}.
        :param passive_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#passive_ip TransferServer#passive_ip}.
        :param set_stat_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#set_stat_option TransferServer#set_stat_option}.
        :param tls_session_resumption_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#tls_session_resumption_mode TransferServer#tls_session_resumption_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a80b1b9dc95bfc9382eca94220c0b2ab338cb22bdace013cae5bb7380a49da)
            check_type(argname="argument as2_transports", value=as2_transports, expected_type=type_hints["as2_transports"])
            check_type(argname="argument passive_ip", value=passive_ip, expected_type=type_hints["passive_ip"])
            check_type(argname="argument set_stat_option", value=set_stat_option, expected_type=type_hints["set_stat_option"])
            check_type(argname="argument tls_session_resumption_mode", value=tls_session_resumption_mode, expected_type=type_hints["tls_session_resumption_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if as2_transports is not None:
            self._values["as2_transports"] = as2_transports
        if passive_ip is not None:
            self._values["passive_ip"] = passive_ip
        if set_stat_option is not None:
            self._values["set_stat_option"] = set_stat_option
        if tls_session_resumption_mode is not None:
            self._values["tls_session_resumption_mode"] = tls_session_resumption_mode

    @builtins.property
    def as2_transports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#as2_transports TransferServer#as2_transports}.'''
        result = self._values.get("as2_transports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def passive_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#passive_ip TransferServer#passive_ip}.'''
        result = self._values.get("passive_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def set_stat_option(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#set_stat_option TransferServer#set_stat_option}.'''
        result = self._values.get("set_stat_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_session_resumption_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#tls_session_resumption_mode TransferServer#tls_session_resumption_mode}.'''
        result = self._values.get("tls_session_resumption_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferServerProtocolDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferServerProtocolDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferServer.TransferServerProtocolDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6978767dc0d3223f408af12eeaf4e963aadf3bbad4b7f331dae06bf1277671d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAs2Transports")
    def reset_as2_transports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAs2Transports", []))

    @jsii.member(jsii_name="resetPassiveIp")
    def reset_passive_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassiveIp", []))

    @jsii.member(jsii_name="resetSetStatOption")
    def reset_set_stat_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSetStatOption", []))

    @jsii.member(jsii_name="resetTlsSessionResumptionMode")
    def reset_tls_session_resumption_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsSessionResumptionMode", []))

    @builtins.property
    @jsii.member(jsii_name="as2TransportsInput")
    def as2_transports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "as2TransportsInput"))

    @builtins.property
    @jsii.member(jsii_name="passiveIpInput")
    def passive_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passiveIpInput"))

    @builtins.property
    @jsii.member(jsii_name="setStatOptionInput")
    def set_stat_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "setStatOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsSessionResumptionModeInput")
    def tls_session_resumption_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsSessionResumptionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="as2Transports")
    def as2_transports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "as2Transports"))

    @as2_transports.setter
    def as2_transports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5776e92a973662d3277bdb03790c73332c7f9cde938fd169674c8357a66af30c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "as2Transports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passiveIp")
    def passive_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passiveIp"))

    @passive_ip.setter
    def passive_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b088bafdea41cf8df31dffffff355b83f43c226c768f63024fa6eedbd2ae5b17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passiveIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="setStatOption")
    def set_stat_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "setStatOption"))

    @set_stat_option.setter
    def set_stat_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62aceb0d4ea2dd430ef8b384bd48089fb69ae253158a08ae2e5f3d643f4dd2a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "setStatOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsSessionResumptionMode")
    def tls_session_resumption_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsSessionResumptionMode"))

    @tls_session_resumption_mode.setter
    def tls_session_resumption_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bad3d6603036a658fcbc6bc9e3eaaaa83aa9f1dcd08b5be12fd48d2e916f42b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsSessionResumptionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TransferServerProtocolDetails]:
        return typing.cast(typing.Optional[TransferServerProtocolDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferServerProtocolDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54c0b289ad0d0cf9713ae74872e05878a6ba15be6c5ca0b15c3defb1f6531b2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferServer.TransferServerS3StorageOptions",
    jsii_struct_bases=[],
    name_mapping={"directory_listing_optimization": "directoryListingOptimization"},
)
class TransferServerS3StorageOptions:
    def __init__(
        self,
        *,
        directory_listing_optimization: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param directory_listing_optimization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#directory_listing_optimization TransferServer#directory_listing_optimization}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da88268872492087126b4ce75787a816a61d9297329744c83e042dec11e38359)
            check_type(argname="argument directory_listing_optimization", value=directory_listing_optimization, expected_type=type_hints["directory_listing_optimization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if directory_listing_optimization is not None:
            self._values["directory_listing_optimization"] = directory_listing_optimization

    @builtins.property
    def directory_listing_optimization(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#directory_listing_optimization TransferServer#directory_listing_optimization}.'''
        result = self._values.get("directory_listing_optimization")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferServerS3StorageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferServerS3StorageOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferServer.TransferServerS3StorageOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37e5d94d6dcc93feca726bef553f18c2f188165aaaf14a1cb570a1fbd66a9c7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDirectoryListingOptimization")
    def reset_directory_listing_optimization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirectoryListingOptimization", []))

    @builtins.property
    @jsii.member(jsii_name="directoryListingOptimizationInput")
    def directory_listing_optimization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directoryListingOptimizationInput"))

    @builtins.property
    @jsii.member(jsii_name="directoryListingOptimization")
    def directory_listing_optimization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "directoryListingOptimization"))

    @directory_listing_optimization.setter
    def directory_listing_optimization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bcf3fb3f367063bc59259d5c2f641e579b4fb4650549b0b36e917813ae26528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directoryListingOptimization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TransferServerS3StorageOptions]:
        return typing.cast(typing.Optional[TransferServerS3StorageOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferServerS3StorageOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c52f93201a3533a23a09f6e28a628933bd0c78bd89ce15e1000be0b681dcffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferServer.TransferServerWorkflowDetails",
    jsii_struct_bases=[],
    name_mapping={"on_partial_upload": "onPartialUpload", "on_upload": "onUpload"},
)
class TransferServerWorkflowDetails:
    def __init__(
        self,
        *,
        on_partial_upload: typing.Optional[typing.Union["TransferServerWorkflowDetailsOnPartialUpload", typing.Dict[builtins.str, typing.Any]]] = None,
        on_upload: typing.Optional[typing.Union["TransferServerWorkflowDetailsOnUpload", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param on_partial_upload: on_partial_upload block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#on_partial_upload TransferServer#on_partial_upload}
        :param on_upload: on_upload block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#on_upload TransferServer#on_upload}
        '''
        if isinstance(on_partial_upload, dict):
            on_partial_upload = TransferServerWorkflowDetailsOnPartialUpload(**on_partial_upload)
        if isinstance(on_upload, dict):
            on_upload = TransferServerWorkflowDetailsOnUpload(**on_upload)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fe080a7ce823308d1a8bb5bf16a8993adab5b787aeca3ab89fe9dafb24b88f5)
            check_type(argname="argument on_partial_upload", value=on_partial_upload, expected_type=type_hints["on_partial_upload"])
            check_type(argname="argument on_upload", value=on_upload, expected_type=type_hints["on_upload"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if on_partial_upload is not None:
            self._values["on_partial_upload"] = on_partial_upload
        if on_upload is not None:
            self._values["on_upload"] = on_upload

    @builtins.property
    def on_partial_upload(
        self,
    ) -> typing.Optional["TransferServerWorkflowDetailsOnPartialUpload"]:
        '''on_partial_upload block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#on_partial_upload TransferServer#on_partial_upload}
        '''
        result = self._values.get("on_partial_upload")
        return typing.cast(typing.Optional["TransferServerWorkflowDetailsOnPartialUpload"], result)

    @builtins.property
    def on_upload(self) -> typing.Optional["TransferServerWorkflowDetailsOnUpload"]:
        '''on_upload block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#on_upload TransferServer#on_upload}
        '''
        result = self._values.get("on_upload")
        return typing.cast(typing.Optional["TransferServerWorkflowDetailsOnUpload"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferServerWorkflowDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferServer.TransferServerWorkflowDetailsOnPartialUpload",
    jsii_struct_bases=[],
    name_mapping={"execution_role": "executionRole", "workflow_id": "workflowId"},
)
class TransferServerWorkflowDetailsOnPartialUpload:
    def __init__(
        self,
        *,
        execution_role: builtins.str,
        workflow_id: builtins.str,
    ) -> None:
        '''
        :param execution_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#execution_role TransferServer#execution_role}.
        :param workflow_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#workflow_id TransferServer#workflow_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa106988be82ea917962b06855c485b97d1671ac098d3f09a2c3c8d024c3460)
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument workflow_id", value=workflow_id, expected_type=type_hints["workflow_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execution_role": execution_role,
            "workflow_id": workflow_id,
        }

    @builtins.property
    def execution_role(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#execution_role TransferServer#execution_role}.'''
        result = self._values.get("execution_role")
        assert result is not None, "Required property 'execution_role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workflow_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#workflow_id TransferServer#workflow_id}.'''
        result = self._values.get("workflow_id")
        assert result is not None, "Required property 'workflow_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferServerWorkflowDetailsOnPartialUpload(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferServerWorkflowDetailsOnPartialUploadOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferServer.TransferServerWorkflowDetailsOnPartialUploadOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84d2ae5bca86f79962910a8af5ef9d69de2c9a868f0f93e30c9996683ce3a2c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="executionRoleInput")
    def execution_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="workflowIdInput")
    def workflow_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workflowIdInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRole"))

    @execution_role.setter
    def execution_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82da48f45f4bce31c74c791644c14991698ca037c30ff235c32e460c9fef38f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workflowId")
    def workflow_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workflowId"))

    @workflow_id.setter
    def workflow_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bbeae7d6080d14024c73e95c51a0ffe9c4734f998ad70813c0f288adee18e30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workflowId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TransferServerWorkflowDetailsOnPartialUpload]:
        return typing.cast(typing.Optional[TransferServerWorkflowDetailsOnPartialUpload], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferServerWorkflowDetailsOnPartialUpload],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daebe5432eb27d3ea57d66b36de7761d6ef4558a59d0b46540da53e4d7fd580b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.transferServer.TransferServerWorkflowDetailsOnUpload",
    jsii_struct_bases=[],
    name_mapping={"execution_role": "executionRole", "workflow_id": "workflowId"},
)
class TransferServerWorkflowDetailsOnUpload:
    def __init__(
        self,
        *,
        execution_role: builtins.str,
        workflow_id: builtins.str,
    ) -> None:
        '''
        :param execution_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#execution_role TransferServer#execution_role}.
        :param workflow_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#workflow_id TransferServer#workflow_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__994121881cebfec643e5e519e6d3d6aa9dd78c6c8266d1568a730a267924e16d)
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument workflow_id", value=workflow_id, expected_type=type_hints["workflow_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execution_role": execution_role,
            "workflow_id": workflow_id,
        }

    @builtins.property
    def execution_role(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#execution_role TransferServer#execution_role}.'''
        result = self._values.get("execution_role")
        assert result is not None, "Required property 'execution_role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workflow_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#workflow_id TransferServer#workflow_id}.'''
        result = self._values.get("workflow_id")
        assert result is not None, "Required property 'workflow_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransferServerWorkflowDetailsOnUpload(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransferServerWorkflowDetailsOnUploadOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferServer.TransferServerWorkflowDetailsOnUploadOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a86ba507d3f58cda122a197ca8aa1de07432d4df00c731e6a7a8de9976ff8ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="executionRoleInput")
    def execution_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="workflowIdInput")
    def workflow_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workflowIdInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRole"))

    @execution_role.setter
    def execution_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__372f535b6c9466724a086919112c3fa9bd26f484fac995e99832fbe4d46a4773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workflowId")
    def workflow_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workflowId"))

    @workflow_id.setter
    def workflow_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5ada9761204d9ef43dd64afd6cf7b7bf479efcf37f11d5bd35c01875f007638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workflowId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TransferServerWorkflowDetailsOnUpload]:
        return typing.cast(typing.Optional[TransferServerWorkflowDetailsOnUpload], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferServerWorkflowDetailsOnUpload],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b787647b2417165867b1872b4381c6138c4d0ba6360e83cd54d9954cbd75f630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TransferServerWorkflowDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.transferServer.TransferServerWorkflowDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b54283dce83a70bff0ee1ba84fe91811572d0f096996ef7c4474825a19b92ff5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOnPartialUpload")
    def put_on_partial_upload(
        self,
        *,
        execution_role: builtins.str,
        workflow_id: builtins.str,
    ) -> None:
        '''
        :param execution_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#execution_role TransferServer#execution_role}.
        :param workflow_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#workflow_id TransferServer#workflow_id}.
        '''
        value = TransferServerWorkflowDetailsOnPartialUpload(
            execution_role=execution_role, workflow_id=workflow_id
        )

        return typing.cast(None, jsii.invoke(self, "putOnPartialUpload", [value]))

    @jsii.member(jsii_name="putOnUpload")
    def put_on_upload(
        self,
        *,
        execution_role: builtins.str,
        workflow_id: builtins.str,
    ) -> None:
        '''
        :param execution_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#execution_role TransferServer#execution_role}.
        :param workflow_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/transfer_server#workflow_id TransferServer#workflow_id}.
        '''
        value = TransferServerWorkflowDetailsOnUpload(
            execution_role=execution_role, workflow_id=workflow_id
        )

        return typing.cast(None, jsii.invoke(self, "putOnUpload", [value]))

    @jsii.member(jsii_name="resetOnPartialUpload")
    def reset_on_partial_upload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnPartialUpload", []))

    @jsii.member(jsii_name="resetOnUpload")
    def reset_on_upload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnUpload", []))

    @builtins.property
    @jsii.member(jsii_name="onPartialUpload")
    def on_partial_upload(
        self,
    ) -> TransferServerWorkflowDetailsOnPartialUploadOutputReference:
        return typing.cast(TransferServerWorkflowDetailsOnPartialUploadOutputReference, jsii.get(self, "onPartialUpload"))

    @builtins.property
    @jsii.member(jsii_name="onUpload")
    def on_upload(self) -> TransferServerWorkflowDetailsOnUploadOutputReference:
        return typing.cast(TransferServerWorkflowDetailsOnUploadOutputReference, jsii.get(self, "onUpload"))

    @builtins.property
    @jsii.member(jsii_name="onPartialUploadInput")
    def on_partial_upload_input(
        self,
    ) -> typing.Optional[TransferServerWorkflowDetailsOnPartialUpload]:
        return typing.cast(typing.Optional[TransferServerWorkflowDetailsOnPartialUpload], jsii.get(self, "onPartialUploadInput"))

    @builtins.property
    @jsii.member(jsii_name="onUploadInput")
    def on_upload_input(self) -> typing.Optional[TransferServerWorkflowDetailsOnUpload]:
        return typing.cast(typing.Optional[TransferServerWorkflowDetailsOnUpload], jsii.get(self, "onUploadInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TransferServerWorkflowDetails]:
        return typing.cast(typing.Optional[TransferServerWorkflowDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TransferServerWorkflowDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb8170a5cbf6524ff4275178161a53c7846fbe6384557d48440e55a9a55b83d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "TransferServer",
    "TransferServerConfig",
    "TransferServerEndpointDetails",
    "TransferServerEndpointDetailsOutputReference",
    "TransferServerProtocolDetails",
    "TransferServerProtocolDetailsOutputReference",
    "TransferServerS3StorageOptions",
    "TransferServerS3StorageOptionsOutputReference",
    "TransferServerWorkflowDetails",
    "TransferServerWorkflowDetailsOnPartialUpload",
    "TransferServerWorkflowDetailsOnPartialUploadOutputReference",
    "TransferServerWorkflowDetailsOnUpload",
    "TransferServerWorkflowDetailsOnUploadOutputReference",
    "TransferServerWorkflowDetailsOutputReference",
]

publication.publish()

def _typecheckingstub__b07ce2b8386429f1f291351751b79399b69e0014027c3c572d7121a9d5118013(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    certificate: typing.Optional[builtins.str] = None,
    directory_id: typing.Optional[builtins.str] = None,
    domain: typing.Optional[builtins.str] = None,
    endpoint_details: typing.Optional[typing.Union[TransferServerEndpointDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_type: typing.Optional[builtins.str] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    function: typing.Optional[builtins.str] = None,
    host_key: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity_provider_type: typing.Optional[builtins.str] = None,
    invocation_role: typing.Optional[builtins.str] = None,
    logging_role: typing.Optional[builtins.str] = None,
    post_authentication_login_banner: typing.Optional[builtins.str] = None,
    pre_authentication_login_banner: typing.Optional[builtins.str] = None,
    protocol_details: typing.Optional[typing.Union[TransferServerProtocolDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    s3_storage_options: typing.Optional[typing.Union[TransferServerS3StorageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    security_policy_name: typing.Optional[builtins.str] = None,
    sftp_authentication_methods: typing.Optional[builtins.str] = None,
    structured_log_destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    url: typing.Optional[builtins.str] = None,
    workflow_details: typing.Optional[typing.Union[TransferServerWorkflowDetails, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__17bd59aed27bc4e14848794c431d4187e85487f95d72a07786a6a19e574e151c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e908c29a7d52a107a3030f0768d3d2e91ef31ec2f849a714413f16beb1a963(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1909e168849216d8b93017c775bece2feb45bc415fd249a7a0183dafdc698a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8db6038c5c805e737434bfe98f7f9d7bc6f1d635164a85d8204857afdfc09a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf586fdf69308c31a5fdffa68f4015543c4cdf1c9052bf522c315b09c7b123ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc3e90d779bf029e795581bf70c76fa2eb133aa43e80d413e37b32f55ef6863(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0a045101cb2941820b7b544809344635073039583bb38600a663920e8f0b9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d98e9dde5c4cfcf270a5fbbf88a685da1e4c6f03096c360ce17d481701fa198(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d49ae8e144d91d535d8a210cd36c7a73683cac9fec7e9c48c3fda0459124f2b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3788ea02f16031b8bdd8d7dd9d0dde1fc4666062b890cf89ad4b7978c33a7a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ba09b80d64edeac368484a9f6064bd6371b53406d7609251fa6df718a04b3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a80a38a1bfacd42fb61475219472eb6a08f3f09a26904753dc41bb1690c303(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab652dfe080cbbd8b8c953e58d3df102b339302f79f2cca6fee8667967b3908(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9705036070d2d3699c542995cac649ea35c6d031ab02031bb1e297c64b3a0a35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7849fc2bf268dc16784b881c694014faa36d72fcf0b5fbaf139b80ec7b69e791(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__863ae668fa8f6bbdc17eb41247adfdccc4c9e3fd68fc41ac8d4dca74f0a36aee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5117c3c19a6ae1eef21d5fd7cede4469b81fe057b6d490bdd78236e27c0498af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be5cc4862cd276276b8cf11b8ca739ec04974edc7865c43202349047b7e9989f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10dc2590e7058e13f0eee27abbb9483ac196c7353fb2de68c9379f65f680648b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9533cc00b00828d31bcb958197bd4cdf51597ca5a978fc57705e942a6e24e48f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be0dce44937110e96c7ff1b72ae2dba92ccdd60fa022d20898bbc036796e56f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b542f162f7942149431b38d270c4ccbf5c64acf69ac89db689b08426f56b33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd011d1fa7c25e69d821066b7109b8d0c43f0df64afa2085944f8410427680e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    certificate: typing.Optional[builtins.str] = None,
    directory_id: typing.Optional[builtins.str] = None,
    domain: typing.Optional[builtins.str] = None,
    endpoint_details: typing.Optional[typing.Union[TransferServerEndpointDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_type: typing.Optional[builtins.str] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    function: typing.Optional[builtins.str] = None,
    host_key: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity_provider_type: typing.Optional[builtins.str] = None,
    invocation_role: typing.Optional[builtins.str] = None,
    logging_role: typing.Optional[builtins.str] = None,
    post_authentication_login_banner: typing.Optional[builtins.str] = None,
    pre_authentication_login_banner: typing.Optional[builtins.str] = None,
    protocol_details: typing.Optional[typing.Union[TransferServerProtocolDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    s3_storage_options: typing.Optional[typing.Union[TransferServerS3StorageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    security_policy_name: typing.Optional[builtins.str] = None,
    sftp_authentication_methods: typing.Optional[builtins.str] = None,
    structured_log_destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    url: typing.Optional[builtins.str] = None,
    workflow_details: typing.Optional[typing.Union[TransferServerWorkflowDetails, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b895c234d48390c17a011cc05d71587f3c0d1074ca5768692cd34bf830f2aa(
    *,
    address_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_endpoint_id: typing.Optional[builtins.str] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec974208dc5ff7ae391a974fd6c089cbb5a7163e39498ce912313707b09c3ab2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b99a6c4c023258199fd55a1ac29fb4acbbf0cf380fd5f8cd48dbd47bc7cea3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c495914791016e02f502ab73e9ccc33e72355ace914cab17e4bfddabb4ff773(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e46671076ff4b86bb9104fefc7e871d44337059908dfaafd2f624f85a85dd14(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7202a768803e2d9907a2ae9b4c69b6f2ad82d77ed6f984cf0ae98b4cc53680b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692e842178056a71ddde6862b4fa13fb6c0009a55cd42416f0ee81273f6edcb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2333673614215d8c687d7b12ec474eecda65b7301f33f040de8fe11745654cac(
    value: typing.Optional[TransferServerEndpointDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a80b1b9dc95bfc9382eca94220c0b2ab338cb22bdace013cae5bb7380a49da(
    *,
    as2_transports: typing.Optional[typing.Sequence[builtins.str]] = None,
    passive_ip: typing.Optional[builtins.str] = None,
    set_stat_option: typing.Optional[builtins.str] = None,
    tls_session_resumption_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6978767dc0d3223f408af12eeaf4e963aadf3bbad4b7f331dae06bf1277671d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5776e92a973662d3277bdb03790c73332c7f9cde938fd169674c8357a66af30c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b088bafdea41cf8df31dffffff355b83f43c226c768f63024fa6eedbd2ae5b17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62aceb0d4ea2dd430ef8b384bd48089fb69ae253158a08ae2e5f3d643f4dd2a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bad3d6603036a658fcbc6bc9e3eaaaa83aa9f1dcd08b5be12fd48d2e916f42b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c0b289ad0d0cf9713ae74872e05878a6ba15be6c5ca0b15c3defb1f6531b2d(
    value: typing.Optional[TransferServerProtocolDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da88268872492087126b4ce75787a816a61d9297329744c83e042dec11e38359(
    *,
    directory_listing_optimization: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e5d94d6dcc93feca726bef553f18c2f188165aaaf14a1cb570a1fbd66a9c7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bcf3fb3f367063bc59259d5c2f641e579b4fb4650549b0b36e917813ae26528(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c52f93201a3533a23a09f6e28a628933bd0c78bd89ce15e1000be0b681dcffa(
    value: typing.Optional[TransferServerS3StorageOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe080a7ce823308d1a8bb5bf16a8993adab5b787aeca3ab89fe9dafb24b88f5(
    *,
    on_partial_upload: typing.Optional[typing.Union[TransferServerWorkflowDetailsOnPartialUpload, typing.Dict[builtins.str, typing.Any]]] = None,
    on_upload: typing.Optional[typing.Union[TransferServerWorkflowDetailsOnUpload, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa106988be82ea917962b06855c485b97d1671ac098d3f09a2c3c8d024c3460(
    *,
    execution_role: builtins.str,
    workflow_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d2ae5bca86f79962910a8af5ef9d69de2c9a868f0f93e30c9996683ce3a2c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82da48f45f4bce31c74c791644c14991698ca037c30ff235c32e460c9fef38f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbeae7d6080d14024c73e95c51a0ffe9c4734f998ad70813c0f288adee18e30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daebe5432eb27d3ea57d66b36de7761d6ef4558a59d0b46540da53e4d7fd580b(
    value: typing.Optional[TransferServerWorkflowDetailsOnPartialUpload],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__994121881cebfec643e5e519e6d3d6aa9dd78c6c8266d1568a730a267924e16d(
    *,
    execution_role: builtins.str,
    workflow_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a86ba507d3f58cda122a197ca8aa1de07432d4df00c731e6a7a8de9976ff8ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__372f535b6c9466724a086919112c3fa9bd26f484fac995e99832fbe4d46a4773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5ada9761204d9ef43dd64afd6cf7b7bf479efcf37f11d5bd35c01875f007638(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b787647b2417165867b1872b4381c6138c4d0ba6360e83cd54d9954cbd75f630(
    value: typing.Optional[TransferServerWorkflowDetailsOnUpload],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54283dce83a70bff0ee1ba84fe91811572d0f096996ef7c4474825a19b92ff5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb8170a5cbf6524ff4275178161a53c7846fbe6384557d48440e55a9a55b83d(
    value: typing.Optional[TransferServerWorkflowDetails],
) -> None:
    """Type checking stubs"""
    pass
