"""Generated wrapper for SymbolDisplaySetting protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .ColorSurrogateVal import ColorSurrogateVal

class SymbolDisplaySettingVal:
    """Simple wrapper for SymbolDisplaySetting with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.SymbolDisplaySetting


    def __init__(self, border_color: Optional[ColorSurrogateVal] = None, fill_color: Optional[ColorSurrogateVal] = None, proto_message: Optional[Any] = None):
        """Initialize the SymbolDisplaySetting wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if border_color is not None:
            self._proto_message.BorderColor.CopyFrom(border_color.to_proto())
            self._border_color_wrapper = border_color
        if fill_color is not None:
            self._proto_message.FillColor.CopyFrom(fill_color.to_proto())
            self._fill_color_wrapper = fill_color


    # Properties

    @property
    def symbol_style(self) -> Any:
        """Get the SymbolStyle field value."""
        return self._proto_message.SymbolStyle
    
    @symbol_style.setter
    def symbol_style(self, value: Any) -> None:
        """Set the SymbolStyle field value."""
        self._proto_message.SymbolStyle = value


    @property
    def border_color(self) -> ColorSurrogateVal:
        """Get the BorderColor field as a wrapper."""
        if not hasattr(self, '_border_color_wrapper'):
            self._border_color_wrapper = ColorSurrogateVal(proto_message=self._proto_message.BorderColor)
        return self._border_color_wrapper
    
    @border_color.setter
    def border_color(self, value: ColorSurrogateVal) -> None:
        """Set the BorderColor field to a wrapper."""
        self._proto_message.BorderColor.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_border_color_wrapper'):
            self._border_color_wrapper._proto_message.CopyFrom(self._proto_message.BorderColor)


    @property
    def is_fill(self) -> bool:
        """Get the IsFill field value."""
        return self._proto_message.IsFill
    
    @is_fill.setter
    def is_fill(self, value: bool) -> None:
        """Set the IsFill field value."""
        self._proto_message.IsFill = value


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


    @property
    def symbol_scale(self) -> float:
        """Get the SymbolScale field value."""
        return self._proto_message.SymbolScale
    
    @symbol_scale.setter
    def symbol_scale(self, value: float) -> None:
        """Set the SymbolScale field value."""
        self._proto_message.SymbolScale = value


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
