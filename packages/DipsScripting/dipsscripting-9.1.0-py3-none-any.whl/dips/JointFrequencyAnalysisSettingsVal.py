"""Generated wrapper for JointFrequencyAnalysisSettings protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .IntervalVal import IntervalVal
from .OrientationDataSetRef import OrientationDataSetRef

class JointFrequencyAnalysisSettingsVal:
    """Simple wrapper for JointFrequencyAnalysisSettings with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.JointFrequencyAnalysisSettings


    def __init__(self, interval: Optional[IntervalVal] = None, proto_message: Optional[Any] = None, channel_to_connect_on: Optional[Any] = None):
        """Initialize the JointFrequencyAnalysisSettings wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        # Store channel for reference types
        self.__channelToConnectOn = channel_to_connect_on

        if interval is not None:
            self._proto_message.Interval.CopyFrom(interval.to_proto())
            self._interval_wrapper = interval


    # Properties

    @property
    def interval(self) -> IntervalVal:
        """Get the Interval field as a wrapper."""
        if not hasattr(self, '_interval_wrapper'):
            self._interval_wrapper = IntervalVal(proto_message=self._proto_message.Interval)
        return self._interval_wrapper
    
    @interval.setter
    def interval(self, value: IntervalVal) -> None:
        """Set the Interval field to a wrapper."""
        self._proto_message.Interval.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_interval_wrapper'):
            self._interval_wrapper._proto_message.CopyFrom(self._proto_message.Interval)


    @property
    def traverses(self) -> List[OrientationDataSetRef]:
        """Get the Traverses field as a list."""
        return _ProtobufListWrapper(self._proto_message.Traverses)
    
    @traverses.setter
    def traverses(self, value: List[OrientationDataSetRef]) -> None:
        """Set the Traverses field to a list."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Expected list or tuple, got {type(value).__name__}")
        # Clear the repeated field using slice assignment
        self._proto_message.Traverses[:] = []
        self._proto_message.Traverses.extend(value)


    @property
    def is_weighted(self) -> bool:
        """Get the IsWeighted field value."""
        return self._proto_message.IsWeighted
    
    @is_weighted.setter
    def is_weighted(self, value: bool) -> None:
        """Set the IsWeighted field value."""
        self._proto_message.IsWeighted = value


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
