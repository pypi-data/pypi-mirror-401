"""Generated wrapper for FreehandWindow protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .TrendPlungeVal import TrendPlungeVal

class FreehandWindowVal:
    """Simple wrapper for FreehandWindow with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.FreehandWindow


    def __init__(self, proto_message: Optional[Any] = None):
        """Initialize the FreehandWindow wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()



    # Properties

    @property
    def polygon(self) -> List[TrendPlungeVal]:
        """Get the Polygon field as a list of wrappers."""
        return _ProtobufListWrapper(self._proto_message.Polygon, TrendPlungeVal)
    
    @polygon.setter
    def polygon(self, value: List[TrendPlungeVal]) -> None:
        """Set the Polygon field to a list of wrappers."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.Polygon[:] = []
        for item in value:
            self._proto_message.Polygon.append(item.to_proto())


    @property
    def is_wrapped(self) -> bool:
        """Get the IsWrapped field value."""
        return self._proto_message.IsWrapped
    
    @is_wrapped.setter
    def is_wrapped(self, value: bool) -> None:
        """Set the IsWrapped field value."""
        self._proto_message.IsWrapped = value


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
