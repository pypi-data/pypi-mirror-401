"""Generated wrapper for VectorDensityContourSettings protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

class VectorDensityContourSettingsVal:
    """Simple wrapper for VectorDensityContourSettings with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.VectorDensityContourSettings


    def __init__(self, proto_message: Optional[Any] = None):
        """Initialize the VectorDensityContourSettings wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()



    # Properties

    @property
    def density_distribution(self) -> Any:
        """Get the DensityDistribution field value."""
        return self._proto_message.DensityDistribution
    
    @density_distribution.setter
    def density_distribution(self, value: Any) -> None:
        """Set the DensityDistribution field value."""
        self._proto_message.DensityDistribution = value


    @property
    def count_circle_size_percent(self) -> float:
        """Get the CountCircleSizePercent field value."""
        return self._proto_message.CountCircleSizePercent
    
    @count_circle_size_percent.setter
    def count_circle_size_percent(self, value: float) -> None:
        """Set the CountCircleSizePercent field value."""
        self._proto_message.CountCircleSizePercent = value


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
