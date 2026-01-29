"""Generated wrapper for LatLong protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

class LatLongVal:
    """Simple wrapper for LatLong with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.LatLong


    def __init__(self, proto_message: Optional[Any] = None):
        """Initialize the LatLong wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()



    # Properties

    @property
    def longitude(self) -> float:
        """Get the Longitude field value."""
        return self._proto_message.Longitude
    
    @longitude.setter
    def longitude(self, value: float) -> None:
        """Set the Longitude field value."""
        self._proto_message.Longitude = value


    @property
    def latitude(self) -> float:
        """Get the Latitude field value."""
        return self._proto_message.Latitude
    
    @latitude.setter
    def latitude(self, value: float) -> None:
        """Set the Latitude field value."""
        self._proto_message.Latitude = value


    @property
    def elevation(self) -> float:
        """Get the Elevation field value."""
        return self._proto_message.Elevation
    
    @elevation.setter
    def elevation(self, value: float) -> None:
        """Set the Elevation field value."""
        self._proto_message.Elevation = value


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
