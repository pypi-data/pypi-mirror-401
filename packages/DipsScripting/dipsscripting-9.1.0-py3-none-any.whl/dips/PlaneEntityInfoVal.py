"""Generated wrapper for PlaneEntityInfo protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .ColorSurrogateVal import ColorSurrogateVal
from .PlaneVal import PlaneVal

class PlaneEntityInfoVal:
    """Simple wrapper for PlaneEntityInfo with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.PlaneEntityInfo


    def __init__(self, color: Optional[ColorSurrogateVal] = None, plane: Optional[PlaneVal] = None, proto_message: Optional[Any] = None):
        """Initialize the PlaneEntityInfo wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if color is not None:
            self._proto_message.Color.CopyFrom(color.to_proto())
            self._color_wrapper = color
        if plane is not None:
            self._proto_message.Plane.CopyFrom(plane.to_proto())
            self._plane_wrapper = plane


    # Properties

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
    def plane(self) -> PlaneVal:
        """Get the Plane field as a wrapper."""
        if not hasattr(self, '_plane_wrapper'):
            self._plane_wrapper = PlaneVal(proto_message=self._proto_message.Plane)
        return self._plane_wrapper
    
    @plane.setter
    def plane(self, value: PlaneVal) -> None:
        """Set the Plane field to a wrapper."""
        self._proto_message.Plane.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_plane_wrapper'):
            self._plane_wrapper._proto_message.CopyFrom(self._proto_message.Plane)


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
