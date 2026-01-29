"""Generated wrapper for AnchorPoint protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .TrendPlungeVal import TrendPlungeVal
from .Vector2DVal import Vector2DVal

class AnchorPointVal:
    """Simple wrapper for AnchorPoint with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.AnchorPoint


    def __init__(self, spherical_point: Optional[TrendPlungeVal] = None, logical_point: Optional[Vector2DVal] = None, proto_message: Optional[Any] = None):
        """Initialize the AnchorPoint wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if spherical_point is not None:
            self._proto_message.SphericalPoint.CopyFrom(spherical_point.to_proto())
            self._spherical_point_wrapper = spherical_point
        if logical_point is not None:
            self._proto_message.LogicalPoint.CopyFrom(logical_point.to_proto())
            self._logical_point_wrapper = logical_point


    # Properties

    @property
    def coordinate_option(self) -> Any:
        """Get the CoordinateOption field value."""
        return self._proto_message.CoordinateOption
    
    @coordinate_option.setter
    def coordinate_option(self, value: Any) -> None:
        """Set the CoordinateOption field value."""
        self._proto_message.CoordinateOption = value


    @property
    def spherical_point(self) -> TrendPlungeVal:
        """Get the SphericalPoint field as a wrapper."""
        if not hasattr(self, '_spherical_point_wrapper'):
            self._spherical_point_wrapper = TrendPlungeVal(proto_message=self._proto_message.SphericalPoint)
        return self._spherical_point_wrapper
    
    @spherical_point.setter
    def spherical_point(self, value: TrendPlungeVal) -> None:
        """Set the SphericalPoint field to a wrapper."""
        self._proto_message.SphericalPoint.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_spherical_point_wrapper'):
            self._spherical_point_wrapper._proto_message.CopyFrom(self._proto_message.SphericalPoint)


    @property
    def logical_point(self) -> Vector2DVal:
        """Get the LogicalPoint field as a wrapper."""
        if not hasattr(self, '_logical_point_wrapper'):
            self._logical_point_wrapper = Vector2DVal(proto_message=self._proto_message.LogicalPoint)
        return self._logical_point_wrapper
    
    @logical_point.setter
    def logical_point(self, value: Vector2DVal) -> None:
        """Set the LogicalPoint field to a wrapper."""
        self._proto_message.LogicalPoint.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_logical_point_wrapper'):
            self._logical_point_wrapper._proto_message.CopyFrom(self._proto_message.LogicalPoint)


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
