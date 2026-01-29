"""Generated wrapper for CircularWindow protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .AngleDataVal import AngleDataVal
from .TrendPlungeVal import TrendPlungeVal

class CircularWindowVal:
    """Simple wrapper for CircularWindow with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.CircularWindow


    def __init__(self, center: Optional[TrendPlungeVal] = None, cone_angle: Optional[AngleDataVal] = None, proto_message: Optional[Any] = None):
        """Initialize the CircularWindow wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if center is not None:
            self._proto_message.Center.CopyFrom(center.to_proto())
            self._center_wrapper = center
        if cone_angle is not None:
            self._proto_message.ConeAngle.CopyFrom(cone_angle.to_proto())
            self._cone_angle_wrapper = cone_angle


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
    def center(self) -> TrendPlungeVal:
        """Get the Center field as a wrapper."""
        if not hasattr(self, '_center_wrapper'):
            self._center_wrapper = TrendPlungeVal(proto_message=self._proto_message.Center)
        return self._center_wrapper
    
    @center.setter
    def center(self, value: TrendPlungeVal) -> None:
        """Set the Center field to a wrapper."""
        self._proto_message.Center.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_center_wrapper'):
            self._center_wrapper._proto_message.CopyFrom(self._proto_message.Center)


    @property
    def cone_angle(self) -> AngleDataVal:
        """Get the ConeAngle field as a wrapper."""
        if not hasattr(self, '_cone_angle_wrapper'):
            self._cone_angle_wrapper = AngleDataVal(proto_message=self._proto_message.ConeAngle)
        return self._cone_angle_wrapper
    
    @cone_angle.setter
    def cone_angle(self, value: AngleDataVal) -> None:
        """Set the ConeAngle field to a wrapper."""
        self._proto_message.ConeAngle.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_cone_angle_wrapper'):
            self._cone_angle_wrapper._proto_message.CopyFrom(self._proto_message.ConeAngle)


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
