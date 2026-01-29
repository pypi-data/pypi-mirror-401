"""Generated wrapper for ValidatableResult_ProtoReference_RectangleToolEntityInfo protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .ValidationErrorVal import ValidationErrorVal
from .RectangleToolEntityInfoRef import RectangleToolEntityInfoRef

class ValidatableResult_ProtoReference_RectangleToolEntityInfoVal:
    """Simple wrapper for ValidatableResult_ProtoReference_RectangleToolEntityInfo with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.ValidatableResult_ProtoReference_RectangleToolEntityInfo


    def __init__(self, result: Optional[RectangleToolEntityInfoRef] = None, proto_message: Optional[Any] = None, channel_to_connect_on: Optional[Any] = None):
        """Initialize the ValidatableResult_ProtoReference_RectangleToolEntityInfo wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        # Store channel for reference types
        self.__channelToConnectOn = channel_to_connect_on

        if result is not None:
            self.result = result


    # Properties

    @property
    def errors(self) -> List[ValidationErrorVal]:
        """Get the Errors field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.Errors, ValidationErrorVal)
    
    @errors.setter
    def errors(self, value: List[ValidationErrorVal]) -> None:
        """Set the Errors field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.Errors[:] = []
        for item in value:
            self._proto_message.Errors.append(item.to_proto())


    @property
    def result(self) -> RectangleToolEntityInfoRef:
        """Get the Result field as a reference."""
        return RectangleToolEntityInfoRef(self.__channelToConnectOn, self._proto_message.Result)
    
    @result.setter
    def result(self, value: RectangleToolEntityInfoRef) -> None:
        """Set the Result field to a reference."""
        self._proto_message.Result.CopyFrom(value.get_model_ref())


    # Utility methods

    def to_proto(self):
        """Get the underlying protobuf message."""
        return self._proto_message
    
    @classmethod
    def from_proto(cls, proto_message):
        """Create wrapper from existing protobuf message."""
        wrapper = cls()
        wrapper._proto_message.CopyFrom(proto_message)
        return wrapper
    
    def copy(self):
        """Create a copy of this wrapper."""
        new_wrapper = self.__class__()
        new_wrapper._proto_message.CopyFrom(self._proto_message)
        return new_wrapper
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}({self._proto_message})"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"{self.__class__.__name__}({self._proto_message})"
