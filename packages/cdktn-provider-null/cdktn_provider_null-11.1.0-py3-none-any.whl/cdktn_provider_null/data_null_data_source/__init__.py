r'''
# `data_null_data_source`

Refer to the Terraform Registry for docs: [`data_null_data_source`](https://registry.terraform.io/providers/hashicorp/null/3.2.4/docs/data-sources/data_source).
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


class DataNullDataSource(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-null.dataNullDataSource.DataNullDataSource",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/null/3.2.4/docs/data-sources/data_source null_data_source}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        has_computed_default: typing.Optional[builtins.str] = None,
        inputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/null/3.2.4/docs/data-sources/data_source null_data_source} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param has_computed_default: If set, its literal value will be stored and returned. If not, its value defaults to ``"default"``. This argument exists primarily for testing and has little practical use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/null/3.2.4/docs/data-sources/data_source#has_computed_default DataNullDataSource#has_computed_default}
        :param inputs: A map of arbitrary strings that is copied into the ``outputs`` attribute, and accessible directly for interpolation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/null/3.2.4/docs/data-sources/data_source#inputs DataNullDataSource#inputs}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e772076170c79f6a31ad9efed804e4a53672175bea61886cff6b43517620b31e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataNullDataSourceConfig(
            has_computed_default=has_computed_default,
            inputs=inputs,
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
        '''Generates CDKTF code for importing a DataNullDataSource resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataNullDataSource to import.
        :param import_from_id: The id of the existing DataNullDataSource that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/null/3.2.4/docs/data-sources/data_source#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataNullDataSource to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab7b39b9dc01cb87918c6ebaf0f6e819c90c7d0a267659d0f11ba9de3b60fd24)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetHasComputedDefault")
    def reset_has_computed_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHasComputedDefault", []))

    @jsii.member(jsii_name="resetInputs")
    def reset_inputs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputs", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="random")
    def random(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "random"))

    @builtins.property
    @jsii.member(jsii_name="hasComputedDefaultInput")
    def has_computed_default_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hasComputedDefaultInput"))

    @builtins.property
    @jsii.member(jsii_name="inputsInput")
    def inputs_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "inputsInput"))

    @builtins.property
    @jsii.member(jsii_name="hasComputedDefault")
    def has_computed_default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hasComputedDefault"))

    @has_computed_default.setter
    def has_computed_default(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d70c3c8eea56bdfa76f81b9845353b7533899066089dd1f3c3ac96d43931199a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hasComputedDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "inputs"))

    @inputs.setter
    def inputs(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a3a3b2f03a95da42dca2dda853bb333ef84a93f2afb96c522f4707dee5b6929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputs", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-null.dataNullDataSource.DataNullDataSourceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "has_computed_default": "hasComputedDefault",
        "inputs": "inputs",
    },
)
class DataNullDataSourceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        has_computed_default: typing.Optional[builtins.str] = None,
        inputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param has_computed_default: If set, its literal value will be stored and returned. If not, its value defaults to ``"default"``. This argument exists primarily for testing and has little practical use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/null/3.2.4/docs/data-sources/data_source#has_computed_default DataNullDataSource#has_computed_default}
        :param inputs: A map of arbitrary strings that is copied into the ``outputs`` attribute, and accessible directly for interpolation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/null/3.2.4/docs/data-sources/data_source#inputs DataNullDataSource#inputs}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c50c9fb2f0f729f968900dcb9d30c2b30df091def71b3151e610d2828ea56f8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument has_computed_default", value=has_computed_default, expected_type=type_hints["has_computed_default"])
            check_type(argname="argument inputs", value=inputs, expected_type=type_hints["inputs"])
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
        if has_computed_default is not None:
            self._values["has_computed_default"] = has_computed_default
        if inputs is not None:
            self._values["inputs"] = inputs

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
    def has_computed_default(self) -> typing.Optional[builtins.str]:
        '''If set, its literal value will be stored and returned.

        If not, its value defaults to ``"default"``. This argument exists primarily for testing and has little practical use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/null/3.2.4/docs/data-sources/data_source#has_computed_default DataNullDataSource#has_computed_default}
        '''
        result = self._values.get("has_computed_default")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inputs(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of arbitrary strings that is copied into the ``outputs`` attribute, and accessible directly for interpolation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/null/3.2.4/docs/data-sources/data_source#inputs DataNullDataSource#inputs}
        '''
        result = self._values.get("inputs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataNullDataSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataNullDataSource",
    "DataNullDataSourceConfig",
]

publication.publish()

def _typecheckingstub__e772076170c79f6a31ad9efed804e4a53672175bea61886cff6b43517620b31e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    has_computed_default: typing.Optional[builtins.str] = None,
    inputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__ab7b39b9dc01cb87918c6ebaf0f6e819c90c7d0a267659d0f11ba9de3b60fd24(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d70c3c8eea56bdfa76f81b9845353b7533899066089dd1f3c3ac96d43931199a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3a3b2f03a95da42dca2dda853bb333ef84a93f2afb96c522f4707dee5b6929(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c50c9fb2f0f729f968900dcb9d30c2b30df091def71b3151e610d2828ea56f8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    has_computed_default: typing.Optional[builtins.str] = None,
    inputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
