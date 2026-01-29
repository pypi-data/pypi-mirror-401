"""Generated wrapper for LengthData protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .DataFormatterVal import DataFormatterVal

class LengthDataVal:
    """Simple wrapper for LengthData with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.LengthData


    def __init__(self, length_unit: Optional[DataFormatterVal] = None, proto_message: Optional[Any] = None):
        """Initialize the LengthData wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if length_unit is not None:
            self._proto_message.LengthUnit.CopyFrom(length_unit.to_proto())
            self._length_unit_wrapper = length_unit


    # Properties

    @property
    def length(self) -> float:
        """Get the Length field value."""
        return self._proto_message.Length
    
    @length.setter
    def length(self, value: float) -> None:
        """Set the Length field value."""
        self._proto_message.Length = value


    @property
    def length_unit(self) -> DataFormatterVal:
        """Get the LengthUnit field as a wrapper."""
        if not hasattr(self, '_length_unit_wrapper'):
            self._length_unit_wrapper = DataFormatterVal(proto_message=self._proto_message.LengthUnit)
        return self._length_unit_wrapper
    
    @length_unit.setter
    def length_unit(self, value: DataFormatterVal) -> None:
        """Set the LengthUnit field to a wrapper."""
        self._proto_message.LengthUnit.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_length_unit_wrapper'):
            self._length_unit_wrapper._proto_message.CopyFrom(self._proto_message.LengthUnit)


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
