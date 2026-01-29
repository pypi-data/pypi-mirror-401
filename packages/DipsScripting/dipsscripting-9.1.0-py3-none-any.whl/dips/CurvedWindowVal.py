"""Generated wrapper for CurvedWindow protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .TrendPlungeVal import TrendPlungeVal

class CurvedWindowVal:
    """Simple wrapper for CurvedWindow with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.CurvedWindow


    def __init__(self, first_corner: Optional[TrendPlungeVal] = None, second_corner: Optional[TrendPlungeVal] = None, proto_message: Optional[Any] = None):
        """Initialize the CurvedWindow wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if first_corner is not None:
            self._proto_message.FirstCorner.CopyFrom(first_corner.to_proto())
            self._first_corner_wrapper = first_corner
        if second_corner is not None:
            self._proto_message.SecondCorner.CopyFrom(second_corner.to_proto())
            self._second_corner_wrapper = second_corner


    # Properties

    @property
    def id(self) -> str:
        """Get the ID field value."""
        return self._proto_message.ID
    
    @id.setter
    def id(self, value: str) -> None:
        """Set the ID field value."""
        self._proto_message.ID = value


    @property
    def first_corner(self) -> TrendPlungeVal:
        """Get the FirstCorner field as a wrapper."""
        if not hasattr(self, '_first_corner_wrapper'):
            self._first_corner_wrapper = TrendPlungeVal(proto_message=self._proto_message.FirstCorner)
        return self._first_corner_wrapper
    
    @first_corner.setter
    def first_corner(self, value: TrendPlungeVal) -> None:
        """Set the FirstCorner field to a wrapper."""
        self._proto_message.FirstCorner.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_first_corner_wrapper'):
            self._first_corner_wrapper._proto_message.CopyFrom(self._proto_message.FirstCorner)


    @property
    def second_corner(self) -> TrendPlungeVal:
        """Get the SecondCorner field as a wrapper."""
        if not hasattr(self, '_second_corner_wrapper'):
            self._second_corner_wrapper = TrendPlungeVal(proto_message=self._proto_message.SecondCorner)
        return self._second_corner_wrapper
    
    @second_corner.setter
    def second_corner(self, value: TrendPlungeVal) -> None:
        """Set the SecondCorner field to a wrapper."""
        self._proto_message.SecondCorner.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_second_corner_wrapper'):
            self._second_corner_wrapper._proto_message.CopyFrom(self._proto_message.SecondCorner)


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
