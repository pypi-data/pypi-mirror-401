"""Generated wrapper for PlaneOptions protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

class PlaneOptionsVal:
    """Simple wrapper for PlaneOptions with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.PlaneOptions


    def __init__(self, proto_message: Optional[Any] = None):
        """Initialize the PlaneOptions wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()



    # Properties

    @property
    def show_plane(self) -> bool:
        """Get the ShowPlane field value."""
        return self._proto_message.ShowPlane
    
    @show_plane.setter
    def show_plane(self, value: bool) -> None:
        """Set the ShowPlane field value."""
        self._proto_message.ShowPlane = value


    @property
    def show_marker_ticks(self) -> bool:
        """Get the ShowMarkerTicks field value."""
        return self._proto_message.ShowMarkerTicks
    
    @show_marker_ticks.setter
    def show_marker_ticks(self, value: bool) -> None:
        """Set the ShowMarkerTicks field value."""
        self._proto_message.ShowMarkerTicks = value


    @property
    def show_pole(self) -> bool:
        """Get the ShowPole field value."""
        return self._proto_message.ShowPole
    
    @show_pole.setter
    def show_pole(self, value: bool) -> None:
        """Set the ShowPole field value."""
        self._proto_message.ShowPole = value


    @property
    def show_daylight_envelope(self) -> bool:
        """Get the ShowDaylightEnvelope field value."""
        return self._proto_message.ShowDaylightEnvelope
    
    @show_daylight_envelope.setter
    def show_daylight_envelope(self, value: bool) -> None:
        """Set the ShowDaylightEnvelope field value."""
        self._proto_message.ShowDaylightEnvelope = value


    @property
    def show_pole_label(self) -> bool:
        """Get the ShowPoleLabel field value."""
        return self._proto_message.ShowPoleLabel
    
    @show_pole_label.setter
    def show_pole_label(self, value: bool) -> None:
        """Set the ShowPoleLabel field value."""
        self._proto_message.ShowPoleLabel = value


    @property
    def show_plane_label(self) -> bool:
        """Get the ShowPlaneLabel field value."""
        return self._proto_message.ShowPlaneLabel
    
    @show_plane_label.setter
    def show_plane_label(self, value: bool) -> None:
        """Set the ShowPlaneLabel field value."""
        self._proto_message.ShowPlaneLabel = value


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
