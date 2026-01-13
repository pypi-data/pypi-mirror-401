r'''
# `tls_self_signed_cert`

Refer to the Terraform Registry for docs: [`tls_self_signed_cert`](https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert).
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


class SelfSignedCert(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-tls.selfSignedCert.SelfSignedCert",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert tls_self_signed_cert}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        allowed_uses: typing.Sequence[builtins.str],
        private_key_pem: builtins.str,
        validity_period_hours: jsii.Number,
        dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        early_renewal_hours: typing.Optional[jsii.Number] = None,
        ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        is_ca_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        set_authority_key_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        set_subject_key_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subject: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SelfSignedCertSubject", typing.Dict[builtins.str, typing.Any]]]]] = None,
        uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert tls_self_signed_cert} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param allowed_uses: List of key usages allowed for the issued certificate. Values are defined in `RFC 5280 <https://datatracker.ietf.org/doc/html/rfc5280>`_ and combine flags defined by both `Key Usages <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.3>`_ and `Extended Key Usages <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.12>`_. Accepted values: ``any_extended``, ``cert_signing``, ``client_auth``, ``code_signing``, ``content_commitment``, ``crl_signing``, ``data_encipherment``, ``decipher_only``, ``digital_signature``, ``email_protection``, ``encipher_only``, ``ipsec_end_system``, ``ipsec_tunnel``, ``ipsec_user``, ``key_agreement``, ``key_encipherment``, ``microsoft_commercial_code_signing``, ``microsoft_kernel_code_signing``, ``microsoft_server_gated_crypto``, ``netscape_server_gated_crypto``, ``ocsp_signing``, ``server_auth``, ``timestamping``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#allowed_uses SelfSignedCert#allowed_uses}
        :param private_key_pem: Private key in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format, that the certificate will belong to. This can be read from a separate file using the ```file`` <https://www.terraform.io/language/functions/file>`_ interpolation function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#private_key_pem SelfSignedCert#private_key_pem}
        :param validity_period_hours: Number of hours, after initial issuing, that the certificate will remain valid for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#validity_period_hours SelfSignedCert#validity_period_hours}
        :param dns_names: List of DNS names for which a certificate is being requested (i.e. certificate subjects). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#dns_names SelfSignedCert#dns_names}
        :param early_renewal_hours: The resource will consider the certificate to have expired the given number of hours before its actual expiry time. This can be useful to deploy an updated certificate in advance of the expiration of the current certificate. However, the old certificate remains valid until its true expiration time, since this resource does not (and cannot) support certificate revocation. Also, this advance update can only be performed should the Terraform configuration be applied during the early renewal period. (default: ``0``) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#early_renewal_hours SelfSignedCert#early_renewal_hours}
        :param ip_addresses: List of IP addresses for which a certificate is being requested (i.e. certificate subjects). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#ip_addresses SelfSignedCert#ip_addresses}
        :param is_ca_certificate: Is the generated certificate representing a Certificate Authority (CA) (default: ``false``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#is_ca_certificate SelfSignedCert#is_ca_certificate}
        :param set_authority_key_id: Should the generated certificate include an `authority key identifier <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.1>`_: for self-signed certificates this is the same value as the `subject key identifier <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.2>`_ (default: ``false``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#set_authority_key_id SelfSignedCert#set_authority_key_id}
        :param set_subject_key_id: Should the generated certificate include a `subject key identifier <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.2>`_ (default: ``false``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#set_subject_key_id SelfSignedCert#set_subject_key_id}
        :param subject: subject block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#subject SelfSignedCert#subject}
        :param uris: List of URIs for which a certificate is being requested (i.e. certificate subjects). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#uris SelfSignedCert#uris}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44d310a6ae1eb0acee8d0d9a73b9a886c89dcd321df0b62c8e0fed7067d8c823)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = SelfSignedCertConfig(
            allowed_uses=allowed_uses,
            private_key_pem=private_key_pem,
            validity_period_hours=validity_period_hours,
            dns_names=dns_names,
            early_renewal_hours=early_renewal_hours,
            ip_addresses=ip_addresses,
            is_ca_certificate=is_ca_certificate,
            set_authority_key_id=set_authority_key_id,
            set_subject_key_id=set_subject_key_id,
            subject=subject,
            uris=uris,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a SelfSignedCert resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SelfSignedCert to import.
        :param import_from_id: The id of the existing SelfSignedCert that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SelfSignedCert to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__058da4162092d27fdd3dcccaf3ad2a9815da1b25bd7457630b91a95fff1ad999)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSubject")
    def put_subject(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SelfSignedCertSubject", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dee79ff6977c8d37eabfc26afc7676711be6c58a005560ba7912e5f6ae19806a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSubject", [value]))

    @jsii.member(jsii_name="resetDnsNames")
    def reset_dns_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsNames", []))

    @jsii.member(jsii_name="resetEarlyRenewalHours")
    def reset_early_renewal_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEarlyRenewalHours", []))

    @jsii.member(jsii_name="resetIpAddresses")
    def reset_ip_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddresses", []))

    @jsii.member(jsii_name="resetIsCaCertificate")
    def reset_is_ca_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsCaCertificate", []))

    @jsii.member(jsii_name="resetSetAuthorityKeyId")
    def reset_set_authority_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSetAuthorityKeyId", []))

    @jsii.member(jsii_name="resetSetSubjectKeyId")
    def reset_set_subject_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSetSubjectKeyId", []))

    @jsii.member(jsii_name="resetSubject")
    def reset_subject(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubject", []))

    @jsii.member(jsii_name="resetUris")
    def reset_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUris", []))

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
    @jsii.member(jsii_name="certPem")
    def cert_pem(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certPem"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="keyAlgorithm")
    def key_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyAlgorithm"))

    @builtins.property
    @jsii.member(jsii_name="readyForRenewal")
    def ready_for_renewal(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "readyForRenewal"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> "SelfSignedCertSubjectList":
        return typing.cast("SelfSignedCertSubjectList", jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="validityEndTime")
    def validity_end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "validityEndTime"))

    @builtins.property
    @jsii.member(jsii_name="validityStartTime")
    def validity_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "validityStartTime"))

    @builtins.property
    @jsii.member(jsii_name="allowedUsesInput")
    def allowed_uses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedUsesInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsNamesInput")
    def dns_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dnsNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="earlyRenewalHoursInput")
    def early_renewal_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "earlyRenewalHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressesInput")
    def ip_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="isCaCertificateInput")
    def is_ca_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isCaCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyPemInput")
    def private_key_pem_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyPemInput"))

    @builtins.property
    @jsii.member(jsii_name="setAuthorityKeyIdInput")
    def set_authority_key_id_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "setAuthorityKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="setSubjectKeyIdInput")
    def set_subject_key_id_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "setSubjectKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SelfSignedCertSubject"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SelfSignedCertSubject"]]], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="urisInput")
    def uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "urisInput"))

    @builtins.property
    @jsii.member(jsii_name="validityPeriodHoursInput")
    def validity_period_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "validityPeriodHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedUses")
    def allowed_uses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedUses"))

    @allowed_uses.setter
    def allowed_uses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beeb19f829b8166b5a7a33379b7c3f1b5be62997362b46fddfc9999451578176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedUses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsNames")
    def dns_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsNames"))

    @dns_names.setter
    def dns_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7429702cd7eaa312d3dd778aef0f8dd71fa66c4db3040c34f3dd225caaf1d790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="earlyRenewalHours")
    def early_renewal_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "earlyRenewalHours"))

    @early_renewal_hours.setter
    def early_renewal_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e02997bd28045ef3d59a0a35e85bd6792889ccf42c2ba68c187f4a990a778dfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "earlyRenewalHours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddresses"))

    @ip_addresses.setter
    def ip_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33cae0e3e4e4b4f724f2a1e698ceb2b939c850d21295aada50bb70a6ad3ed15b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isCaCertificate")
    def is_ca_certificate(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isCaCertificate"))

    @is_ca_certificate.setter
    def is_ca_certificate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__765eb0dbfac13115a7d52fd24d8e418d0704635ffac61bdaafa8611dbd137511)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isCaCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKeyPem")
    def private_key_pem(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKeyPem"))

    @private_key_pem.setter
    def private_key_pem(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60211a60476ab32491c7d7dfed366325c3b787f7442bc771b0431c74415e8146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeyPem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="setAuthorityKeyId")
    def set_authority_key_id(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "setAuthorityKeyId"))

    @set_authority_key_id.setter
    def set_authority_key_id(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da3c8114345b0484430c0ba1f4a436ac8bf87898c81424f2fa0b40b444a03a12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "setAuthorityKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="setSubjectKeyId")
    def set_subject_key_id(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "setSubjectKeyId"))

    @set_subject_key_id.setter
    def set_subject_key_id(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b589a076469f8ea72430a9dd3b0d0f48ca1a2964ed05742fc7839c20324842b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "setSubjectKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uris")
    def uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "uris"))

    @uris.setter
    def uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc440e92ec04a993b03fd894e97c90521c65af45deaa52b7ecb5152e236ae3a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validityPeriodHours")
    def validity_period_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "validityPeriodHours"))

    @validity_period_hours.setter
    def validity_period_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b7558a3f755c75235ab266d96e9d9db8d6491a5a771a6e5873adb182ee9f405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validityPeriodHours", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-tls.selfSignedCert.SelfSignedCertConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "allowed_uses": "allowedUses",
        "private_key_pem": "privateKeyPem",
        "validity_period_hours": "validityPeriodHours",
        "dns_names": "dnsNames",
        "early_renewal_hours": "earlyRenewalHours",
        "ip_addresses": "ipAddresses",
        "is_ca_certificate": "isCaCertificate",
        "set_authority_key_id": "setAuthorityKeyId",
        "set_subject_key_id": "setSubjectKeyId",
        "subject": "subject",
        "uris": "uris",
    },
)
class SelfSignedCertConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        allowed_uses: typing.Sequence[builtins.str],
        private_key_pem: builtins.str,
        validity_period_hours: jsii.Number,
        dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        early_renewal_hours: typing.Optional[jsii.Number] = None,
        ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        is_ca_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        set_authority_key_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        set_subject_key_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subject: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SelfSignedCertSubject", typing.Dict[builtins.str, typing.Any]]]]] = None,
        uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param allowed_uses: List of key usages allowed for the issued certificate. Values are defined in `RFC 5280 <https://datatracker.ietf.org/doc/html/rfc5280>`_ and combine flags defined by both `Key Usages <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.3>`_ and `Extended Key Usages <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.12>`_. Accepted values: ``any_extended``, ``cert_signing``, ``client_auth``, ``code_signing``, ``content_commitment``, ``crl_signing``, ``data_encipherment``, ``decipher_only``, ``digital_signature``, ``email_protection``, ``encipher_only``, ``ipsec_end_system``, ``ipsec_tunnel``, ``ipsec_user``, ``key_agreement``, ``key_encipherment``, ``microsoft_commercial_code_signing``, ``microsoft_kernel_code_signing``, ``microsoft_server_gated_crypto``, ``netscape_server_gated_crypto``, ``ocsp_signing``, ``server_auth``, ``timestamping``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#allowed_uses SelfSignedCert#allowed_uses}
        :param private_key_pem: Private key in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format, that the certificate will belong to. This can be read from a separate file using the ```file`` <https://www.terraform.io/language/functions/file>`_ interpolation function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#private_key_pem SelfSignedCert#private_key_pem}
        :param validity_period_hours: Number of hours, after initial issuing, that the certificate will remain valid for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#validity_period_hours SelfSignedCert#validity_period_hours}
        :param dns_names: List of DNS names for which a certificate is being requested (i.e. certificate subjects). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#dns_names SelfSignedCert#dns_names}
        :param early_renewal_hours: The resource will consider the certificate to have expired the given number of hours before its actual expiry time. This can be useful to deploy an updated certificate in advance of the expiration of the current certificate. However, the old certificate remains valid until its true expiration time, since this resource does not (and cannot) support certificate revocation. Also, this advance update can only be performed should the Terraform configuration be applied during the early renewal period. (default: ``0``) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#early_renewal_hours SelfSignedCert#early_renewal_hours}
        :param ip_addresses: List of IP addresses for which a certificate is being requested (i.e. certificate subjects). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#ip_addresses SelfSignedCert#ip_addresses}
        :param is_ca_certificate: Is the generated certificate representing a Certificate Authority (CA) (default: ``false``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#is_ca_certificate SelfSignedCert#is_ca_certificate}
        :param set_authority_key_id: Should the generated certificate include an `authority key identifier <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.1>`_: for self-signed certificates this is the same value as the `subject key identifier <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.2>`_ (default: ``false``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#set_authority_key_id SelfSignedCert#set_authority_key_id}
        :param set_subject_key_id: Should the generated certificate include a `subject key identifier <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.2>`_ (default: ``false``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#set_subject_key_id SelfSignedCert#set_subject_key_id}
        :param subject: subject block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#subject SelfSignedCert#subject}
        :param uris: List of URIs for which a certificate is being requested (i.e. certificate subjects). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#uris SelfSignedCert#uris}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52085aa6f8bac0e6156cc1edbf19666615eb093e3c320a9ccc0157b4bc3ce672)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument allowed_uses", value=allowed_uses, expected_type=type_hints["allowed_uses"])
            check_type(argname="argument private_key_pem", value=private_key_pem, expected_type=type_hints["private_key_pem"])
            check_type(argname="argument validity_period_hours", value=validity_period_hours, expected_type=type_hints["validity_period_hours"])
            check_type(argname="argument dns_names", value=dns_names, expected_type=type_hints["dns_names"])
            check_type(argname="argument early_renewal_hours", value=early_renewal_hours, expected_type=type_hints["early_renewal_hours"])
            check_type(argname="argument ip_addresses", value=ip_addresses, expected_type=type_hints["ip_addresses"])
            check_type(argname="argument is_ca_certificate", value=is_ca_certificate, expected_type=type_hints["is_ca_certificate"])
            check_type(argname="argument set_authority_key_id", value=set_authority_key_id, expected_type=type_hints["set_authority_key_id"])
            check_type(argname="argument set_subject_key_id", value=set_subject_key_id, expected_type=type_hints["set_subject_key_id"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument uris", value=uris, expected_type=type_hints["uris"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_uses": allowed_uses,
            "private_key_pem": private_key_pem,
            "validity_period_hours": validity_period_hours,
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
        if dns_names is not None:
            self._values["dns_names"] = dns_names
        if early_renewal_hours is not None:
            self._values["early_renewal_hours"] = early_renewal_hours
        if ip_addresses is not None:
            self._values["ip_addresses"] = ip_addresses
        if is_ca_certificate is not None:
            self._values["is_ca_certificate"] = is_ca_certificate
        if set_authority_key_id is not None:
            self._values["set_authority_key_id"] = set_authority_key_id
        if set_subject_key_id is not None:
            self._values["set_subject_key_id"] = set_subject_key_id
        if subject is not None:
            self._values["subject"] = subject
        if uris is not None:
            self._values["uris"] = uris

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
    def allowed_uses(self) -> typing.List[builtins.str]:
        '''List of key usages allowed for the issued certificate.

        Values are defined in `RFC 5280 <https://datatracker.ietf.org/doc/html/rfc5280>`_ and combine flags defined by both `Key Usages <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.3>`_ and `Extended Key Usages <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.12>`_. Accepted values: ``any_extended``, ``cert_signing``, ``client_auth``, ``code_signing``, ``content_commitment``, ``crl_signing``, ``data_encipherment``, ``decipher_only``, ``digital_signature``, ``email_protection``, ``encipher_only``, ``ipsec_end_system``, ``ipsec_tunnel``, ``ipsec_user``, ``key_agreement``, ``key_encipherment``, ``microsoft_commercial_code_signing``, ``microsoft_kernel_code_signing``, ``microsoft_server_gated_crypto``, ``netscape_server_gated_crypto``, ``ocsp_signing``, ``server_auth``, ``timestamping``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#allowed_uses SelfSignedCert#allowed_uses}
        '''
        result = self._values.get("allowed_uses")
        assert result is not None, "Required property 'allowed_uses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def private_key_pem(self) -> builtins.str:
        '''Private key in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format, that the certificate will belong to. This can be read from a separate file using the ```file`` <https://www.terraform.io/language/functions/file>`_ interpolation function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#private_key_pem SelfSignedCert#private_key_pem}
        '''
        result = self._values.get("private_key_pem")
        assert result is not None, "Required property 'private_key_pem' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def validity_period_hours(self) -> jsii.Number:
        '''Number of hours, after initial issuing, that the certificate will remain valid for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#validity_period_hours SelfSignedCert#validity_period_hours}
        '''
        result = self._values.get("validity_period_hours")
        assert result is not None, "Required property 'validity_period_hours' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def dns_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of DNS names for which a certificate is being requested (i.e. certificate subjects).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#dns_names SelfSignedCert#dns_names}
        '''
        result = self._values.get("dns_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def early_renewal_hours(self) -> typing.Optional[jsii.Number]:
        '''The resource will consider the certificate to have expired the given number of hours before its actual expiry time.

        This can be useful to deploy an updated certificate in advance of the expiration of the current certificate. However, the old certificate remains valid until its true expiration time, since this resource does not (and cannot) support certificate revocation. Also, this advance update can only be performed should the Terraform configuration be applied during the early renewal period. (default: ``0``)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#early_renewal_hours SelfSignedCert#early_renewal_hours}
        '''
        result = self._values.get("early_renewal_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ip_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of IP addresses for which a certificate is being requested (i.e. certificate subjects).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#ip_addresses SelfSignedCert#ip_addresses}
        '''
        result = self._values.get("ip_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def is_ca_certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Is the generated certificate representing a Certificate Authority (CA) (default: ``false``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#is_ca_certificate SelfSignedCert#is_ca_certificate}
        '''
        result = self._values.get("is_ca_certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def set_authority_key_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the generated certificate include an `authority key identifier <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.1>`_: for self-signed certificates this is the same value as the `subject key identifier <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.2>`_ (default: ``false``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#set_authority_key_id SelfSignedCert#set_authority_key_id}
        '''
        result = self._values.get("set_authority_key_id")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def set_subject_key_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the generated certificate include a `subject key identifier <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.2>`_ (default: ``false``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#set_subject_key_id SelfSignedCert#set_subject_key_id}
        '''
        result = self._values.get("set_subject_key_id")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def subject(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SelfSignedCertSubject"]]]:
        '''subject block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#subject SelfSignedCert#subject}
        '''
        result = self._values.get("subject")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SelfSignedCertSubject"]]], result)

    @builtins.property
    def uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of URIs for which a certificate is being requested (i.e. certificate subjects).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#uris SelfSignedCert#uris}
        '''
        result = self._values.get("uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SelfSignedCertConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-tls.selfSignedCert.SelfSignedCertSubject",
    jsii_struct_bases=[],
    name_mapping={
        "common_name": "commonName",
        "country": "country",
        "email_address": "emailAddress",
        "locality": "locality",
        "organization": "organization",
        "organizational_unit": "organizationalUnit",
        "postal_code": "postalCode",
        "province": "province",
        "serial_number": "serialNumber",
        "street_address": "streetAddress",
    },
)
class SelfSignedCertSubject:
    def __init__(
        self,
        *,
        common_name: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        email_address: typing.Optional[builtins.str] = None,
        locality: typing.Optional[builtins.str] = None,
        organization: typing.Optional[builtins.str] = None,
        organizational_unit: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        serial_number: typing.Optional[builtins.str] = None,
        street_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param common_name: Distinguished name: ``CN``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#common_name SelfSignedCert#common_name}
        :param country: Distinguished name: ``C``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#country SelfSignedCert#country}
        :param email_address: ASN.1 Object Identifier (OID): ``1.2.840.113549.1.9.1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#email_address SelfSignedCert#email_address}
        :param locality: Distinguished name: ``L``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#locality SelfSignedCert#locality}
        :param organization: Distinguished name: ``O``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#organization SelfSignedCert#organization}
        :param organizational_unit: Distinguished name: ``OU``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#organizational_unit SelfSignedCert#organizational_unit}
        :param postal_code: Distinguished name: ``PC``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#postal_code SelfSignedCert#postal_code}
        :param province: Distinguished name: ``ST``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#province SelfSignedCert#province}
        :param serial_number: Distinguished name: ``SERIALNUMBER``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#serial_number SelfSignedCert#serial_number}
        :param street_address: Distinguished name: ``STREET``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#street_address SelfSignedCert#street_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e766cffa73b8876527c1b32e3765da12f6535a68f18c0032fff6ab981e4d0554)
            check_type(argname="argument common_name", value=common_name, expected_type=type_hints["common_name"])
            check_type(argname="argument country", value=country, expected_type=type_hints["country"])
            check_type(argname="argument email_address", value=email_address, expected_type=type_hints["email_address"])
            check_type(argname="argument locality", value=locality, expected_type=type_hints["locality"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument organizational_unit", value=organizational_unit, expected_type=type_hints["organizational_unit"])
            check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
            check_type(argname="argument province", value=province, expected_type=type_hints["province"])
            check_type(argname="argument serial_number", value=serial_number, expected_type=type_hints["serial_number"])
            check_type(argname="argument street_address", value=street_address, expected_type=type_hints["street_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if common_name is not None:
            self._values["common_name"] = common_name
        if country is not None:
            self._values["country"] = country
        if email_address is not None:
            self._values["email_address"] = email_address
        if locality is not None:
            self._values["locality"] = locality
        if organization is not None:
            self._values["organization"] = organization
        if organizational_unit is not None:
            self._values["organizational_unit"] = organizational_unit
        if postal_code is not None:
            self._values["postal_code"] = postal_code
        if province is not None:
            self._values["province"] = province
        if serial_number is not None:
            self._values["serial_number"] = serial_number
        if street_address is not None:
            self._values["street_address"] = street_address

    @builtins.property
    def common_name(self) -> typing.Optional[builtins.str]:
        '''Distinguished name: ``CN``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#common_name SelfSignedCert#common_name}
        '''
        result = self._values.get("common_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country(self) -> typing.Optional[builtins.str]:
        '''Distinguished name: ``C``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#country SelfSignedCert#country}
        '''
        result = self._values.get("country")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_address(self) -> typing.Optional[builtins.str]:
        '''ASN.1 Object Identifier (OID): ``1.2.840.113549.1.9.1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#email_address SelfSignedCert#email_address}
        '''
        result = self._values.get("email_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locality(self) -> typing.Optional[builtins.str]:
        '''Distinguished name: ``L``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#locality SelfSignedCert#locality}
        '''
        result = self._values.get("locality")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization(self) -> typing.Optional[builtins.str]:
        '''Distinguished name: ``O``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#organization SelfSignedCert#organization}
        '''
        result = self._values.get("organization")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organizational_unit(self) -> typing.Optional[builtins.str]:
        '''Distinguished name: ``OU``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#organizational_unit SelfSignedCert#organizational_unit}
        '''
        result = self._values.get("organizational_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''Distinguished name: ``PC``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#postal_code SelfSignedCert#postal_code}
        '''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def province(self) -> typing.Optional[builtins.str]:
        '''Distinguished name: ``ST``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#province SelfSignedCert#province}
        '''
        result = self._values.get("province")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serial_number(self) -> typing.Optional[builtins.str]:
        '''Distinguished name: ``SERIALNUMBER``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#serial_number SelfSignedCert#serial_number}
        '''
        result = self._values.get("serial_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def street_address(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Distinguished name: ``STREET``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/self_signed_cert#street_address SelfSignedCert#street_address}
        '''
        result = self._values.get("street_address")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SelfSignedCertSubject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SelfSignedCertSubjectList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-tls.selfSignedCert.SelfSignedCertSubjectList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8e7566cd38e62758f0526f5fb6a4397553e03308f227ba9d803696e57f1392f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SelfSignedCertSubjectOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6180bbbcbac5b323559a7f0a26efc072b1b8499f96431f3a2df0de21cfb9442d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SelfSignedCertSubjectOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7657acec339691e1454a2b5493bd42594bc91d97a4e5a5f478bf5d3600540254)
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
            type_hints = typing.get_type_hints(_typecheckingstub__acf943a4104b9d70ef5e5e33ab726ddecf044cde9d67017f40ffd49d89e50b31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9687af1d9de7c1d04278ef920984c039407560e48ef0c13cf9f9cf8b525f86d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SelfSignedCertSubject]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SelfSignedCertSubject]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SelfSignedCertSubject]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39ca48809613a765f5c06538e89885d092eb7c338993613c83d3e1f8a5f11ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SelfSignedCertSubjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-tls.selfSignedCert.SelfSignedCertSubjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c14c6926b3afb95ebdde81f6e762e622fa466838fd1d6d3f99f2c7820edc572)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCommonName")
    def reset_common_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommonName", []))

    @jsii.member(jsii_name="resetCountry")
    def reset_country(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountry", []))

    @jsii.member(jsii_name="resetEmailAddress")
    def reset_email_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailAddress", []))

    @jsii.member(jsii_name="resetLocality")
    def reset_locality(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocality", []))

    @jsii.member(jsii_name="resetOrganization")
    def reset_organization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganization", []))

    @jsii.member(jsii_name="resetOrganizationalUnit")
    def reset_organizational_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationalUnit", []))

    @jsii.member(jsii_name="resetPostalCode")
    def reset_postal_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostalCode", []))

    @jsii.member(jsii_name="resetProvince")
    def reset_province(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvince", []))

    @jsii.member(jsii_name="resetSerialNumber")
    def reset_serial_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSerialNumber", []))

    @jsii.member(jsii_name="resetStreetAddress")
    def reset_street_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStreetAddress", []))

    @builtins.property
    @jsii.member(jsii_name="commonNameInput")
    def common_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commonNameInput"))

    @builtins.property
    @jsii.member(jsii_name="countryInput")
    def country_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAddressInput")
    def email_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="localityInput")
    def locality_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localityInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationalUnitInput")
    def organizational_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property
    @jsii.member(jsii_name="postalCodeInput")
    def postal_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postalCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="provinceInput")
    def province_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provinceInput"))

    @builtins.property
    @jsii.member(jsii_name="serialNumberInput")
    def serial_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serialNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="streetAddressInput")
    def street_address_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "streetAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="commonName")
    def common_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commonName"))

    @common_name.setter
    def common_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84ed1e850caa81099c0325eda562d796c7f856c0ba3904738732ccb4447ec10f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commonName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="country")
    def country(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "country"))

    @country.setter
    def country(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2de73a5ad3521da04a5cbb03c9b8c8d056515139105fa49d70bb0a74896967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "country", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailAddress")
    def email_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailAddress"))

    @email_address.setter
    def email_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__302eea5ef83d56695be8fc312178b81d18a938345e3dd671567e36769a769a48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locality")
    def locality(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locality"))

    @locality.setter
    def locality(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19013c6886518c849e691a963449aa9dffe27ec0b7fd1d1d6eeb504060bd64cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locality", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a0ab3f3d8e398723ceb1ec475cf56c35f50d42440ee775aac96c93a4e24f96a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationalUnit")
    def organizational_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationalUnit"))

    @organizational_unit.setter
    def organizational_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07ca5f83058fd18a284cb6f56c79df2b0a9502b5f8734bc721d9eb79d4cbc2d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bcb8fc5348acd2ba42ce7c1f1729d2862ef611617e7186c1d9bf8b7ca4a5df0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="province")
    def province(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "province"))

    @province.setter
    def province(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e87e98fa9a65c847fa7c25e3fcd705ada445b36b8b82879b3860bd52b120d8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "province", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serialNumber")
    def serial_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serialNumber"))

    @serial_number.setter
    def serial_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70f79dedc28e8f1c0abaf40c08b09478a1361a9ac2a456224d02b077cb3d2a4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serialNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streetAddress")
    def street_address(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "streetAddress"))

    @street_address.setter
    def street_address(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__facc3614d25deb386aa62e329b9e8a716f42868f58c4d03425277c8408bbfab1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streetAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SelfSignedCertSubject]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SelfSignedCertSubject]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SelfSignedCertSubject]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa56837339267dfd7d08ab9585ec0fd89945ce53b8a0b0bcf0975abb24459fd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SelfSignedCert",
    "SelfSignedCertConfig",
    "SelfSignedCertSubject",
    "SelfSignedCertSubjectList",
    "SelfSignedCertSubjectOutputReference",
]

publication.publish()

def _typecheckingstub__44d310a6ae1eb0acee8d0d9a73b9a886c89dcd321df0b62c8e0fed7067d8c823(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allowed_uses: typing.Sequence[builtins.str],
    private_key_pem: builtins.str,
    validity_period_hours: jsii.Number,
    dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    early_renewal_hours: typing.Optional[jsii.Number] = None,
    ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    is_ca_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    set_authority_key_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    set_subject_key_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subject: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SelfSignedCertSubject, typing.Dict[builtins.str, typing.Any]]]]] = None,
    uris: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__058da4162092d27fdd3dcccaf3ad2a9815da1b25bd7457630b91a95fff1ad999(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee79ff6977c8d37eabfc26afc7676711be6c58a005560ba7912e5f6ae19806a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SelfSignedCertSubject, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beeb19f829b8166b5a7a33379b7c3f1b5be62997362b46fddfc9999451578176(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7429702cd7eaa312d3dd778aef0f8dd71fa66c4db3040c34f3dd225caaf1d790(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02997bd28045ef3d59a0a35e85bd6792889ccf42c2ba68c187f4a990a778dfd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33cae0e3e4e4b4f724f2a1e698ceb2b939c850d21295aada50bb70a6ad3ed15b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765eb0dbfac13115a7d52fd24d8e418d0704635ffac61bdaafa8611dbd137511(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60211a60476ab32491c7d7dfed366325c3b787f7442bc771b0431c74415e8146(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da3c8114345b0484430c0ba1f4a436ac8bf87898c81424f2fa0b40b444a03a12(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b589a076469f8ea72430a9dd3b0d0f48ca1a2964ed05742fc7839c20324842b3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc440e92ec04a993b03fd894e97c90521c65af45deaa52b7ecb5152e236ae3a7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7558a3f755c75235ab266d96e9d9db8d6491a5a771a6e5873adb182ee9f405(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52085aa6f8bac0e6156cc1edbf19666615eb093e3c320a9ccc0157b4bc3ce672(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allowed_uses: typing.Sequence[builtins.str],
    private_key_pem: builtins.str,
    validity_period_hours: jsii.Number,
    dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    early_renewal_hours: typing.Optional[jsii.Number] = None,
    ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    is_ca_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    set_authority_key_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    set_subject_key_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subject: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SelfSignedCertSubject, typing.Dict[builtins.str, typing.Any]]]]] = None,
    uris: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e766cffa73b8876527c1b32e3765da12f6535a68f18c0032fff6ab981e4d0554(
    *,
    common_name: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    email_address: typing.Optional[builtins.str] = None,
    locality: typing.Optional[builtins.str] = None,
    organization: typing.Optional[builtins.str] = None,
    organizational_unit: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    province: typing.Optional[builtins.str] = None,
    serial_number: typing.Optional[builtins.str] = None,
    street_address: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e7566cd38e62758f0526f5fb6a4397553e03308f227ba9d803696e57f1392f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6180bbbcbac5b323559a7f0a26efc072b1b8499f96431f3a2df0de21cfb9442d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7657acec339691e1454a2b5493bd42594bc91d97a4e5a5f478bf5d3600540254(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf943a4104b9d70ef5e5e33ab726ddecf044cde9d67017f40ffd49d89e50b31(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9687af1d9de7c1d04278ef920984c039407560e48ef0c13cf9f9cf8b525f86d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39ca48809613a765f5c06538e89885d092eb7c338993613c83d3e1f8a5f11ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SelfSignedCertSubject]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c14c6926b3afb95ebdde81f6e762e622fa466838fd1d6d3f99f2c7820edc572(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ed1e850caa81099c0325eda562d796c7f856c0ba3904738732ccb4447ec10f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2de73a5ad3521da04a5cbb03c9b8c8d056515139105fa49d70bb0a74896967(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__302eea5ef83d56695be8fc312178b81d18a938345e3dd671567e36769a769a48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19013c6886518c849e691a963449aa9dffe27ec0b7fd1d1d6eeb504060bd64cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0ab3f3d8e398723ceb1ec475cf56c35f50d42440ee775aac96c93a4e24f96a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ca5f83058fd18a284cb6f56c79df2b0a9502b5f8734bc721d9eb79d4cbc2d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bcb8fc5348acd2ba42ce7c1f1729d2862ef611617e7186c1d9bf8b7ca4a5df0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e87e98fa9a65c847fa7c25e3fcd705ada445b36b8b82879b3860bd52b120d8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f79dedc28e8f1c0abaf40c08b09478a1361a9ac2a456224d02b077cb3d2a4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__facc3614d25deb386aa62e329b9e8a716f42868f58c4d03425277c8408bbfab1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa56837339267dfd7d08ab9585ec0fd89945ce53b8a0b0bcf0975abb24459fd9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SelfSignedCertSubject]],
) -> None:
    """Type checking stubs"""
    pass
