r'''
# `provider`

Refer to the Terraform Registry for docs: [`tls`](https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs).
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


class TlsProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-tls.provider.TlsProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs tls}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
        proxy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TlsProviderProxy", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs tls} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs#alias TlsProvider#alias}
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs#proxy TlsProvider#proxy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a52372e67b0208faae6d0ffe5796b5014667d18b559a90fe4ea6d4407cd344f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = TlsProviderConfig(alias=alias, proxy=proxy)

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
        '''Generates CDKTF code for importing a TlsProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the TlsProvider to import.
        :param import_from_id: The id of the existing TlsProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the TlsProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffe92b1fa8880ad67c0318b46dc1f80574993376d5a547863abd3315a59c5c08)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetProxy")
    def reset_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxy", []))

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
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyInput")
    def proxy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TlsProviderProxy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TlsProviderProxy"]]], jsii.get(self, "proxyInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f626997ec564d90d03af2003b58a68c92e07f1faa855f9d921c08806696bd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxy")
    def proxy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TlsProviderProxy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TlsProviderProxy"]]], jsii.get(self, "proxy"))

    @proxy.setter
    def proxy(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TlsProviderProxy"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea149e1f9c7c14cc0dda4238b239c13c39805f9c65848ede3ba57d7f1a1451ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxy", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-tls.provider.TlsProviderConfig",
    jsii_struct_bases=[],
    name_mapping={"alias": "alias", "proxy": "proxy"},
)
class TlsProviderConfig:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        proxy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TlsProviderProxy", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs#alias TlsProvider#alias}
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs#proxy TlsProvider#proxy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7352cb12db5baf9d6208de57d742060c78d4f0d2e4c906b2fe8ed9d8eedc38d8)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument proxy", value=proxy, expected_type=type_hints["proxy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if proxy is not None:
            self._values["proxy"] = proxy

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs#alias TlsProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TlsProviderProxy"]]]:
        '''proxy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs#proxy TlsProvider#proxy}
        '''
        result = self._values.get("proxy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TlsProviderProxy"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TlsProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-tls.provider.TlsProviderProxy",
    jsii_struct_bases=[],
    name_mapping={
        "from_env": "fromEnv",
        "password": "password",
        "url": "url",
        "username": "username",
    },
)
class TlsProviderProxy:
    def __init__(
        self,
        *,
        from_env: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param from_env: When ``true`` the provider will discover the proxy configuration from environment variables. This is based upon ```http.ProxyFromEnvironment`` <https://pkg.go.dev/net/http#ProxyFromEnvironment>`_ and it supports the same environment variables (default: ``true``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs#from_env TlsProvider#from_env}
        :param password: Password used for Basic authentication against the Proxy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs#password TlsProvider#password}
        :param url: URL used to connect to the Proxy. Accepted schemes are: ``http``, ``https``, ``socks5``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs#url TlsProvider#url}
        :param username: Username (or Token) used for Basic authentication against the Proxy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs#username TlsProvider#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d1dd99fe705157d3277cf8a86e5c83c125ca31017f6426cf827172de17e1dda)
            check_type(argname="argument from_env", value=from_env, expected_type=type_hints["from_env"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if from_env is not None:
            self._values["from_env"] = from_env
        if password is not None:
            self._values["password"] = password
        if url is not None:
            self._values["url"] = url
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def from_env(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When ``true`` the provider will discover the proxy configuration from environment variables.

        This is based upon ```http.ProxyFromEnvironment`` <https://pkg.go.dev/net/http#ProxyFromEnvironment>`_ and it supports the same environment variables (default: ``true``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs#from_env TlsProvider#from_env}
        '''
        result = self._values.get("from_env")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password used for Basic authentication against the Proxy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs#password TlsProvider#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''URL used to connect to the Proxy. Accepted schemes are: ``http``, ``https``, ``socks5``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs#url TlsProvider#url}
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username (or Token) used for Basic authentication against the Proxy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs#username TlsProvider#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TlsProviderProxy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "TlsProvider",
    "TlsProviderConfig",
    "TlsProviderProxy",
]

publication.publish()

def _typecheckingstub__4a52372e67b0208faae6d0ffe5796b5014667d18b559a90fe4ea6d4407cd344f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias: typing.Optional[builtins.str] = None,
    proxy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TlsProviderProxy, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe92b1fa8880ad67c0318b46dc1f80574993376d5a547863abd3315a59c5c08(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f626997ec564d90d03af2003b58a68c92e07f1faa855f9d921c08806696bd2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea149e1f9c7c14cc0dda4238b239c13c39805f9c65848ede3ba57d7f1a1451ee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TlsProviderProxy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7352cb12db5baf9d6208de57d742060c78d4f0d2e4c906b2fe8ed9d8eedc38d8(
    *,
    alias: typing.Optional[builtins.str] = None,
    proxy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TlsProviderProxy, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d1dd99fe705157d3277cf8a86e5c83c125ca31017f6426cf827172de17e1dda(
    *,
    from_env: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
