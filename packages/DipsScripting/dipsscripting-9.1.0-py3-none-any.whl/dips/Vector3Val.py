"""Generated wrapper for Vector3 protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

class Vector3Val:
    """Simple wrapper for Vector3 with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.Vector3


    def __init__(self, proto_message: Optional[Any] = None):
        """Initialize the Vector3 wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()



    # Properties

    @property
    def x(self) -> float:
        """Get the X field value."""
        return self._proto_message.X
    
    @x.setter
    def x(self, value: float) -> None:
        """Set the X field value."""
        self._proto_message.X = value


    @property
    def y(self) -> float:
        """Get the Y field value."""
        return self._proto_message.Y
    
    @y.setter
    def y(self, value: float) -> None:
        """Set the Y field value."""
        self._proto_message.Y = value


    @property
    def z(self) -> float:
        """Get the Z field value."""
        return self._proto_message.Z
    
    @z.setter
    def z(self, value: float) -> None:
        """Set the Z field value."""
        self._proto_message.Z = value


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
