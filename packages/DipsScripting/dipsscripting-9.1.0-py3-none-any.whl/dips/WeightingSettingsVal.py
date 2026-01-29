"""Generated wrapper for WeightingSettings protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .AngleDataVal import AngleDataVal

class WeightingSettingsVal:
    """Simple wrapper for WeightingSettings with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.WeightingSettings


    def __init__(self, minimum_bias_angle: Optional[AngleDataVal] = None, proto_message: Optional[Any] = None):
        """Initialize the WeightingSettings wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if minimum_bias_angle is not None:
            self._proto_message.MinimumBiasAngle.CopyFrom(minimum_bias_angle.to_proto())
            self._minimum_bias_angle_wrapper = minimum_bias_angle


    # Properties

    @property
    def weighting_option(self) -> Any:
        """Get the WeightingOption field value."""
        return self._proto_message.WeightingOption
    
    @weighting_option.setter
    def weighting_option(self, value: Any) -> None:
        """Set the WeightingOption field value."""
        self._proto_message.WeightingOption = value


    @property
    def minimum_bias_angle(self) -> AngleDataVal:
        """Get the MinimumBiasAngle field as a wrapper."""
        if not hasattr(self, '_minimum_bias_angle_wrapper'):
            self._minimum_bias_angle_wrapper = AngleDataVal(proto_message=self._proto_message.MinimumBiasAngle)
        return self._minimum_bias_angle_wrapper
    
    @minimum_bias_angle.setter
    def minimum_bias_angle(self, value: AngleDataVal) -> None:
        """Set the MinimumBiasAngle field to a wrapper."""
        self._proto_message.MinimumBiasAngle.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_minimum_bias_angle_wrapper'):
            self._minimum_bias_angle_wrapper._proto_message.CopyFrom(self._proto_message.MinimumBiasAngle)


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
