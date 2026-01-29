"""Generated wrapper for StereonetProjectionMode protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

class StereonetProjectionModeVal:
    """Simple wrapper for StereonetProjectionMode with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.StereonetProjectionMode


    def __init__(self, proto_message: Optional[Any] = None):
        """Initialize the StereonetProjectionMode wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()



    # Properties

    @property
    def hemisphere_draw_option(self) -> Any:
        """Get the HemisphereDrawOption field value."""
        return self._proto_message.HemisphereDrawOption
    
    @hemisphere_draw_option.setter
    def hemisphere_draw_option(self, value: Any) -> None:
        """Set the HemisphereDrawOption field value."""
        self._proto_message.HemisphereDrawOption = value


    @property
    def projection_method_draw_option(self) -> Any:
        """Get the ProjectionMethodDrawOption field value."""
        return self._proto_message.ProjectionMethodDrawOption
    
    @projection_method_draw_option.setter
    def projection_method_draw_option(self, value: Any) -> None:
        """Set the ProjectionMethodDrawOption field value."""
        self._proto_message.ProjectionMethodDrawOption = value


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
