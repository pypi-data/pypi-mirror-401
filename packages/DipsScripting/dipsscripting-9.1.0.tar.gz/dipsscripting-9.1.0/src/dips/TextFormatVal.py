"""Generated wrapper for TextFormat protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .ColorSurrogateVal import ColorSurrogateVal

class TextFormatVal:
    """Simple wrapper for TextFormat with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.TextFormat


    def __init__(self, text_color: Optional[ColorSurrogateVal] = None, proto_message: Optional[Any] = None):
        """Initialize the TextFormat wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if text_color is not None:
            self._proto_message.TextColor.CopyFrom(text_color.to_proto())
            self._text_color_wrapper = text_color


    # Properties

    @property
    def text_horizontal_alignment(self) -> Any:
        """Get the TextHorizontalAlignment field value."""
        return self._proto_message.TextHorizontalAlignment
    
    @text_horizontal_alignment.setter
    def text_horizontal_alignment(self, value: Any) -> None:
        """Set the TextHorizontalAlignment field value."""
        self._proto_message.TextHorizontalAlignment = value


    @property
    def text_color(self) -> ColorSurrogateVal:
        """Get the TextColor field as a wrapper."""
        if not hasattr(self, '_text_color_wrapper'):
            self._text_color_wrapper = ColorSurrogateVal(proto_message=self._proto_message.TextColor)
        return self._text_color_wrapper
    
    @text_color.setter
    def text_color(self, value: ColorSurrogateVal) -> None:
        """Set the TextColor field to a wrapper."""
        self._proto_message.TextColor.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_text_color_wrapper'):
            self._text_color_wrapper._proto_message.CopyFrom(self._proto_message.TextColor)


    @property
    def font_name(self) -> str:
        """Get the FontName field value."""
        return self._proto_message.FontName
    
    @font_name.setter
    def font_name(self, value: str) -> None:
        """Set the FontName field value."""
        self._proto_message.FontName = value


    @property
    def font_size(self) -> int:
        """Get the FontSize field value."""
        return self._proto_message.FontSize
    
    @font_size.setter
    def font_size(self, value: int) -> None:
        """Set the FontSize field value."""
        self._proto_message.FontSize = value


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
