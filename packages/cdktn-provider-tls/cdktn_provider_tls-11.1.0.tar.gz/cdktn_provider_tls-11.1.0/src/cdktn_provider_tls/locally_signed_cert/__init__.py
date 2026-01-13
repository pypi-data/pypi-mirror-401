r'''
# `tls_locally_signed_cert`

Refer to the Terraform Registry for docs: [`tls_locally_signed_cert`](https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert).
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


class LocallySignedCert(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-tls.locallySignedCert.LocallySignedCert",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert tls_locally_signed_cert}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        allowed_uses: typing.Sequence[builtins.str],
        ca_cert_pem: builtins.str,
        ca_private_key_pem: builtins.str,
        cert_request_pem: builtins.str,
        validity_period_hours: jsii.Number,
        early_renewal_hours: typing.Optional[jsii.Number] = None,
        is_ca_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        set_subject_key_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert tls_locally_signed_cert} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param allowed_uses: List of key usages allowed for the issued certificate. Values are defined in `RFC 5280 <https://datatracker.ietf.org/doc/html/rfc5280>`_ and combine flags defined by both `Key Usages <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.3>`_ and `Extended Key Usages <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.12>`_. Accepted values: ``any_extended``, ``cert_signing``, ``client_auth``, ``code_signing``, ``content_commitment``, ``crl_signing``, ``data_encipherment``, ``decipher_only``, ``digital_signature``, ``email_protection``, ``encipher_only``, ``ipsec_end_system``, ``ipsec_tunnel``, ``ipsec_user``, ``key_agreement``, ``key_encipherment``, ``microsoft_commercial_code_signing``, ``microsoft_kernel_code_signing``, ``microsoft_server_gated_crypto``, ``netscape_server_gated_crypto``, ``ocsp_signing``, ``server_auth``, ``timestamping``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#allowed_uses LocallySignedCert#allowed_uses}
        :param ca_cert_pem: Certificate data of the Certificate Authority (CA) in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#ca_cert_pem LocallySignedCert#ca_cert_pem}
        :param ca_private_key_pem: Private key of the Certificate Authority (CA) used to sign the certificate, in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#ca_private_key_pem LocallySignedCert#ca_private_key_pem}
        :param cert_request_pem: Certificate request data in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#cert_request_pem LocallySignedCert#cert_request_pem}
        :param validity_period_hours: Number of hours, after initial issuing, that the certificate will remain valid for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#validity_period_hours LocallySignedCert#validity_period_hours}
        :param early_renewal_hours: The resource will consider the certificate to have expired the given number of hours before its actual expiry time. This can be useful to deploy an updated certificate in advance of the expiration of the current certificate. However, the old certificate remains valid until its true expiration time, since this resource does not (and cannot) support certificate revocation. Also, this advance update can only be performed should the Terraform configuration be applied during the early renewal period. (default: ``0``) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#early_renewal_hours LocallySignedCert#early_renewal_hours}
        :param is_ca_certificate: Is the generated certificate representing a Certificate Authority (CA) (default: ``false``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#is_ca_certificate LocallySignedCert#is_ca_certificate}
        :param set_subject_key_id: Should the generated certificate include a `subject key identifier <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.2>`_ (default: ``false``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#set_subject_key_id LocallySignedCert#set_subject_key_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e39b6a1371b765c115c7f0e47627ac6dc6436ef9292b159954cb8713586b884)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = LocallySignedCertConfig(
            allowed_uses=allowed_uses,
            ca_cert_pem=ca_cert_pem,
            ca_private_key_pem=ca_private_key_pem,
            cert_request_pem=cert_request_pem,
            validity_period_hours=validity_period_hours,
            early_renewal_hours=early_renewal_hours,
            is_ca_certificate=is_ca_certificate,
            set_subject_key_id=set_subject_key_id,
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
        '''Generates CDKTF code for importing a LocallySignedCert resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LocallySignedCert to import.
        :param import_from_id: The id of the existing LocallySignedCert that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LocallySignedCert to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2b29ffca5089c75700227e38d77e2d96932420ae970efbef5c9c408e68ab4d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetEarlyRenewalHours")
    def reset_early_renewal_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEarlyRenewalHours", []))

    @jsii.member(jsii_name="resetIsCaCertificate")
    def reset_is_ca_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsCaCertificate", []))

    @jsii.member(jsii_name="resetSetSubjectKeyId")
    def reset_set_subject_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSetSubjectKeyId", []))

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
    @jsii.member(jsii_name="caKeyAlgorithm")
    def ca_key_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caKeyAlgorithm"))

    @builtins.property
    @jsii.member(jsii_name="certPem")
    def cert_pem(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certPem"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="readyForRenewal")
    def ready_for_renewal(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "readyForRenewal"))

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
    @jsii.member(jsii_name="caCertPemInput")
    def ca_cert_pem_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caCertPemInput"))

    @builtins.property
    @jsii.member(jsii_name="caPrivateKeyPemInput")
    def ca_private_key_pem_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caPrivateKeyPemInput"))

    @builtins.property
    @jsii.member(jsii_name="certRequestPemInput")
    def cert_request_pem_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certRequestPemInput"))

    @builtins.property
    @jsii.member(jsii_name="earlyRenewalHoursInput")
    def early_renewal_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "earlyRenewalHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="isCaCertificateInput")
    def is_ca_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isCaCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="setSubjectKeyIdInput")
    def set_subject_key_id_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "setSubjectKeyIdInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__81e73cfc99ca4848f324852ec8beeea43ee7a9e25ff1702c628a07ae047437a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedUses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="caCertPem")
    def ca_cert_pem(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCertPem"))

    @ca_cert_pem.setter
    def ca_cert_pem(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8993b5451264bfb9bfed707228030ab4dd27782adb3492e17234754f13851cf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCertPem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="caPrivateKeyPem")
    def ca_private_key_pem(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caPrivateKeyPem"))

    @ca_private_key_pem.setter
    def ca_private_key_pem(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61630066af3c26a77a02b19fcec4995e367e49ac303cc0990057c33cbc295b65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caPrivateKeyPem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certRequestPem")
    def cert_request_pem(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certRequestPem"))

    @cert_request_pem.setter
    def cert_request_pem(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b51b518ae985cc078c87f73e045986904611ca915457596289de306560b983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certRequestPem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="earlyRenewalHours")
    def early_renewal_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "earlyRenewalHours"))

    @early_renewal_hours.setter
    def early_renewal_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a1e5373152e2b0b42c6d3bed955bf511c7374ba0b7d07a2365c265a5fbb945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "earlyRenewalHours", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__cbb7d78dbab93c69a9b803c87c21c081534a02dd82af3c380224236cdb4749c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isCaCertificate", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__0dcbff2b17cfb6e96df56695beb376865d3bd4389bf2f39f78f01978a21d2947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "setSubjectKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validityPeriodHours")
    def validity_period_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "validityPeriodHours"))

    @validity_period_hours.setter
    def validity_period_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9abaefc96c1a48b850a4fdbb7186be8a7eeda7a4f35637aeafedf569175b7695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validityPeriodHours", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-tls.locallySignedCert.LocallySignedCertConfig",
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
        "ca_cert_pem": "caCertPem",
        "ca_private_key_pem": "caPrivateKeyPem",
        "cert_request_pem": "certRequestPem",
        "validity_period_hours": "validityPeriodHours",
        "early_renewal_hours": "earlyRenewalHours",
        "is_ca_certificate": "isCaCertificate",
        "set_subject_key_id": "setSubjectKeyId",
    },
)
class LocallySignedCertConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        ca_cert_pem: builtins.str,
        ca_private_key_pem: builtins.str,
        cert_request_pem: builtins.str,
        validity_period_hours: jsii.Number,
        early_renewal_hours: typing.Optional[jsii.Number] = None,
        is_ca_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        set_subject_key_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param allowed_uses: List of key usages allowed for the issued certificate. Values are defined in `RFC 5280 <https://datatracker.ietf.org/doc/html/rfc5280>`_ and combine flags defined by both `Key Usages <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.3>`_ and `Extended Key Usages <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.12>`_. Accepted values: ``any_extended``, ``cert_signing``, ``client_auth``, ``code_signing``, ``content_commitment``, ``crl_signing``, ``data_encipherment``, ``decipher_only``, ``digital_signature``, ``email_protection``, ``encipher_only``, ``ipsec_end_system``, ``ipsec_tunnel``, ``ipsec_user``, ``key_agreement``, ``key_encipherment``, ``microsoft_commercial_code_signing``, ``microsoft_kernel_code_signing``, ``microsoft_server_gated_crypto``, ``netscape_server_gated_crypto``, ``ocsp_signing``, ``server_auth``, ``timestamping``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#allowed_uses LocallySignedCert#allowed_uses}
        :param ca_cert_pem: Certificate data of the Certificate Authority (CA) in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#ca_cert_pem LocallySignedCert#ca_cert_pem}
        :param ca_private_key_pem: Private key of the Certificate Authority (CA) used to sign the certificate, in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#ca_private_key_pem LocallySignedCert#ca_private_key_pem}
        :param cert_request_pem: Certificate request data in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#cert_request_pem LocallySignedCert#cert_request_pem}
        :param validity_period_hours: Number of hours, after initial issuing, that the certificate will remain valid for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#validity_period_hours LocallySignedCert#validity_period_hours}
        :param early_renewal_hours: The resource will consider the certificate to have expired the given number of hours before its actual expiry time. This can be useful to deploy an updated certificate in advance of the expiration of the current certificate. However, the old certificate remains valid until its true expiration time, since this resource does not (and cannot) support certificate revocation. Also, this advance update can only be performed should the Terraform configuration be applied during the early renewal period. (default: ``0``) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#early_renewal_hours LocallySignedCert#early_renewal_hours}
        :param is_ca_certificate: Is the generated certificate representing a Certificate Authority (CA) (default: ``false``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#is_ca_certificate LocallySignedCert#is_ca_certificate}
        :param set_subject_key_id: Should the generated certificate include a `subject key identifier <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.2>`_ (default: ``false``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#set_subject_key_id LocallySignedCert#set_subject_key_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef5d673fe2e6ff587995dc84a61cb7adccd648a7015edb2315248beac969a30c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument allowed_uses", value=allowed_uses, expected_type=type_hints["allowed_uses"])
            check_type(argname="argument ca_cert_pem", value=ca_cert_pem, expected_type=type_hints["ca_cert_pem"])
            check_type(argname="argument ca_private_key_pem", value=ca_private_key_pem, expected_type=type_hints["ca_private_key_pem"])
            check_type(argname="argument cert_request_pem", value=cert_request_pem, expected_type=type_hints["cert_request_pem"])
            check_type(argname="argument validity_period_hours", value=validity_period_hours, expected_type=type_hints["validity_period_hours"])
            check_type(argname="argument early_renewal_hours", value=early_renewal_hours, expected_type=type_hints["early_renewal_hours"])
            check_type(argname="argument is_ca_certificate", value=is_ca_certificate, expected_type=type_hints["is_ca_certificate"])
            check_type(argname="argument set_subject_key_id", value=set_subject_key_id, expected_type=type_hints["set_subject_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_uses": allowed_uses,
            "ca_cert_pem": ca_cert_pem,
            "ca_private_key_pem": ca_private_key_pem,
            "cert_request_pem": cert_request_pem,
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
        if early_renewal_hours is not None:
            self._values["early_renewal_hours"] = early_renewal_hours
        if is_ca_certificate is not None:
            self._values["is_ca_certificate"] = is_ca_certificate
        if set_subject_key_id is not None:
            self._values["set_subject_key_id"] = set_subject_key_id

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#allowed_uses LocallySignedCert#allowed_uses}
        '''
        result = self._values.get("allowed_uses")
        assert result is not None, "Required property 'allowed_uses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def ca_cert_pem(self) -> builtins.str:
        '''Certificate data of the Certificate Authority (CA) in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#ca_cert_pem LocallySignedCert#ca_cert_pem}
        '''
        result = self._values.get("ca_cert_pem")
        assert result is not None, "Required property 'ca_cert_pem' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ca_private_key_pem(self) -> builtins.str:
        '''Private key of the Certificate Authority (CA) used to sign the certificate, in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#ca_private_key_pem LocallySignedCert#ca_private_key_pem}
        '''
        result = self._values.get("ca_private_key_pem")
        assert result is not None, "Required property 'ca_private_key_pem' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cert_request_pem(self) -> builtins.str:
        '''Certificate request data in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#cert_request_pem LocallySignedCert#cert_request_pem}
        '''
        result = self._values.get("cert_request_pem")
        assert result is not None, "Required property 'cert_request_pem' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def validity_period_hours(self) -> jsii.Number:
        '''Number of hours, after initial issuing, that the certificate will remain valid for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#validity_period_hours LocallySignedCert#validity_period_hours}
        '''
        result = self._values.get("validity_period_hours")
        assert result is not None, "Required property 'validity_period_hours' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def early_renewal_hours(self) -> typing.Optional[jsii.Number]:
        '''The resource will consider the certificate to have expired the given number of hours before its actual expiry time.

        This can be useful to deploy an updated certificate in advance of the expiration of the current certificate. However, the old certificate remains valid until its true expiration time, since this resource does not (and cannot) support certificate revocation. Also, this advance update can only be performed should the Terraform configuration be applied during the early renewal period. (default: ``0``)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#early_renewal_hours LocallySignedCert#early_renewal_hours}
        '''
        result = self._values.get("early_renewal_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def is_ca_certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Is the generated certificate representing a Certificate Authority (CA) (default: ``false``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#is_ca_certificate LocallySignedCert#is_ca_certificate}
        '''
        result = self._values.get("is_ca_certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def set_subject_key_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the generated certificate include a `subject key identifier <https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.2>`_ (default: ``false``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/resources/locally_signed_cert#set_subject_key_id LocallySignedCert#set_subject_key_id}
        '''
        result = self._values.get("set_subject_key_id")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LocallySignedCertConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LocallySignedCert",
    "LocallySignedCertConfig",
]

publication.publish()

def _typecheckingstub__1e39b6a1371b765c115c7f0e47627ac6dc6436ef9292b159954cb8713586b884(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allowed_uses: typing.Sequence[builtins.str],
    ca_cert_pem: builtins.str,
    ca_private_key_pem: builtins.str,
    cert_request_pem: builtins.str,
    validity_period_hours: jsii.Number,
    early_renewal_hours: typing.Optional[jsii.Number] = None,
    is_ca_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    set_subject_key_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__0c2b29ffca5089c75700227e38d77e2d96932420ae970efbef5c9c408e68ab4d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81e73cfc99ca4848f324852ec8beeea43ee7a9e25ff1702c628a07ae047437a1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8993b5451264bfb9bfed707228030ab4dd27782adb3492e17234754f13851cf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61630066af3c26a77a02b19fcec4995e367e49ac303cc0990057c33cbc295b65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b51b518ae985cc078c87f73e045986904611ca915457596289de306560b983(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a1e5373152e2b0b42c6d3bed955bf511c7374ba0b7d07a2365c265a5fbb945(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb7d78dbab93c69a9b803c87c21c081534a02dd82af3c380224236cdb4749c3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dcbff2b17cfb6e96df56695beb376865d3bd4389bf2f39f78f01978a21d2947(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9abaefc96c1a48b850a4fdbb7186be8a7eeda7a4f35637aeafedf569175b7695(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5d673fe2e6ff587995dc84a61cb7adccd648a7015edb2315248beac969a30c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allowed_uses: typing.Sequence[builtins.str],
    ca_cert_pem: builtins.str,
    ca_private_key_pem: builtins.str,
    cert_request_pem: builtins.str,
    validity_period_hours: jsii.Number,
    early_renewal_hours: typing.Optional[jsii.Number] = None,
    is_ca_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    set_subject_key_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
