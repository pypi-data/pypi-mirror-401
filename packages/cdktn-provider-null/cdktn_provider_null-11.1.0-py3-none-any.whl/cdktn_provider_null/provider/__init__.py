r'''
# `provider`

Refer to the Terraform Registry for docs: [`null`](https://registry.terraform.io/providers/hashicorp/null/3.2.4/docs).
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


class NullProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-null.provider.NullProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/null/3.2.4/docs null}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/null/3.2.4/docs null} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/null/3.2.4/docs#alias NullProvider#alias}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6a0e83b9afb9f289dfcf423eb2a134b3012aba7c36c13b485699e90fe100a7e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = NullProviderConfig(alias=alias)

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
        '''Generates CDKTF code for importing a NullProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NullProvider to import.
        :param import_from_id: The id of the existing NullProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/null/3.2.4/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NullProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fcd255816deaa4d18a827c02dd38d369eb9976739f3ab81a864a804a8947c95)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

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
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5530694fc150138ba247514f7ce9e2e08ed9dd7e88942ae3b48a0f05ea666f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-null.provider.NullProviderConfig",
    jsii_struct_bases=[],
    name_mapping={"alias": "alias"},
)
class NullProviderConfig:
    def __init__(self, *, alias: typing.Optional[builtins.str] = None) -> None:
        '''
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/null/3.2.4/docs#alias NullProvider#alias}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99cd1453d24431b729827727d2ac4e3676e740d6c0de985ca1e38198408a1ea2)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/null/3.2.4/docs#alias NullProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NullProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NullProvider",
    "NullProviderConfig",
]

publication.publish()

def _typecheckingstub__a6a0e83b9afb9f289dfcf423eb2a134b3012aba7c36c13b485699e90fe100a7e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fcd255816deaa4d18a827c02dd38d369eb9976739f3ab81a864a804a8947c95(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5530694fc150138ba247514f7ce9e2e08ed9dd7e88942ae3b48a0f05ea666f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99cd1453d24431b729827727d2ac4e3676e740d6c0de985ca1e38198408a1ea2(
    *,
    alias: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
