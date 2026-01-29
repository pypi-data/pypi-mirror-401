"""Generated wrapper for ValidationError protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

class ValidationErrorVal:
    """Simple wrapper for ValidationError with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.ValidationError


    def __init__(self, proto_message: Optional[Any] = None):
        """Initialize the ValidationError wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()



    # Properties

    @property
    def property_name(self) -> str:
        """Get the PropertyName field value."""
        return self._proto_message.PropertyName
    
    @property_name.setter
    def property_name(self, value: str) -> None:
        """Set the PropertyName field value."""
        self._proto_message.PropertyName = value


    @property
    def error_message(self) -> str:
        """Get the ErrorMessage field value."""
        return self._proto_message.ErrorMessage
    
    @error_message.setter
    def error_message(self, value: str) -> None:
        """Set the ErrorMessage field value."""
        self._proto_message.ErrorMessage = value


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
