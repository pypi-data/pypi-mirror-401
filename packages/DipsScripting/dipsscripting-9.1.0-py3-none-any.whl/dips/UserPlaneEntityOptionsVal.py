"""Generated wrapper for UserPlaneEntityOptions protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .LineationVal import LineationVal
from .PlaneOptionsVal import PlaneOptionsVal

class UserPlaneEntityOptionsVal:
    """Simple wrapper for UserPlaneEntityOptions with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.UserPlaneEntityOptions


    def __init__(self, plane_options: Optional[PlaneOptionsVal] = None, proto_message: Optional[Any] = None):
        """Initialize the UserPlaneEntityOptions wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if plane_options is not None:
            self._proto_message.PlaneOptions.CopyFrom(plane_options.to_proto())
            self._plane_options_wrapper = plane_options


    # Properties

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


    @property
    def show_lineations(self) -> bool:
        """Get the ShowLineations field value."""
        return self._proto_message.ShowLineations
    
    @show_lineations.setter
    def show_lineations(self, value: bool) -> None:
        """Set the ShowLineations field value."""
        self._proto_message.ShowLineations = value


    @property
    def lineations(self) -> List[LineationVal]:
        """Get the Lineations field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.Lineations, LineationVal)
    
    @lineations.setter
    def lineations(self, value: List[LineationVal]) -> None:
        """Set the Lineations field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.Lineations[:] = []
        for item in value:
            self._proto_message.Lineations.append(item.to_proto())


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
