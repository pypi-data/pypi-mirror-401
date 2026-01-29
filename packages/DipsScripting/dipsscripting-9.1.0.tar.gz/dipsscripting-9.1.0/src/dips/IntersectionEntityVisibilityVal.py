"""Generated wrapper for IntersectionEntityVisibility protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .IntersectionOptionsVal import IntersectionOptionsVal

class IntersectionEntityVisibilityVal:
    """Simple wrapper for IntersectionEntityVisibility with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.IntersectionEntityVisibility


    def __init__(self, intersection_options: Optional[IntersectionOptionsVal] = None, proto_message: Optional[Any] = None):
        """Initialize the IntersectionEntityVisibility wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if intersection_options is not None:
            self._proto_message.IntersectionOptions.CopyFrom(intersection_options.to_proto())
            self._intersection_options_wrapper = intersection_options


    # Properties

    @property
    def is_visible(self) -> bool:
        """Get the IsVisible field value."""
        return self._proto_message.IsVisible
    
    @is_visible.setter
    def is_visible(self, value: bool) -> None:
        """Set the IsVisible field value."""
        self._proto_message.IsVisible = value


    @property
    def intersection_options(self) -> IntersectionOptionsVal:
        """Get the IntersectionOptions field as a wrapper."""
        if not hasattr(self, '_intersection_options_wrapper'):
            self._intersection_options_wrapper = IntersectionOptionsVal(proto_message=self._proto_message.IntersectionOptions)
        return self._intersection_options_wrapper
    
    @intersection_options.setter
    def intersection_options(self, value: IntersectionOptionsVal) -> None:
        """Set the IntersectionOptions field to a wrapper."""
        self._proto_message.IntersectionOptions.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_intersection_options_wrapper'):
            self._intersection_options_wrapper._proto_message.CopyFrom(self._proto_message.IntersectionOptions)


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
