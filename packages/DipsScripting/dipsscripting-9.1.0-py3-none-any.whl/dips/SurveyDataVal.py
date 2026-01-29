"""Generated wrapper for SurveyData protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .CustomRowRawDataVal import CustomRowRawDataVal
from .TrendPlungeVal import TrendPlungeVal

class SurveyDataVal:
    """Simple wrapper for SurveyData with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.SurveyData


    def __init__(self, orientation: Optional[TrendPlungeVal] = None, extra_data: Optional[CustomRowRawDataVal] = None, proto_message: Optional[Any] = None):
        """Initialize the SurveyData wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        if orientation is not None:
            self._proto_message.Orientation.CopyFrom(orientation.to_proto())
            self._orientation_wrapper = orientation
        if extra_data is not None:
            self._proto_message.ExtraData.CopyFrom(extra_data.to_proto())
            self._extra_data_wrapper = extra_data


    # Properties

    @property
    def distance(self) -> float:
        """Get the Distance field value."""
        return self._proto_message.Distance
    
    @distance.setter
    def distance(self, value: float) -> None:
        """Set the Distance field value."""
        self._proto_message.Distance = value


    @property
    def orientation(self) -> TrendPlungeVal:
        """Get the Orientation field as a wrapper."""
        if not hasattr(self, '_orientation_wrapper'):
            self._orientation_wrapper = TrendPlungeVal(proto_message=self._proto_message.Orientation)
        return self._orientation_wrapper
    
    @orientation.setter
    def orientation(self, value: TrendPlungeVal) -> None:
        """Set the Orientation field to a wrapper."""
        self._proto_message.Orientation.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_orientation_wrapper'):
            self._orientation_wrapper._proto_message.CopyFrom(self._proto_message.Orientation)


    @property
    def extra_data(self) -> CustomRowRawDataVal:
        """Get the ExtraData field as a wrapper."""
        if not hasattr(self, '_extra_data_wrapper'):
            self._extra_data_wrapper = CustomRowRawDataVal(proto_message=self._proto_message.ExtraData)
        return self._extra_data_wrapper
    
    @extra_data.setter
    def extra_data(self, value: CustomRowRawDataVal) -> None:
        """Set the ExtraData field to a wrapper."""
        self._proto_message.ExtraData.CopyFrom(value.to_proto())
        # Update the cached wrapper if it exists
        if hasattr(self, '_extra_data_wrapper'):
            self._extra_data_wrapper._proto_message.CopyFrom(self._proto_message.ExtraData)


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
