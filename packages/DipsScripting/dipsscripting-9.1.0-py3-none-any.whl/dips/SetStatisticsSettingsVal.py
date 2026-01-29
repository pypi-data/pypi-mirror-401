"""Generated wrapper for SetStatisticsSettings protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

class SetStatisticsSettingsVal:
    """Simple wrapper for SetStatisticsSettings with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.SetStatisticsSettings


    def __init__(self, proto_message: Optional[Any] = None):
        """Initialize the SetStatisticsSettings wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()



    # Properties

    @property
    def one_std_dev(self) -> bool:
        """Get the OneStdDev field value."""
        return self._proto_message.OneStdDev
    
    @one_std_dev.setter
    def one_std_dev(self, value: bool) -> None:
        """Set the OneStdDev field value."""
        self._proto_message.OneStdDev = value


    @property
    def two_std_dev(self) -> bool:
        """Get the TwoStdDev field value."""
        return self._proto_message.TwoStdDev
    
    @two_std_dev.setter
    def two_std_dev(self, value: bool) -> None:
        """Set the TwoStdDev field value."""
        self._proto_message.TwoStdDev = value


    @property
    def three_std_dev(self) -> bool:
        """Get the ThreeStdDev field value."""
        return self._proto_message.ThreeStdDev
    
    @three_std_dev.setter
    def three_std_dev(self, value: bool) -> None:
        """Set the ThreeStdDev field value."""
        self._proto_message.ThreeStdDev = value


    @property
    def use_custom_interval(self) -> bool:
        """Get the UseCustomInterval field value."""
        return self._proto_message.UseCustomInterval
    
    @use_custom_interval.setter
    def use_custom_interval(self, value: bool) -> None:
        """Set the UseCustomInterval field value."""
        self._proto_message.UseCustomInterval = value


    @property
    def custom_interval(self) -> float:
        """Get the CustomInterval field value."""
        return self._proto_message.CustomInterval
    
    @custom_interval.setter
    def custom_interval(self, value: float) -> None:
        """Set the CustomInterval field value."""
        self._proto_message.CustomInterval = value


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
