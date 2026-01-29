"""Generated wrapper for ColorSurrogate protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

class ColorSurrogateVal:
    """Simple wrapper for ColorSurrogate with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.ColorSurrogate


    def __init__(self, proto_message: Optional[Any] = None):
        """Initialize the ColorSurrogate wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()



    # Properties

    @property
    def a(self) -> int:
        """Get the A field value."""
        return self._proto_message.A
    
    @a.setter
    def a(self, value: int) -> None:
        """Set the A field value."""
        self._proto_message.A = value


    @property
    def r(self) -> int:
        """Get the R field value."""
        return self._proto_message.R
    
    @r.setter
    def r(self, value: int) -> None:
        """Set the R field value."""
        self._proto_message.R = value


    @property
    def g(self) -> int:
        """Get the G field value."""
        return self._proto_message.G
    
    @g.setter
    def g(self, value: int) -> None:
        """Set the G field value."""
        self._proto_message.G = value


    @property
    def b(self) -> int:
        """Get the B field value."""
        return self._proto_message.B
    
    @b.setter
    def b(self, value: int) -> None:
        """Set the B field value."""
        self._proto_message.B = value


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
