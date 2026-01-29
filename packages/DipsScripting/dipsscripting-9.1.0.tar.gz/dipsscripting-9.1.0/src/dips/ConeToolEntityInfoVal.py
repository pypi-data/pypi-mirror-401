"""Generated wrapper for ConeToolEntityInfo protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .ColorSurrogateVal import ColorSurrogateVal
from .ConeVal import ConeVal

class ConeToolEntityInfoVal:
    """Simple wrapper for ConeToolEntityInfo with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.ConeToolEntityInfo


    def __init__(self, color: Optional[ColorSurrogateVal] = None, cone: Optional[ConeVal] = None, proto_message: Optional[Any] = None):
        """Initialize the ConeToolEntityInfo wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if color is not None:
            self._proto_message.Color.CopyFrom(color.to_proto())
            self._color_wrapper = color
        if cone is not None:
            self._proto_message.Cone.CopyFrom(cone.to_proto())
            self._cone_wrapper = cone


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
    def name(self) -> str:
        """Get the Name field value."""
        return self._proto_message.Name
    
    @name.setter
    def name(self, value: str) -> None:
        """Set the Name field value."""
        self._proto_message.Name = value


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
    def cone(self) -> ConeVal:
        """Get the Cone field as a wrapper."""
        if not hasattr(self, '_cone_wrapper'):
            self._cone_wrapper = ConeVal(proto_message=self._proto_message.Cone)
        return self._cone_wrapper
    
    @cone.setter
    def cone(self, value: ConeVal) -> None:
        """Set the Cone field to a wrapper."""
        self._proto_message.Cone.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_cone_wrapper'):
            self._cone_wrapper._proto_message.CopyFrom(self._proto_message.Cone)


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
