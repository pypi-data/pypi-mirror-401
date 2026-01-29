"""Generated wrapper for CustomRowRawData protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

class CustomRowRawDataVal:
    """Simple wrapper for CustomRowRawData with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.CustomRowRawData


    def __init__(self, proto_message: Optional[Any] = None):
        """Initialize the CustomRowRawData wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()



    # Properties

    @property
    def raw_data(self) -> Dict[int, str]:
        """Get the RawData field as a Python dictionary."""
        if not hasattr(self, '_raw_data_wrapper'):
            self._raw_data_wrapper = _ProtobufMapWrapper(self._proto_message.RawData)
        return self._raw_data_wrapper
    
    @raw_data.setter
    def raw_data(self, value: Dict[int, str]) -> None:
        """Set the RawData field to a Python dictionary."""
        if not isinstance(value, (dict, _ProtobufMapWrapper)):
            raise TypeError(f"Expected dict or _ProtobufMapWrapper, got {type(value).__name__}")
        self._proto_message.RawData.clear()
        if isinstance(value, _ProtobufMapWrapper):
            self._proto_message.RawData.update(value._proto_field)
        else:
            self._proto_message.RawData.update(value)
        # Update the cached wrapper if it exists
        if hasattr(self, '_raw_data_wrapper'):
            self._raw_data_wrapper._proto_field.clear()
            self._raw_data_wrapper._proto_field.update(self._proto_message.RawData)


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
