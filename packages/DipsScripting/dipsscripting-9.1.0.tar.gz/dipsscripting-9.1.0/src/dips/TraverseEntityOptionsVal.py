"""Generated wrapper for TraverseEntityOptions protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

class TraverseEntityOptionsVal:
    """Simple wrapper for TraverseEntityOptions with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.TraverseEntityOptions


    def __init__(self, proto_message: Optional[Any] = None):
        """Initialize the TraverseEntityOptions wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()



    # Properties

    @property
    def show_all_points(self) -> bool:
        """Get the ShowAllPoints field value."""
        return self._proto_message.ShowAllPoints
    
    @show_all_points.setter
    def show_all_points(self, value: bool) -> None:
        """Set the ShowAllPoints field value."""
        self._proto_message.ShowAllPoints = value


    @property
    def show_label(self) -> bool:
        """Get the ShowLabel field value."""
        return self._proto_message.ShowLabel
    
    @show_label.setter
    def show_label(self, value: bool) -> None:
        """Set the ShowLabel field value."""
        self._proto_message.ShowLabel = value


    @property
    def show_blind_zone(self) -> bool:
        """Get the ShowBlindZone field value."""
        return self._proto_message.ShowBlindZone
    
    @show_blind_zone.setter
    def show_blind_zone(self, value: bool) -> None:
        """Set the ShowBlindZone field value."""
        self._proto_message.ShowBlindZone = value


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
