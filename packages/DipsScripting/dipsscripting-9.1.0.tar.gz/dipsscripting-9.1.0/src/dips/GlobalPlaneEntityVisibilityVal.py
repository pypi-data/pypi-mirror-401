"""Generated wrapper for GlobalPlaneEntityVisibility protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .ColorSurrogateVal import ColorSurrogateVal
from .PlaneOptionsVal import PlaneOptionsVal

class GlobalPlaneEntityVisibilityVal:
    """Simple wrapper for GlobalPlaneEntityVisibility with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.GlobalPlaneEntityVisibility


    def __init__(self, color: Optional[ColorSurrogateVal] = None, plane_options: Optional[PlaneOptionsVal] = None, proto_message: Optional[Any] = None):
        """Initialize the GlobalPlaneEntityVisibility wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if color is not None:
            self._proto_message.Color.CopyFrom(color.to_proto())
            self._color_wrapper = color
        if plane_options is not None:
            self._proto_message.PlaneOptions.CopyFrom(plane_options.to_proto())
            self._plane_options_wrapper = plane_options


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
    def color(self) -> ColorSurrogateVal:
        """Get the Color field as a wrapper."""
        if not hasattr(self, '_color_wrapper'):
            self._color_wrapper = ColorSurrogateVal(proto_message=self._proto_message.Color)
        return self._color_wrapper
    
    @color.setter
    def color(self, value: ColorSurrogateVal) -> None:
        """Set the Color field to a wrapper."""
        self._proto_message.Color.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_color_wrapper'):
            self._color_wrapper._proto_message.CopyFrom(self._proto_message.Color)


    @property
    def plane_options(self) -> PlaneOptionsVal:
        """Get the PlaneOptions field as a wrapper."""
        if not hasattr(self, '_plane_options_wrapper'):
            self._plane_options_wrapper = PlaneOptionsVal(proto_message=self._proto_message.PlaneOptions)
        return self._plane_options_wrapper
    
    @plane_options.setter
    def plane_options(self, value: PlaneOptionsVal) -> None:
        """Set the PlaneOptions field to a wrapper."""
        self._proto_message.PlaneOptions.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_plane_options_wrapper'):
            self._plane_options_wrapper._proto_message.CopyFrom(self._proto_message.PlaneOptions)


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
