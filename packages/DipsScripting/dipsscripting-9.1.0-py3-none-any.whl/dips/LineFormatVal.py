"""Generated wrapper for LineFormat protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .ColorSurrogateVal import ColorSurrogateVal

class LineFormatVal:
    """Simple wrapper for LineFormat with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.LineFormat


    def __init__(self, line_color: Optional[ColorSurrogateVal] = None, proto_message: Optional[Any] = None):
        """Initialize the LineFormat wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if line_color is not None:
            self._proto_message.LineColor.CopyFrom(line_color.to_proto())
            self._line_color_wrapper = line_color


    # Properties

    @property
    def line_color(self) -> ColorSurrogateVal:
        """Get the LineColor field as a wrapper."""
        if not hasattr(self, '_line_color_wrapper'):
            self._line_color_wrapper = ColorSurrogateVal(proto_message=self._proto_message.LineColor)
        return self._line_color_wrapper
    
    @line_color.setter
    def line_color(self, value: ColorSurrogateVal) -> None:
        """Set the LineColor field to a wrapper."""
        self._proto_message.LineColor.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_line_color_wrapper'):
            self._line_color_wrapper._proto_message.CopyFrom(self._proto_message.LineColor)


    @property
    def line_width(self) -> int:
        """Get the LineWidth field value."""
        return self._proto_message.LineWidth
    
    @line_width.setter
    def line_width(self, value: int) -> None:
        """Set the LineWidth field value."""
        self._proto_message.LineWidth = value


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
