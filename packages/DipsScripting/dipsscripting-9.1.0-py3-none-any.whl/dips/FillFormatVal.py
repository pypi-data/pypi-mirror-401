"""Generated wrapper for FillFormat protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .ColorSurrogateVal import ColorSurrogateVal

class FillFormatVal:
    """Simple wrapper for FillFormat with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.FillFormat


    def __init__(self, fill_color: Optional[ColorSurrogateVal] = None, proto_message: Optional[Any] = None):
        """Initialize the FillFormat wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if fill_color is not None:
            self._proto_message.FillColor.CopyFrom(fill_color.to_proto())
            self._fill_color_wrapper = fill_color


    # Properties

    @property
    def apply_fill(self) -> bool:
        """Get the ApplyFill field value."""
        return self._proto_message.ApplyFill
    
    @apply_fill.setter
    def apply_fill(self, value: bool) -> None:
        """Set the ApplyFill field value."""
        self._proto_message.ApplyFill = value


    @property
    def fill_color(self) -> ColorSurrogateVal:
        """Get the FillColor field as a wrapper."""
        if not hasattr(self, '_fill_color_wrapper'):
            self._fill_color_wrapper = ColorSurrogateVal(proto_message=self._proto_message.FillColor)
        return self._fill_color_wrapper
    
    @fill_color.setter
    def fill_color(self, value: ColorSurrogateVal) -> None:
        """Set the FillColor field to a wrapper."""
        self._proto_message.FillColor.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_fill_color_wrapper'):
            self._fill_color_wrapper._proto_message.CopyFrom(self._proto_message.FillColor)


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
