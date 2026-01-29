"""Generated wrapper for Lineation protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .AngleDataVal import AngleDataVal

class LineationVal:
    """Simple wrapper for Lineation with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.Lineation


    def __init__(self, angle: Optional[AngleDataVal] = None, proto_message: Optional[Any] = None):
        """Initialize the Lineation wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if angle is not None:
            self._proto_message.Angle.CopyFrom(angle.to_proto())
            self._angle_wrapper = angle


    # Properties

    @property
    def angle(self) -> AngleDataVal:
        """Get the Angle field as a wrapper."""
        if not hasattr(self, '_angle_wrapper'):
            self._angle_wrapper = AngleDataVal(proto_message=self._proto_message.Angle)
        return self._angle_wrapper
    
    @angle.setter
    def angle(self, value: AngleDataVal) -> None:
        """Set the Angle field to a wrapper."""
        self._proto_message.Angle.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_angle_wrapper'):
            self._angle_wrapper._proto_message.CopyFrom(self._proto_message.Angle)


    @property
    def direction(self) -> Any:
        """Get the Direction field value."""
        return self._proto_message.Direction
    
    @direction.setter
    def direction(self, value: Any) -> None:
        """Set the Direction field value."""
        self._proto_message.Direction = value


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
