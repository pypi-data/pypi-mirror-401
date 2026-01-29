"""Generated wrapper for SetVersusSet protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .SetEntityInfoRef import SetEntityInfoRef

class SetVersusSetVal:
    """Simple wrapper for SetVersusSet with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.SetVersusSet


    def __init__(self, set_a: Optional[SetEntityInfoRef] = None, set_b: Optional[SetEntityInfoRef] = None, proto_message: Optional[Any] = None, channel_to_connect_on: Optional[Any] = None):
        """Initialize the SetVersusSet wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        # Store channel for reference types
        self.__channelToConnectOn = channel_to_connect_on

        if set_a is not None:
            self.set_a = set_a
        if set_b is not None:
            self.set_b = set_b


    # Properties

    @property
    def set_a(self) -> SetEntityInfoRef:
        """Get the SetA field as a reference."""
        return SetEntityInfoRef(self.__channelToConnectOn, self._proto_message.SetA)
    
    @set_a.setter
    def set_a(self, value: SetEntityInfoRef) -> None:
        """Set the SetA field to a reference."""
        self._proto_message.SetA.CopyFrom(value.get_model_ref())


    @property
    def set_b(self) -> SetEntityInfoRef:
        """Get the SetB field as a reference."""
        return SetEntityInfoRef(self.__channelToConnectOn, self._proto_message.SetB)
    
    @set_b.setter
    def set_b(self, value: SetEntityInfoRef) -> None:
        """Set the SetB field to a reference."""
        self._proto_message.SetB.CopyFrom(value.get_model_ref())


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
