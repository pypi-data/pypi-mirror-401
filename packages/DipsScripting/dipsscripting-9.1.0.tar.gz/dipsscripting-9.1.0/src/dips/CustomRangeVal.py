"""Generated wrapper for CustomRange protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

class CustomRangeVal:
    """Simple wrapper for CustomRange with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.CustomRange


    def __init__(self, proto_message: Optional[Any] = None):
        """Initialize the CustomRange wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()



    # Properties

    @property
    def apply_custom_range(self) -> bool:
        """Get the ApplyCustomRange field value."""
        return self._proto_message.ApplyCustomRange
    
    @apply_custom_range.setter
    def apply_custom_range(self, value: bool) -> None:
        """Set the ApplyCustomRange field value."""
        self._proto_message.ApplyCustomRange = value


    @property
    def min(self) -> float:
        """Get the Min field value."""
        return self._proto_message.Min
    
    @min.setter
    def min(self, value: float) -> None:
        """Set the Min field value."""
        self._proto_message.Min = value


    @property
    def max(self) -> float:
        """Get the Max field value."""
        return self._proto_message.Max
    
    @max.setter
    def max(self, value: float) -> None:
        """Set the Max field value."""
        self._proto_message.Max = value


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
