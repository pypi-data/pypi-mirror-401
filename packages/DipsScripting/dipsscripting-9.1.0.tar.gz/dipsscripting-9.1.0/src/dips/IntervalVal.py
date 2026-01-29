"""Generated wrapper for Interval protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .LengthDataVal import LengthDataVal

class IntervalVal:
    """Simple wrapper for Interval with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.Interval


    def __init__(self, distance_interval: Optional[LengthDataVal] = None, distance_move_increment: Optional[LengthDataVal] = None, proto_message: Optional[Any] = None):
        """Initialize the Interval wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if distance_interval is not None:
            self._proto_message.DistanceInterval.CopyFrom(distance_interval.to_proto())
            self._distance_interval_wrapper = distance_interval
        if distance_move_increment is not None:
            self._proto_message.DistanceMoveIncrement.CopyFrom(distance_move_increment.to_proto())
            self._distance_move_increment_wrapper = distance_move_increment


    # Properties

    @property
    def interval_option(self) -> Any:
        """Get the IntervalOption field value."""
        return self._proto_message.IntervalOption
    
    @interval_option.setter
    def interval_option(self, value: Any) -> None:
        """Set the IntervalOption field value."""
        self._proto_message.IntervalOption = value


    @property
    def distance_interval(self) -> LengthDataVal:
        """Get the DistanceInterval field as a wrapper."""
        if not hasattr(self, '_distance_interval_wrapper'):
            self._distance_interval_wrapper = LengthDataVal(proto_message=self._proto_message.DistanceInterval)
        return self._distance_interval_wrapper
    
    @distance_interval.setter
    def distance_interval(self, value: LengthDataVal) -> None:
        """Set the DistanceInterval field to a wrapper."""
        self._proto_message.DistanceInterval.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_distance_interval_wrapper'):
            self._distance_interval_wrapper._proto_message.CopyFrom(self._proto_message.DistanceInterval)


    @property
    def distance_move_increment(self) -> LengthDataVal:
        """Get the DistanceMoveIncrement field as a wrapper."""
        if not hasattr(self, '_distance_move_increment_wrapper'):
            self._distance_move_increment_wrapper = LengthDataVal(proto_message=self._proto_message.DistanceMoveIncrement)
        return self._distance_move_increment_wrapper
    
    @distance_move_increment.setter
    def distance_move_increment(self, value: LengthDataVal) -> None:
        """Set the DistanceMoveIncrement field to a wrapper."""
        self._proto_message.DistanceMoveIncrement.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_distance_move_increment_wrapper'):
            self._distance_move_increment_wrapper._proto_message.CopyFrom(self._proto_message.DistanceMoveIncrement)


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
