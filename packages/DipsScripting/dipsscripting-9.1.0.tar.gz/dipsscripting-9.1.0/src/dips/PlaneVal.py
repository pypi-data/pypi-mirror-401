"""Generated wrapper for Plane protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .TrendPlungeVal import TrendPlungeVal

class PlaneVal:
    """Simple wrapper for Plane with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.Plane


    def __init__(self, pole: Optional[TrendPlungeVal] = None, proto_message: Optional[Any] = None):
        """Initialize the Plane wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if pole is not None:
            self._proto_message.Pole.CopyFrom(pole.to_proto())
            self._pole_wrapper = pole


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
    def pole(self) -> TrendPlungeVal:
        """Get the Pole field as a wrapper."""
        if not hasattr(self, '_pole_wrapper'):
            self._pole_wrapper = TrendPlungeVal(proto_message=self._proto_message.Pole)
        return self._pole_wrapper
    
    @pole.setter
    def pole(self, value: TrendPlungeVal) -> None:
        """Set the Pole field to a wrapper."""
        self._proto_message.Pole.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_pole_wrapper'):
            self._pole_wrapper._proto_message.CopyFrom(self._proto_message.Pole)


    @property
    def quantity(self) -> float:
        """Get the Quantity field value."""
        return self._proto_message.Quantity
    
    @quantity.setter
    def quantity(self, value: float) -> None:
        """Set the Quantity field value."""
        self._proto_message.Quantity = value


    @property
    def weight(self) -> float:
        """Get the Weight field value."""
        return self._proto_message.Weight
    
    @weight.setter
    def weight(self, value: float) -> None:
        """Set the Weight field value."""
        self._proto_message.Weight = value


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
