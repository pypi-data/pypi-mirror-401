"""Generated wrapper for SetWindowEntityVisibility protobuf message."""

from typing import Any, Optional, List, Dict
from . import DipsAPI_pb2

from .ProtobufCollectionWrappers import _ProtobufListWrapper, _ProtobufMapWrapper

from .SetEntityInfoRef import SetEntityInfoRef

class SetWindowEntityVisibilityVal:
    """Simple wrapper for SetWindowEntityVisibility with Pythonic getters and setters."""

    _proto_class = DipsAPI_pb2.SetWindowEntityVisibility


    def __init__(self, set_entity_reference: Optional[SetEntityInfoRef] = None, proto_message: Optional[Any] = None, channel_to_connect_on: Optional[Any] = None):
        """Initialize the SetWindowEntityVisibility wrapper."""
        # Initialize the protobuf message
        if proto_message is not None:
            self._proto_message = proto_message
        else:
            self._proto_message = self._proto_class()

        # Store channel for reference types
        self.__channelToConnectOn = channel_to_connect_on

        if set_entity_reference is not None:
            self.set_entity_reference = set_entity_reference


    # Properties

    @property
    def is_visible(self) -> bool:
        """Get the IsVisible field value."""
        return self._proto_message.IsVisible
    
    @is_visible.setter
    def is_visible(self, value: bool) -> None:
        """Set the IsVisible field value."""
        self._proto_message.IsVisible = value


    @property
    def set_entity_reference(self) -> SetEntityInfoRef:
        """Get the SetEntityReference field as a reference."""
        return SetEntityInfoRef(self.__channelToConnectOn, self._proto_message.SetEntityReference)
    
    @set_entity_reference.setter
    def set_entity_reference(self, value: SetEntityInfoRef) -> None:
        """Set the SetEntityReference field to a reference."""
        self._proto_message.SetEntityReference.CopyFrom(value.get_model_ref())


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
