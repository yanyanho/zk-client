# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
    RepeatedScalarFieldContainer as google___protobuf___internal___containers___RepeatedScalarFieldContainer,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    Iterable as typing___Iterable,
    Optional as typing___Optional,
    Text as typing___Text,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int


class ZethNote(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    apk = ... # type: typing___Text
    value = ... # type: typing___Text
    rho = ... # type: typing___Text
    trap_r = ... # type: typing___Text

    def __init__(self,
        *,
        apk : typing___Optional[typing___Text] = None,
        value : typing___Optional[typing___Text] = None,
        rho : typing___Optional[typing___Text] = None,
        trap_r : typing___Optional[typing___Text] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> ZethNote: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"apk",u"rho",u"trap_r",u"value"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[u"apk",b"apk",u"rho",b"rho",u"trap_r",b"trap_r",u"value",b"value"]) -> None: ...

class JoinsplitInput(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    merkle_path = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]
    address = ... # type: builtin___int
    spending_ask = ... # type: typing___Text
    nullifier = ... # type: typing___Text

    @property
    def note(self) -> ZethNote: ...

    def __init__(self,
        *,
        merkle_path : typing___Optional[typing___Iterable[typing___Text]] = None,
        address : typing___Optional[builtin___int] = None,
        note : typing___Optional[ZethNote] = None,
        spending_ask : typing___Optional[typing___Text] = None,
        nullifier : typing___Optional[typing___Text] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> JoinsplitInput: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"note"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"address",u"merkle_path",u"note",u"nullifier",u"spending_ask"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"note",b"note"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"address",b"address",u"merkle_path",b"merkle_path",u"note",b"note",u"nullifier",b"nullifier",u"spending_ask",b"spending_ask"]) -> None: ...

class ProofInputs(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    mk_roots = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]
    pub_in_value = ... # type: typing___Text
    pub_out_value = ... # type: typing___Text
    h_sig = ... # type: typing___Text
    phi = ... # type: typing___Text

    @property
    def js_inputs(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[JoinsplitInput]: ...

    @property
    def js_outputs(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[ZethNote]: ...

    def __init__(self,
        *,
        mk_roots : typing___Optional[typing___Iterable[typing___Text]] = None,
        js_inputs : typing___Optional[typing___Iterable[JoinsplitInput]] = None,
        js_outputs : typing___Optional[typing___Iterable[ZethNote]] = None,
        pub_in_value : typing___Optional[typing___Text] = None,
        pub_out_value : typing___Optional[typing___Text] = None,
        h_sig : typing___Optional[typing___Text] = None,
        phi : typing___Optional[typing___Text] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> ProofInputs: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"h_sig",u"js_inputs",u"js_outputs",u"mk_roots",u"phi",u"pub_in_value",u"pub_out_value"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[u"h_sig",b"h_sig",u"js_inputs",b"js_inputs",u"js_outputs",b"js_outputs",u"mk_roots",b"mk_roots",u"phi",b"phi",u"pub_in_value",b"pub_in_value",u"pub_out_value",b"pub_out_value"]) -> None: ...
