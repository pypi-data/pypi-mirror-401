"""Generated wrapper for TrendPlunge protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .AngleDataVal import AngleDataVal

class TrendPlungeVal:
    """Simple wrapper for TrendPlunge with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.TrendPlunge


    def __init__(self, trend: Optional[AngleDataVal] = None, plunge: Optional[AngleDataVal] = None, proto_message: Optional[Any] = None):
        """Initialize the TrendPlunge wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if trend is not None:
            self._proto_message.Trend.CopyFrom(trend.to_proto())
            self._trend_wrapper = trend
        if plunge is not None:
            self._proto_message.Plunge.CopyFrom(plunge.to_proto())
            self._plunge_wrapper = plunge


    # Properties

    @property
    def trend(self) -> AngleDataVal:
        """Get the Trend field as a wrapper."""
        if not hasattr(self, '_trend_wrapper'):
            self._trend_wrapper = AngleDataVal(proto_message=self._proto_message.Trend)
        return self._trend_wrapper
    
    @trend.setter
    def trend(self, value: AngleDataVal) -> None:
        """Set the Trend field to a wrapper."""
        self._proto_message.Trend.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_trend_wrapper'):
            self._trend_wrapper._proto_message.CopyFrom(self._proto_message.Trend)


    @property
    def plunge(self) -> AngleDataVal:
        """Get the Plunge field as a wrapper."""
        if not hasattr(self, '_plunge_wrapper'):
            self._plunge_wrapper = AngleDataVal(proto_message=self._proto_message.Plunge)
        return self._plunge_wrapper
    
    @plunge.setter
    def plunge(self, value: AngleDataVal) -> None:
        """Set the Plunge field to a wrapper."""
        self._proto_message.Plunge.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_plunge_wrapper'):
            self._plunge_wrapper._proto_message.CopyFrom(self._proto_message.Plunge)


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
